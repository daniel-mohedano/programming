#include <iostream>
#include <algorithm>
#include <vector>
#include <string.h>
#include <math.h>

using namespace std;

int main()
{
    int temp1;
    int temp2;
    vector<int> sizes;
    vector<int> cells;
    do{
        scanf("%d",&temp1);
        sizes.insert(sizes.end(),temp1);
        for (int i = 0; i < pow(sizes.back(),2); ++i){
            scanf("%d",&temp2);
            cells.insert(cells.end(),temp2);
        }
    }while(sizes.back() != 0);

    //int offset = 0;
    //for (int i = 0; i < sizes.size() - 1; ++i){
    //    cout<<sizes[i]<<'\n';
    //    for (int j = 0; j < sizes[i]; ++j){
    //        for (int k = 0; k < sizes[i]; ++k){
    //            cout<<cells[sizes[i]*j + k + offset]<<' ';
    //        }
    //        cout<<'\n';
    //    }
    //    offset += pow(sizes[i],2);
    //}
    
    int current = 0;
    int offset = 0;
    while(sizes[current] != 0){
		//calculate first CM
		int CM = 0;
		int flag = 2;
		vector<int> digits(sizes[current]*sizes[current], 0);
		for (int j = 0; j < sizes[current]; j++) CM += cells[j + offset];
		
		int check_diag1 = 0;
		int check_diag2 = 0;
		for (int i = 0; i < sizes[current]; ++i)
		{
			int check_row = 0;
			int check_column = 0;
			for (int j = 0; j < sizes[current]; j++)
			{
				//check rows i
				check_row += cells[sizes[current]*i + j + offset];
				//check column i
				check_column += cells[sizes[current]*j + i + offset];
				if (digits[cells[sizes[current]*i + j + offset] - 1] != 0) flag = 1;
				else digits[cells[sizes[current]*i + j + offset] - 1] = 1;
			}
			if (check_row != CM || check_column != CM)
			{
				flag = 0;
				break;
			}
			//check main diagonal 1
			check_diag1 += cells[sizes[current]*i + i + offset];
			//check main diagonal 2
			check_diag2 += cells[sizes[current]*(sizes[current] - i - 1) + (sizes[current] - i - 1) + offset];
		} 
		if (check_diag1 != CM || check_diag2 != CM) flag = 0;
		
		if (!flag) cout<<"NO\n";
		else if (flag == 2)
		{
			int CM2 = cells[offset] + cells[sizes[current] - 1 + offset] + cells[sizes[current] * (sizes[current] - 1) + offset] + cells[sizes[current] * (sizes[current] - 1) + sizes[current] - 1 + offset];
			if ((double)CM2 != (double)(4 * CM)/sizes[current]) cout<<"DIABOLICO\n";
			else
			{
				if (sizes[current] % 2)
				{
					int mid = sizes[current]/ 2;
					int sum_mid = cells[mid + offset] + cells[sizes[current]*mid + offset] + cells[sizes[current]*mid + sizes[current] - 1 + offset] + cells[sizes[current]*(sizes[current]-1) + mid + offset];
					if (CM2 != sum_mid || CM2 != 4*cells[sizes[current]*mid + mid + offset]) cout<<"DIABOLICO\n";
					else cout<<"ESOTERICO\n";
				}
				else
				{
					int mid = sizes[current]/ 2;
					int sum_mid1 = cells[mid + offset] + cells[sizes[current]*mid + offset] + cells[sizes[current]*mid + sizes[current] - 1 + offset] + cells[sizes[current]*(sizes[current]-1) + mid + offset];
					int sum_mid2 = cells[mid - 1 + offset] + cells[sizes[current]*(mid-1) + offset] + cells[sizes[current]*(mid-1) + sizes[current] - 1 + offset] + cells[sizes[current]*(sizes[current]-1) + mid - 1 + offset];
					int sum_center = cells[sizes[current]*(mid) + mid + offset] + cells[sizes[current]*(mid-1) + mid + offset] + cells[sizes[current]*(mid) + mid - 1 + offset] + cells[sizes[current]*(mid-1) + mid - 1 + offset];
					if (2*CM2 != sum_mid1+sum_mid2 || CM2 != sum_center) cout<<"DIABOLICO\n";
					else cout<<"ESOTERICO\n";
				}
			}
		}
		else cout<<"DIABOLICO\n";
		
		offset += pow(sizes[current],2);
		++current;
	}
		
    
    
    
    

    
    return 0;
}
