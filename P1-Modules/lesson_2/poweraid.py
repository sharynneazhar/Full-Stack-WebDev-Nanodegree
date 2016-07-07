def find_power(number, exponent) :
    result = pow(number, exponent)
    print(result)

print("Enter two numbers x and y where x^y: ")
x = int(input("x: "))
y = int(input("y: "))
find_power(x, y)
