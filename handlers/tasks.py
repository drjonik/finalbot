from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pydantic import BaseModel, ValidationError
from utils.parser import parse_natural
from db.database import add_task, get_user_tasks
from utils.lang import I18n, _

router = Router()

class TaskIn(BaseModel):
    text: str
    date_time: str  # will be parsed again
    repeat: str | None = None

class AddTask(StatesGroup):
    waiting_for_input = State()

@router.callback_query(Text('add'))
async def callback_add(call: types.CallbackQuery, state: FSMContext):
    user_lang = I18n.get_user_lang(call.from_user.id)
    await call.message.answer(
        _('✍️ Напиши напоминание в свободной форме:', user_lang) + "\n"
        + _('Пример: каждый понедельник в 10:00 спортзал', user_lang)
    )
    await state.set_state(AddTask.waiting_for_input)
    await call.answer()

@router.message(AddTask.waiting_for_input)
async def process_task_input(message: types.Message, state: FSMContext):
    user_lang = I18n.get_user_lang(message.from_user.id)
    try:
        parsed = parse_natural(message.text, user_lang)
    except Exception:
        await message.answer(_('Не удалось понять запрос.', user_lang))
        await state.clear()
        return
    try:
        task = await add_task(message.from_user.id, parsed)
    except ValidationError:
        await message.answer(_('Не удалось создать задачу.', user_lang))
        await state.clear()
        return
    await message.answer(_(f'Задача добавлена: {task.text}', user_lang))
    await state.clear()

@router.callback_query(Text('view'))
async def callback_view(call: types.CallbackQuery):
    user_lang = I18n.get_user_lang(call.from_user.id)
    tasks = await get_user_tasks(call.from_user.id)
    if not tasks:
        await call.message.answer(_('📋 Ваши задачи отсутствуют.', user_lang))
    else:
        lines = []
        for i, t in enumerate(tasks, 1):
            lines.append(f"{i}. {t.text} — {t.date_time.strftime('%Y-%m-%d %H:%M')}")
        await call.message.answer('\n'.join(lines))
    await call.answer()

@router.callback_query(Text('settings'))
async def callback_settings(call: types.CallbackQuery):
    user_lang = I18n.get_user_lang(call.from_user.id)
    await call.message.answer(_('⚙️ Здесь позже будут настройки.', user_lang))
    await call.answer()

@router.message(Command(commands=['cancel', 'Отмени']))
async def cancel_task(message: types.Message):
    user_lang = I18n.get_user_lang(message.from_user.id)
    success = await remove_task(message.from_user.id, message.text)
    if success:
        await message.answer(_('Задача отменена.', user_lang))
    else:
        await message.answer(_('Совпадающих задач не найдено.', user_lang))

# Registration

def register(dp):
    dp.include_router(router)
