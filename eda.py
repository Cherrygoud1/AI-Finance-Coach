import pandas as pd

df = pd.read_csv("cleaned_data.csv")

# Income vs Expense
income = df[df['Amount'] > 0]['Amount'].sum()
expense = df[df['Amount'] < 0]['Amount'].sum()

print("Total Income:", income)
print("Total Expense:", expense)

# Monthly trend
monthly = df.groupby(['Year','Month'])['Amount'].sum()
print(monthly)

# Category spend
category = df.groupby('Category')['Amount'].sum().sort_values()
print(category)