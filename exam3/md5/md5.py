def PlaintextGroup(filepath):
    '''
    明文以512位分组,若信息长度对512求余结果不为448,就要补位
    用64位存储填充信息前的长度
    input:
        filepath -- 文件路径
    output:
        data -- 512bit明文分组 list
    '''
    with open(filepath, "r") as t:
        msg=t.read()
    msg = bytes(msg,'UTF-8')
    msg=msg.hex()
    msg_len=len(msg)
    data=[]
    left = 0
    for i in range(msg_len):
        if i>0 and i % 128 == 0:
            data.append(msg[left: i])
            left = i
        elif (msg_len - left < 128):
            num='8'
            while(msg_len-left+len(num)%128!=112):
                num+='0'       
            add_len=(msg_len*4)&0xFFFFFFFFFFFFFFFF        
            add_len=hex(add_len).replace('0x','')
            while(len(add_len)<16):add_len=add_len+'0'
            num+=add_len
            msg+=num
            data.append(msg[left: left+128])
            if (msg_len-left)%128<122:break
            left+=128
            data.append(msg[left: left+128])
            break
    # print("md5 明文分组:",data)
    return data
def sub_block(msg):
    '''
    将512位明文分解为16个32位子分组
    input:
        msg -- 512bit明文
    output:
        M -- 16个32bit子分组 list
    ''' 
    msg_len=len(msg)
    M=[]
    left=0
    for i in range(msg_len+1):
        if i>0 and i % 8 == 0:
            res=msg[left: i]
            l=list(res)
            for k in range(2):
                t=l[k*2]
                l[k*2]=l[7-k*2-1]
                l[7-k*2-1]=t
                t=l[k*2+1]
                l[k*2+1]=l[7-k*2]
                l[7-k*2]=t
            string=''.join(l)
            M.append(int('0x'+string,16))
            left = i
    # print("md5 子分组:",M)
    return M
# x y z 均为32bit整数
def F(x,y,z): return (x&y)|((~x)&z)
def G(x,y,z): return (x&z)|(y&(~z))
def H(x,y,z): return x^y^z
def I(x,y,z): return y^(x|(~z))
def RLS32(input, n): return (input<<n)|(input>>(32-n))&0xFFFFFFFF
def FF(a,b,c,d,Mj,s,ti): return (b+RLS32((a+F(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def GG(a,b,c,d,Mj,s,ti): return (b+RLS32((a+G(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def HH(a,b,c,d,Mj,s,ti): return (b+RLS32((a+H(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def II(a,b,c,d,Mj,s,ti): return (b+RLS32((a+I(b,c,d)+Mj+ti)&0xFFFFFFFF,s))&0xFFFFFFFF
def Roll_4(res,M):
    '''
    对M进行4轮循环运算
    input:
        res -- A B C D
        M -- 16个32bit分组 list
    output:
        res -- A B C D
    '''
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
    return res
def Encrypto(filepath,savepath):
    '''
    md5加密并生成加密文件
    '''
    res=[0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476]
    # res=[0x01234567,0x89ABCDEF,0xFEDCBA98,0x76543210]
    data=PlaintextGroup(filepath)
    cipher=''
    for msg in data:
        M=sub_block(msg)
        res=Roll_4(res,M)
        # print(hex(res[0]),hex(res[1]),hex(res[2]),hex(res[3]))
    for data in res:
        msg=hex(data).replace('0x','')
        while(len(msg)<8):msg='0'+msg
        # print(msg)
        l=list(msg)
        for k in range(2):
            t=l[k*2]
            l[k*2]=l[7-k*2-1]
            l[7-k*2-1]=t
            t=l[k*2+1]
            l[k*2+1]=l[7-k*2]
            l[7-k*2]=t
        string=''.join(l)
        cipher+=string
    print("md5 32 加密结果:",cipher)
    with open(savepath+"\md5_encrypto.txt", "w") as t:
        t.write(cipher)
    return cipher
if __name__ == '__main__':
    Encrypto(r'I:\homework\crypto_exam\exam2\md5\test.txt',r'I:\homework\crypto_exam\exam2\md5')