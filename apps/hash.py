import streamlit as st
import hashlib


def utf8(s: bytes):
    return str(s, 'utf-8')


def hash():
    st.title("Hash Encoder")

    bytes_file = st.file_uploader("Data File")
    if bytes_file:
        data = bytes_file.getvalue()
    else:
        raw_text = st.text_area("Raw Text", value="Sample text to encode")
        data = raw_text.encode('ascii')

    hash_algo = st.selectbox("Hash Algorithm", options=["sha1", "sha224", "sha256", "sha384", "sha512",
                                                        "sha3_224", "sha3_256", "sha3_384", "sha3_512",
                                                        "shake_128", "shake_256", "blake2b", "blake2s",
                                                        "md5"])

    hash = getattr(hashlib, hash_algo)
    m = hash()
    m.update(data)
    prehashed = m.hexdigest()

    st.write("Encoded")
    st.code(prehashed)


if __name__ == '__main__':
    hash()
