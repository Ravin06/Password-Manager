import random
import string

print("Welcome to Password Manager")
print("Choose an option:")
print("1. Check Password Strength")
print("2. Generate Password")
print("3. Save Password")
print("4. Retrieve Password")
print("5. Exit")

# Checks if the password is at least 8 characters long and contains at least one uppercase letter, one lowercase letter, one digit, and one special character.
def check_password_strength(password):
    if len(password) < 8:
        return "Password is too short. Minimum length is 8 characters."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    if not any(not char.isalnum() for char in password):
        return "Password must contain at least one special character."
    return "Password is strong."

# Generates a random password of length 12
def generate_password():
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    print(password)
    print("Do you want to save this password? [Y/N]")
    save = input()
    if save.lower() == 'y':
        service = input("Enter service: ")
        username = input("Enter username: ")
        save_password(service, username, password)
        print("Password saved successfully.")
    return "Password generated successfully."

key = 'somereallycoolkeythatshouldnotreallybeeasilyguessable'
# XOR encryption/decryption for password
def encdec_password(password, key):
    key_length = len(key)
    result = []
    for i in range(len(password)):
        result.append(chr(ord(password[i]) ^ ord(key[i % key_length])))
    return ''.join(result)

# Saves the password to a file
def save_password(service, username, password):
    encrypted_password = encdec_password(password, key)
    with open('passwords.txt', 'a') as file:
        file.write(f"{service}: {username} - {encrypted_password}\n")
    print("Password saved successfully.")

# Retrieves the password for a given service
def retrieve_password(service):
    with open('passwords.txt', 'r') as file:
        for line in file:
            if service in line:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    encrypted_password = parts[1]
                    return encdec_password(encrypted_password, key)
    return "Password not found."

while True:
    choice = input("Enter your choice: ")

    if choice == '1':
        password = input("Enter password: ")
        print(check_password_strength(password))
    elif choice == '2':
        print(generate_password())
    elif choice == '3':
        service = input("Enter service: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        save_password(service, username, password)
    elif choice == '4':
        service = input("Enter service: ")
        print(retrieve_password(service))
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")
