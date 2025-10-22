FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV MEMORY_STORAGE_1=https://storagememory-2-bngo.onrender.com
ENV MEMORY_STORAGE_2=https://storagemem.onrender.com
ENV RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
