# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 22:45:47 2020

@author: dmitrixsha
"""
import telebot
import tmp_cian
import tmp_cian_read
bot = telebot.TeleBot('TOKEN_HERE')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет\n Или напиши /parse для запуска парсера\n Или напиши /update для обновления экселя\n Или напиши /file для получения эксель файла\n Или напиши /print для получения сегодняшних объявлений")
    elif message.text == "/parse":
        bot.send_message(message.from_user.id, "Парсинг начат")
        tmp_cian.get_urls(tmp_cian.get_json())
        bot.send_message(message.from_user.id, "Парсинг завершен")
    elif message.text == "/update":
        tmp_cian_read.save_xls()        
        bot.send_message(message.from_user.id, "База обновляется")
    elif message.text == "/file":
        with open('cian_koptevo.xlsx', 'rb') as xls:
            bot.send_document(message.chat.id,xls)
    elif message.text == "/print":
        bot.send_message(message.from_user.id, tmp_cian_read.get_today())                    
        for i in tmp_cian_read.get_today():
            bot.send_message(message.from_user.id, str(str(i[3])+"\n"+str(i[4])+"\n"+str(i[2])+"\n"))            
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
            
        
bot.polling(none_stop=True, interval=0)        