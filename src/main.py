import threading
import tasks
import utils

def main():
    task_done_event = threading.Event()
    
    thread = threading.Thread(target=tasks.get_contests, args=(task_done_event,))
    thread.start()
    
    task_done_event.wait()
    
    utils.show_notification()
    
if __name__ == "__main__":
    main()
