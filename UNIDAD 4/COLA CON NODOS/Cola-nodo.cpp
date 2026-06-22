#include <iostream>
#include <string>

using namespace std;

struct Cliente {
    string nombre;
    int boxAsignado;
};

struct Nodo {
    Cliente datos;
    Nodo* siguiente;
};

// Clase que implementa de forma manual la estructura de Cola (FIFO)
class ColaTurnos {
private:
    Nodo* frente;
    Nodo* final;
public:
    ColaTurnos() { frente = nullptr; final = nullptr; }

    bool estaVacia() { return frente == nullptr; }

    void registrarCliente(string nombre) {
        Nodo* nuevo = new Nodo();
        nuevo->datos.nombre = nombre;
        nuevo->datos.boxAsignado = 0; // Se asignará al llamarlo
        nuevo->siguiente = nullptr;

        if (estaVacia()) {
            frente = nuevo;
            final = nuevo;
        } else {
            final->siguiente = nuevo;
            final = nuevo;
        }
        cout << "[REGISTRO] Cliente '" << nombre << "' cargado en la fila.\n";
    }

    void proximoCliente(int numeroBox) {
        if (estaVacia()) {
            cout << "[PANTALLA] No hay clientes en espera en este momento.\n";
            return;
        }
        Nodo* temporal = frente;
        Cliente clienteAtendido = temporal->datos;
        clienteAtendido.boxAsignado = numeroBox;

        cout << "\n========================================\n";
        cout << "      PROXIMO CLIENTE: " << clienteAtendido.nombre << "\n";
        cout << "      POR FAVOR DIRIGIRSE AL BOX: " << clienteAtendido.boxAsignado << "\n";
        cout << "========================================\n";

        frente = frente->siguiente;
        if (frente == nullptr) {
            final = nullptr;
        }
        delete temporal;
    }

    ~ColaTurnos() {
        while (!estaVacia()) {
            Nodo* temp = frente;
            frente = frente->siguiente;
            delete temp;
        }
    }
};

int main() {
    ColaTurnos sistema;
    sistema.registrarCliente("Juan Perez");
    sistema.registrarCliente("Maria Gomez");
    
    sistema.proximoCliente(1); // Llama a Juan
    sistema.proximoCliente(3); // Llama a Maria
    sistema.proximoCliente(2); // Cola vacía
    return 0;
}