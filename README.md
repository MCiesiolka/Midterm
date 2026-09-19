# Midterm

Confidentiality: By using AES-256 encryption, it renders the input unreadable to unauthorized people without the secret key.

Integrity: By using SHA-256 the original and decrypted hashes are compared to ensure byte-level tampering is detected.

Availability: Through both AESGCM and SHA-256 corrupted data is caught before processing further, which prevents system crashes
or invalid states by bad inputs
