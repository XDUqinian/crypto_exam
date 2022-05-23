#include<cstdio>
#include<string>
#include<iostream>
using namespace std;
int main()
{
    FILE *fp = fopen("test.txt", "rt");
    FILE *res = fopen("map_encrypto.txt", "wt+");
    char ch;
    if(fp == NULL) printf("Cannot open file\n");
    if(res == NULL) printf("Cannot open file\n");
    ch = fgetc(fp);
    int a,b;;
    cout<<"a:";
	cin>>a;
	cout<<"b:";
	cin>>b;
    while(ch != EOF)
	{
    	if(ch>='A'&&ch<='Z') fputc((char)('A'+((ch-'A')*a+b)%26),res);
    	else if(ch>='a'&&ch<='z') fputc((char)('a'+((ch-'a')*a+b)%26),res); 
    	else fputc(ch ,res);
    	ch = fgetc(fp);
    }
    fclose(fp);
    fclose(res);
    return 0;
}
