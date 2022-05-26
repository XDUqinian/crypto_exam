# md5 python 实现

## 补位

信息计算前先要进行位补位，设补位后信息的长度为LEN(bit)，则LEN%512 = 448(bit)，即数据扩展至 K * 512 + 448(bit)。即K * 64+56(byte)，K为整数。

补位操作始终要执行，即使补位前信息的长度对512求余的结果是448。

具体补位操作：补一个1，然后补0至满足上述要求。总共最少要补1bit，最多补512bit。

# 尾部加上信息长度

将输入信息的原始长度b(bit)表示成一个64-bit的数字，把它添加到上一步的结果后面。

在32位的机器上，这64位将用**2个字来表示**并且**低位在前**。

当遇到b大于2^64这种极少的情况时，b的高位被截去，仅使用b的低64位。

经过上面两步，数据就被填补成长度为512(bit)的倍数。也就是说，此时的数据长度是16个字(32byte)的整数倍。此时的数据表示为： M[0 ... N-1] 其中的N是16的倍数。

# 初始化

用一个四个字的缓冲器(A，B，C，D)来计算报文摘要，A,B,C,D分别是32位的寄存器，初始化使用的是十六进制表示的数字，注意**低字节在前**。

```python
res=[0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476]
```

 # 4轮转换

一些辅助函数：

```python
def F(x,y,z): return (x&y)|((~x)&z)
def G(x,y,z): return (x&z)|(y&(~z))
def H(x,y,z): return x^y^z
def I(x,y,z): return y^(x|(~z))
def RLS32(input, n): return (input<<n)|(input>>(32-n))&0xFFFFFFFF
def FF(a,b,c,d,Mj,s,ti): return (b+RLS32((a+F(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def GG(a,b,c,d,Mj,s,ti): return (b+RLS32((a+G(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def HH(a,b,c,d,Mj,s,ti): return (b+RLS32((a+H(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def II(a,b,c,d,Mj,s,ti): return (b+RLS32((a+I(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
```

4轮转换如下，然后用下一组数据继续运行算法，最后得到res。

```python
a=res[0]
b=res[1]
c=res[2]
d=res[3]
# print(hex(a),hex(b),hex(c),hex(d))
#Round 1
a=FF(a,b,c,d,M[0],7,0xd76aa478)
d=FF(d,a,b,c,M[1],12,0xe8c7b756)
c=FF(c,d,a,b,M[2],17,0x242070db)
b=FF(b,c,d,a,M[3],22,0xc1bdceee)
# print(hex(a),hex(b),hex(c),hex(d))
a=FF(a,b,c,d,M[4],7,0xf57c0faf)
d=FF(d,a,b,c,M[5],12,0x4787c62a)
c=FF(c,d,a,b,M[6],17,0xa8304613)
b=FF(b,c,d,a,M[7],22,0xfd469501)
# print(hex(a),hex(b),hex(c),hex(d))
a=FF(a,b,c,d,M[8],7,0x698098d8)
d=FF(d,a,b,c,M[9],12,0x8b44f7af)
c=FF(c,d,a,b,M[10],17,0xffff5bb1)
b=FF(b,c,d,a,M[11],22,0x895cd7be)
# print(hex(a),hex(b),hex(c),hex(d))
a=FF(a,b,c,d,M[12],7,0x6b901122)
d=FF(d,a,b,c,M[13],12,0xfd987193)
c=FF(c,d,a,b,M[14],17,0xa679438e)
b=FF(b,c,d,a,M[15],22,0x49b40821)
# print(hex(a),hex(b),hex(c),hex(d))
#Round 2
a=GG(a,b,c,d,M[1],5,0xf61e2562)
d=GG(d,a,b,c,M[6],9,0xc040b340)
c=GG(c,d,a,b,M[11],14,0x265e5a51)
b=GG(b,c,d,a,M[0],20,0xe9b6c7aa)
# print(hex(a),hex(b),hex(c),hex(d))
a=GG(a,b,c,d,M[5],5,0xd62f105d)
d=GG(d,a,b,c,M[10],9,0x02441453)
c=GG(c,d,a,b,M[15],14,0xd8a1e681)
b=GG(b,c,d,a,M[4],20,0xe7d3fbc8)
# print(hex(a),hex(b),hex(c),hex(d))
a=GG(a,b,c,d,M[9],5,0x21e1cde6)
d=GG(d,a,b,c,M[14],9,0xc33707d6)
c=GG(c,d,a,b,M[3],14,0xf4d50d87)
b=GG(b,c,d,a,M[8],20,0x455a14ed)
# print(hex(a),hex(b),hex(c),hex(d))
a=GG(a,b,c,d,M[13],5,0xa9e3e905)
d=GG(d,a,b,c,M[2],9,0xfcefa3f8)
c=GG(c,d,a,b,M[7],14,0x676f02d9)
b=GG(b,c,d,a,M[12],20,0x8d2a4c8a)
# print(hex(a),hex(b),hex(c),hex(d))
#Round 3
a=HH(a,b,c,d,M[5],4,0xfffa3942)
d=HH(d,a,b,c,M[8],11,0x8771f681)
c=HH(c,d,a,b,M[11],16,0x6d9d6122)
b=HH(b,c,d,a,M[14],23,0xfde5380c)
# print(hex(a),hex(b),hex(c),hex(d))
a=HH(a,b,c,d,M[1],4,0xa4beea44)
d=HH(d,a,b,c,M[4],11,0x4bdecfa9)
c=HH(c,d,a,b,M[7],16,0xf6bb4b60)
b=HH(b,c,d,a,M[10],23,0xbebfbc70)
# print(hex(a),hex(b),hex(c),hex(d))
a=HH(a,b,c,d,M[13],4,0x289b7ec6)
d=HH(d,a,b,c,M[0],11,0xeaa127fa)
c=HH(c,d,a,b,M[3],16,0xd4ef3085)
b=HH(b,c,d,a,M[6],23,0x04881d05)
# print(hex(a),hex(b),hex(c),hex(d))
a=HH(a,b,c,d,M[9],4,0xd9d4d039)
d=HH(d,a,b,c,M[12],11,0xe6db99e5)
c=HH(c,d,a,b,M[15],16,0x1fa27cf8)
b=HH(b,c,d,a,M[2],23,0xc4ac5665)
# print(hex(a),hex(b),hex(c),hex(d))
#Round 4
a=II(a,b,c,d,M[0],6,0xf4292244)
d=II(d,a,b,c,M[7],10,0x432aff97)
c=II(c,d,a,b,M[14],15,0xab9423a7)
b=II(b,c,d,a,M[5],21,0xfc93a039)
# print(hex(a),hex(b),hex(c),hex(d))
a=II(a,b,c,d,M[12],6,0x655b59c3)
d=II(d,a,b,c,M[3],10,0x8f0ccc92)
c=II(c,d,a,b,M[10],15,0xffeff47d)
b=II(b,c,d,a,M[1],21,0x85845dd1)
# print(hex(a),hex(b),hex(c),hex(d))
a=II(a,b,c,d,M[8],6,0x6fa87e4f)
d=II(d,a,b,c,M[15],10,0xfe2ce6e0)
c=II(c,d,a,b,M[6],15,0xa3014314)
b=II(b,c,d,a,M[13],21,0x4e0811a1)
# print(hex(a),hex(b),hex(c),hex(d))
a=II(a,b,c,d,M[4],6,0xf7537e82)
d=II(d,a,b,c,M[11],10,0xbd3af235)
c=II(c,d,a,b,M[2],15,0x2ad7d2bb)
b=II(b,c,d,a,M[9],21,0xeb86d391) 
# print(hex(a),hex(b),hex(c),hex(d))
res[0]=(res[0]+a)&0xFFFFFFFF
res[1]=(res[1]+b)&0xFFFFFFFF
res[2]=(res[2]+c)&0xFFFFFFFF
res[3]=(res[3]+d)&0xFFFFFFFF
```

## 得到结果

将ABCD (**分别为小端存储，低字节在前**) 转换为正常顺序，级联即为密文。

## 体会

python 的与或非优先级没有加减高。

注意md5中的小端存储。

计算过程中溢出采取截断策略。

最坑的是，实验室里的文档有问题……