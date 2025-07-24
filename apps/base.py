import streamlit as st
import base64


def utf8(s: bytes):
    return str(s, 'utf-8')


def base():
    st.title("Base64 Encoder/Decoder")

    st.subheader("Encoding")
    bytes_file = st.file_uploader("Data File")
    if bytes_file:
        data = bytes_file.getvalue()
    else:
        raw_text = st.text_area("Raw Text", value="Sample text to encode")
        data = raw_text.encode('ascii')

    encoded = base64.b64encode(data)
    st.write("Encoded")
    st.code(utf8(encoded))
    if encoded:
        st.download_button("Download Base64",
                           data=encoded,
                           file_name="encoded.base64")
        st.caption("Later, you probably need to rename the file name and extension.")

    st.subheader("Decoding")
    try:
        decoded = None
        encoded_input = st.text_area("Base64", value=utf8(encoded))
        encoded_input = encoded_input.encode('ascii')
        decoded = base64.b64decode(encoded_input)
        st.write("Decoded")
        st.code(utf8(decoded))
    except Exception as err:
        st.error(err)
    finally:
        if decoded:
            st.download_button("Download as a binary file",
                               data=decoded,
                               file_name="decoded.bin")
            st.caption("Later, you probably need to rename the file name and extension.")


if __name__ == '__main__':
    base()
