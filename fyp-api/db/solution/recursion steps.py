def fib1():
    return 1
def fib2():
    return 1
def fib3():
    return fib1()+fib2()
def fib4():
    return fib2()+fib3()
# fib(n-1)+fib(n-2)
# fib(n)+fib(n-1)
def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1)+fib(n-2)


