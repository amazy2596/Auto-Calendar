import sqlite3
import os

data_dir = os.path.join(os.path.dirname(__file__))
database_path = os.path.join(data_dir, 'added.db')
conn = sqlite3.connect(database_path)
cursor = conn.cursor()
cursor.execute(''' create table if not exists events(
    time text,
    name text,
    content text
)''')

cursor.execute("select * from events")

to_delete = "2024-08-21 00:00:00"

try:
    cursor.execute("delete from contests where time = ?", (to_delete,))
except Exception as e:
    print(e)
    
add_time = "2024-08-21"
add_name = "顽强的Z"
add_content = f"动态互动抽奖
黑神话马上就要上了8月下血本发福利！送8份《黑神话》标准版1份《黑神话》豪华版！
关注@顽强的Z +转发此动态，就能参加抽奖！一共有9个中奖名额哦！
抽奖结果将在8月21日公布~"

cursor.execute("insert into events values(?, ?, ?)", (add_time, add_name, add_content))
    
conn.commit()

cursor.close()
conn.close()