import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCHOOL_COLORS = {'GP': '#4C72B0', 'MS': '#DD8452'}
BACKGROUND_COLOR = '#F7F7F7'
TREND_COLOR = '#C0392B'
ACCENT_GREEN = '#2D6A4F'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.facecolor': BACKGROUND_COLOR,
    'figure.facecolor': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

output_dir = './savedCharts'
os.makedirs(output_dir, exist_ok=True)

try:
    df = pd.read_csv('./datasets/student-mat.csv', sep=';')
except FileNotFoundError:
    print("Error: Could not find 'student-mat.csv' in the specified path.")
    exit()

for col in ['G1', 'G2', 'G3']:
    df[col] = pd.to_numeric(df[col], errors='coerce')


avg_g3 = df.groupby('school')['G3'].mean()

plt.figure(figsize=(7, 5))

bars = plt.bar(
    avg_g3.index, avg_g3.values,
    color=[SCHOOL_COLORS[school] for school in avg_g3.index],
    width=0.45, zorder=3, edgecolor='white', linewidth=1.5
)

plt.grid(True, axis='y', color='white', linewidth=1.2, zorder=0)
plt.gca().set_axisbelow(True) 

plt.title('Average Final Grade (G3) by School', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('School', fontsize=11)
plt.ylabel('Average G3', fontsize=11)
plt.ylim(0, 20)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, height + 0.3,
        f'{height:.1f}', ha='center', va='bottom', fontsize=11, fontweight='bold'
    )

plt.tight_layout()
plt.savefig(f'{output_dir}/bar_grade_by_school.png', dpi=150, bbox_inches='tight')
print("Saved: bar_grade_by_school.png")
plt.show()

plt.figure(figsize=(7, 6))

# Loop and plot data for each school group
for school, group in df.groupby('school'):
    plt.scatter(
        group['G1'], group['G3'],
        label=f'School {school}', color=SCHOOL_COLORS[school],
        alpha=0.65, s=45, edgecolors='white', linewidths=0.5, zorder=3
    )

# Calculate and plot the trend line across all data
m, b = np.polyfit(df['G1'], df['G3'], 1)
x_vals = np.linspace(df['G1'].min(), df['G1'].max(), 200)
plt.plot(x_vals, m * x_vals + b, color=TREND_COLOR, linewidth=2, linestyle='--', label='Trend line', zorder=4)

# Customizing elements
plt.grid(True, axis='both', color='white', linewidth=1.2, zorder=0)
plt.gca().set_axisbelow(True)

plt.title('G1 vs G3 Scores by School', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('G1 (First Period Grade)', fontsize=11)
plt.ylabel('G3 (Final Grade)', fontsize=11)
plt.legend(framealpha=0.9, fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/scatter_G1_vs_G3.png', dpi=150, bbox_inches='tight')
print("Saved: scatter_G1_vs_G3.png")
plt.show()


# =====================================================================
# 3. Histogram: Age Distribution
# =====================================================================
plt.figure(figsize=(7, 5))
age_bins = range(df['age'].min(), df['age'].max() + 2)

# Create histogram
counts, edges, patches = plt.hist(
    df['age'], bins=age_bins, color=ACCENT_GREEN, 
    edgecolor='white', linewidth=1.2, zorder=3, align='left'
)

# Customizing elements
plt.grid(True, axis='y', color='white', linewidth=1.2, zorder=0)
plt.gca().set_axisbelow(True)

plt.title('Age Distribution of Students', fontsize=14, fontweight='bold', pad=12)
plt.xlabel('Age', fontsize=11)
plt.ylabel('Number of Students', fontsize=11)
plt.xticks(range(df['age'].min(), df['age'].max() + 1))

# Add clean labels above each active histogram bar
for count, patch in zip(counts, patches):
    if count > 0:
        plt.text(
            patch.get_x() + patch.get_width() / 2, count + 0.8, 
            str(int(count)), ha='center', va='bottom', fontsize=9, color='#333'
        )

plt.tight_layout()
plt.savefig(f'{output_dir}/histogram_age.png', dpi=150, bbox_inches='tight')
print("Saved: histogram_age.png")
plt.show()


# =====================================================================
# 4. Line Chart: Average Grade Trend (G1 -> G2 -> G3)
# =====================================================================
periods = ['G1\n(Period 1)', 'G2\n(Period 2)', 'G3\n(Final)']
overall_means = [df['G1'].mean(), df['G2'].mean(), df['G3'].mean()]

plt.figure(figsize=(8, 5))

# Plot trends for each school distinctly
for school, group in df.groupby('school'):
    school_means = [group['G1'].mean(), group['G2'].mean(), group['G3'].mean()]
    plt.plot(
        periods, school_means, marker='o', markersize=7,
        color=SCHOOL_COLORS[school], linewidth=2, label=f'School {school}', alpha=0.8
    )

# Plot overall baseline trend line
plt.plot(
    periods, overall_means, marker='D', markersize=9,
    color=TREND_COLOR, linewidth=2.5, linestyle='--', label='Overall average', zorder=5
)

# Customizing elements
plt.grid(True, axis='y', color='white', linewidth=1.2, zorder=0)
plt.gca().set_axisbelow(True)

plt.title('Grade Trend: G1 → G2 → G3', fontsize=14, fontweight='bold', pad=12)
plt.ylabel('Average Grade', fontsize=11)
plt.ylim(0, 20)
plt.legend(framealpha=0.9, fontsize=10)

# Label data points directly onto the overall average line
for x_coord, y_coord in zip(periods, overall_means):
    plt.annotate(
        f'{y_coord:.1f}', xy=(x_coord, y_coord), xytext=(0, 10),
        textcoords='offset points', ha='center', fontsize=10, fontweight='bold', color=TREND_COLOR
    )

plt.tight_layout()
plt.savefig(f'{output_dir}/line_grade_trend.png', dpi=150, bbox_inches='tight')
print("Saved: line_grade_trend.png")
plt.show()

print("\n✅ All 4 individual charts have been saved and displayed successfully.")
