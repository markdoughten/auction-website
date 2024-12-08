from hashlib import sha512

def get_hash(data):
    final_pass = data + "including a random salt";
    return sha512(final_pass.encode('utf-8')).hexdigest()