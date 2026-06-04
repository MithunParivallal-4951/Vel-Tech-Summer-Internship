import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./datasets/student-mat.csv', sep=';')

df['G3'] = pd.to_numeric(df['G3'], errors='coerce')

group1 = df[df['studytime'] == 1]
group2 = df[df['studytime'] == 2]
group3 = df[df['studytime'] == 3]
group4 = df[df['studytime'] == 4]

avg1 = group1['G3'].mean()
avg2 = group2['G3'].mean()
avg3 = group3['G3'].mean()
avg4 = group4['G3'].mean()


overall_mean = df['G3'].mean()

x_labels = ['<2 hrs', '2–5 hrs', '5–10 hrs', '>10 hrs']
averages = [avg1, avg2, avg3, avg4]

plt.figure()


plt.bar(x_labels, averages, color=['blue', 'orange', 'green', 'red'], width=0.5)

plt.axhline(overall_mean, color='black', linestyle='--', label='Overall mean')

plt.text(0, avg1 + 0.2, str(round(avg1, 2)), ha='center')
plt.text(1, avg2 + 0.2, str(round(avg2, 2)), ha='center')
plt.text(2, avg3 + 0.2, str(round(avg3, 2)), ha='center')
plt.text(3, avg4 + 0.2, str(round(avg4, 2)), ha='center')

plt.title('Average Final Grade (G3) by Weekly Study Time')
plt.xlabel('Weekly Study Time')
plt.ylabel('Average G3 Grade')
plt.ylim(0, 16)
plt.legend()

plt.savefig('./savedCharts/bar_studytime.png')
print("Saved: bar_studytime.png")
plt.show()
