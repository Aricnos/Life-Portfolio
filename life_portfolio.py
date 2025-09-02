import pandas as pd
import matplotlib.pyplot as plt


life_portfolio = []

col = ['Average_time_spent', 'Importance', 'Satisfaction']
sla = [
    'Significant other', 'Family', 'Friendship', 'Phy. Health/sports',
    'Mental Health/mindfullness', 'Spirituality/faith', 'Community/citizenship',
    'Social Engagement', 'Job/career', 'Education/learning', 'Finances',
    'Hobbies/interests', 'Online entertainment', 'offline entertainment',
    'Physiological needs', 'Activities of daily living'
]

# Input number of categories, ideally should be 16
for i in range(int(input("Enter number of categories (16): "))):
    user_in = list(map(int, input(f"Enter Average_time_spent, Importance, Satisfaction for {sla[i]} (comma-separated): ").split(',')))
    life_portfolio.append(user_in)

data_df = pd.DataFrame(data=life_portfolio, columns=col, index=sla)
print(data_df)

# Create scatter plot
plt.figure(figsize=(20, 12))
scatter = plt.scatter(
    data_df['Satisfaction'], data_df['Importance'],
    s=[max(20, x*8) for x in data_df['Average_time_spent']],  # size by avg time spent
    alpha=0.6, c='skyblue', edgecolor='k'
)

# Add labels to each point using index (category)
for i, row in data_df.iterrows():
    plt.text(row['Satisfaction'] + 0.2, row['Importance'] + 0.2, row.name, fontsize=9)

plt.xlabel('Satisfaction')
plt.ylabel('Importance')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title('Life Categories: Importance vs. Satisfaction (Bubble size = Avg Time Spent)')
plt.grid(True)
plt.tight_layout()
plt.show()

data_df.to_csv('sample_life_portfolio')