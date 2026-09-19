import os
import sys
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def process_data(data: bytes, source_name: str):
    print(f"\n[+] Input Loaded ({len(data)} bytes from '{source_name}')")
    
    # 1. Hashing (SHA-256)
    orig_hash = hashlib.sha256(data).hexdigest()
    print(f"[1] Original SHA-256 Hash:\n    {orig_hash}")

    # 2. Key Generation & Symmetric Encryption (AES-256-GCM)
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit unique IV
    ciphertext = aesgcm.encrypt(nonce, data, None)
    print(f"[2] AES-256 Encrypted (First 32 hex bytes):\n    {ciphertext.hex()[:64]}...")

    # 3. Decryption
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
    print(f"[3] Decryption successful.")

    # 4. Hash Comparison & Integrity Verification
    decrypted_hash = hashlib.sha256(decrypted_data).hexdigest()
    print(f"[4] Decrypted SHA-256 Hash:\n    {decrypted_hash}")
    
    match = (orig_hash == decrypted_hash)
    print(f"\n[RESULT] Integrity Match: {match} ({'VALID' if match else 'CORRUPTED'})")

def main():
    print("   SDEV-245 Midterm Project  ")
    print("Choose input mode:")
    print("1) Enter text manually")
    print("2) Provide path to a file")
    
    choice = input("\nSelect option (1 or 2): ").strip()
    
    if choice == "1":
        user_text = input("Enter your message: ")
        if not user_text:
            print("Empty message. Exiting.")
            sys.exit(1)
        process_data(user_text.encode('utf-8'), source_name="Text Input")
        
    elif choice == "2":
        file_path = input("Enter path to file: ").strip()
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
        with open(file_path, "rb") as f:
            file_data = f.read()
        process_data(file_data, source_name=os.path.basename(file_path))
        
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()