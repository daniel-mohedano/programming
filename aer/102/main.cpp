#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;


int main(){
    while(true){
        string str;
        int diff;
        getline(cin, str);

        //Decode the string
        diff = str[0] - 'p';
        //cout << str << " ---> ";
        for (long i = 0; i < str.length(); i++){
            int ch;
            if (str[i] >= 'A' && str[i] <= 'Z'){
                ch = str[i] - diff - 'A';
                if (ch < 0){ ch += 26;}
                else if (ch > 25){ ch -= 26;}
                str[i] = ch + 'A';
            }
            else if (str[i] >= 'a' && str[i] <= 'z'){
                ch = str[i] - diff - 'a';
                if (ch < 0){ ch += 26;}
                else if (ch > 25){ ch -= 26;}
                str[i] = ch + 'a';
            }
        }

        //cout << str << "\n";
        //Check for FIN
        if (str.length() == 4){
            if (str.compare(1, 3, "FIN") == 0){
                break;
            }
        }

        //Count vowels
        long counter = 0;
        for (long i = 1; i < str.length(); i++){
            if (str[i] == 'a' || str[i] == 'e' || str[i] == 'i' || str[i] == 'o' || str[i] == 'u' || str[i] == 'A' || str[i] == 'E' || str[i] == 'I' || str[i] == 'O' || str[i] == 'U'){
                counter++;
            }
        }

        cout << counter << "\n";
    }
    return 0;
}
