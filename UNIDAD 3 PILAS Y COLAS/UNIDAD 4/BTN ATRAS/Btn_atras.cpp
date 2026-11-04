#include <iostream>
#include <stack>
#include <string>

using namespace std;

class HistorialLlamadas {
private:
    stack<string> historialPasado;
    stack<string> historialFuturo;
    string llamadaActual;

public:
    HistorialLlamadas() {
        llamadaActual = "";
    }

    // Registrar o marcar un nuevo número telefónico
    void llamarNumero(string numero) {
        if (!llamadaActual.empty()) {
            historialPasado.push(llamadaActual);
        }
        llamadaActual = numero;
        // Al realizar una nueva llamada limpia la pila de avance (futuro)
        while (!historialFuturo.empty()) {
            historialFuturo.pop();
        }
        cout << "[LLAMADA] Conectando con: " << llamadaActual << "\n";
    }

    // Operación de volver atrás (Botón Back)
    void volverAtras() {
        if (historialPasado.empty()) {
            cout << "[HISTORIAL] No hay llamadas anteriores en el registro.\n";
            return;
        }
        historialFuturo.push(llamadaActual);
        llamadaActual = historialPasado.top();
        historialPasado.pop();
        cout << "[BACK] Regresando a llamada: " << llamadaActual << "\n";
    }

    // Operación de avanzar (Botón Forward)
    void avanzarSiguiente() {
        if (historialFuturo.empty()) {
            cout << "[HISTORIAL] No hay registros para avanzar.\n";
            return;
        }
        historialPasado.push(llamadaActual);
        llamadaActual = historialFuturo.top();
        historialFuturo.pop();
        cout << "[FORWARD] Avanzando a llamada: " << llamadaActual << "\n";
    }

    void mostrarLlamadaActual() {
        if (llamadaActual.empty()) {
            cout << "[ESTADO] No se han realizado llamadas aun.\n";
        } else {
            cout << "[ACTUAL] Mostrando en pantalla: " << llamadaActual << "\n";
        }
    }
};

int main() {
    HistorialLlamadas telefono;
    
    cout << "=== Simulación de Historial de Llamadas ===\n";
    telefono.llamarNumero("2235123456");
    telefono.llamarNumero("2236987654");
    telefono.llamarNumero("1142001234");
    
    telefono.mostrarLlamadaActual(); // 1142001234
    
    telefono.volverAtras();          // Regresa a 2236987654
    telefono.volverAtras();          // Regresa a 2235123456
    
    telefono.avanzarSiguiente() ;    // Avanza de nuevo a 2236987654
    
    return 0;
}