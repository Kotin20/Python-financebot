import sqlite3

import telebot


from telebot import types
from config import token


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start']) 
def send_welcome(message):
	bot.reply_to(message, "Здравствуйте <b>{0} {1}</b>, Вас приветсвует финансовый бот. Данный бот предназначен для записи <b>доходов</b> и <b>расходов</b> ваших финансов.\n<b>На данный момент бот содержит следующие команды:</b>\n1) /stats - показать основную статистику.\n2) /fullstats - показать полную статистику.\n3) /earnings - записать свои доходы.\n4) /spending - записать свои расходы.\n5) /delete - удалить всю свою информацию.".format(message.from_user.first_name, message.from_user.last_name), parse_mode = 'html')

@bot.message_handler(commands=['earnings']) 
def send_earnings(message):
	keyboard = types.ReplyKeyboardMarkup() 
	work = types.KeyboardButton(text='👨‍💼 Основная работа')
	under_work = types.KeyboardButton(text='👨‍💻 Дополнительный заработок')
	keyboard.add(work)
	keyboard.add(under_work)
	bot.send_message(message.from_user.id, "Выберите нужную категорию", reply_markup = keyboard)

@bot.message_handler(commands=['spending']) 
def send_spendings(message):
	keyboard = types.ReplyKeyboardMarkup() 
	House = types.KeyboardButton(text='🏠 Дом')
	Food_products = types.KeyboardButton(text='🍞 Продукты питания')
	Entertainments = types.KeyboardButton(text='🎡 Развлечения')
	Eating_out = types.KeyboardButton(text='🍨 Еда вне дома')
	Clothing = types.KeyboardButton(text='👕 Одежда и обувь')
	Transport = types.KeyboardButton(text='🚘 Транспорт')
	Services_communications = types.KeyboardButton(text='☎ Услуги и связи')
	Health = types.KeyboardButton(text='👨‍⚕️ Здоровье')
	Without_category = types.KeyboardButton(text='Без категории')
	keyboard.add(House,Food_products,Entertainments,Eating_out,Clothing,Transport,Services_communications,Health,Without_category)
	bot.send_message(message.from_user.id, "Выберите нужную категорию", reply_markup = keyboard)



@bot.message_handler(commands=['stats']) 
def show_statistic(message):
	with sqlite3.connect('Finance.db') as connect: # подключение к базе данных
		cur =  connect.cursor()
		cur.execute(''' SELECT SUM(income) FROM earnings;''')
		all_earn = cur.fetchone()
		cur.execute(''' SELECT category, MAX(income) FROM earnings; ''')
		max_earn = cur.fetchall()
		cur.execute(''' SELECT SUM(costs) FROM spending; ''')
		all_spend = cur.fetchone()
		cur.execute(''' SELECT categories, MAX(costs) FROM spending; ''')
		max_spend = cur.fetchall()
		profit = all_earn[0] - all_spend[0]

	bot.send_message(message.from_user.id,'<b>Основная информация:</b>\n<u>Полный заработок составляет</u> <b>{0}</b> <i>Рублей</i>.\n<u>Наиболее прибыльный заработок:</u> <b>{1}</b> <i>Рублей</i> ({2}).\n<u>Расходы составляют</u> <b>{3}</b> <i>Рублей</i>\n<u>Наибольший расход:</u> <b>{4}</b> <i>Рублей</i> ({5})\n<u>Ваша прибыль составляет</u> <b>{6}</b> <i>Рублей</i>'.format(all_earn[0],max_earn[0][1],max_earn[0][0],all_spend[0],max_spend[0][1],max_spend[0][0],profit), parse_mode = 'html')


@bot.message_handler(commands=['fullstats']) 
def show_fullstatistic(message):
	with sqlite3.connect('Finance.db') as connect:
		cur =  connect.cursor()
		cur.execute(''' SELECT category,income FROM earnings ORDER BY income DESC;''')
		earn_result = cur.fetchall()
		cur.execute(''' SELECT categories,costs FROM spending ORDER BY costs DESC;''')
		spend_result = cur.fetchall()

	bot.send_message(message.from_user.id,'<b>Полная статистика</b>:\n<u>Доход</u>:\n{0} - <b>{1}</b> <i>Рублей</i>\n{2} - <b>{3}</b> <i>Рублей</i>\n<u>Расходы:</u>\n{4} - <b>{5}</b> <i>Рублей</i>\n{6} - <b>{7}</b> <i>Рублей</i>\n{8} - <b>{9}</b> <i>Рублей</i>\n{10} - <b>{11}</b> <i>Рублей</i>\n{12} - <b>{13}</b> <i>Рублей</i>\n{14} - <b>{15}</b> <i>Рублей</i>\n{16} - <b>{17}</b> <i>Рублей</i>\n{18} - <b>{19}</b> <i>Рублей</i>'.format(earn_result[0][0],earn_result[0][1],earn_result[1][0],earn_result[1][1],spend_result[0][0],spend_result[0][1],spend_result[1][0],spend_result[1][1],spend_result[2][0],spend_result[2][1],spend_result[3][0],spend_result[3][1],spend_result[4][0],spend_result[4][1],spend_result[5][0],spend_result[5][1],spend_result[6][0],spend_result[6][1],spend_result[7][0],spend_result[7][1],spend_result[8][0],spend_result[8][1]), parse_mode = 'html')

@bot.message_handler(commands=['delete'])
def delete_statistic(message):
	with sqlite3.connect('Finance.db') as connect:
		cur =  connect.cursor()
		cur.execute(''' UPDATE earnings SET income = 0 WHERE income > 0 ''')
		cur.execute (''' UPDATE spending SET costs = 0 WHERE costs > 0 ''')
	bot.send_message(message.from_user.id, 'Информация успешно очищена')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	if message.text == '👨‍💼 Основная работа':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_earning,'Основная работа')
	elif message.text == '👨‍💻 Дополнительный заработок':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_earning, 'Дополнительный заработок')
	elif message.text == '🏠 Дом':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Дом')
	elif message.text == '🍞 Продукты питания':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Продукты питания')
	elif message.text == '🎡 Развлечения':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Развлечения')
	elif message.text == '🍨 Еда вне дома':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Еда вне дома')
	elif message.text == '👕 Одежда и обувь':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Одежда и обувь')
	elif message.text == '🚘 Транспорт':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Транспорт')
	elif message.text == '☎ Услуги и связи':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Услуги и связи')
	elif message.text == '👨‍⚕️ Здоровье':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Здоровье')
	elif message.text == 'Без категории':
		bot.send_message(message.from_user.id, 'Введите цифрами, какую сумму вы хотите внести',reply_markup = types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, send_spending,'Без категории')


def decorator(func):
	''' Декоратор  '''
	def inner(message,category):
		sum_ = 0
		while sum_ == 0:
			try:
				sum_ = int(message.text)
			except Exception:
				bot.send_message(message.from_user.id, 'Нельзя менять категорию, если уже выбрали одну, а также информацию нужно вводить цифрами')
				break
		if sum_ == 0:
			bot.register_next_step_handler(message, inner,category)
		else:
			func(message,category)

	return inner

@decorator
def send_earning(message,category):
	sum_ = int(message.text)
	with sqlite3.connect('Finance.db') as connect: 
		cur =  connect.cursor()
		cur.execute(f'''UPDATE earnings SET income = income + {sum_} 
		WHERE category = '{category}'; ''') 
	bot.send_message(message.from_user.id, "Информация успешно передана")

@decorator
def send_spending(message,category):
	sum_ = int(message.text)
	with sqlite3.connect('Finance.db') as connect: 
		cur =  connect.cursor()
		cur.execute(f'''UPDATE spending	SET costs = costs + {sum_}
		WHERE categories = '{category}'; ''') 
	bot.send_message(message.from_user.id, "Информация успешно передана")




if __name__ == '__main__':
	bot.polling()
