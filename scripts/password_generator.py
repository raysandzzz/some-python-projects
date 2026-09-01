import secrets
import string

def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    
    # Check if the input length is at least 4
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    # Base pool: lowercase characters are always included
    char_pool = string.ascii_lowercase
    guaranteed_chars = [secrets.choice(string.ascii_lowercase)]

    # Add optional character sets and guarantee at least one of each selected type
    if use_upper:
        char_pool += string.ascii_uppercase
        guaranteed_chars.append(secrets.choice(string.ascii_uppercase))

    if use_digits:
        char_pool += string.digits
        guaranteed_chars.append(secrets.choice(string.digits))

    if use_symbols:
        char_pool += string.punctuation
        guaranteed_chars.append(secrets.choice(string.punctuation))

    # Fill the remaining length with random choices from the combined pool
    remaining_length = length - len(guaranteed_chars)
    remaining_chars = [
        secrets.choice(char_pool) for _ in range(remaining_length)
    ]

    # Combine and shuffle to avoid predictable character positions
    password_list = guaranteed_chars + remaining_chars
    secrets.SystemRandom().shuffle(password_list)

    return "".join(password_list)


# User input
def main():
    print("=" * 45)
    print("       Secure Password Generator 🔑")
    print("=" * 45)

    # Length input with validation
    while True:
        try:
            raw_len = input(
                "Password length (default: 16, min: 4): "
            ).strip()
            if not raw_len:
                length = 16
                break
            length = int(raw_len)
            if length >= 4:
                break
            else:
                print("❌ Length must be at least 4.")    
        except ValueError:
            print("❌ Please enter a valid number.")

    def ask_bool(prompt: str, default: bool = True) -> bool:
        default_str = "Y/n" if default else "y/N"
        answer = input(f"{prompt} [{default_str}]: ").strip().lower()
        if not answer:
            return default
        return answer in ("y", "yes", "s", "si")

    use_upper = ask_bool("Include uppercase letters (A-Z)?", default=True)
    use_digits = ask_bool("Include numbers (0-9)?", default=True)
    use_symbols = ask_bool("Include special symbols (!@#$)?", default=True)

    # Number of passwords to generate
    raw_count = input(
        "How many passwords to generate? [default: 1]: "
    ).strip()
    # Return 'count' as the number of passwords the user requests
    count = int(raw_count) if raw_count.isdigit() and int(raw_count) > 0 else 1

    print("\n" + "-" * 45)
    print("Generated Passwords:")
    print("-" * 45)

    for i in range(count):
        pwd = generate_password(
            length=length,
            use_upper=use_upper,
            use_digits=use_digits,
            use_symbols=use_symbols,
        )
        if count == 1:
            print(f"\n  👉  {pwd}\n")
        else:
            print(f"  {i + 1}. {pwd}")

    print("-" * 45)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()