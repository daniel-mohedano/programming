#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;

int main(){
    do{
        double ventas[6], first;
        string dias[6] = {"MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"};
        string min_s = "", max_s = "";
        int min_i = 0, max_i = 0;
        double sum = 0;

        cin >> first;
        if (first == -1) break;
        ventas[0] = first;
        sum += first;

        for (int i = 1; i < 6; i++){
            cin >> ventas[i];
            if (ventas[i] == ventas[min_i]){
                min_s = "EMPATE";
            } else if (ventas[i] < ventas[min_i]){
                min_i = i;
                min_s = "";
            } 
            if (ventas[i] == ventas[max_i]){
                max_s = "EMPATE";
            } else if (ventas[i] > ventas[max_i]){
                max_i = i;
                max_s = "";
            }

            sum += ventas[i];        
        }
        sum /= 6;

        if (min_s.empty()) min_s = dias[min_i];
        if (max_s.empty()) max_s = dias[max_i];

        cout << max_s << ' ' << min_s << ' ' << ((ventas[5] > sum) ? "SI" : "NO") << endl;
    }while(true);
    return 0;
}
