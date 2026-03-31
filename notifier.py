import time
import database
from datetime import datetime
from win11toast import toast
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def check_alarms():
    conn = database.get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Query pending tasks that are due AND not yet notified
    query = '''
        SELECT * FROM tasks 
        WHERE status = 'Pending' 
        AND due_date IS NOT NULL 
        AND due_date <= ? 
        AND notified = 0
    '''
    due_tasks = conn.execute(query, (now_str,)).fetchall()
    conn.close()
    
    for t in due_tasks:
        logging.info(f"Triggering alarm for task {t['id']}: {t['description']}")
        
        # Windows Native Toast Notification with Sound!
        toast(
            f"⏰ Task Due: {t['description']}", 
            f"Priority: {t['priority']}\nDue: {t['due_date']}",
            audio={'src': 'ms-winsoundevent:Notification.Reminder'}
        )
        
        # Mark as notified so it doesn't trigger again (or triggers once per task)
        database.mark_notified(t['id'])

def run_daemon():
    print("=" * 50)
    print("⏰ Smart To-Do Alarm Daemon Started!")
    print("Running silently in the background...")
    print("You will receive Windows notifications as tasks become due.")
    print("You can close this window to stop the alarms.")
    print("=" * 50)
    
    while True:
        try:
            check_alarms()
        except Exception as e:
            logging.error(f"Error checking alarms: {e}")
        time.sleep(15) # Check every 15 seconds

if __name__ == "__main__":
    run_daemon()
