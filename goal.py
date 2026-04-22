def calculate_goal(goal_amount, months):
    monthly_saving = goal_amount / months
    return monthly_saving

goal = 500000
months = 12

print("Monthly saving needed:", calculate_goal(goal, months))