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
    int n;
    cin >> n;
    // Read input
    vi uni(n), skills(n);
    for0(i, n){
        cin >> uni[i];
        --uni[i];
    }
    for0(i, n) cin >> skills[i];

    // Store and sort skills of each university
    vvi us(n);
    for0(i, n) us[uni[i]].pb(skills[i]);
    for0(i, n) sort(all(us[i]), greater<int>());

    // Pre calculate sums of all lengths 
    vvl pre(n, vl(1, 0));
    for0(i, n) for(int x: us[i]) pre[i].pb(pre[i].back() + x);

    // Calculate answer
    vl answer(n);
    for0(i, n){
        for1(k, us[i].size())
            answer[k-1] += pre[i][us[i].size() / k * k];
    }
    for0(i, n)
        cout << answer[i] << " ";
    cout << "\n";
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    
    int t;
    cin >> t;
    while (t--)
        test_case();
    return 0;
}
