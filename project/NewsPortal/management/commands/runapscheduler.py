import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from NewsPortal.models import Post, Category
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


def my_job():
    d_1 = datetime(year=datetime.now().year,
                   month=datetime.now().month,
                   day=datetime.now().day,
                   hour=0,
                   minute=0,
                   second=0)
    d_2 = d_1 - timedelta(days=7)
    d = {}
    for i in range(1, len(Category.objects.all())):
        d[f"{Category.objects.get(id=i)}"] = Post.objects.filter(
            category=Category.objects.get(id=i), date_of_creation__range=[d_2, d_1])

    for k, v in d.items():
        e = Category.objects.get(category=f'{k}').subscrubers.all().values('email')
        email = [e[i]['email'] for i in range(0, len(e))]
        mail = EmailMultiAlternatives(
            subject=f'Все публикации за неделю в категории {k}',
            body='',
            from_email='Foma26199622@mail.ru',
            to=email
        )

        html = render_to_string('send_week.html',
                                context={'post': d[k],
                                         })

        mail.attach_alternative(html, 'text/html')

        mail.send()

        # print("Отправлено")


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
