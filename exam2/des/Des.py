import numpy as np
import function as f
import form
from form import show

def CreateC(M,Kn):
    '''
    将给定的8位16进制明文转换为密文
    并展示中间结果

    input:
        Kn -- 16*48的数组,每行存放1个48位二进制子密钥,存16个
        K -- 8位16进制的密钥
        M -- 8位16进制的明文
        t -- 0表示加密 1表示解密
    output:
        C -- 密文
    '''
    M=f.tranBin(M)
    M=list(map(int,M))
    # print("m:")
    # show(M)
    M0=f.tranIP(M)
    # print("m0:")
    # show(M0)
    l=[]
    r=[]
    l.append(M0[0:32])
    r.append(M0[32:64])
    # print("l0:")
    # show(l[0])
    # print("r0:")
    # show(r[0])
    for i in range(16):
        # print("#第",i+1,"次迭代：")
        l.append(r[i])
        # print("l",i+1,":")
        # show(l[i+1])
        mid1=np.array(r[i])
        mid2=f.fXor(mid1,Kn[i+1])
        mid2=np.array(mid2)
        mid3=np.array(l[i])
        mid=mid3^mid2
        mid=mid.tolist()
        r.append(mid)
        # print("r",i+1,":")
        # show(r[i+1])
    C=r[16]+l[16]
    # print("r16l16:")
    # show(C)
    C=f.tranIP_1(C)
    # print("IP_1:")
    # show(C)
    Str = ','.join(str(i) for i in C)
    Str = Str.replace(',', '')
    Str = '0b'+Str
    ans=int(Str,2)
    ans=hex(ans)
    return ans

    
    
