from flask import Flask
from flask_apscheduler import APScheduler
import jianlai

class Config(object):
    JOBS = [
        {
            'id': 'jianlai_job_notice',
            'func': 'jianlai:job',
            # 'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True

if __name__ == "__main__":
    app = Flask(__name__)

    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(port=9998)
