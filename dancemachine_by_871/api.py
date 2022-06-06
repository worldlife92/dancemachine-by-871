from fastapi import FastAPI
from dancemachine_by_871.data_preproc import Preprocessor
from dancemachine_by_871.gcp import get_urls
from dancemachine_by_871.model import DanceModel



app = FastAPI()

@app.get("/")
def index():
    return {"ok": True}

@app.get('/predict')
def predict(filename):

    #Receive filename from frontend
    #Function should call the Videofile name from Google bucket
    preproc = Preprocessor(get_urls(filename))
    X_0, y_0, maxlen = preproc.extract_X_y_angles(0)
    model = DanceModel()
    return {'score': model.predict(X_0)}
