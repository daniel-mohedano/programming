#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <unordered_map>

using namespace std;

int main(){
    unordered_map<string, int> db;
    string output = "";
    int n;
    string input;
    scanf("%d", &n);

    for (int i = 0; i < n; ++i){
        cin >> input;
        if(db.find(input) != db.end()){
            int post = db.at(input);
            db[input] = post + 1;
            output += input + to_string(post) + '\n';
        }else{
            db.insert({input, 1});
            output += "OK\n";
        }   
    }

    cout << output;
    return 0;
}
