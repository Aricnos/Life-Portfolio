import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Column names
col = ['Average_time_spent', 'Importance', 'Satisfaction']
sla = [
    'Significant other', 'Family', 'Friendship', 'Phy. Health/sports',
    'Mental Health/mindfullness', 'Spirituality/faith', 'Community/citizenship',
    'Social Engagement', 'Job/career', 'Education/learning', 'Finances',
    'Hobbies/interests', 'Online entertainment', 'Offline entertainment',
    'Physiological needs', 'Activities of daily living'
]

# CLI parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "--manual",
    action="store_true",
    help="If set, enter data manually instead of using sample dataset."
)
parser.add_argument(
    "--datafile",
    type=str,
    default="sample_life_portfolio.csv",
    help="Path to dataset file (default: sample_life_portfolio.csv). Ignored if --manual is used."
)


# this is for the jupyter notebook
args, unknown = parser.parse_known_args()

# for terminal user -- args = parser.parse_args()

# Load data
if args.manual:
    print("Manual input mode selected.")
    life_portfolio = []
    for i in range(len(sla)):
        user_in = list(map(int, input(
            f"Enter Average_time_spent, Importance, Satisfaction for {sla[i]} (comma-separated): "
        ).split(',')))
        life_portfolio.append(user_in)

    data_df = pd.DataFrame(data=life_portfolio, columns=col, index=sla)

else:
    print(f"Loading sample dataset from {args.datafile}...")
    data_df = pd.read_csv(args.datafile, index_col=0)  # assumes first col is index (sla)

# Show dataframe
print(data_df)

# Plotting
plt.figure(figsize=(20, 12))
plt.scatter(
    data_df['Satisfaction'], data_df['Importance'],
    s=[max(40, x*100) for x in data_df['Average_time_spent']],
    alpha=0.6, c='skyblue', edgecolor='k'
)

# Add labels
for i, row in data_df.iterrows():
    plt.text(row['Satisfaction'] + 0.2, row['Importance'] + 0.2, row.name, fontsize=15)

plt.xlabel('Satisfaction')
plt.ylabel('Importance')
# plt.xlim(0, 10)
# plt.ylim(0, 10)
plt.title('Life Categories: Importance vs. Satisfaction (Bubble size = Avg Time Spent)')
plt.grid(True)
# plt.tight_layout()
plt.show()
