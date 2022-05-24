import form
import numpy as np
from form import show

def tranBin(x):
    '''
    将给定的8位16进制数转换为64位2进制数

    input:
        x -- 8位16进制数
    output:
        ans -- 64位2进制数
    '''
    ans=bin(x).replace('0b','')
    l=len(ans)
    if(l<64):
        for i in range(64-l):
            ans='0'+ans
    return ans

def tranPc_1(K):
    '''
    将K进行Pc_1变换
    input:
        K -- 64bit 2进制数
    output:    
        K0 -- 56bit 2进制数
    '''
    tran=form.getPc_1()
    K0=[]
    for i in range(56):
        K0.append(K[tran[i]-1])
    return K0

def tranPc_2(K):
    '''
    将K进行Pc_1变换
    input:
        K -- 56 2进制数组
    output:    
        K0 -- 48 2进制数组
    '''
    tran=form.getPc_2()
    K0=[]
    for i in range(48):
        K0.append(K[tran[i]-1])
    return K0

def tranIP(M):
    '''
    将M进行IP变换
    input:
        M -- 64 2进制数组
    output:    
        M0 -- 64 2进制数组
    '''
    tran=form.getIP()
    M0=[]
    for i in range(64):
        M0.append(M[tran[i]-1])
    return M0

def fXor(r,k):
    '''
    将r扩展为48bit，和k作异或，结果再变为32位
    input:
        r -- 32bit 2进制数组
        k -- 48bit 2进制数组
    output:    
        res -- 32bit 2进制数组
    '''
    r=tranE(r)
    # print("the extend Rn-1:")
    # show(r)
    # print("the Kn:")
    # show(k)
    r=np.array(r)
    k=np.array(k)
    res=r^k
    res=np.array(res)
    # print("the answer of r^k:")
    # show(res)
    res=res.reshape((8,6))
    res=tranS(res)
    # print("32bit before S：")
    # show(res)
    res=tranP(res)
    # print("32bit after P：")
    # show(res)
    return res

def tranE(r):
    '''
    将r进行E变换
    input:
        r -- 32 2进制数组
    output:    
        res -- 48 2进制数组
    '''
    tran=form.getE()
    res=[]
    for i in range(48):
        res.append(r[tran[i]-1])
    return res

def tranS(res):
    '''
    将res进行S变换
    input:
        res -- 8*6 2进制数组
    output:    
        ans -- 32bit 2进制数组
    '''
    ans=[]
    for i in range(8):
        tran=form.getS(i+1)
        x=res[i][0]*2+res[i][5]
        y=res[i][1]*8+res[i][2]*4+res[i][3]*2+res[i][4]
        k=tran[x][y]
        k=bin(k).replace('0b','')
        l=len(k)
        if(l<4):
            for j in range(4-l):
                k='0'+k
        k=list(map(int,k))
        ans.append(k)
    ans=np.array(ans)
    ans=ans.ravel()
    return ans

def tranP(res):
    '''
    将res进行S变换
    input:
        res -- 32bit 2进制数组
    output:    
        ans -- 32bit 2进制数组
    '''
    tran=form.getP()
    ans=[]
    for i in range(32):
        ans.append(res[tran[i]-1])
    return ans

def tranIP_1(C):
    '''
    将C进行IP_1变换
    input:
        C -- 64bit 2进制数组
    output:    
        ans -- 64bit 2进制数组
    '''
    tran=form.getIP_1()
    ans=[]
    for i in range(64):
        ans.append(C[tran[i]-1])
    return ans


