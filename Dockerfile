# docker build --progress=plain --no-cache -t kavehbc/crypto-tools:latest -t kavehbc/crypto-tools:1.1.2 .
# docker save -o crypto-tools.tar kavehbc/crypto-tools
# docker load --input crypto-tools.tar

FROM python:3.11-slim

LABEL version="1.1.2"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/crypto-tools"
LABEL description="Cryptography Tokens and Tools"

WORKDIR /app
COPY . .

# installing the requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]