from tensorflow.keras.models import load_model
from dancemachine_by_871.data_preproc import MAX_LEN
import numpy as np


class DanceModel:
    def __init__(self, maxlen_pad=MAX_LEN):
        self.model = load_model("90_pct_model.h5")

    def predict(self, X_test_preproc):

        return self.model.predict(X_test_preproc)


if __name__ == "__main__":
    model = DanceModel()
