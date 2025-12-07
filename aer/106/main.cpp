#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>

using namespace std;

string known[9] = {"0", "380", "50", "539", "560", "70", "759", "850", "890"};
string countries[9] = {"EEUU", "Bulgaria", "Inglaterra", "Irlanda", "Portugal", "Noruega", "Venezuela", "Cuba", "India"};

string process(string input){
    /* Process codes */
    string output = "";
    if (input.length() < 8){
        while(output.length() < 8 - input.length()) output += "0";
        return output + input;
    }
    else if (input.length() > 8 && input.length() < 13){
        while(output.length() < 13 - input.length()) output += "0";
        return output + input;
    }
    return input;
}

int check(string code){
    int country = -1;
    string real_code = code;
    if (code.length() == 13){
        for (int i = 0; i < 9; i++){
            if (!code.compare(0, known[i].length(), known[i])){
                country = i;
                break;
            }
        }

    }



    int control = real_code.back() - '0';
    int sum = 0;
    for (int i = 2; i <= real_code.length(); i++){
        if (!(i%2)) sum += (real_code[real_code.length()-i] - '0')*3;
        else sum += real_code[real_code.length()-i] - '0';
    }

    if ((sum+control)%10) return -1;
    else return country + 1;
}

int main(){
    vector<string> codes;
    string in = "";
    int result;

    while (in.compare("0")){
        cin >> in;
        if (in.compare("0")){
            codes.push_back(in);
        }
    }

    for (int i = 0; i < codes.size(); i++){
        codes[i] = process(codes[i]);
        result = check(codes[i]);
        if (result == -1) cout << "NO";
        else{
            cout << "SI";
            if (codes[i].length() == 13){
                if (result == 0) cout << " Desconocido";
                else cout << " " << countries[result-1];
            }
        }
        cout << "\n";
    }

    return 0;
}
