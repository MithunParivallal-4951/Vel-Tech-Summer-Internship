import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv('./datasets/student-mat.csv', sep=';')

feature_columns = ['studytime', 'failures', 'absences', 'G1', 'G2']
X = df[feature_columns]
y = df['G3']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)


random_student_features = X_test.sample(1, random_state=10) 

student_index = random_student_features.index[0]

real_grade = y_test.loc[student_index]
predicted_grade = model.predict(random_student_features)

print("=== MODEL EFFICIENCY ===")
print("Average Error (MAE):", round(mae, 2), "grade points")
print("Model Accuracy (R2 Score):", round(r2, 2))
print("-" * 40)

print("=== RANDOM STUDENT TEST ===")
print("Student Features used:")
print(random_student_features.to_string(index=False))
print("Predicted Grade by Model:", round(predicted_grade[0], 2))
print("Correct (Actual) Grade:  ", real_grade)
