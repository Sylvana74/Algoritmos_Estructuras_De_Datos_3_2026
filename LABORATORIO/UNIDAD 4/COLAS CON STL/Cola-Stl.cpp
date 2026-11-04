#include <iostream>
#include <queue>
#include <string>

using namespace std;

struct Cliente {
    string nombre;
};

int main() {
    queue<Cliente> colaEspera;

    // Registrar clientes (Enqueue de la STL)
    colaEspera.push({"Carlos Lopez"});
    colaEspera.push({"Ana Martinez"});

    // Llamar clientes (FIFO)
    int boxActual = 1;
    while (!colaEspera.empty()) {
        Cliente proximo = colaEspera.front(); // Consulta el frente
        
        cout << "\n[PANTALLA STL] Proximo cliente: " << proximo.nombre 
             << " -- Box Nro: " << boxActual++ << "\n";
             
        colaEspera.pop(); // Desencola de forma segura
    }
    return 0;
}