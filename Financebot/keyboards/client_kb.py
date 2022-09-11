from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


button_earn = KeyboardButton('/Доходы')
button_spend = KeyboardButton('/Расходы')
button_stats = KeyboardButton('/Статистика')
button_full_stats = KeyboardButton('/Подробная_статистика')
button_delete_info = KeyboardButton('/Удалить')

kb_client = ReplyKeyboardMarkup()
kb_client.add(button_earn,button_spend).row(button_stats,button_full_stats).add(button_delete_info)


work = KeyboardButton(text='Основная работа')
under_work = KeyboardButton(text='Дополнительный заработок')

earn_buttons = ReplyKeyboardMarkup(one_time_keyboard=True)
earn_buttons.add(work,under_work)


House = KeyboardButton(text='Дом')
Food_products = KeyboardButton(text='Продукты питания')
Entertainments = KeyboardButton(text='Развлечения')
Eating_out = KeyboardButton(text='Еда вне дома')
Clothing = KeyboardButton(text='Одежда и обувь')
Transport = KeyboardButton(text='Транспорт')
Services_communications = KeyboardButton(text='Услуги и связи')
Health = KeyboardButton(text='Здоровье')
Without_category = KeyboardButton(text='Без категории')

spend_buttons = ReplyKeyboardMarkup(one_time_keyboard=True)
spend_buttons.add(House,Food_products,Entertainments,Eating_out,Clothing,Transport,Services_communications,Health,Without_category)


button_yes = KeyboardButton(text='✔Да')
button_no = KeyboardButton(text='❌Нет')

confirmation_buttons =  ReplyKeyboardMarkup(one_time_keyboard=True)
confirmation_buttons.add(button_yes,button_no)