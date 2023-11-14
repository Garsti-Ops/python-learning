import datetime

user_input = input("enter your goal with a deadline spearated bei colon\n")
input_list = user_input.split(":")

goal = input_list[0]
deadline = input_list[1]

deadline_date = datetime.datetime.strptime(deadline, "%d.%m.%Y")
time_till = today_date = datetime.datetime.today()
hours_till = int(time_till.total_seconds() / 60 / 60)
print(f"Time remaining for your goal: {goal} is {hours_till}")