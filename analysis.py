import pandas as pd

df = pd.read_csv("cleaned_data.csv")

# Monthly spending
monthly_spend = df[df['Amount'] < 0].groupby('Month')['Amount'].sum()

# Top categories
top_categories = df.groupby('Category')['Amount'].sum().sort_values()

print("Monthly Spend:\n", monthly_spend)
print("Top Categories:\n", top_categories)