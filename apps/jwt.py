import streamlit as st
import jwt
import json
import time
import datetime


def main():
    st.title("JWT - JSON Web Token")
    algorithms = ["HS256", "HS384", "HS512", "ES256", "ES256K", "ES384", "ES512", "RS256",
                  "RS384", "RS512", "PS256", "PS384", "PS512", "EdDSA"]

    rsa_key = None
    required = []

    token = st.text_area("JSON/Token", value='{"some": "payload"}')
    try:
        json_object = json.loads(token)
        encode = True
    except json.decoder.JSONDecodeError:
        encode = False

    encryption_algorithm = st.selectbox("Algorithms", options=algorithms)

    if not encode:
        decode_params = st.expander("Decode Parameters")
        with decode_params:
            # expiration date/time
            col1, col2, col3 = st.columns(3)
            input_date = col1.date_input("exp date")
            input_time = col2.time_input("exp tate")
            x = datetime.datetime(input_date.year, input_date.month, input_date.day,
                                  input_time.hour, input_time.minute, input_time.second)
            def_value = int(time.mktime(x.timetuple()))
            exp = col3.number_input("exp", value=def_value, min_value=0, step=1)
            col3.caption("Set to zero to ignore")
            if exp > 0:
                required.append("exp")

            # nbf: Not Before Time Claim
            col1, col2, col3 = st.columns(3)
            input_date = col1.date_input("nbf date")
            input_time = col2.time_input("nbf time")
            x = datetime.datetime(input_date.year, input_date.month, input_date.day,
                                  input_time.hour, input_time.minute, input_time.second)
            def_value = int(time.mktime(x.timetuple()))
            nbf = col3.number_input("nbf", value=def_value, min_value=0, step=1)
            col3.caption("Set to zero to ignore")
            if nbf > 0:
                required.append("nbf")

            # iat: Issued At Claim
            col1, col2, col3 = st.columns(3)
            input_date = col1.date_input("iat date")
            input_time = col2.time_input("iat time")
            x = datetime.datetime(input_date.year, input_date.month, input_date.day,
                                  input_time.hour, input_time.minute, input_time.second)
            def_value = int(time.mktime(x.timetuple()))
            iat = col3.number_input("iat", value=def_value, min_value=0, step=1)
            col3.caption("Set to zero to ignore")
            if iat > 0:
                required.append("iat")

            # params
            col_iss, col_aud, col_leeway = st.columns(3)
            iss = col_iss.text_input("iss")
            aud = col_aud.text_input("aud")
            leeway = col_leeway.number_input("leeway", value=0, min_value=0, step=1)
            if iss == "":
                iss = None
            if aud == "":
                aud = None

    if encryption_algorithm[:2] == "RS":
        if encode:
            lbl_rsa_key = "Private Key"
        else:
            lbl_rsa_key = "Public Key"

        rsa_key_file = st.file_uploader(lbl_rsa_key, type=["pem", "ssh"])

        if rsa_key_file:
            rsa_key = rsa_key_file.read()
    else:
        secret = st.text_input("Secret", value="secret")

    jwt_result = ""
    err_message = ""

    if encode:
        btn_encode = st.button("Encode")
        if btn_encode:
            if encryption_algorithm[:2] == "RS" and rsa_key:
                secret = rsa_key
            jwt_result = jwt.encode(json_object, secret, algorithm=encryption_algorithm)
    else:
        btn_decode = st.button("Decode")
        if btn_decode:
            if encryption_algorithm[:2] == "RS" and rsa_key:
                secret = rsa_key
            try:
                jwt_result_obj = jwt.decode(token, secret, algorithms=[encryption_algorithm],
                                            options={"verify_signature": True, "require": required},
                                            audience=aud, issuer=iss, leeway=leeway)
                # jwt_result_obj = jwt.get_unverified_header(token)

                jwt_result = json.dumps(jwt_result_obj)
            except jwt.exceptions.InvalidSignatureError as err:
                err_message = err
                jwt_result_obj = jwt.decode(token, secret, algorithms=[encryption_algorithm],
                                            options={"verify_signature": False, "require": required},
                                            audience=aud, issuer=iss, leeway=leeway)
                jwt_result = json.dumps(jwt_result_obj)
            except Exception as err:
                err_message = err

    st.subheader("Error")
    st.code(err_message)
    st.subheader("Output")
    st.code(jwt_result)


if __name__ == '__main__':
    main()
