import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

training_data = {
    'text': [
        'KFC burger',
        'Pizza Hut dinner',
        'Bus ticket',
        'Uber ride',
        'Electricity bill',
        'Netflix subscription',
        'Textbook purchase',
        'Doctor appointment',
        'Cinema ticket',
        'Fuel refill'
    ],
    'category': [
        'Food',
        'Food',
        'Transport',
        'Transport',
        'Bills',
        'Entertainment',
        'Education',
        'Healthcare',
        'Entertainment',
        'Transport'
    ]
}


df = pd.DataFrame(training_data)

model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

model.fit(df['text'], df['category'])

with open('models/category_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print('Model trained successfully!')