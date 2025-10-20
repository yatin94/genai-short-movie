from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",   # Redis as broker
)

celery_app.conf.task_routes = {
    "src.bg_tasks.*": {"queue": "llm_queue"},
}


from src import bg_tasks  # this line is crucial
