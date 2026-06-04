import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('./datasets/student-mat.csv', sep=';')

X = df[['G1']]
y = df['G3']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

with open('./models/best_student_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("SUCCESS: Model saved as 'best_student_model.pkl'!")
