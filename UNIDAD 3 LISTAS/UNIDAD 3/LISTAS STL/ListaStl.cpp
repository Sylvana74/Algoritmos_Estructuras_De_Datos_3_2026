#include <iostream>
#include <list>
#include <string>
#include <algorithm>

using namespace std;

// Estructura que representa los datos de un Paciente
struct Paciente {
    int id;
    string nombre;
    int edad;
};

// Función para listar todos los pacientes usando iteradores de la STL
void listarPacientesSTL(const list<Paciente>& lista) {
    if (lista.empty()) { // Manejo de error nativo de la STL
        cout << "\n[AVISO] No hay pacientes registrados en la clinica.\n";
        return;
    }

    cout << "\n=== LISTA DE PACIENTES REGISTRADOS (STL) ===\n";
    // Recorrido moderno basado en rangos (Range-based for loop)
    for (const auto& paciente : lista) {
        cout << "ID: " << paciente.id 
             << " | Nombre: " << paciente.nombre 
             << " | Edad: " << paciente.edad << " anos\n";
    }
}

// Función para modificar un paciente usando iteradores de la STL
void modificarPacienteSTL(list<Paciente>& lista, int id) {
    for (auto& paciente : lista) {
        if (paciente.id == id) {
            cout << "\nPaciente encontrado. Ingrese los nuevos datos:\n";
            cout << "Nuevo Nombre: ";
            cin.ignore();
            getline(cin, paciente.nombre);
            cout << "Nueva Edad: ";
            cin >> paciente.edad;
            cout << "\n[OK] Datos del paciente actualizados correctamente.\n";
            return;
        }
    }
    cout << "\n[ERROR] No se encontro ningun paciente con el ID especificado.\n";
}

// Función para eliminar un paciente utilizando las herramientas de remoción de la STL
void eliminarPacienteSTL(list<Paciente>& lista, int id) {
    if (lista.empty()) {
        cout << "\n[ERROR] La lista esta vacia. No se puede eliminar.\n";
        return;
    }

    // Buscamos el elemento mediante un iterador estándar
    auto it = find_if(lista.begin(), lista.end(), [id](const Paciente& p) {
        return p.id == id;
    });

    if (it != lista.end()) {
        lista.erase(it); // Remueve el nodo y libera memoria automáticamente de forma O(1)
        cout << "\n[OK] Paciente eliminado correctamente del sistema.\n";
    } else {
        cout << "\n[ERROR] No se encontro ningun paciente con el ID especificado.\n";
    }
}

int main() {
    list<Paciente> clinicaSTL; // Declaración del contenedor dinámico STL
    int opcion, id, edad;
    string nombre;

    do {
        cout << "\n=== MENU CLINICA LOCAL (LISTAS STL) ===\n";
        cout << "1. Registrar Paciente\n";
        cout << "2. Listar Pacientes\n";
        cout << "3. Modificar Paciente\n";
        cout << "4. Eliminar Paciente\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        switch (opcion) {
            case 1: {
                cout << "Ingrese ID único: ";
                cin >> id;
                cout << "Ingrese Nombre completo: ";
                cin.ignore();
                getline(cin, nombre);
                cout << "Ingrese Edad: ";
                cin >> edad;
                
                Paciente nuevo{id, nombre, edad};
                clinicaSTL.push_back(nuevo); // Inserción limpia y directa al final de la lista
                cout << "\n[OK] Paciente registrado con exito.\n";
                break;
            }
            case 2:
                listarPacientesSTL(clinicaSTL);
                break;
            case 3:
                cout << "Ingrese el ID del paciente a modificar: ";
                cin >> id;
                modificarPacienteSTL(clinicaSTL, id);
                break;
            case 4:
                cout << "Ingrese el ID del paciente a eliminar: ";
                cin >> id;
                eliminarPacienteSTL(clinicaSTL, id);
                break;
            case 5:
                cout << "\nSaliendo del sistema...\n";
                break;
            default:
                cout << "\n[OPCION INVALIDA] Intente nuevamente.\n";
        }
    } while (opcion != 5);

    return 0;
}