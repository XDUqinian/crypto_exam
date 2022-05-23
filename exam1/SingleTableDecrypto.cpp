#include<cstdio>
#include<string>
#include<iostream>
#include<map> 
using namespace std;
string t1="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
string t2="abcdefghijklmnopqrstuvwxyz";
void update(string key)
{
	map<char,int> cnt;
	int len=key.length();
	t1="",t2="";
	for(int i=0;i<len;i++)
	{
		if(key[i]>='a'&&key[i]<='z')
		{
			cnt[key[i]]++,cnt[key[i]-'a'+'A']++;
			if(cnt[key[i]]==1) t1+=key[i],t2+=key[i]-'a'+'A';
		}
		if(key[i]>='A'&&key[i]<='Z')
		{
			cnt[key[i]]++,cnt[key[i]-'A'+'a']++;
			if(cnt[key[i]]==1) t2+=key[i],t1+=key[i]-'A'+'a';
		}
	}
	for(char i='a';i<='z';i++) if(cnt[i]==0) t1+=i,t2+=(i-'a'+'A');
}
inline int find(char ch,int op)
{
	if(op==1) for(int i=0;i<26;i++) if(ch==t1[i]) return i;
	else if(op==2) for(int i=0;i<26;i++) if(ch==t2[i]) return i;
}
int main()
{
    FILE *fp = fopen("SingleTab_encrypto.txt", "rt");
    FILE *res = fopen("SingleTab_decrypto.txt", "wt+");
    char ch;
    if(fp == NULL) printf("Cannot open file\n");
    if(res == NULL) printf("Cannot open file\n");
    ch = fgetc(fp);  
    string key;
    cout<<"key:";
	cin>>key;
	update(key); 
    while(ch != EOF)
	{
    	if(ch>='A'&&ch<='Z') fputc((char)('A'+find(ch,2)),res);
    	else if(ch>='a'&&ch<='z') fputc((char)('a'+find(ch,1)),res); 
    	else fputc(ch ,res);
    	ch = fgetc(fp);
    }
    fclose(fp);
    fclose(res);
    return 0;
}
