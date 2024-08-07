import random
import string
#import os

users = {
    'admin': 'admin'
}


print("Welcome to Password Manager")
print("[L]ogin, [S]ignup, [E]xit")
choice = input("Enter your choice: ")
if choice.lower() == 'l':
    print("Enter your username and password to login.")
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username] == password:
        print("Login successful.")
    else:
        print("Invalid username or password.")
        exit()
elif choice.lower() == 's':
    print("Enter your details to signup.")
    username = input("Username: ")
    password = input("Password: ")
    print("Signup successful. You are now logged in as", username)
    users[username] = password
else:
    exit()

#check if user logged in
if username not in users:
    print("Please login to continue.")
    exit()
else:
    print(f"Welcome, {username}!")
    print("1. Check Password Strength")
    print("2. Generate Password")
    print("3. Save Password")
    print("4. Retrieve Password")
    print("5. Change compromised password")
    print("6. Change master password") 
    print("7. Exit")


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
                    #os.system("attrib +h passwords.txt")
                    return encdec_password(encrypted_password, key)
    return "Password not found."

def change_password(service):
    with open('passwords.txt', 'r') as file:
        lines = file.readlines()
    with open('passwords.txt', 'w') as file:
        for line in lines:
            if service in line:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    username, encrypted_password = parts[0].split(': ')
                    password = encdec_password(encrypted_password, key)
                    print(f"Enter new password for {service}: ")
                    new_password = input()
                    encrypted_new_password = encdec_password(new_password, key)
                    file.write(f"{service}: {username} - {encrypted_new_password}\n")
                    print("Password changed successfully.")
            else:
                file.write(line)


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
        service = input("Enter service: ")
        change_password(service)
    elif choice == '6':
        print("Enter your new master password: ")
        new_password = input()
        users[username] = new_password
        print("Master password changed successfully.")
    elif choice == '7':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")