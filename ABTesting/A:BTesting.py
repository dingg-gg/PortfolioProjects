import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt

path = kagglehub.dataset_download("mursideyarkin/mobile-games-ab-testing-cookie-cats")

files = os.listdir(path)
print(f"Files found in folder: {files}")

csv_file = [f for f in files if f.endswith('.csv')][0]
full_path = os.path.join(path, csv_file)

df = pd.read_csv(full_path)

# Check the number of users in each group
group_counts = df['version'].value_counts()
print("User Counts per Group:")
print(group_counts)

# Calculate percentages
print("\nPercentage Split:")
print(df['version'].value_counts(normalize=True) * 100)


# Plotting the distribution of game rounds
plt.boxplot(df['sum_gamerounds'])
plt.title("Checking for Outliers in Game Rounds")
plt.show()

# Find the max value and remove it
df = df[df['sum_gamerounds'] < df['sum_gamerounds'].max()]

# Average 1-day retention for each group
retention_stats = df.groupby('version')[['retention_1', 'retention_7']].mean()
print("Retention Rates by Group:")
print(retention_stats)

# We perform bootstrap analysis to simulate 1000 times and give me the probability that gate 30 is better

boot_means = []
for i in range(1000):
    # Resample with replacement and calculate mean for both groups
    boot_sample = df.sample(frac=1, replace=True).groupby('version')['retention_7'].mean()
    boot_means.append(boot_sample)

# 2. Convert to DataFrame for calculation
boot_df = pd.DataFrame(boot_means)

# 3. Calculate the percentage difference
boot_df['diff'] = (boot_df['gate_30'] - boot_df['gate_40']) / boot_df['gate_40'] * 100

# 4. Calculate the probability that the difference is greater than 0
prob_gate_30_is_better = (boot_df['diff'] > 0).mean()

print(f"Bootstrap Analysis Results:")
print(f"Probability that Gate 30 has higher 7-day retention: {prob_gate_30_is_better:.1%}")

boot_df['diff'].plot(kind='kde')
plt.axvline(0, color='red')
plt.show()
plt.savefig('results_plot.png')
