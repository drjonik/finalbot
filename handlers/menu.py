from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.lang import I18n, _

router = Router()

def get_main_menu(user_lang: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=_('View Tasks', user_lang), callback_data='view')
    builder.button(text=_('Add Task', user_lang), callback_data='add')
    builder.button(text=_('Settings', user_lang), callback_data='settings')
    builder.adjust(2)
    return builder.as_markup()

@router.message(Command(commands=['start', 'menu']))
async def start_menu(message: types.Message):
    user_lang = I18n.get_user_lang(message.from_user.id)
    text = _('Welcome! I am your personal secretary.', user_lang)
    await message.answer(text, reply_markup=get_main_menu(user_lang))

@router.callback_query(Text('view'))
async def callback_view(call: types.CallbackQuery):
    # Здесь вы должны достать список задач из БД и ответить
    await call.message.answer("📋 Ваши задачи: (пока заглушка)")
    await call.answer()  # закрывает «крутилку» на кнопке

@router.callback_query(Text('add'))
async def callback_add(call: types.CallbackQuery):
    await call.message.answer(
        "✍️ Напиши напоминание в свободной форме:\n"
        "Пример: 'каждый понедельник в 10:00 спортзал'"
    )
    await call.answer()

@router.callback_query(Text('settings'))
async def callback_settings(call: types.CallbackQuery):
    await call.message.answer("⚙️ Здесь позже будут настройки.")
    await call.answer()

def register(dp):
    dp.include_router(router)
    
