import streamlit as st
import pyotp
import datetime
import qrcode
import io


def generate_base32():
    secret_base32 = pyotp.random_base32()
    st.session_state['otp_base32'] = secret_base32
    return secret_base32


def main():
    st.title("One-Time Password (OTP)")
    st.markdown("___")

    if 'otp_base32' in st.session_state:
        secret_base32 = st.session_state['otp_base32']
    else:
        secret_base32 = generate_base32()

    btn_generate = st.button("Generate Secret (Base32)")
    if btn_generate:
        secret_base32 = generate_base32()
    secret_base32 = st.text_input("Secret (Base32)", value=secret_base32)

    with st.expander("Provisioning URI"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", value='alice@google.com')
        with col2:
            issuer_name = st.text_input("Issuer Name", value="Secure App")

        provisioning_uri = pyotp.totp.TOTP(secret_base32).provisioning_uri(name=name, issuer_name=issuer_name)
        st.code(provisioning_uri)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=3,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(byte_im)

    st.markdown("___")
    st.header("Time-Based")
    st.subheader("Time-Based Values")
    totp = pyotp.TOTP(secret_base32)
    totp_now = totp.now()
    totp_next = totp.at(datetime.datetime.now() + datetime.timedelta(seconds=30))
    time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval

    st.write(f"Now: {totp_now}")
    st.write(f"Next: {totp_next}")
    st.write(f"Time Remaining: {time_remaining:0.0f}s")

    st.subheader("Validate Time-Based")
    code = st.text_input("Secret Code (TOTP)", value=totp_now)
    if st.button("Validate TOTP"):
        if totp.verify(code):
            st.success("Valid")
        else:
            st.error("Not Valid")

    st.markdown("___")
    st.header("Counter-Based")
    st.subheader("Counter-Based Values")
    hotp = pyotp.HOTP(secret_base32)
    hotp_values = []
    for i in range(10):
        hotp_values.append(hotp.at(i))
    st.write(hotp_values)

    st.subheader("Validate Counter-Based")
    counter_code = st.text_input("Secret Code (HOTP)", value=hotp.at(0))
    counter = st.number_input("Counter", value=0)
    if st.button("Validate HOTP"):
        if hotp.verify(counter_code, counter):
            st.success("Valid")
        else:
            st.error("Not Valid")


if __name__ == '__main__':
    main()
