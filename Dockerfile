FROM python:3.11

# Copier le script wait-for-it.sh
COPY wait-for-it.sh /wait-for-it.sh

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
