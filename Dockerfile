FROM python:3.8.6-buster

COPY api /api
COPY dancemachine_by_871 /dancemachine_by_871
COPY my_model.h5 /my_model.h5
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
