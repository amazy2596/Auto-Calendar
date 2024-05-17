from auto_calendar import AutoCalendar

def get_contests(task_done_event):
    instance = AutoCalendar()
    instance.get_codeforces_contest()
    instance.get_atcoder_contest()
    instance.get_nowcoder_contest()
    instance.get_luogu_contest()
    
    task_done_event.set()
    