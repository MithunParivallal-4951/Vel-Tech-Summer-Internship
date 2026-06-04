import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


filepath = "student-mat.csv"
separator = ";"
df = pd.read_csv(filepath, sep=separator)

total_rows = df.shape[0]
total_cols = df.shape[1]

print("=" * 55)
print(f"  Dataset loaded: {total_rows} rows x {total_cols} columns")
print("=" * 55)

all_columns = df.columns.tolist()
categorical_columns = df.select_dtypes(include="object").columns.tolist()
numerical_columns = df.select_dtypes(exclude="object").columns.tolist()

label_encoder = LabelEncoder()
df_encoded = df.copy()

for column_name in categorical_columns:
    original_values = df_encoded[column_name]
    encoded_values = label_encoder.fit_transform(original_values)
    df_encoded[column_name] = encoded_values

grade_columns_to_drop = ["G1", "G2", "G3"]
feature_dataframe = df_encoded.drop(columns=grade_columns_to_drop)
target_series_raw = df_encoded["G3"]
pass_threshold = 10
target_series = (target_series_raw >= pass_threshold).astype(int)

total_features = feature_dataframe.shape[1]
total_samples = feature_dataframe.shape[0]
total_pass = int(target_series.sum())
total_fail = int((target_series == 0).sum())

print(f"\n  Features : {total_features}")
print(f"  Samples  : {total_samples}")
print(f"  Class balance  -> Pass: {total_pass}  |  Fail: {total_fail}")

feature_array = feature_dataframe.values
target_array = target_series.values

test_size_value_one = 0.1
test_size_value_two = 0.2
test_size_value_three = 0.3
all_test_sizes = [test_size_value_one, test_size_value_two, test_size_value_three]

random_state_value = 42
n_estimators_value = 100

results_list = []

print("\n" + "=" * 55)
print(f"  {'Test%':>6}  {'Train N':>8}  {'Test N':>7}  {'Accuracy':>10}")
print("=" * 55)

current_test_size = all_test_sizes[0]

X_train_split1, X_test_split1, y_train_split1, y_test_split1 = train_test_split(
    feature_array,
    target_array,
    test_size=current_test_size,
    random_state=random_state_value
)

train_size_split1 = len(X_train_split1)
test_size_split1 = len(X_test_split1)

model_split1 = RandomForestClassifier(
    n_estimators=n_estimators_value,
    random_state=random_state_value
)
model_split1.fit(X_train_split1, y_train_split1)
predictions_split1 = model_split1.predict(X_test_split1)
accuracy_split1 = accuracy_score(y_test_split1, predictions_split1)

result_entry_1 = {
    "test_size": current_test_size,
    "train_n": train_size_split1,
    "test_n": test_size_split1,
    "accuracy": accuracy_split1
}
results_list.append(result_entry_1)

print(f"  {int(current_test_size * 100):>5}%  {train_size_split1:>8}  {test_size_split1:>7}  {accuracy_split1:>9.4f}")

current_test_size = all_test_sizes[1]

X_train_split2, X_test_split2, y_train_split2, y_test_split2 = train_test_split(
    feature_array,
    target_array,
    test_size=current_test_size,
    random_state=random_state_value
)

train_size_split2 = len(X_train_split2)
test_size_split2 = len(X_test_split2)

model_split2 = RandomForestClassifier(
    n_estimators=n_estimators_value,
    random_state=random_state_value
)
model_split2.fit(X_train_split2, y_train_split2)
predictions_split2 = model_split2.predict(X_test_split2)
accuracy_split2 = accuracy_score(y_test_split2, predictions_split2)

result_entry_2 = {
    "test_size": current_test_size,
    "train_n": train_size_split2,
    "test_n": test_size_split2,
    "accuracy": accuracy_split2
}
results_list.append(result_entry_2)

print(f"  {int(current_test_size * 100):>5}%  {train_size_split2:>8}  {test_size_split2:>7}  {accuracy_split2:>9.4f}")

current_test_size = all_test_sizes[2]

X_train_split3, X_test_split3, y_train_split3, y_test_split3 = train_test_split(
    feature_array,
    target_array,
    test_size=current_test_size,
    random_state=random_state_value
)

train_size_split3 = len(X_train_split3)
test_size_split3 = len(X_test_split3)

model_split3 = RandomForestClassifier(
    n_estimators=n_estimators_value,
    random_state=random_state_value
)
model_split3.fit(X_train_split3, y_train_split3)
predictions_split3 = model_split3.predict(X_test_split3)
accuracy_split3 = accuracy_score(y_test_split3, predictions_split3)

result_entry_3 = {
    "test_size": current_test_size,
    "train_n": train_size_split3,
    "test_n": test_size_split3,
    "accuracy": accuracy_split3
}
results_list.append(result_entry_3)

print(f"  {int(current_test_size * 100):>5}%  {train_size_split3:>8}  {test_size_split3:>7}  {accuracy_split3:>9.4f}")

print("=" * 55)

accuracy_values = [result_entry_1["accuracy"], result_entry_2["accuracy"], result_entry_3["accuracy"]]
max_accuracy_value = max(accuracy_values)

best_result = None
for each_result in results_list:
    if each_result["accuracy"] == max_accuracy_value:
        best_result = each_result
        break

best_test_size = best_result["test_size"]
best_train_n = best_result["train_n"]
best_test_n = best_result["test_n"]
best_accuracy = best_result["accuracy"]

print(f"\n  Best split  ->  test_size = {best_test_size}")
print(f"     Train size  : {best_train_n}")
print(f"     Test size   : {best_test_n}")
print(f"     Accuracy    : {best_accuracy:.4f}\n")
