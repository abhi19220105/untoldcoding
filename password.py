import random
import string
import secrets
import sys

def generate_password(length=12, uppercase=True, lowercase=True, digits=True, special_chars=True):
    """
    Generate a strong random password with customizable requirements
    
    Parameters:
    - length: int (default 12) - length of the password
    - uppercase: bool (default True) - include uppercase letters
    - lowercase: bool (default True) - include lowercase letters
    - digits: bool (default True) - include numbers
    - special_chars: bool (default True) - include special characters
    
    Returns:
    - str: generated password
    """
    character_sets = []
    
    if uppercase:
        character_sets.append(string.ascii_uppercase)
    if lowercase:
        character_sets.append(string.ascii_lowercase)
    if digits:
        character_sets.append(string.digits)
    if special_chars:
        character_sets.append(string.punctuation)
    
    if not character_sets:
        raise ValueError("At least one character set must be selected")
    
    # Ensure the password contains at least one character from each selected set
    password = []
    for charset in character_sets:
        password.append(secrets.choice(charset))
    
    # Fill the rest of the password with random choices from all selected sets
    all_chars = ''.join(character_sets)
    password.extend(secrets.choice(all_chars) for _ in range(length - len(password)))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

def get_user_preferences():
    """Get password requirements from user input"""
    print("Password Generator Settings:")
    
    while True:
        try:
            length = int(input("Password length (8-64): "))
            if 8 <= length <= 64:
                break
            print("Please enter a length between 8 and 64")
        except ValueError:
            print("Please enter a valid number")
    
    uppercase = input("Include uppercase letters? (Y/n): ").lower() != 'n'
    lowercase = input("Include lowercase letters? (Y/n): ").lower() != 'n'
    digits = input("Include numbers? (Y/n): ").lower() != 'n'
    special = input("Include special characters? (Y/n): ").lower() != 'n'
    
    return length, uppercase, lowercase, digits, special

def main():
    print("=== Secure Password Generator ===")
    print("This tool creates strong, random passwords to enhance your security.\n")
    
    while True:
        try:
            length, upper, lower, digits, special = get_user_preferences()
            password = generate_password(length, upper, lower, digits, special)
            
            print("\nGenerated Password:")
            print(password)
            
            # Calculate password strength
            strength = "Weak"
            entropy = 0
            charsets = 0
            
            if upper: 
                charsets += 1
                entropy += 26
            if lower: 
                charsets += 1
                entropy += 26
            if digits: 
                charsets += 1
                entropy += 10
            if special: 
                charsets += 1
                entropy += 32
            
            # Very approximate strength estimation
            if length >= 12 and charsets >= 3:
                strength = "Strong"
            elif length >= 8 and charsets >= 2:
                strength = "Medium"
            
            print(f"\nPassword Strength: {strength}")
            print(f"Length: {length} characters")
            print("Character sets used:", end=" ")
            print("Uppercase" if upper else "", end=" ")
            print("Lowercase" if lower else "", end=" ")
            print("Numbers" if digits else "", end=" ")
            print("Special" if special else "")
            
            another = input("\nGenerate another password? (y/N): ").lower()
            if another != 'y':
                print("\nStay secure! Goodbye!")
                break
                
        except ValueError as e:
            print(f"Error: {e}")
            print("Please select at least one character set")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()