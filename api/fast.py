from fastapi import FastAPI
from dancemachine_by_871.data_preproc import Preprocessor
from dancemachine_by_871.model import DanceModel

<<<<<<< HEAD:dancemachine_by_871/api.py

=======
>>>>>>> 91bf9899f6d44bba3846e03c13c2512b34f2c1f3:api/fast.py
app = FastAPI()


@app.get("/")
def index():
    return {"ok": True}


<<<<<<< HEAD:dancemachine_by_871/api.py
@app.get("/predict")
def predict(filename):

    # Receive filename from frontend
    # Function should call the Videofile name from Google bucket
    PATH = ["https://storage.googleapis.com/dance_871/UPLOADED/" + filename]
=======
@app.get('/predict')
def predict(filename):
    # Receive filename from frontend
    # Function should call the Videofile name from Google bucket
    PATH = ['https://storage.googleapis.com/dance_871/UPLOADED/' + filename]
>>>>>>> 91bf9899f6d44bba3846e03c13c2512b34f2c1f3:api/fast.py
    preproc = Preprocessor(PATH)
    X_0, y_0 = preproc.extract_X_y_angles(0)
    model = DanceModel()
    return {"score": int(model.predict(X_0)[0][0] * 100)}
<<<<<<< HEAD:dancemachine_by_871/api.py


if __name__ == "__main__":

    preproc2 = Preprocessor(
        [
            "raw_data/Snaptik_6814651446827535621_josh_Full_HD.mp4",
            "raw_data/Snaptik_6870595517517221126_emerson-rock_Full_HD.mp4",
            "raw_data/Snaptik_7087484696686316802_kyra-thompson_Full_HD.mp4",
            "raw_data/Snaptik_7092500890128616747_meg-sarah-dodini_Full_HD.mp4",
            "raw_data/Snaptik_7093157430942567685_janjabalant_Full_HD.mp4",
        ]
    )
=======


if __name__ == '__main__':
    preproc2 = Preprocessor(["raw_data/Snaptik_6814651446827535621_josh_Full_HD.mp4",
                             "raw_data/Snaptik_6870595517517221126_emerson-rock_Full_HD.mp4",
                             "raw_data/Snaptik_7087484696686316802_kyra-thompson_Full_HD.mp4",
                             "raw_data/Snaptik_7092500890128616747_meg-sarah-dodini_Full_HD.mp4",
                             "raw_data/Snaptik_7093157430942567685_janjabalant_Full_HD.mp4"])
>>>>>>> 91bf9899f6d44bba3846e03c13c2512b34f2c1f3:api/fast.py
    X_1, y_1 = preproc2.extract_X_y_angles()
    model2 = DanceModel()
    print(model2.predict(X_1))
