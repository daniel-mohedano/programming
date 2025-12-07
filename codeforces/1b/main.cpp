#include <bits/stdc++.h>

using namespace std;

// Definitions
#define fi first
#define se second
#define pb push_back
#define mp make_pair 
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).end()
#define tr(it, x) for(auto it = x.begin(); it != x.end(); it++)
#define trr(it, x) for (auto it = x.rbegin(); it != x.rend(); it++)
#define for0(i, n) for (int i = 0; i < n; ++i)
#define for1(i, n) for (int i = 1; i <= n; ++i)
#define fork(i, k, n) for (int i = k; i < n; ++i)

typedef long long ll;
typedef vector<int> vi;
typedef vector<ll> vl;
typedef vector<string> vs;
typedef vector<vector<int>> vvi;
typedef vector<vector<ll>> vvl;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;
typedef vector<pii> vii;
typedef vector<pll> vll;

inline int _gcd(int a, int b){
    return b ? _gcd(b, a % b) : a;
}

/*---------------------------------------------------------------*/
/*---------------------------------------------------------------*/
/*---------------------------------------------------------------*/

string num_to_string(int n){
    string s = "";

    while (n != 0){
        s.insert(0, 1, 'A' + ((n - 1) % 26));
        n = (int)floor((n - 1) / 26);
    }

    return s;
}

int string_to_num(string s){
    int n = 0;

    for (auto &c : s){
        n *= 26;
        n += c - 'A' + 1;
    }

    return n;
}

void test_case(){
    string coord;
    cin >> coord;

    if (coord[0] == 'R' && coord[1] >= '0' && coord[1] <= '9' && coord.find("C") != string::npos){
        // Type 2
        size_t pos_C = coord.find("C");
        int row = stoi(coord.substr(1, pos_C - 1));
        int col = stoi(coord.substr(pos_C + 1, coord.length() - (pos_C + 1)));

        cout << num_to_string(col) << row << "\n";
    }else{
        // Type 1
        size_t change = 0;
        for (size_t i = 0; i < coord.length(); ++i){
            if (coord[i] >= '0' && coord[i] <= '9'){
                change = i;
                break;
            }
        }

        string col_str = coord.substr(0, change);
        string row_str = coord.substr(change, coord.length() - change);

        cout << "R" << row_str << "C" << string_to_num(col_str) << "\n";
    }
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    
    int t;
    cin >> t;
    while (t--)
        test_case();
    return 0;
}
