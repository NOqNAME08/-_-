import tkinter as tk
from datetime import datetime, timedelta

def update_time():
    now = datetime.now()
    today_weekday = now.weekday()
    days_until_friday = (4 - today_weekday) % 7
    arrival = now + timedelta(days=days_until_friday)
    arrival = arrival.replace(hour=15, minute=30, second=0, microsecond=0)

    remaining = arrival - now
    if remaining.total_seconds() < 0:
        result_label.config(text="이미 집인 듯")
    else:
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        result_label.config(text=f"{hours}시간 {minutes}분 {seconds}초 남음")

    
    root.after(1000, update_time)

root = tk.Tk()
root.title("집 갈 시간 계산기")
root.geometry("300x150")

result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=40)

update_time()

root.mainloop()