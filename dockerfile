FROM python 

WORKDIR /rpa

COPY transformador.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "transformandor.ipynb"]