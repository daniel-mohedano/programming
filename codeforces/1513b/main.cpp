#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <unordered_map>
#include <set>

using namespace std;
/*bool check(int n, uint32_t nums[]){
    if (count(nums, nums+n, nums[0]) == n) return true;

    if (nums[0] != nums[n-1]) return false;

    for (int i = 1; i < n - 1; ++i) if ((nums[i] & nums[0]) != nums[0]) return false; 
    return true;
}*/

/*long long factorial(int n){
    return (n==1 || n==0) ? 1: 1LL*n*factorial(n-1);
}*/

/*int permutations(int n, uint32_t nums[]){
    unordered_map<int, int> counts;
    int result = 1;
    for (int i = 0; i < n; ++i){
        counts[nums[i]]++;
    }

    for (auto it : counts) result *= factorial(it.second);
    return result;
}*/

/*void test_case(){
    int n, result;
    scanf("%d", &n);
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) cin >> nums[i];

    int min = *min_element(nums.begin(), nums.end());
    int count = 0;

    for (int elem : nums){
        if (elem == min) ++count;
        if (elem & min != min){
            cout << "0" << endl;
            return;
        }
    }

    int f = factorial(n-2) % int(1e9+7);
    result = (1LL * count * (count - 1) * f) % int(1e9+7);    
    cout << result << endl;
}*/

void test_case(){
    int MOD=1e9+7;
    int n;
    cin>>n;
    vector<int> a(n);
    for(int i=0;i<n;i++)cin>>a[i];
    
    int min1=*min_element(a.begin(),a.end());
    int cnt=0;
    
    for(int x:a)
    {
        if(min1==x)cnt++;
        if((min1&x)!=min1)
        {
            printf("0\n");
            return;
        }
    }
    
    int fact=1;
    for(int i=1;i<=n-2;i++)fact=(1LL*fact*i)%MOD;
    int ans=(1LL * cnt * (cnt-1))%MOD;
    ans = (1LL * ans * fact) % MOD;
    printf("%d\n",ans);
}

int main(){
    int t;
    scanf("%d", &t);
    while (t--){
        test_case();
    }
    return 0;
}
