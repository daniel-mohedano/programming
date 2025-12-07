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

/*---------------------------------------------------------------*/
/*---------------------------------------------------------------*/
/*---------------------------------------------------------------*/

void test_case(){
    vi s(4);

    for0(i, 4){
        cin >> s[i];
    }

    if ((*max_element(s.begin(), s.end() - 2) < *min_element(s.begin() + 2, s.end())) ||
        (*min_element(s.begin(), s.end() - 2) > *max_element(s.begin() + 2, s.end())))
        cout << "NO\n";
    else
        cout << "YES\n";
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    
    int t;
    cin >> t;
    while (t--)
        test_case();
    return 0;
}
