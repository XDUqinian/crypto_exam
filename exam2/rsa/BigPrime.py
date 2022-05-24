from random import randint
def miller_rabin(p):
    '''
    Miller_Rabin 法判断素数
    input:
        p -- 素数
    output:
        True or False -- 表示不确定或不是素数
    '''
    if p == 1: return False
    if p == 2: return True
    if p % 2 == 0: return False
    m, k, = p - 1, 0
    while m % 2 == 0:
        m, k = m // 2, k + 1
        a = randint(2, p - 1)
        x = pow(a, m, p)
        if x == 1 or x == p - 1: return True
    while k > 1:
        x = pow(x, 2, p)
        if x == 1: return False
        if x == p - 1: return True
        k = k - 1
    return False
def is_prime(p, r = 40):
    '''
    判断素数,多次检测
    input:
        p -- 素数
        r -- 检验次数
    output:
        True or False -- 表示是或不是素数
    '''
    for i in range(r):
        if miller_rabin(p) == False:
            return False
    return True
def createBigPrime():
    '''
    生成1024位大素数
    input:
        p -- 素数
    output:
        True or False -- 表示不确定或不是素数
    '''
    #index大一点才能保证后面的分组够加解密
    index = 12
    # 处理一下让最高位是1保证素数够大
    num = 1
    for i in range(index-1):
        num = num * 2 + randint(0, 1)
    while is_prime(num) == False:
        num = num + 1
    return num