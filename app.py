import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="AI Finance Coach", layout="wide")

st.title("🤖 AI-Powered Personal Finance Coach")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("cleaned_data.csv")

# ---------------- USER SELECTION ----------------
user_id = st.selectbox("Select User", df['User_ID'].unique(), key="user_select")
user_df = df[df['User_ID'] == user_id].copy()

month = st.selectbox("Select Month", user_df['Month'].unique(), key="month_select")
monthly_df = user_df[user_df['Month'] == month]

# ---------------- METRICS ----------------
income = monthly_df[monthly_df['Amount'] > 0]['Amount'].sum()
expense = monthly_df[monthly_df['Amount'] < 0]['Amount'].sum()
savings = income + expense

col1, col2, col3 = st.columns(3)
col1.metric("Monthly Income", f"₹{income:.0f}")
col2.metric("Monthly Expense", f"₹{expense:.0f}")
col3.metric("Monthly Savings", f"₹{savings:.0f}")

# ---------------- TRANSACTION HISTORY ----------------
st.subheader("📄 Transaction History")

st.dataframe(
    monthly_df[['Date', 'Description', 'Category', 'Amount']]
)

# ---------------- BUDGET DASHBOARD ----------------
st.subheader("📊 Budget Dashboard")

category_df = monthly_df.groupby('Category')['Amount'].sum().reset_index()
category_df['Amount'] = category_df['Amount'].abs()
category_df['Recommended'] = category_df['Amount'] * 1.1
category_df['Variance'] = category_df['Amount'] - category_df['Recommended']

st.dataframe(category_df)

for _, row in category_df.iterrows():
    if row['Amount'] > row['Recommended']:
        st.warning(f"Overspending in {row['Category']} 🚨")

st.bar_chart(category_df.set_index('Category')[['Amount', 'Recommended']])

# ---------------- SPENDING INSIGHTS ----------------
st.subheader("📈 Spending Insights")

if not category_df.empty:
    top_cat = category_df.sort_values(by='Amount', ascending=False).iloc[0]
    st.write(f"🔝 Highest spending category: **{top_cat['Category']}**")
    st.write(f"💰 Amount spent: ₹{top_cat['Amount']:.0f}")

# ---------------- RECURRING EXPENSES ----------------
st.subheader("🔁 Recurring Expenses")

recurring = user_df['Description'].value_counts()
recurring = recurring[recurring > 3]

if not recurring.empty:
    st.write(recurring.head())
else:
    st.write("No strong recurring expenses detected")

# ---------------- GOAL PLANNER ----------------
st.subheader("🎯 Goal Planner")

goal_amount = st.number_input("Goal Amount ₹", value=500000)
months = st.slider("Timeline (months)", 1, 36, 12)

monthly_required = goal_amount / months
st.write(f"💡 Save ₹{monthly_required:.0f} per month")

total_savings = monthly_df['Amount'].sum()
progress = (total_savings / goal_amount) * 100
progress = max(0, min(progress, 100))

st.progress(progress / 100)
st.write(f"📊 Progress: {progress:.2f}%")

if monthly_required > savings:
    st.error("❌ Not on track")
    st.warning("⚠️ Suggestion: Reduce expenses or extend timeline")
else:
    st.success("✅ On track")

# ---------------- ANOMALY DETECTION ----------------
st.subheader("🚨 Anomaly Detection")

model = IsolationForest(contamination=0.02, random_state=42)
user_df['Anomaly'] = model.fit_predict(user_df[['Amount']])

anomalies = user_df[user_df['Anomaly'] == -1]

st.write(f"⚠️ Detected {len(anomalies)} anomalies")
st.dataframe(anomalies[['Date', 'Description', 'Amount']].head())

# ---------------- HEALTH SCORE ----------------
st.subheader("💡 Financial Health Score")

if income != 0:
    savings_ratio = savings / income
    spending_ratio = abs(expense) / income
else:
    savings_ratio = 0
    spending_ratio = 1

spending_score = max(0, 100 - (spending_ratio * 100))
goal_score = progress

health_score = (0.4 * savings_ratio * 100) + (0.3 * spending_score) + (0.3 * goal_score)
health_score = max(0, min(health_score, 100))

st.metric("💯 Health Score", f"{health_score:.2f}")

if health_score > 75:
    st.success("✅ Excellent Financial Health")
elif health_score > 50:
    st.warning("⚠️ Average - Improve savings")
else:
    st.error("❌ Poor Financial Health")

# ---------------- SMART AI COACH ----------------
st.subheader("🤖 AI Finance Coach")

user_query = st.text_input("Ask your financial question:", key="chat_input")

if user_query:

    query = user_query.lower()

    if "save" in query:
        answer = f"""
💡 Savings Advice:

• Current Savings: ₹{savings:.0f}
• Try saving at least 20% of income
• Reduce unnecessary expenses
"""

    elif "expense" in query or "spend" in query:
        top_category = category_df.sort_values(by='Amount', ascending=False).iloc[0]['Category']

        answer = f"""
📊 Spending Insight:

• Highest spending category: {top_category}

Suggestions:
• Reduce non-essential expenses
• Track daily spending
"""

    elif "goal" in query:
        answer = f"""
🎯 Goal Planning:

• Progress: {progress:.2f}%
• Required/month: ₹{monthly_required:.0f}

👉 Increase savings or extend timeline
"""

    elif "health" in query:
        answer = f"""
💯 Health Score: {health_score:.2f}

Suggestions:
• Improve savings ratio
• Reduce expenses
"""

    else:
        answer = f"""
🤖 General Advice:

• Track expenses regularly
• Save at least 20% income
• Avoid unnecessary spending
"""

    st.success(answer)