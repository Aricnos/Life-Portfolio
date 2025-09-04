import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Constants
COLS = ['Average_time_spent', 'Importance', 'Satisfaction']
SLAS = [
    'Significant other', 'Family', 'Friendship', 'Physical Health/sports',
    'Mental Health/Mindfullness', 'Spirituality/Faith', 'Community/Citizenship',
    'Social Engagement', 'Job/Career', 'Education/Learning', 'Finances',
    'Hobbies/Interests', 'Online entertainment', 'Offline entertainment',
    'Physiological needs', 'Activities of daily living'
]

def load_manual_data():
    """Prompt the user for manual input of life portfolio data."""
    while True:  # keep asking until valid
        life_portfolio = []
        for i in range(len(SLAS)):
            user_in = list(map(int, input(
                f"Enter Average_time_spent, Importance, Satisfaction for {SLAS[i]} (comma-separated): "
            ).split(',')))
            life_portfolio.append(user_in)

        # Check total hours (first column of all rows)
        total_hours = sum(row[0] for row in life_portfolio)
        if total_hours != 168:
            print(f"The total average time spent is {total_hours}, but it should be 168. Please re-enter your data.")
        else:
            break

    return pd.DataFrame(data=life_portfolio, columns=COLS, index=SLAS)


def plot_life_portfolio(data_df):
    plt.figure(figsize=(10, 8))
    slus = list(data_df.index)
    n_bubbles = len(slus)
    numbers = np.arange(1, n_bubbles+1)
    
    # Bubble sizes
    bubble_sizes = np.array([max(400, x*50) for x in data_df['Average_time_spent']])
    radii = np.sqrt(bubble_sizes/np.pi) / 60  # Estimate: adjust denominator if bubbles are too large/small

    # Padding for axes
    pad = radii.max()
    x_min, x_max = 1 + pad, 9 - pad
    y_min, y_max = 1 + pad, 9 - pad

    # Clip satisfaction/importance values so bubbles are not too close to edges
    satisfaction = np.clip(data_df['Satisfaction'].values, x_min, x_max)
    importance = np.clip(data_df['Importance'].values, y_min, y_max)
    
    # Jitter for overlapping
    for i in range(n_bubbles):
        for j in range(i):
            if abs(satisfaction[i] - satisfaction[j])<0.1 and abs(importance[i] - importance[j])<0.1:
                satisfaction[i] += np.random.uniform(-0.10, 0.10)
                importance[i] += np.random.uniform(-0.10, 0.10)
    
    # Plot bubbles
    plt.scatter(
        satisfaction, importance,
        s=bubble_sizes, color='#63c3ff', edgecolor='deepskyblue', alpha=0.7, linewidths=1.5
    )
    # Annotate numbers
    for i, num in enumerate(numbers):
        plt.annotate(str(num), (satisfaction[i], importance[i]), fontsize=14, ha='center', va='center', weight='bold', color='black')
    
    # Quadrant lines and styling
    plt.axhline(y=5, color='gray', linestyle='--', linewidth=1.2)
    plt.axvline(x=5, color='gray', linestyle='--', linewidth=1.2)
    plt.xlabel("Satisfaction", fontsize=16, labelpad=15)
    plt.ylabel("Importance", fontsize=16, labelpad=15)
    plt.xlim(1, 9)
    plt.ylim(1, 9)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.box(False)
    plt.title("Life Portfolio", fontsize=20, weight='bold', pad=20)
    plt.text(1, 0.2, "LOW", ha="left", va="center", fontsize=14)
    plt.text(9, 0.2, "HIGH", ha="right", va="center", fontsize=14)
    plt.text(0.2, 1, "LOW", ha="center", va="bottom", rotation=90, fontsize=14)
    plt.text(0.2, 9, "HIGH", ha="center", va="top", rotation=90, fontsize=14)
    legend_text = "\n".join([f"{num}. {slu}" for num, slu in zip(numbers, slus)])
    plt.gcf().text(0.82, 0.5, legend_text, fontsize=13, va='center', ha='left', bbox=dict(facecolor='white', edgecolor='gray'), color='black')
    plt.tight_layout(rect=[0, 0, 0.78, 1])
    plt.savefig("life_portfolio_chart.png", bbox_inches='tight', dpi=150)
    plt.show()




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manual",
        action="store_true",
        help="If set, enter data manually instead of using sample dataset."
    )
    parser.add_argument(
        "--datafile",
        type=str,
        default="data/sample_life_portfolio.csv",
        help="Path to dataset file (default: data/sample_life_portfolio.csv). Ignored if --manual is used."
    )

    args, _ = parser.parse_known_args()

    if args.manual:
        data_df = load_manual_data()
    else:
        data_df = pd.read_csv(args.datafile, index_col=0)

    print(data_df)
    plot_life_portfolio(data_df)
