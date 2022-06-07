FROM python:3.8.6-buster

COPY api /api
COPY dancemachine_by_871 /dancemachine_by_871
COPY 90_pct_model.h5 /90_pct_model.h5
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

#These commands install the cv2 dependencies that are normally present on the local machine, but might be missing in your Docker container causing the issue.
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
