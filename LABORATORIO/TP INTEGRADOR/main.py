from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path

from controllers import (
    HitoController,
    NotificacionController,
    ProductoController,
    TicketController,
)
from database import conectar, inicializar_bd
from domain.enums import RubroTipo
from domain.exceptions import ReaperturaFueraDePlazoError
from domain.producto import Producto
from domain.ticket import Ticket
from domain.usuario import Cliente, Tecnico, Usuario
from repositories import (
    SQLiteHitoRepository,
    SQLiteProductoRepository,
    SQLiteTicketRepository,
    SQLiteUsuarioRepository,
)

DB_FILE = Path(__file__).with_name("ticketing.db")


def separador(titulo: str) -> None:
    print()
    print("=" * 78)
    print(titulo)
    print("=" * 78)


def describir_usuario(usuario: Usuario) -> str:
    if isinstance(usuario, Cliente):
        return (
            f"Cliente #{usuario.idUsuario} - {usuario.nombre} "
            f"({usuario.email}, tel. {usuario.telefono})"
        )
    if isinstance(usuario, Tecnico):
        estado = "disponible" if usuario.disponible else "ocupado"
        return (
            f"Técnico #{usuario.idUsuario} - {usuario.nombre} "
            f"({usuario.rubroEspecialidad.value}, {estado})"
        )
    return f"Usuario #{usuario.idUsuario} - {usuario.nombre} ({usuario.email})"


def describir_producto(producto: Producto) -> str:
    return (
        f"Producto #{producto.idProducto} - {producto.nombre} "
        f"{producto.marca} {producto.modelo} "
        f"[{producto.obtenerRubro().value}]"
    )


def mostrar_ticket(ticket: Ticket) -> None:
    tecnico = ticket.tecnico.nombre if ticket.tecnico else "sin asignar"
    cierre = (
        ticket.fechaCierre.strftime("%Y-%m-%d %H:%M:%S")
        if ticket.fechaCierre
        else "no cerrado"
    )
    print(f"Ticket #{ticket.idTicket}")
    print(f"  Estado       : {ticket.estado.value}")
    print(f"  Cliente      : {ticket.cliente.nombre}")
    print(f"  Técnico      : {tecnico}")
    print(f"  Producto     : {describir_producto(ticket.producto)}")
    print(f"  Descripción  : {ticket.descripcion}")
    print(f"  Creación     : {ticket.fechaCreacion.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Fecha cierre : {cierre}")
    print("  Hitos:")
    if not ticket.hitos:
        print("    (sin hitos)")
    for hito in ticket.hitos:
        fecha = hito.fechaHora.strftime("%Y-%m-%d %H:%M:%S")
        print(f"    [{fecha}] {hito.autor.nombre}: {hito.mensaje}")


def sembrar_datos(
    producto_repo: SQLiteProductoRepository,
    usuario_repo: SQLiteUsuarioRepository,
) -> tuple[Cliente, Tecnico, Tecnico, Producto, Producto]:
    separador("PASO 0 - SEMBRADO DE DATOS INICIALES")

    cliente = usuario_repo.guardar(
        Cliente(
            nombre="María López",
            email="maria.lopez@example.com",
            telefono="+54 11 5555-1234",
            direccion="Av. Siempre Viva 742",
        )
    )
    tecnico1 = usuario_repo.guardar(
        Tecnico(
            nombre="Carlos Pérez",
            email="carlos.perez@servicio.com",
            rubroEspecialidad=RubroTipo.LINEA_BLANCA,
            disponible=True,
        )
    )
    tecnico2 = usuario_repo.guardar(
        Tecnico(
            nombre="Lucía Gómez",
            email="lucia.gomez@servicio.com",
            rubroEspecialidad=RubroTipo.COCINA,
            disponible=True,
        )
    )
    producto1 = producto_repo.guardar(
        Producto(
            nombre="Heladera No Frost",
            marca="Samsung",
            modelo="RT29K5710",
            rubro=RubroTipo.LINEA_BLANCA,
        )
    )
    producto2 = producto_repo.guardar(
        Producto(
            nombre="Horno Microondas",
            marca="BGH",
            modelo="BGHMB20",
            rubro=RubroTipo.COCINA,
        )
    )

    if not isinstance(cliente, Cliente):
        raise RuntimeError("El cliente sembrado no es válido.")
    if not isinstance(tecnico1, Tecnico) or not isinstance(tecnico2, Tecnico):
        raise RuntimeError("Los técnicos sembrados no son válidos.")

    print(describir_usuario(cliente))
    print(describir_usuario(tecnico1))
    print(describir_usuario(tecnico2))
    print(describir_producto(producto1))
    print(describir_producto(producto2))
    return cliente, tecnico1, tecnico2, producto1, producto2


def verificar_integridad(conn) -> None:
    separador("VERIFICACIÓN DE INTEGRIDAD DE LA BASE DE DATOS")
    violaciones = conn.execute("PRAGMA foreign_key_check").fetchall()
    resultado = conn.execute("PRAGMA integrity_check").fetchone()[0]
    if violaciones:
        print(f"PRAGMA foreign_key_check : {len(violaciones)} violación(es) detectada(s)")
        for violacion in violaciones:
            print(f"  - {tuple(violacion)}")
    else:
        print("PRAGMA foreign_key_check : OK (sin violaciones)")
    print(f"PRAGMA integrity_check   : {resultado}")


def ejecutar_demo(conn) -> None:
    producto_repo = SQLiteProductoRepository(conn)
    usuario_repo = SQLiteUsuarioRepository(conn)
    hito_repo = SQLiteHitoRepository(conn, usuario_repo)
    ticket_repo = SQLiteTicketRepository(
        conn,
        producto_repo,
        usuario_repo,
        hito_repo,
    )

    notificacion = NotificacionController()
    hito_controller = HitoController(hito_repo, notificacion)
    ticket_controller = TicketController(
        ticket_repo,
        producto_repo,
        usuario_repo,
        hito_controller,
        notificacion,
    )
    producto_controller = ProductoController(producto_repo)

    cliente, tecnico1, tecnico2, producto1, producto2 = sembrar_datos(
        producto_repo,
        usuario_repo,
    )

    separador("DS-01 - CREAR TICKET")
    print(f"Seleccionando producto: {describir_producto(producto1)}")
    rubro = producto1.obtenerRubro()
    print(f"Rubro obtenido del producto: {rubro.value}")
    ticket = ticket_controller.crearTicket(
        idProducto=producto1.idProducto or 0,
        idCliente=cliente.idUsuario or 0,
        mensaje="La heladera hace un ruido extraño y no enfría.",
    )
    print(f"Ticket creado con estado {ticket.estado.value}.")
    mostrar_ticket(ticket)

    separador("DS-02 - ASIGNAR TICKET POR RUBRO")
    print(f"Buscando técnico disponible que pueda atender {rubro.value}...")
    ticket = ticket_controller.iniciarAsignacion(ticket.idTicket or 0, rubro)
    print(f"Ticket asignado. Estado actual: {ticket.estado.value}.")
    mostrar_ticket(ticket)

    separador("DS-03 - REGISTRAR MENSAJE EN HITO")
    if ticket.tecnico is None:
        raise RuntimeError("El ticket debería tener un técnico asignado.")
    print("El técnico agrega un mensaje al ticket...")
    hito_controller.agregarHito(
        ticket,
        "Hola, estoy revisando el compresor. En breve le confirmo.",
        ticket.tecnico,
    )
    print("El cliente responde...")
    hito_controller.agregarHito(
        ticket,
        "Gracias, quedo atento. ¿Necesita que deje la llave?",
        cliente,
    )
    print("Hitos registrados (inmutables):")
    for hito in ticket.hitos:
        fecha = hito.fechaHora.strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [{fecha}] {hito.autor.nombre}: {hito.mensaje}")

    separador("DS-04 - CERRAR TICKET")
    print(cliente.solicitarCierreTicket())
    ticket = ticket_controller.cerrarTicket(ticket.idTicket or 0, cliente)
    print(f"Estado actual: {ticket.estado.value}.")
    mostrar_ticket(ticket)

    separador("DS-04 - REABRIR TICKET (dentro de los 30 días)")
    print(cliente.solicitarReaperturaTicket())
    ticket = ticket_controller.reabrirTicket(ticket.idTicket or 0, cliente)
    print(f"Estado actual: {ticket.estado.value}.")
    mostrar_ticket(ticket)

    separador("PRUEBA ADICIONAL - VALIDACIÓN DEL PLAZO DE 30 DÍAS")
    ticket2 = ticket_controller.crearTicket(
        idProducto=producto2.idProducto or 0,
        idCliente=cliente.idUsuario or 0,
        mensaje="El microondas no calienta.",
    )
    ticket2 = ticket_controller.iniciarAsignacion(
        ticket2.idTicket or 0,
        producto2.obtenerRubro(),
    )
    ticket2 = ticket_controller.cerrarTicket(ticket2.idTicket or 0, cliente)
    print(f"Ticket #{ticket2.idTicket} cerrado. Intentando reabrir 31 días después...")
    try:
        ticket_controller.reabrirTicket(
            ticket2.idTicket or 0,
            cliente,
            fechaReferencia=datetime.now() + timedelta(days=31),
        )
    except ReaperturaFueraDePlazoError as error:
        print(f"Reapertura rechazada correctamente: {error}")

    separador("CONSULTAS POR REPOSITORIO")
    print("Tickets del cliente:")
    for item in ticket_repo.listarPorCliente(cliente.idUsuario or 0):
        print(f"  - Ticket #{item.idTicket} [{item.estado.value}] {item.descripcion}")

    print("Tickets del técnico asignado al primer ticket:")
    if ticket.tecnico is not None:
        for item in ticket_repo.listarPorTecnico(ticket.tecnico.idUsuario or 0):
            print(
                f"  - Ticket #{item.idTicket} [{item.estado.value}] "
                f"{item.descripcion}"
            )

    separador("PRODUCTOCONTROLLER - ASIGNAR TIPO DE PRODUCTO")
    print(f"Antes : {describir_producto(producto2)}")
    producto2_actualizado = producto_controller.asignarTipoProducto(
        producto2.idProducto or 0,
        RubroTipo.ELECTRO,
    )
    print(f"Después: {describir_producto(producto2_actualizado)}")

    separador("RESUMEN DE NOTIFICACIONES EMITIDAS")
    for mensaje in notificacion.historial:
        print(f"  - {mensaje}")

    verificar_integridad(conn)

    print()
    print(
        "Demo finalizada. Técnicos sembrados: "
        f"{describir_usuario(tecnico1)} | {describir_usuario(tecnico2)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sistema de Ticketing - Trabajo Práctico Integrador",
    )
    parser.add_argument(
        "--memory",
        action="store_true",
        help="Usar una base SQLite en memoria (:memory:) en lugar de un archivo.",
    )
    parser.add_argument(
        "--db",
        default=str(DB_FILE),
        help="Ruta del archivo SQLite a utilizar.",
    )
    args = parser.parse_args()

    if args.memory:
        db_path: str | Path = ":memory:"
        print("Base de datos: :memory:")
    else:
        archivo = Path(args.db)
        if archivo.exists():
            archivo.unlink()
            print(f"Base anterior eliminada: {archivo}")
        db_path = archivo
        print(f"Base de datos: {archivo}")

    conn = conectar(db_path)
    try:
        inicializar_bd(conn)
        ejecutar_demo(conn)
    finally:
        conn.close()

    if not args.memory:
        print(f"\nDatos persistidos en: {Path(args.db).resolve()}")


if __name__ == "__main__":
    main()
