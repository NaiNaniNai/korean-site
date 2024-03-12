from base.service import OnlineService
from project_root.celery import app


@app.task
def delete_irrelevant_online_user():
    service = OnlineService()
    service.delete()
