#include <iostream>
#include <string>

using namespace std;

// Estructura que representa los datos de un Paciente
struct Paciente {
    int id;
    string nombre;
    int edad;
};

// Estructura del Nodo de la Lista Enlazada
struct Nodo {
    Paciente datos;
    Nodo* siguiente;
};

// Función para registrar un nuevo paciente (Insertar al inicio)
void registrarPaciente(Nodo*& cabeza, int id, string nombre, int edad) {
    Nodo* nuevoNodo = new Nodo();
    nuevoNodo->datos.id = id;
    nuevoNodo->datos.nombre = nombre;
    nuevoNodo->datos.edad = edad;
    nuevoNodo->siguiente = cabeza;
    cabeza = nuevoNodo;
    cout << "\n[OK] Paciente registrado con exito.\n";
}

// Función para listar todos los pacientes registrados
void listarPacientes(Nodo* cabeza) {
    if (cabeza == nullptr) { // Manejo de error para lista vacía
        cout << "\n[AVISO] No hay pacientes registrados en la clinica.\n";
        return;
    }
    
    cout << "\n=== LISTA DE PACIENTES REGISTRADOS ===\n";
    Nodo* actual = cabeza;
    while (actual != nullptr) {
        cout << "ID: " << actual->datos.id 
             << " | Nombre: " << actual->datos.nombre 
             << " | Edad: " << actual->datos.edad << " anos\n";
        actual = actual->siguiente;
    }
}

// Función para modificar los datos de un paciente por su ID
void modificarPaciente(Nodo* cabeza, int id) {
    Nodo* actual = cabeza;
    while (actual != nullptr) {
        if (actual->datos.id == id) {
            cout << "\nPaciente encontrado. Ingrese los nuevos datos:\n";
            cout << "Nuevo Nombre: ";
            cin.ignore();
            getline(cin, actual->datos.nombre);
            cout << "Nueva Edad: ";
            cin >> actual->datos.edad;
            cout << "\n[OK] Datos del paciente actualizados correctamente.\n";
            return;
        }
        actual = actual->siguiente;
    }
    cout << "\n[ERROR] No se encontro ningun paciente con el ID especificado.\n";
}

// Función para eliminar un paciente por su ID
void eliminarPaciente(Nodo*& cabeza, int id) {
    if (cabeza == nullptr) { // Manejo de error para lista vacía
        cout << "\n[ERROR] La lista esta vacia. No se puede eliminar.\n";
        return;
    }

    Nodo* actual = cabeza;
    Nodo* anterior = nullptr;

    while (actual != nullptr && actual->datos.id != id) {
        anterior = actual;
        actual = actual->siguiente;
    }

    if (actual == nullptr) {
        cout << "\n[ERROR] No se encontro ningun paciente con el ID especificado.\n";
        return;
    }

    // Si el nodo a eliminar es la cabeza de la lista
    if (anterior == nullptr) {
        cabeza = cabeza->siguiente;
    } else {
        anterior->siguiente = actual->siguiente;
    }

    delete actual; // Liberación de memoria física
    cout << "\n[OK] Paciente eliminado correctamente del sistema.\n";
}

int main() {
    Nodo* clinica = nullptr; // Inicialización de la lista vacía
    int opcion, id, edad;
    string nombre;

    do {
        cout << "\n=== MENU CLINICA LOCAL (LISTA MANUAL) ===\n";
        cout << "1. Registrar Paciente\n";
        cout << "2. Listar Pacientes\n";
        cout << "3. Modificar Paciente\n";
        cout << "4. Eliminar Paciente\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                cout << "Ingrese ID único: ";
                cin >> id;
                cout << "Ingrese Nombre completo: ";
                cin.ignore();
                getline(cin, nombre);
                cout << "Ingrese Edad: ";
                cin >> edad;
                registrarPaciente(clinica, id, nombre, edad);
                break;
            case 2:
                listarPacientes(clinica);
                break;
            case 3:
                cout << "Ingrese el ID del paciente a modificar: ";
                cin >> id;
                modificarPaciente(clinica, id);
                break;
            case 4:
                cout << "Ingrese el ID del paciente a eliminar: ";
                cin >> id;
                eliminarPaciente(clinica, id);
                break;
            case 5:
                cout << "\nSaliendo del sistema...\n";
                break;
            default:
                cout << "\n[OPCION INVALIDA] Intente nuevamente.\n";
        }
    } while (opcion != 5);

    // Limpieza de memoria al finalizar el programa
    while (clinica != nullptr) {
        Nodo* temporal = clinica;
        clinica = clinica->siguiente;
        delete temporal;
    }

    return 0;
}