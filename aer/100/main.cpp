#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;

int convert(vector<int> x, bool type){
    int n = 0;
    int factor = 1000;
    if (type){
        for (int i = 0; i < 4; ++i){
            n += factor*x[i];
            factor/=10;
        }
    }else{
        for (int i = 3; i >= 0; --i){
            n += factor*x[i];
            factor/=10;
        }
    }
    return n;
}



int main(){
    int n;
    scanf("%d",&n);
    char numbers[n][5];
    for (int i = 0; i < n; ++i){
        scanf("%s", numbers[i]);
        if (strlen(numbers[i]) < 4){
            if (strlen(numbers[i]) < 3){
                if (strlen(numbers[i]) < 2){
                    for (int j = 4; j > 2; --j) numbers[i][j] = numbers[i][j-3];
                    numbers[i][0] = '0';
                    numbers[i][1] = '0';
                    numbers[i][2] = '0';
                }else
                {
                    for (int j = 4; j > 1; --j) numbers[i][j] = numbers[i][j-2];
                    numbers[i][0] = '0';
                    numbers[i][1] = '0';
                }
                
            }else{
                for (int j = 4; j > 0; --j) numbers[i][j] = numbers[i][j-1];
                numbers[i][0] = '0';
            }
        }
    }

    for (int i=0;i<n;++i){
        if (numbers[n][0] == numbers[n][1] && numbers[n][1] == numbers[n][2] && numbers[n][2] == numbers[n][3]){
            cout<<8<<'\n';
        }
        else{
            vector<int> digits(4);
            for (int j=0; j<4; ++j) digits[j] = numbers[i][j] - '0';
            int counter = 0;
            while(convert(digits,1) != 6174 && counter < 8){    
                sort(digits.begin(), digits.end());                
                int newn = convert(digits, 0) - convert(digits, 1);
                int factor = 1000;
                for (int k = 0; k < 4; ++k){
                    digits[k] = newn/factor;
                    newn = newn - digits[k]*factor;
                    factor/=10;
                }
                ++counter;
            }
            cout<<counter<<'\n';
        }
    }
    return 0;
}
