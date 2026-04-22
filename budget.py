import pandas as pd

df = pd.read_csv("cleaned_data.csv")

income = df[df['Amount'] > 0]['Amount'].sum()
expenses = df[df['Amount'] < 0]['Amount'].sum()

savings_target = 0.2 * income

available_budget = income - savings_target

category_budget = df.groupby('Category')['Amount'].mean()

print("Recommended Budget:", category_budget)