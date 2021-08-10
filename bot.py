from os import link, path
from typing import Text
import telebot
import os
from telebot import types
from parcing import parcing, booknumber, filename
bot = telebot.TeleBot("1918741680:AAGibE_7ISExJoAjaDHIC2HdX1Qkz7OcGLE") 

links=['']*5
def ReInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, напиши мне название книги. \n Об ошибках, багах пишите @higherupanddown")

@bot.message_handler(content_types = ['text'])
def get_bookname_messages(message):
	bookname = message.text
	listofbooks = parcing(bookname, message.chat.id)
	if listofbooks != '404':
		msg = bot.send_message(message.chat.id, listofbooks)
		bot.register_next_step_handler(msg, list_of_books)
	else:
		bot.send_message(message.chat.id, 'Не найдено')
		try:
			os.remove(f'dicts/books{message.chat.id}.json')
		except:
			pass

def list_of_books(message):
	
	number = message.text
	
	if ReInt(number) != False:
		links=booknumber(number, message.chat.id,)
		if links != 'Цифры, Мейсон!':
			msg = bot.send_message(message.chat.id, links)
			bot.register_next_step_handler(msg, book_url)
		else:
			bot.send_message(message.chat.id, "Цифры, Мейсон!")
			try:
				os.remove(f'dicts/books{message.chat.id}.json')
			except:
				pass
	else:
		bookname = message.text
		listofbooks = parcing(bookname, message.chat.id)
		if listofbooks != '404':
			msg = bot.send_message(message.chat.id, listofbooks)
			bot.register_next_step_handler(msg, list_of_books)
		else:
			msg=bot.send_message(message.chat.id, 'Не найдено')
			bot.register_next_step_handler(msg, get_bookname_messages)
			try:
				os.remove(f'dicts/books{message.chat.id}.json')
			except:
				pass

def book_url(message):
	if ReInt(message.text) != False and int(message.text) <= 3:
		number=message.text
		path='./' + filename(number, message.chat.id,)
		doc = open(path, 'rb')
		bot.send_document(message.chat.id, doc)
		os.remove(f'dicts/books{message.chat.id}.json')
	else:
		bookname = message.text
		listofbooks = parcing(bookname, message.chat.id)
		if listofbooks != '404':
			msg = bot.send_message(message.chat.id, listofbooks)
			bot.register_next_step_handler(msg, list_of_books)
		else:
			msg=bot.send_message(message.chat.id, 'Не найдено')
			bot.register_next_step_handler(msg, get_bookname_messages)
			try:
				os.remove(f'dicts/books{message.chat.id}.json')
			except:
				pass
		

	


	

bot.polling(none_stop=True, interval=0)