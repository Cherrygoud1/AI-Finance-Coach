import pandas as pd

# Load dataset
df = pd.read_csv("C:/Users/chara/Downloads/finance_advanced_25k.csv")

# Convert date
df['Date'] = pd.to_datetime(df['Date'])

# Sort data
df = df.sort_values(by='Date')

# Create features
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.month_name()

# Transaction type
df['Transaction_Type'] = df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')

# Save cleaned data
df.to_csv("cleaned_data.csv", index=False)

print("✅ Data preprocessing completed")