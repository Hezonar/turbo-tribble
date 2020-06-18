n = int(input())
m = 0
while n > 0:
    d = n % 10
    if d > 1:
        m = d + 10*m
    print(n, d)
    n = (n - d) // 10
    print(n)
print(m)