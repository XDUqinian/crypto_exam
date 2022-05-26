import RSAKeyGenerator as mykey
def PlaintextGroup():
    '''
    返回明文分组
    input:
        null 
    output:
        data list
    ''' 
    with open("test.txt", "r",encoding='UTF-8') as t:
        msg=t.read()
    msg = bytes(msg,'UTF-8')
    print(msg)
    msg=msg.hex()
    print(msg)
    msg_len=len(msg)
    data=[]
    left = 0
    for i in range(msg_len):
        if i>0 and i % 5 == 0:
            data.append(msg[left: i])
            left = i
        elif (msg_len - left < 5):
            num=''
            for j in range(5 - msg_len % 5-1):
                num+='0'
            num+=str(5-msg_len%5)
            data.append(msg[left:msg_len]+num)
            break
    return data
def ksm(a,k,mod):
    '''
    快速幂
    input:
        a -- 底数
        k -- 幂数
        mod -- 模数 
    output:
        res -- 结果
    ''' 
    res=1
    while(k>0):	
        if k&1 : res=res*a%mod
        a=a*a%mod
        k>>=1
    return res%mod
def Encrypto(e,n,data):
    '''
    RSA加密,生成加密文件
    input:
        e n -- 公钥
        data -- 明文list 
    output:
        C -- 密文
    ''' 
    C=[]
    for m in data:
        cipher=ksm(int('0x'+m,16),e,n)
        cipher=hex(cipher)
        cipher=cipher.replace('0x','')
        while len(cipher)<6:
            cipher='0'+cipher
        C.append(cipher)
    CreateEncryptoFile(C)
    print(C)
    return C
def Decrypto(d,n,C):
    '''
    RSA解密,生成明文文件
    input:
        d,n -- 私钥
        C -- 密文 
    output:
        M -- 明文
    ''' 
    M=[]
    for cipher in C:
        # msg=ksm(cipher,d,n)
        msg=ksm(int('0x'+cipher,16),d,n)
        msg=hex(msg).replace('0x','')
        while len(msg)<5:
            msg='0'+msg
        M.append(msg)
    print(M)
    CreateDecryptoFile(M)
    return M
def CreateEncryptoFile(C):
    '''
    生成加密文件
    input:
        C -- 密文
    ''' 
    with open("rsa_encrypto.txt", "w",encoding='UTF-8') as t:
        for cipher in C:
            t.write(cipher)
def CreateDecryptoFile(M):
    '''
    生成解密文件
    input:
        M -- 明文
    ''' 
    msg=""
    for row in M: msg+=row
    msg_len=len(msg)
    if msg[-2]=='0': msg_len=len(msg)-int(msg[-1])
    msg=msg[0:msg_len]
    msg=bytes.fromhex(msg)
    msg=msg.decode("utf-8")
    with open("rsa_decrypto.txt","w",encoding="UTF-8") as t:
        t.write(msg)
if __name__ == '__main__':
    data=PlaintextGroup()
    # print(data)
    key=mykey.KeyGenerator()
    e=key[0][0]
    n=key[0][1]
    d=key[1][0]
    # print(e)
    # print(d)
    # print(n)
    C=Encrypto(e,n,data)
    Decrypto(d,n,C)