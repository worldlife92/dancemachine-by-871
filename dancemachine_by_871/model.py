from tensorflow.keras.models import load_model

class DanceModel:

    def __init__(self, path):
        self.path = path
        self.model = load_model(self.path)

    def predict(self, X_test_preproc):
        return self.model.predict(X_test_preproc)



if __name__ == '__main__':
    model = DanceModel('model3')
    print('testtesttest')
