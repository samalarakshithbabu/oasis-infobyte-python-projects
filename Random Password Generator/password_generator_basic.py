import random
import string

class PasswordCreator:
    def __init__(self):
        self.alphabet_chars = string.ascii_letters
        self.numeric_chars = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def build_char_pool(self, use_alpha, use_nums, use_specials):
        pool = ""
        if use_alpha:
            pool += self.alphabet_chars
        if use_nums:
            pool += self.numeric_chars
        if use_specials:
            pool += self.special_chars
        return pool
    
    def create_secure_password(self, pwd_length, char_pool):
        if not char_pool:
            raise ValueError("Character pool cannot be empty")
        return ''.join(random.choice(char_pool) for _ in range(pwd_length))
    
    def verify_length_input(self, user_input):
        try:
            pwd_len = int(user_input)
            if pwd_len < 4:
                print("⚠️ Minimum password length is 4 characters")
                return None
            if pwd_len > 128:
                print("⚠️ Maximum password length is 128 characters")
                return None
            return pwd_len
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return None
    
    def collect_user_choices(self):
        print("🔐 Password Length Configuration")
        while True:
            user_length = input("➤ Enter desired length (4-128): ")
            validated_length = self.verify_length_input(user_length)
            if validated_length:
                break
        
        print("\n📝 Character Type Selection:")
        use_letters = input("➤ Include alphabetic characters (a-z, A-Z)? [y/n]: ").lower() == 'y'
        use_digits = input("➤ Include numeric characters (0-9)? [y/n]: ").lower() == 'y'
        use_symbols = input("➤ Include special symbols (!@#$...)? [y/n]: ").lower() == 'y'
        
        return validated_length, use_letters, use_digits, use_symbols
    
    def execute_generation(self):
        print("🚀 Advanced Password Creation Tool\n" + "="*40)
        
        while True:
            try:
                pwd_len, alpha_flag, digit_flag, symbol_flag = self.collect_user_choices()
                character_pool = self.build_char_pool(alpha_flag, digit_flag, symbol_flag)
                
                if not character_pool:
                    print("\n❌ Error: At least one character type must be selected!\n")
                    continue
                
                generated_pwd = self.create_secure_password(pwd_len, character_pool)
                
                display_choice = input("\n🔍 Show password on screen? [y/n]: ").lower() == 'y'
                if display_choice:
                    print(f"\n✅ Your Password: {generated_pwd}")
                else:
                    print("\n🔒 Password created successfully (hidden for security)")
                
                print(f"📏 Character Count: {len(generated_pwd)}")
                
                continue_choice = input("\n🔄 Create another password? [y/n]: ")
                if continue_choice.lower() != 'y':
                    print("\n👋 Thank you for using Password Creator!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Operation cancelled. Goodbye!")
                break
            except Exception as error:
                print(f"\n❌ Unexpected error: {error}")

def main():
    creator = PasswordCreator()
    creator.execute_generation()

if __name__ == "__main__":
    main()