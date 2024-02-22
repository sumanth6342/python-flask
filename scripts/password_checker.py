def password_checker():
    password = input("Please enter your password : ")
    is_upper_available, is_lower_available, is_digit_available = False, False, False

    if len(password) >= 8:
        for character in password:
            if character.isdigit():
                is_digit_available = True

            if character.isupper():
                is_upper_available = True

            if character.islower():
                is_lower_available = True

        if is_upper_available and is_lower_available and is_digit_available:
            print("valid password")

        else:
            print(is_upper_available, is_lower_available, is_digit_available)
            print("invalid password inside if")
            is_password_valid = False
            
    else:
        print("invalid password inside else")


password_checker()
