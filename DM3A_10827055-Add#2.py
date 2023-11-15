a = int(input('請輸入整數N，計算N!,2^N,20N：'))
b = 1
c = 1
d = []
e = 0
for i in range(1, a+1):
    b *= i
d.append(b)
c = 2**a
a *= 20
d.append(c)
d.append(a)
print('N! =', b)
print('2^N =', c)
print('20N =', a)
for i in d:
    e += 1
    if e != len(d):
        print(i, end=">")
    else:
        print(i)