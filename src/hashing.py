import hashlib

def get_media_hash(text: str, bytes: int = 8) -> int:
    """Generate a hash for the given media. Used to name the resulting file that will be attached to each card.

    :param text: text the media was generated from
    :type text: str
    :param bytes: size of the generated hash, defaults to 8
    :type bytes: int, optional
    :return: MD5 hash for the file
    :rtype: int
    """
    encoded = text.encode()
    return int.from_bytes(hashlib.md5(encoded).digest()[ :bytes ], byteorder='big')