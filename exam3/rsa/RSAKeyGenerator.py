from rsa import BigPrime
from random import randint
def CreateN():
    '''
    随机生成两个大素数p和q且保密,计算并公开n=pq
    input:
        null
    output:
        N list -- n phi(n)
    '''
    p=BigPrime.createBigPrime()
    q=BigPrime.createBigPrime()
    # print("两个大素数：")
    # print(p)
    # print(q)
    n=p*q
    phi_n=(p-1)*(q-1)
    N=[]
    N.append(n)
    N.append(phi_n)
    return N

def exgcd(a, m):
    '''
    拓展欧几里德算法求逆元
    input:
        a m -- 求a模m的逆元 
    output:
        x -- 逆元
    ''' 
    if a < m:
        a, m = m, a
        x1, x2,x3= 1, 0, a
        y1, y2,y3= 0, 1, m
        while y3 != 0:
            Q = x3//y3
            t1, t2, t3 = x1 - Q*y1, x2 - Q*y2, x3 - Q*y3
            x1, x2, x3 = y1, y2, y3
            y1, y2, y3 = t1, t2, t3
        return x2
    else:
        x1, x2, x3 = 1, 0, a
        y1, y2, y3 = 0, 1, m
        while y3 != 0:
            Q = x3 // y3
            t1, t2, t3 = x1 - Q*y1, x2 - Q*y2, x3 - Q*y3
            x1, x2, x3 = y1, y2, y3
            y1, y2, y3 = t1, t2, t3
        return x1
def is_gcd(x,y):
    '''
    判断是否互质
    input:
        x y -- 待判断的数
    output:
        True or False -- 是否互质
    '''
    while x%y:
        x,y=y,x%y
    if y==1 : return True
    return False
def KeyGenerator():
    '''
    生成公私钥对
    input:
        null 
    output:
        key list
        e n -- 公钥
        d n -- 私钥
    ''' 
    N=CreateN()
    phi_n=N[1]
    n=N[0]
    e=randint(2,phi_n-1)
    while(is_gcd(e,phi_n)==False):
        e=randint(2,phi_n-1)
    # print(is_gcd(e,phi_n))
    d=(exgcd(e,phi_n)+phi_n)%phi_n
    # print(e*d%phi_n)
    # print(e)
    # print(d)
    key=[]
    temp=[]
    temp.append(e)
    temp.append(n)
    key.append(temp)
    temp1=[]
    temp1.append(d)
    temp1.append(n)
    key.append(temp1)
    # print(key)
    return key
if __name__ == '__main__':
    key=KeyGenerator()
    print(key)