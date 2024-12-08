from hashlib import sha512

def get_hash(data):
    """Hash the input data with a salt."""
    data = data.strip()
    final_pass = data + "including a random salt"
    return sha512(final_pass.encode('utf-8')).hexdigest()

def check_password_hash(stored_hash, password):
    """Check if the provided password matches the stored hash."""
    computed_hash = get_hash(password)  # Hash the input password
    return computed_hash == stored_hash  # Compare with the stored hash