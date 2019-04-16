import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler({
    'apscheduler.jobstores.default': {
         'type': 'mongodb'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '10'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '3'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})


scheduler.start()

scheduler.print_jobs()
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
# scheduler.print_jobs()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
time.sleep(10)