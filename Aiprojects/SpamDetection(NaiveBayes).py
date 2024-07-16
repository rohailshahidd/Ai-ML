# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m7Rrhrf3ZCIGVG75vb5_QtdMA9clAqRG
"""

import pandas as pd

file_path = 'spam.csv'
data = pd.read_csv(file_path, encoding='latin-1')
data

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')

# Rename columns for consistency if necessary
data = data.rename(columns={'v1': 'label', 'v2': 'text'})  # replace with actual column names

# Map 'ham' to 0 and 'spam' to 1
data['label'] = data['label'].map({'ham': 0, 'spam': 1})
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# Text preprocessing
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the Naive Bayes classifier
naive_bayes = MultinomialNB()
naive_bayes.fit(X_train_tfidf, y_train)

# Predictions and evaluation
y_pred = naive_bayes.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Function to predict if a new email is spam or not spam
def predict_spam(email):
    email_tfidf = vectorizer.transform([email])
    prediction = naive_bayes.predict(email_tfidf)
    return 'spam' if prediction[0] == 1 else 'not spam'

# Example usage of the function
new_email = "Congratulations! You've won a $1,000 Walmart gift card. Click here to claim your prize."
print(f'The new email is: {predict_spam(new_email)}')

new_email = "Hey, I hope you're doing well. Let's catch up over lunch tomorrow."
print(f'The new email is: {predict_spam(new_email)}')