correct_pin = "1234"
attempts = 0
max_attempts = 3
while attempts < max_attempts:
    pin = input("Enter your PIN: ")
    
    if pin == correct_pin:
        print("Access Granted")
        break
    else:
        attempts += 1
        if attempts < max_attempts:
            print(f"Incorrect PIN. Attempts remaining: {max_attempts - attempts}")
        else:
            print("Card Blocked")
