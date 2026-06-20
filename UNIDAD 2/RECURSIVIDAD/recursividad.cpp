#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Estructura para representar a cada cliente
struct Cliente {
    string nombre;
    int tiempoAtencion; // Tiempo estimado que tomará atenderlo en minutos
};

// Función RECURSIVA para calcular e imprimir los tiempos de espera acumulados
// Procesa la lista desde el último que llegó hacia el primero, acumulando los tiempos.
int calcularEsperaRecursiva(const vector<Cliente>& lista, int indice) {
    // Caso Base: El primer cliente de la fila (índice 0) solo espera su propio tiempo de atención
    if (indice == 0) {
        cout << "Cliente: " << lista[indice].nombre 
             << " -> Tiempo de espera en cola: 0 min (Sera atendido de inmediato. Tiempo de Box: " 
             << lista[indice].tiempoAtencion << " min)." << endl;
        return lista[indice].tiempoAtencion;
    }
    
    // Caso Recursivo: El tiempo de espera del cliente actual depende de la suma de los anteriores
    int esperaAcumuladaAnteriores = calcularEsperaRecursiva(lista, indice - 1);
    
    cout << "Cliente: " << lista[indice].nombre 
         << " -> Tiempo de espera en cola: " << esperaAcumuladaAnteriores << " min." << endl;
         
    // Retorna el total acumulado hasta este cliente para el próximo en la fila
    return esperaAcumuladaAnteriores + lista[indice].tiempoAtencion;
}

int main() {
    // Simulación del registro de clientes según orden de llegada (Box de Atención)
    vector<Cliente> colaTurnos;
    
    colaTurnos.push_back({"Juan Perez", 10});    // Llega 1° (Toma 10 min)
    colaTurnos.push_back({"Maria Gomez", 15});  // Llega 2° (Toma 15 min)
    colaTurnos.push_back({"Carlos Lopez", 8});   // Llega 3° (Toma 8 min)
    colaTurnos.push_back({"Ana Martinez", 12}); // Llega 4° (Toma 12 min)

    cout << "=== PANTALLA DE TURNOS ===" << endl;
    cout << "Proximo cliente -> Box 1" << endl;
    cout << "----------------------------------------" << endl;
    cout << "=== REPORTE DE TIEMPOS DE ESPERA (RECURSIVO) ===" << endl;
    
    if (!colaTurnos.empty()) {
        // Llamada inicial pasando el índice del último cliente en la cola
        calcularEsperaRecursiva(colaTurnos, colaTurnos.size() - 1);
    }

    return 0;
}