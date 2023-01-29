import hashlib

def createHash(password):
  password_byte = password.encode('utf-8')
  password_hash = hashlib.sha256(password_byte).hexdigest()
  return password_hash
