#include<cstdio>
#include<string>
#include<iostream>
using namespace std;
int niyuan(int x)
{
	int res=1;
	while((x*res)%26!=1) res++;
	return res;
}
int main()
{
    FILE *fp = fopen("map_encrypto.txt", "rt");
    FILE *res = fopen("map_decrypto.txt", "wt+");
    char ch;
    if(fp == NULL) printf("Cannot open file\n");
    if(res == NULL) printf("Cannot open file\n");
    ch = fgetc(fp);
    int a,b;;
    cout<<"a:";
	cin>>a;
	cout<<"b:";
	cin>>b;
	a=niyuan(a);
    while(ch != EOF)
	{
    	if(ch>='A'&&ch<='Z') fputc((char)('A'+((ch-'A'+26-b)%26*a)%26),res);
    	else if(ch>='a'&&ch<='z') fputc((char)('a'+((ch-'a'+26-b)%26*a)%26),res); 
    	else fputc(ch ,res);
    	ch = fgetc(fp);
    }
    fclose(fp);
    fclose(res);
    return 0;
}
