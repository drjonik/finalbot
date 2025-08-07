from aiogram import Router, types, F
from aiogram.filters import Command
from pydantic import BaseModel, ValidationError
from datetime import datetime
from utils.parser import parse_natural
from db.database import add_task, remove_task
from utils.lang import I18n, _

router = Router()

class TaskIn(BaseModel):
    text: str
    date_time: datetime
    repeat: str | None = None  # e.g. 'weekly:mon'

@router.message(F.text.startswith(('Напомни','Remind')))
async def create_reminder(message: types.Message):
    user_id = message.from_user.id
    user_lang = I18n.get_user_lang(user_id)
    try:
        parsed = parse_natural(message.text, user_lang)
        task_in = TaskIn(**parsed)
    except ValidationError:
        await message.answer(_('Could not understand your request.', user_lang))
        return

    task = await add_task(user_id, task_in)
    await message.answer(_('Task added: {task}', user_lang).format(task=task.text))

@router.message(Command(commands=['cancel', 'Отмени']))
async def cancel_task(message: types.Message):
    user_id = message.from_user.id
    user_lang = I18n.get_user_lang(user_id)
    text = message.text
    success = await remove_task(user_id, text)
    if success:
        await message.answer(_('Task cancelled.', user_lang))
    else:
        await message.answer(_('No matching task found.', user_lang))

def register(dp):
    dp.include_router(router)
