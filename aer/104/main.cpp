#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;

bool balanced(int pi, int di, int pd, int dd, int &weight){
    bool left = true;
    if (pi == 0){
        int ipi, idi, ipd, idd;
        cin >> ipi >> idi >> ipd >> idd;
        left = balanced(ipi, idi, ipd, idd, pi);
    }

    bool right = true;
    if (pd == 0){
        int dpi, ddi, dpd, ddd;
        cin >> dpi >> ddi >> dpd >> ddd;
        right = balanced(dpi, ddi, dpd, ddd, pd);
    }

    weight = pi + pd;
    return left && right && pi*di == pd*dd;
}

int main(){
    int pi, di, pd, dd, w;
    while (cin >> pi >> di >> pd >> dd && !(pi == 0 && di == 0 && pd == 0 && dd == 0)){
        cout << (balanced(pi, di, pd, dd, w) ? "SI" : "NO") << '\n';
    }
    return 0;
}
