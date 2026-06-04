import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv('./datasets/student-mat.csv', sep=';')

features_to_test = ['studytime', 'failures', 'absences', 'G1']
target = 'G3'

rmse_results = {}

print("=== TRAINING 4 SEPARATE MODELS ===")

for col in features_to_test:
    X = df[[col]]  
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    
    rmse_results[col] = rmse
    print(f"Model using ONLY '{col}' -> RMSE: {round(rmse, 2)}")

print("-" * 50)

best_feature = min(rmse_results, key=rmse_results.get)
print(f"🏆 WINNER: The single best predictor is '{best_feature}' with the lowest RMSE of {round(rmse_results[best_feature], 2)}")
print("-" * 50)


print("=== RANDOM STUDENT TEST (Using Best Feature) ===")

X_best = df[[best_feature]]
y_best = df[target]
X_train, X_test, y_train, y_test = train_test_split(X_best, y_best, test_size=0.2, random_state=42)

best_model = LinearRegression()
best_model.fit(X_train, y_train)

# Pick a random student from the test dataset
random_student_features = X_test.sample(1, random_state=10)
student_index = random_student_features.index[0]

# Get the real grade and make the single-feature prediction
real_grade = y_test.loc[student_index]
predicted_grade = best_model.predict(random_student_features)

print(f"Student's value for '{best_feature}':", random_student_features.values[0][0])
print("Predicted Grade by Model:", round(predicted_grade[0], 2))
print("Correct (Actual) Grade:  ", real_grade)
