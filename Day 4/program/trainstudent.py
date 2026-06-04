import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


df = pd.read_csv('./datasets/student-mat.csv', sep=';')

feature_columns = ['studytime', 'failures', 'absences', 'G1', 'G2']

X = df[feature_columns]
y = df['G3']

fake_student = pd.DataFrame([[4, 0, 2, 15, 16]], columns=feature_columns)

fake_studytime = 4
fake_failures = 0
fake_absences = 2
fake_g1 = 15
fake_g2 = 16

test_size_one = 0.1
test_size_two = 0.2
test_size_three = 0.3

random_state_value = 42

X_train1, X_test1, y_train1, y_test1 = train_test_split(
    X,
    y,
    test_size=test_size_one,
    random_state=random_state_value
)

train_length_1 = len(X_train1)
test_length_1 = len(X_test1)

model1 = LinearRegression()
model1.fit(X_train1, y_train1)

predictions1 = model1.predict(X_test1)

mae1 = mean_absolute_error(y_test1, predictions1)
r2_1 = r2_score(y_test1, predictions1)

mae1_rounded = round(mae1, 2)
r2_1_rounded = round(r2_1, 2)

fake_pred1 = model1.predict(fake_student)
fake_pred1_rounded = round(fake_pred1[0], 2)

print("=== RESULTS FOR TEST SIZE 0.1 ===")
print("Train Size:", train_length_1)
print("Test Size :", test_length_1)
print("Average Error (MAE):", mae1_rounded)
print("Model Accuracy (R2):", r2_1_rounded)
print("Fake Student Prediction:", fake_pred1_rounded)
print("-" * 40)

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X,
    y,
    test_size=test_size_two,
    random_state=random_state_value
)

train_length_2 = len(X_train2)
test_length_2 = len(X_test2)

model2 = LinearRegression()
model2.fit(X_train2, y_train2)

predictions2 = model2.predict(X_test2)

mae2 = mean_absolute_error(y_test2, predictions2)
r2_2 = r2_score(y_test2, predictions2)

mae2_rounded = round(mae2, 2)
r2_2_rounded = round(r2_2, 2)

fake_pred2 = model2.predict(fake_student)
fake_pred2_rounded = round(fake_pred2[0], 2)

print("=== RESULTS FOR TEST SIZE 0.2 ===")
print("Train Size:", train_length_2)
print("Test Size :", test_length_2)
print("Average Error (MAE):", mae2_rounded)
print("Model Accuracy (R2):", r2_2_rounded)
print("Fake Student Prediction:", fake_pred2_rounded)
print("-" * 40)

X_train3, X_test3, y_train3, y_test3 = train_test_split(
    X,
    y,
    test_size=test_size_three,
    random_state=random_state_value
)

train_length_3 = len(X_train3)
test_length_3 = len(X_test3)

model3 = LinearRegression()
model3.fit(X_train3, y_train3)

predictions3 = model3.predict(X_test3)

mae3 = mean_absolute_error(y_test3, predictions3)
r2_3 = r2_score(y_test3, predictions3)

mae3_rounded = round(mae3, 2)
r2_3_rounded = round(r2_3, 2)

fake_pred3 = model3.predict(fake_student)
fake_pred3_rounded = round(fake_pred3[0], 2)

print("=== RESULTS FOR TEST SIZE 0.3 ===")
print("Train Size:", train_length_3)
print("Test Size :", test_length_3)
print("Average Error (MAE):", mae3_rounded)
print("Model Accuracy (R2):", r2_3_rounded)
print("Fake Student Prediction:", fake_pred3_rounded)
print("-" * 40)

r2_list = [r2_1, r2_2, r2_3]
mae_list = [mae1, mae2, mae3]
size_list = [test_size_one, test_size_two, test_size_three]

best_r2_value = r2_list[0]
best_r2_index = 0

if r2_list[1] > best_r2_value:
    best_r2_value = r2_list[1]
    best_r2_index = 1

if r2_list[2] > best_r2_value:
    best_r2_value = r2_list[2]
    best_r2_index = 2

best_test_size = size_list[best_r2_index]
best_mae_value = mae_list[best_r2_index]

print("=== BEST PERFORMING SPLIT ===")
print("Best Test Size :", best_test_size)
print("Best R2 Score  :", round(best_r2_value, 2))
print("Best MAE       :", round(best_mae_value, 2))
print("-" * 40)
