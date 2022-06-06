from tensorflow.keras.models import load_model
# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import Dense, LSTM, GRU, Masking, Dropout
# from tensorflow.keras import regularizers
import numpy as np

# MASKING = np.zeros((10,))
# MASKING[:] = -20
# REG_l12 = regularizers.L1L2(0.1, 0.1)
# PATH = 'training1/cp.ckpt'

class DanceModel:

    def __init__(self, maxlen_pad=400):
        self.model = load_model('my_model.h5')
        # self.model = Sequential([Masking(mask_value=MASKING, input_shape=(maxlen_pad,10)),
        #             LSTM(30, return_sequences=True),
        #             GRU(30),
        #             Dropout(0.2),
        #             Dense(10, kernel_regularizer=REG_l12),
        #             Dense(1, activation='sigmoid')])

        # self.model.load_weights(PATH)

    def predict(self, X_test_preproc):

        return self.model.predict(X_test_preproc)

if __name__ == '__main__':
    model = DanceModel()
