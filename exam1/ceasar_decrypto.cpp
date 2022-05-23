#include<stdio.h>
int main()
{    
    FILE *fp = fopen("ceasar_encrypto.txt", "rt");
    FILE *res = fopen("ceasar_decrypto.txt", "wt+");
    char ch;
    int k=3;
    if(fp == NULL) printf("Cannot open file\n");
    if(res == NULL) printf("Cannot open file\n");
    ch = fgetc(fp);
    while(ch != EOF)
	{
    	if(ch>='A'&&ch<='Z') fputc((ch-'A'-k+26)%26+'A', res);
    	else if(ch>='a'&&ch<='z') fputc((ch-'a'-k+26)%26+'a', res);
    	else fputc(ch ,res);
    	ch = fgetc(fp);
    }
    fclose(fp);
    fclose(res);
    return 0;
}
