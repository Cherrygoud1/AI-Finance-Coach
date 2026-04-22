import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("C:/Users/chara/Downloads/cleaned_data.csv")

model = IsolationForest(contamination=0.01)

df['anomaly'] = model.fit_predict(df[['Amount']])

print(df[df['anomaly'] == -1])