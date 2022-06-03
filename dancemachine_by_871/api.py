from fastapi import FastAPI
from dancemachine_by_871.data_preproc import Preprocessor
from dancemachine_by_871.gcp import get_urls



app = FastAPI()

@app.get("/")
def index():
    return {"ok": True}

@app.get('/predict-test')
def predict(filename):

    #Receive filename from frontend
    #Function should call the Videofile name from Google bucket
    preproc = Preprocessor(get_urls(filename))
    X_0, y_0, maxlen = preproc.extract_X_y_angles(0)
    X, y = preproc.create_X_y([X_0], [y_0], maxlen)
    return {'ok': True}
