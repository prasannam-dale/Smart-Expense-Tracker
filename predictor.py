import pickle


with open('models/category_model.pkl', 'rb') as file:
    model = pickle.load(file)


def predict_category(description):
    prediction = model.predict([description])
    return prediction[0]