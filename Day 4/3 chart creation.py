import pandas as pd
import matplotlib.pyplot as plt

# ── Load dataset ────────────────────────────────────────────────────────────
df = pd.read_csv('student-mat.csv', sep=';')

# ── CHART 1: Bar — Average G3 grade by school ──────────────────────────────
plt.figure(figsize=(8, 5))
avg_grade = df.groupby('school')['G3'].mean()
colors = ['#4C72B0', '#DD8452']
bars = plt.bar(avg_grade.index, avg_grade.values, color=colors, edgecolor='white', linewidth=1.2, width=0.5)

for bar, val in zip(bars, avg_grade.values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
             f'{val:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Average Final Grade (G3) by School', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('School', fontsize=12)
plt.ylabel('Average Grade (G3)', fontsize=12)
plt.ylim(0, 20)
plt.tight_layout()
plt.savefig('chart1_bar_grade_by_school.png', dpi=150)
plt.show()
print("Saved: chart1_bar_grade_by_school.png")

# ── CHART 2: Scatter — G1 vs G3 ────────────────────────────────────────────
plt.figure(figsize=(8, 5))
gp = df[df['school'] == 'GP']
ms = df[df['school'] == 'MS']

plt.scatter(gp['G1'], gp['G3'], color='#4C72B0', alpha=0.7, s=80,
            edgecolors='white', linewidth=0.5, label='GP School')
plt.scatter(ms['G1'], ms['G3'], color='#DD8452', alpha=0.7, s=80,
            edgecolors='white', linewidth=0.5, marker='^', label='MS School')

max_val = max(df['G1'].max(), df['G3'].max())
plt.plot([0, max_val], [0, max_val], 'gray', linestyle='--', linewidth=1,
         alpha=0.5, label='Perfect correlation')

plt.title('First Period Grade (G1) vs Final Grade (G3)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('First Period Grade (G1)', fontsize=12)
plt.ylabel('Final Grade (G3)', fontsize=12)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('chart2_scatter_G1_vs_G3.png', dpi=150)
plt.show()
print("Saved: chart2_scatter_G1_vs_G3.png")

# ── CHART 3: Histogram — Age distribution ──────────────────────────────────
plt.figure(figsize=(8, 5))
plt.hist(df['age'], bins=range(int(df['age'].min()), int(df['age'].max()) + 2),
         color='#4C72B0', edgecolor='white', linewidth=1.2, alpha=0.85)

plt.axvline(df['age'].mean(), color='#DD8452', linestyle='--', linewidth=2,
            label=f'Mean age: {df["age"].mean():.1f}')

plt.title('Age Distribution of Students', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Age', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.xticks(range(int(df['age'].min()), int(df['age'].max()) + 1))
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('chart3_histogram_age.png', dpi=150)
plt.show()
print("Saved: chart3_histogram_age.png")

# ── CHART 4: Line — G1 → G2 → G3 average trend ────────────────────────────
plt.figure(figsize=(8, 5))
averages = [df['G1'].mean(), df['G2'].mean(), df['G3'].mean()]
periods  = ['G1\n(1st Period)', 'G2\n(2nd Period)', 'G3\n(Final)']

plt.plot(periods, averages, color='#4C72B0', marker='o', markersize=10,
         linewidth=2.5, markerfacecolor='white', markeredgewidth=2.5)

for i, avg in enumerate(averages):
    plt.text(i, avg + 0.15, f'{avg:.2f}', ha='center', va='bottom',
             fontsize=12, fontweight='bold', color='#4C72B0')

plt.title('Average Grade Trend: G1 → G2 → G3', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Period', fontsize=12)
plt.ylabel('Average Grade', fontsize=12)
plt.ylim(0, 20)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('chart4_line_grade_trend.png', dpi=150)
plt.show()
print("Saved: chart4_line_grade_trend.png")

print("\nAll 4 charts saved!")