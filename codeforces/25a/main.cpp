#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;

int main(){
    int n, input;
    scanf("%d", &n);

    int last_odd = 0, last_even = 0, count_even = 0;
    for (int i = 1; i <= n; ++i){
        scanf("%d", &input);
        if (input % 2) {
            last_even = i;
            ++count_even;
        }
        else {
            last_odd = i;
        }
    }

    if (count_even == 1) cout << last_even << endl;
    else cout << last_odd << endl;
    
    return 0;
}
