#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <math.h>

using namespace std;

double calc(int degree, int* coefs, double x){
    //Calculate the value of a certain point
    double value = 0;
    for (int i = 0; i < degree + 1; i++){
        value += double(coefs[i])*pow(x, double(degree - i));
    }
    //cout << "f(" << x << ") = " << value << '\n';
    return value;
}

int main(){
    do{
        int degree;
        int coef;
        long rects;

        double cain = 0;
        double width;
        double height;

        //Read data
        scanf("%d",&degree);
        if (degree == 20) break;
        int coefs[degree+1];

        for (int i = 0; i < degree + 1; i++){
            scanf("%d", &(coefs[i]));
        }
        scanf("%ld", &rects);

        /*cout << degree << '\n';
        for (int i = 0; i < degree + 1; i++){
            cout << coefs[i] << ' ';
        }
        cout << '\n';
        cout << rects << '\n';*/


        //Calculate CAIN's area
        width = 1.0/rects;
        double x = 0;
        for (double i = 0; i < rects; i++){
            height = calc(degree, coefs, x);
            height = min(height, 1.0);
            height = max(height, 0.0);
            cain += height;
            x += width;
            //cout << "Rect(" << i << ") = " << cain << '\n';
        }

        cain *= width;

        //Result
        if (cain >= 0.499 && cain <= 0.501) cout << "JUSTO\n";
        else if (cain > 0.5) cout << "CAIN\n";
        else cout << "ABEL\n";

    }while(true);

    return 0;
}
