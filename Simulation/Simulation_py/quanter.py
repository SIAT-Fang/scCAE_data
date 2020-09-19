def quanter(x: int):

    res = []
    while x > 3:
        res.append(str(x % 4))
        x = x // 4
    if x:
        res.append(str(x))

    length = len(res)
    for i in range(16-length):
        res.append('0')

    x = ''.join(reversed(res))

    return x


def ACGT(x: int):
    dic = {'0': 'A', '1': 'C', '2': 'G', '3': 'T'}
    q = quanter(x)

    res = []
    for i in q:
        res.append(dic[i])

    x = ''.join(res)+'-1'

    return x


def ACGT_list(x: int):
    lis = []
    for i in range(x):
        lis.append(ACGT(i))

    return lis


if __name__ == '__main__':
    import time
    start = time.time()
    a = ACGT_list(10000000)
    end = time.time()
    print(end-start)
