"""
Crypto Fernet
"""
import argparse
import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class BinaryFileType(argparse.FileType):
    """
    Wrapper class returning stdin/stdout buffers,
    so I/O is always byte-oriented
    """
    def __call__(self, string):
        if string == '-':
            if 'r' in self._mode:
                return sys.stdin.buffer
            elif 'w' in self._mode:
                return sys.stdout.buffer
        return super().__call__(string)


def create_salt() -> bytes:
    """Returns random salt bytes"""
    return os.urandom(16)


def get_kdf(salt: bytes):
    """Returns key deriving function"""
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )


def add_salt(salt: bytes, ciphertext: bytes) -> bytes:
    """Encodes salt and combines with ciphertext

    Returns salted ciphertext bytes"""
    encoded_salt = base64.urlsafe_b64encode(salt)
    return encoded_salt + b':' + ciphertext


def extract_salt(salted_ciphertext: bytes):
    """
    Extract salt and ciphertext from salted ciphertext and returns as a tuple
    """
    encoded_salt, ciphertext = salted_ciphertext.split(b':')
    salt = base64.urlsafe_b64decode(encoded_salt)
    return salt, ciphertext


def derive_key(secret: bytes, salt: bytes):
    """Derives the key from specified secret and salt using KDF function"""
    kdf = get_kdf(salt)
    key = base64.urlsafe_b64encode(kdf.derive(secret))
    return key


def encrypt(plain_text, secret):
    salt = create_salt()
    key = derive_key(secret, salt)
    f = Fernet(key)
    ciphertext = f.encrypt(plain_text)
    salted_ciphertext = add_salt(salt, ciphertext)
    return salted_ciphertext


def encrypt_command(args):
    """Handler for argparse encrypt subcommand"""
    secret = args.secret.read()
    plain_text = args.input.read()
    args.output.write(encrypt(plain_text, secret))


def decrypt(salted_ciphertext, secret):
    salt, ciphertext = extract_salt(salted_ciphertext)
    key = derive_key(secret, salt)
    f = Fernet(key)
    return f.decrypt(ciphertext)


def decrypt_command(args):
    """Handler for argparse decrypt subcommand"""
    salted_ciphertext = args.input.read()
    secret = args.secret.read()
    args.output.write(decrypt(salted_ciphertext, secret))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(prog='crypto_fernet')
    parser.add_argument(
        '-s', '--secret', required=True,
        type=BinaryFileType('rb'),
        help='Path to the file with the secret for encryption/decryption')

    subparsers = parser.add_subparsers(help='sub-command help')

    encrypt_parser = subparsers.add_parser('encrypt', help='encrypt help')
    encrypt_parser.add_argument(
        '-i', '--input', type=BinaryFileType('rb'),
        default=sys.stdin.buffer,
        help='Path to the plain text input')
    encrypt_parser.add_argument(
        '-o', '--output', type=BinaryFileType('wb'),
        default=sys.stdout.buffer,
        help='Path to the cipher text output')
    encrypt_parser.set_defaults(func=encrypt_command)

    decrypt_parser = subparsers.add_parser('decrypt', help='decrypt help')
    decrypt_parser.add_argument(
        '-i', '--input', type=BinaryFileType('rb'),
        default=sys.stdin.buffer,
        help='Path to the cipher text input')
    decrypt_parser.add_argument(
        '-o', '--output', type=BinaryFileType('wb'),
        default=sys.stdout.buffer,
        help='Path to the plain text output')
    decrypt_parser.set_defaults(func=decrypt_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
