from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client, earn_buttons, spend_buttons, confirmation_buttons
from aiogram.types import ReplyKeyboardRemove
from date_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMearn(StatesGroup):
	category_of_earning = State()
	price_of_earning = State()

class FSMspend(StatesGroup):
	category_of_spending = State()
	price_of_spending = State()

#@dp.message_handler(commands = ['start']) # обработчик комманд
async def send_welcome(message: types.Message):
	await bot.send_message(message.from_user.id, "Здравствуйте <b>{0} {1}</b>, Вас приветсвует финансовый бот Себастьян. Данный бот предназначен для записи <b>доходов</b> и <b>расходов</b> ваших финансов.\n<u><b>Перед началом работы пропишите комманду</b></u> /register <u><b>чтобы создать аккаунт</b></u>".format(message.from_user.first_name, message.from_user.last_name), parse_mode = 'html', reply_markup=kb_client)


#@dp.message_handler(commands = ['register']) # обработчик комманд
async def reg_table(message: types.Message):
	await sqlite_db.create_tables(message)
	await bot.send_message(message.from_user.id, 'Ваш аккаунт готов', reply_markup=kb_client)

#@dp.message_handler(commands = ['Доходы'])
async def send_earnings(message: types.Message):
	await FSMearn.category_of_earning.set()
	await message.reply('Выберите категорию дохода', reply_markup = earn_buttons)


#@dp.message_handler(state=FSMearn.category_of_earning)
async def send_ern_category(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		data['category_of_earning'] = message.text
	await FSMearn.next()
	await message.reply('Теперь введите сумму, которую вы хотите занести')

#@dp.message_handler(state=FSMearn.price_of_earning)
async def send_ern_price(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		sum_ = 0
		while sum_ == 0:
			try:
				sum_ = int(message.text)
			except Exception:
				await bot.send_message(message.from_user.id, 'Нельзя менять категорию, если уже выбрали одну, а также информацию нужно вводить цифрами')
				await state.finish()
				break
		if sum_ > 0:
			data['price_of_earning'] = int(message.text)

	try:	
		await sqlite_db.sql_add_earn(state,message)
	except KeyError:
		await bot.send_message(message.from_user.id, 'Попробуйте сначала', reply_markup=kb_client)

	await state.finish()

#@dp.message_handler(commands = ['Расходы'])
async def send_spendings(message: types.Message):
	await FSMspend.category_of_spending.set()
	await message.reply('Выберите категорию расхода', reply_markup = spend_buttons)

#@dp.message_handler(state=FSMspend.category_of_spending)
async def send_spend_category(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		data['category_of_spending'] = message.text
	await FSMspend.next()
	await message.reply('Теперь введите сумму, которую вы хотите занести')

#@dp.message_handler(state=FSMspend.price_of_spending)
async def send_spend_price(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		sum_ = 0
		while sum_ == 0:
			try:
				sum_ = int(message.text)
			except Exception:
				await bot.send_message(message.from_user.id, 'Нельзя менять категорию, если уже выбрали одну, а также информацию нужно вводить цифрами')
				await state.finish()
				break
		if sum_ > 0:	
			data['price_of_spending'] = sum_
	try:
		await sqlite_db.sql_add_spend(state,message)
	except KeyError:
		await bot.send_message(message.from_user.id, 'Попробуйте сначала', reply_markup=kb_client)

	await state.finish()

#@dp.message_handler(commands=['Статистика'])
async def show_statistic(message: types.Message):
	await sqlite_db.sql_show_statistic(message)

#@dp.message_handler(commands=['Подробная_статистика'])
async def show_full_statistic(message: types.Message):
	await sqlite_db.sql_show_full_statistic(message)

#@dp.message_handler(commands=['Удалить'])
async def delete_info(message):
	await message.answer('Вы уверены?', reply_markup = confirmation_buttons)


#@dp.message_handler()
async def confirmation(message: types.Message):
	if message.text == '✔Да':
		await sqlite_db.sql_delete_info(message)
	if message.text == '❌Нет':
		await bot.send_message(message.from_user.id, 'Операция отменена', reply_markup=kb_client)	



def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(send_welcome, commands = ['start'])
	dp.register_message_handler(reg_table, commands = ['register'])
	dp.register_message_handler(send_earnings, commands = ['Доходы'])
	dp.register_message_handler(send_ern_category,state=FSMearn.category_of_earning)
	dp.register_message_handler(send_ern_price,state=FSMearn.price_of_earning)
	dp.register_message_handler(send_spendings,commands = ['Расходы'])
	dp.register_message_handler(send_spend_category,state=FSMspend.category_of_spending)
	dp.register_message_handler(send_spend_price,state=FSMspend.price_of_spending)
	dp.register_message_handler(show_statistic, commands=['Статистика'])
	dp.register_message_handler(show_full_statistic, commands=['Подробная_статистика'])
	dp.register_message_handler(delete_info, commands=['Удалить'])
	dp.register_message_handler(confirmation)