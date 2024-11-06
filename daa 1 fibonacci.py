#Non-recursive program

def fibonacci(n):
    if n <= 0:  # Handling edge case when n <= 0
        print("Please enter a positive integer.")
    elif n == 1:  # For the first Fibonacci number
        print(0)
    elif n == 2:  # For the second Fibonacci number
        print(1)
    else:
        arr=[0,1]
        fnm2 = 0  # (n-2)th Fibonacci number
        fnm1 = 1  # (n-1)th Fibonacci number
        for i in range(2, n):
            fn = fnm1 + fnm2  # Calculate nth Fibonacci number
            fnm2 = fnm1
            fnm1 = fn
            arr.append(fn)
        print(fn)
        print("The fibonacci series is:{}".format(arr))
#Main function
if __name__=="__main__":
    fibonacci(7) # This should print 8 as the 7th Fibonacci number
    fibonacci(0)

# recursion program

def fibonacci(n):
    if n<=0:
        return "enter a positive integer"
    elif n==1:
        return 0
    elif n==2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_series(n):
    series=[]
    for i in range(1,n+1):
        series.append(fibonacci(i))
    return series

n=int(input("Enter the number:"))
print("Fibonacci number at position",n,"is:",fibonacci(n))
print("Fibonacci series up to",n,"is:",fibonacci_series(n))
        
