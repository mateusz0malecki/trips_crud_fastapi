FROM python:3.10

COPY requirments.txt .

RUN pip install -r requirments.txt

WORKDIR crud

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]