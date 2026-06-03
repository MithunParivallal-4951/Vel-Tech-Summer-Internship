import pandas as pd

data = {
    'name':  ['Mithun', 'Arjun', 'Priya', 'Sneha', 'Rahul'],
    'age':   [20, 21, 19, 22, 20],
    'city':  ['Chennai', 'Mumbai', 'Delhi', 'Pune', 'Hyderabad'],
    'marks': [88, 74, 91, 65, 79]
}

df = pd.DataFrame(data)
print(df.head())
print("Shape:", df.shape)
print("Dtypes:\n", df.dtypes)

df['result'] = df['marks'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')
print(df)
