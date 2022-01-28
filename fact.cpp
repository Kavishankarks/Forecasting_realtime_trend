#include <iostream>
using namespace std;
long long int fact(int n)
{
	if(n==0 || n==1)
		return 1;
	else
		return n*fact(n-1);
}
int main()
{
	int a;
	cout<<"fact:";
	cin>>a;
	cout<<fact(a);
}