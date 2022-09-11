import sqlite3 
from create_bot import bot
import time

from keyboards import kb_client



def sql_start():
	global connect, cur
	connect = sqlite3.connect('finance.db')
	cur = connect.cursor()
	if connect:
		print('Data base connected OK!')



async def create_tables(message):
	try:
		cur.execute(f'''CREATE TABLE earn_{message.from_user.id}(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			category TEXT NOT NULL,
			income INTEGER DEFAULT 0) ''')


		cur.execute(f'''INSERT INTO earn_{message.from_user.id}(category) VALUES
		('Основная работа'),
		('Дополнительный заработок')''')


		cur.execute(f'''CREATE TABLE spend_{message.from_user.id}(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			categories TEXT NOT NULL,
			costs INTEGER DEFAULT 0)''')


		cur.execute(f'''INSERT INTO spend_{message.from_user.id}(categories) VALUES
		('Дом'),
		('Продукты питания'),
		('Развлечения'),
		('Еда вне дома'),
		('Одежда и обувь'),
		('Транспорт'),
		('Услуги и связи'),
		('Здоровье'),
		('Без категории') ''')
		connect.commit()
	except sqlite3.Error as e:
		await bot.send_message(message.from_user.id, 'У вас уже есть аккаунт')

async def sql_add_earn(state,message):
	async with state.proxy() as data: #открываем словарь state.proxy
		cur.execute(f'''UPDATE earn_{message.from_user.id} SET income = income + {data['price_of_earning']} 
		WHERE category = '{data['category_of_earning']}'; ''') # добавляем значения словаря, переведенные в кортеж в бд
		connect.commit()
	await bot.send_message(message.from_user.id, 'Данные переданы', reply_markup=kb_client)

async def sql_add_spend(state,message):
	async with state.proxy() as data: #открываем словарь state.proxy
		cur.execute(f'''UPDATE spend_{message.from_user.id} SET costs = costs + {data['price_of_spending']} 
		WHERE categories = '{data['category_of_spending']}'; ''') # добавляем значения словаря, переведенные в кортеж в бд
		connect.commit()
	await bot.send_message(message.from_user.id, 'Данные переданы', reply_markup=kb_client)


async def sql_show_statistic(message):
	cur.execute(f''' SELECT SUM(income) FROM earn_{message.from_user.id};''')
	all_earn = cur.fetchone()
	cur.execute(f''' SELECT category, MAX(income) FROM earn_{message.from_user.id}; ''')
	max_earn = cur.fetchall()
	cur.execute(f''' SELECT SUM(costs) FROM spend_{message.from_user.id}; ''')
	all_spend = cur.fetchone()
	cur.execute(f''' SELECT categories, MAX(costs) FROM spend_{message.from_user.id}; ''')
	max_spend = cur.fetchall()
	profit = all_earn[0] - all_spend[0]

	await bot.send_message(message.from_user.id, '<b>Основная информация:</b>\n<u>Полный заработок составляет</u> <b>{0}</b> <i>Рублей</i>.\n<u>Наиболее прибыльный заработок:</u> <b>{1}</b> <i>Рублей</i> ({2}).\n<u>Расходы составляют</u> <b>{3}</b> <i>Рублей</i>\n<u>Наибольший расход:</u> <b>{4}</b> <i>Рублей</i> ({5})\n<u>Ваша прибыль составляет</u> <b>{6}</b> <i>Рублей</i>'.format(all_earn[0],max_earn[0][1],max_earn[0][0],all_spend[0],max_spend[0][1],max_spend[0][0],profit), parse_mode = 'html')

async def sql_show_full_statistic(message):
	cur.execute(f''' SELECT category,income FROM earn_{message.from_user.id} ORDER BY income DESC;''')
	earn_result = cur.fetchall()
	cur.execute(f''' SELECT categories,costs FROM spend_{message.from_user.id} ORDER BY costs DESC;''')
	spend_result = cur.fetchall()

	await bot.send_message(message.from_user.id,'<b>Полная статистика</b>:\n<u>Доход</u>:\n{0} - <b>{1}</b> <i>Рублей</i>\n{2} - <b>{3}</b> <i>Рублей</i>\n<u>Расходы:</u>\n{4} - <b>{5}</b> <i>Рублей</i>\n{6} - <b>{7}</b> <i>Рублей</i>\n{8} - <b>{9}</b> <i>Рублей</i>\n{10} - <b>{11}</b> <i>Рублей</i>\n{12} - <b>{13}</b> <i>Рублей</i>\n{14} - <b>{15}</b> <i>Рублей</i>\n{16} - <b>{17}</b> <i>Рублей</i>\n{18} - <b>{19}</b> <i>Рублей</i>'.format(earn_result[0][0],earn_result[0][1],earn_result[1][0],earn_result[1][1],spend_result[0][0],spend_result[0][1],spend_result[1][0],spend_result[1][1],spend_result[2][0],spend_result[2][1],spend_result[3][0],spend_result[3][1],spend_result[4][0],spend_result[4][1],spend_result[5][0],spend_result[5][1],spend_result[6][0],spend_result[6][1],spend_result[7][0],spend_result[7][1],spend_result[8][0],spend_result[8][1]), parse_mode = 'html' )

async def sql_delete_info(message):
	cur.execute(f''' UPDATE earn_{message.from_user.id} SET income = 0 WHERE income > 0 ''')
	cur.execute (f''' UPDATE spend_{message.from_user.id} SET costs = 0 WHERE costs > 0 ''')
	connect.commit()
	await bot.send_message(message.from_user.id,  'Информация успешно очищена', reply_markup=kb_client)