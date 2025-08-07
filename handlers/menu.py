from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.lang import I18n, _

router = Router()

def get_main_menu(user_lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(_('Просмотр задач', user_lang), callback_data='view'),
        InlineKeyboardButton(_('Добавить задачу', user_lang), callback_data='add'),
    )
    kb.add(InlineKeyboardButton(_('Настройки', user_lang), callback_data='settings'))
    return kb

@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    user_lang = I18n.get_user_lang(message.from_user.id)
    kb = get_main_menu(user_lang)
    await message.answer(
        _('Добро пожаловать! Я ваш персональный секретарь.', user_lang),
        reply_markup=kb
    )

def register(dp):
    """Регистрирует все хэндлеры этого модуля в диспетчере"""
    dp.include_router(router)
