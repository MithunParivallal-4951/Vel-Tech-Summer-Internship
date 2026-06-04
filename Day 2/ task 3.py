def times_table(n):
    print(f"\nMultiplication Table for {n}")
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")

# Get 3 numbers from the user
for j in range(3):
    num = int(input(f"Enter number {j+1}: "))
    times_table(num)
