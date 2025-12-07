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
#define PI 3.14159265358979323846

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

double gcd(double x, double y)
{
    return fabs(y) < 1e-4 ? x : gcd(y, fmod(x, y));
}

/*---------------------------------------------------------------*/
/*---------------------------------------------------------------*/
/*---------------------------------------------------------------*/

pair<double, double> equidistant_point(vector<pair<double, double>> p){
    pair<double, double> solution;
    double D;

    D = 2 * (p[0].first * (p[1].second - p[2].second) + 
             p[1].first * (p[2].second - p[0].second) +
             p[2].first * (p[0].second - p[1].second));

    solution.first = ((pow(p[0].first, 2) + pow(p[0].second, 2)) * (p[1].second - p[2].second) +
                      (pow(p[1].first, 2) + pow(p[1].second, 2)) * (p[2].second - p[0].second) +
                      (pow(p[2].first, 2) + pow(p[2].second, 2)) * (p[0].second - p[1].second)) / D;
    solution.second = ((pow(p[0].first, 2) + pow(p[0].second, 2)) * (p[2].first - p[1].first) +
                       (pow(p[1].first, 2) + pow(p[1].second, 2)) * (p[0].first - p[2].first) +
                       (pow(p[2].first, 2) + pow(p[2].second, 2)) * (p[1].first - p[0].first)) / D;

    return solution;
}

double angle_of_vectors(pair<double, double> a, pair<double, double> b){
    double dot = a.first * b.first + a.second * b.second;
    double dem = sqrt(pow(a.first, 2) + pow(a.second, 2)) * sqrt(pow(b.first, 2) + pow(b.second, 2));
    return acos(dot / dem);
}

double area_polygon(int n_sides, double radius){
    return radius * radius * n_sides  * 0.5 * sin(2 * PI / n_sides);
}

void test_case(){
    vector<pair<double, double>> pillars(3);
    int i = -1;

    while (++i < 3){
        cin >> pillars[i].first >> pillars[i].second;
    }

    // Calculate center of circle
    pair<double, double> center = equidistant_point(pillars);

    // Compute vectors from center to pillars
    vector<pair<double, double>> vectors(3);
    for (i = 0; i < 3; ++i){
        vectors[i].first = pillars[i].first - center.first;
        vectors[i].second = pillars[i].second - center.second;
    }

    // Angles 
    vector<double> angles(2);
    for (i = 0; i < 2; ++i){
        angles[i] = angle_of_vectors(vectors[i], vectors[i+1]);
    }

    // Look for valid number of sides
    double sector_angle = gcd(angles[0], angles[1]);
    int n = round(2 * PI / sector_angle);
    cout << "N: " << n << endl;

    double radius = sqrt(pow(vectors[0].first, 2) + pow(vectors[0].second, 2));

    printf("%.6lf\n", area_polygon(n, radius));
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    
    test_case();
    return 0;
}
