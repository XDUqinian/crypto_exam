import Des
import form
import function as f
import numpy as np
from form import show

def CreateKn(K,t):
    '''
    将给定的8位16进制密钥转换为16个子密钥
    并展示中间结果

    input:
        K -- 8位16进制的密钥
    output:
        Kn -- 16*48的数组,每行存放1个48位二进制子密钥,存16个
    '''
    K=f.tranBin(K)
    K=list(map(int,K))
    # print("k:",K)
    K0=f.tranPc_1(K)
    # print("k0:")
    # show(K0)
    c=[]
    d=[]
    Kn=[]
    c.append(K0[0:28])
    d.append(K0[28:56])
    Kn.append(K0)
    Ml=form.getMoveLeft()
    for i in range(16):
        x=Ml[i]
        nc=c[i][x:28]+c[i][0:x]
        nd=d[i][x:28]+d[i][0:x]
        c.append(nc)
        d.append(nd)
        Kn.append(nc+nd)

        # print("c",i+1,":")
        # show(nc)
        # print("d",i+1,":")
        # show(nd)

    for i in range(17):
        Kn[i]=f.tranPc_2(Kn[i])
    Kn=np.array(Kn)
    if(t==1):
        Kn=np.flip(Kn,0)
        Kn=np.roll(Kn,1,0)
    # for i in range(17):
        # print("K",i,":")
        # show(Kn[i])
    return Kn

def DesEncrypt(M,K):
    '''
    将给定的8位16进制明文转换为密文
    input:
        K -- 8位16进制的密钥
        M -- 8位16进制的明文 list
    output:
        C -- 密文 list
    '''
    Kn=CreateKn(K,0)
    C=[]
    for msg in M:
        cipher=Des.CreateC(int(msg,16),Kn)
        C.append(cipher.replace('0x',''))
    # print(C)
    return C

def DesDecrypt(C,K):
    '''
    将给定的8位16进制密文转换为明文
    input:
        K -- 8位16进制的密钥
        C -- 8位16进制的密文
    output:
        M -- 明文 list
    '''
    Kn=CreateKn(K,1)
    M=[]
    for cipher in C:
        msg=Des.CreateC(int(cipher,16),Kn)
        M.append(msg.replace('0x',''))
    # print(M)
    return M

def PlaintextGroup():
    '''
    获取明文文件,实现明文分组,不足8位补0,最后一位记录补0的个数
    output:
        data -- list 明文分组,每组8位16进制
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
        if i>0 and i % 16 == 0:
            data.append(msg[left: i])
            left = i
        elif (msg_len - left < 16):
            num=''
            for j in range(16 - msg_len % 16-1):
                num+='0'
            res=16-msg_len%16
            if res==10:res='A'
            elif res==11:res='B'
            elif res==12:res='C'
            elif res==13:res='D'
            elif res==14:res='E'
            elif res==15:res='F'
            num+=str(res)
            data.append(msg[left:msg_len]+num)
            break
    return data
def CreateEncryptoFile(C):
    with open("des_encrypto.txt", "w",encoding='UTF-8') as t:
        for cipher in C:
            t.write(cipher)
def CreateDecryptoFile(M):
    msg=""
    for row in M:
        msg+=row
    res="0123456789abcdef"
    a=0
    for i in range(len(res)):
        if msg[-1]==res[i]:
            a=i
            break
    print(a)
    msg_len=len(msg)-a
    msg=msg[0:msg_len]
    msg=bytes.fromhex(msg)
    print(msg)
    msg=msg.decode("utf-8")
    print(msg)   
    with open("des_decrypto.txt", "w",encoding='UTF-8') as t:
        t.write(msg)
    
if __name__ == '__main__':
    M=PlaintextGroup()
    print(M)
    K=0x133457799BBCDFF1
    # M=0x0123456789ABCDEF
    print("++++++++++++++加密++++++++++++++")
    C=DesEncrypt(M,K)
    CreateEncryptoFile(C)
    print("++++++++++++++解密++++++++++++++")
    Mt=DesDecrypt(C,K)
    CreateDecryptoFile(Mt)