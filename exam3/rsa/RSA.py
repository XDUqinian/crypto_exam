from rsa import RSAKeyGenerator as mykey
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
    # print(msg)
    msg=msg.hex()
    # print(msg)
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
def Encrypto(e,n,data,savepath):
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
    # print(C)
    cipher_text=CreateEncryptoFile(C,savepath)
    print("rsa    加密结果:",cipher_text)
    return cipher_text
def Decrypto(d,n,C,savepath):
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
    # print(M)
    data_text=CreateDecryptoFile(M,savepath)
    return data_text
def CreateEncryptoFile(C,savepath):
    '''
    生成加密文件
    input:
        C -- 密文
    ''' 
    cipher_text=''
    with open(savepath+"/rsa_encrypto.txt", "w",encoding='UTF-8') as t:
        for cipher in C:
            cipher_text+=cipher
            t.write(cipher)
    return cipher_text
def CreateDecryptoFile(M,savepath):
    '''
    生成解密文件
    input:
        M -- 明文
    ''' 
    msg=""
    for row in M: msg+=row
    msg_len=len(msg)
    msg_len=len(msg)-int(msg[-1])
    msg=msg[0:msg_len]
    # print("here",msg)
    msg=bytes.fromhex(msg)
    # print(msg)
    msg=msg.decode("utf-8")
    with open(savepath+"/rsa_decrypto.txt","w",encoding="UTF-8") as t:
        t.write(msg)
    return msg
def RSAEncrypyo(e,n,msg,savepath):
    msg = bytes(msg,'UTF-8')
    # print(msg)
    msg=msg.hex()
    # print(msg)
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
    # print("data",data)
    cipher_text=Encrypto(e,n,data,savepath)
    return cipher_text
def RSADecrypyo(d,n,msg,savepath):
    msg_len=len(msg)
    data=[]
    left = 0
    for i in range(msg_len+1):
        if i>0 and i % 6 == 0:
            data.append(msg[left: i])
            left = i
    msg_text=Decrypto(d,n,data,savepath)
    return msg_text
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