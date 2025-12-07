#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <unordered_map>

using namespace std;

int main(){
    int n;
    scanf("%d", &n);
    vector<vector<int>> board;
    vector<int> perm;
    for (int i = 0; i < n; ++i) {
        board.push_back(vector<int>(i+1, 0));
        cin >> board[i][i];
        perm.push_back(board[i][i]);
    }
    
    for (int i = 1; i < n; ++i){
        perm.erase(find(perm.begin(), perm.end(), i));
        for (int ii = 0; ii < perm.size(); ++ii){
            board[n - perm.size() + ii][ii] = perm[ii];
        }
    }

    for (auto line : board){
        for (auto it = line.begin(); it != line.end(); ++it){
            cout << *it << ' ';
        }
        cout << endl;
    }

    return 0;
}


