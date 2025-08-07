from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import pytz

from db.database import get_pending_tasks, get_task, remove_task

class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        # Явно указываем ваш часовой пояс
        self.sched = AsyncIOScheduler(timezone="Europe/Amsterdam")
        self.sched.start()

    async def load_jobs(self):
        # Загружаем все незавершённые задачи
        pending = await get_pending_tasks()
        for t in pending:
            # создаём триггер на конкретную дату/время
            trigger = DateTrigger(
                run_date=t.date_time,
                timezone=pytz.timezone("Europe/Amsterdam")
            )
            # job_id на уровне APScheduler можно указать t.id, чтобы можно было сбрасывать
            self.sched.add_job(self.send_reminder, trigger, args=[t.id], id=str(t.id))

    async def send_reminder(self, task_id: int):
        # достаём задачу по id
        task = await get_task(task_id)
        if not task or task.done:
            return
        # шлём сообщение пользователю
        await self.bot.send_message(task.user_id, f"🔔 {task.text}")
        # если задача не повторяется — отмечаем её выполненной
        if not task.repeat:
            await remove_task(task.user_id, task.text)
