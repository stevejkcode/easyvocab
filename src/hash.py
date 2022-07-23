import hashlib

# Simple utility function to generate a hash string for media files
def get_media_hash(text, bytes=8):
    encoded = text.encode()
    return int.from_bytes(hashlib.md5(encoded).digest()[ :bytes ], byteorder='big')