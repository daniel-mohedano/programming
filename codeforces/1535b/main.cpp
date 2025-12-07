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

void test_case(){
    int n;
    cin >> n;
    vi even, odd;
    int temp;
    for0(i, n){
        cin >> temp;
        if (temp % 2) odd.pb(temp);
        else even.pb(temp);
    }

    // Every even number forms a good pair with everyone
    // Sum(good pairs caused by even numbers) = arithmetic series
    // (n-1) + (n-2) + ... + n_odd
    ll answer = even.size() * (odd.size() + n - 1) / 2;

    // Check odd numbers (order doesn't matter)
    for0(i, odd.size()){
        fork(j, i+1, odd.size()){
            if (_gcd(odd[i], odd[j]) > 1) ++answer;
        }
    }
    cout << answer << "\n";
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    
    int t;
    cin >> t;
    while (t--)
        test_case();
    return 0;
}
