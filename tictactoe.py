import telebot
import emoji
import time

API_TOKEN='5775895145:AAHFBY_06oYIfZBMwfrOgb7fmpE4lkTTiIU'
bot = telebot.TeleBot(API_TOKEN)

def CheckWinner(array):
    status = False
    if array[0] == array[1] == array[2] != " ":
        status = True
    elif array[3] == array[4] == array[5] != " ":
        status = True
    elif array[6] == array[7] == array[8] != " ":
        status = True
    elif array[0] == array[4] == array[8] != " ":
        status = True
    elif array[2] == array[4] == array[6] != " ":
        status = True
    elif array[0] == array[3] == array[6] != " ":
        status = True
    elif array[1] == array[4] == array[7] != " ":
        status = True
    elif array[2] == array[5] == array[8] != " ":
        status = True
    return status

@bot.message_handler(commands=['start'])
def greetings(message):
    global a
    a = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    bot.send_message(message.chat.id, f'''Добро пожаловать в игру "крестики-нолики"!
Поле состоит из 9 клеток, каждая из которых
по умолчанию именована следующим образом:

 ---------------
| 1 | 2 | 3 |
 ---------------
| 4 | 5 | 6 |
 ---------------
| 7 | 8 | 9 |
 ---------------
Сначала ходит игрок 1. Он вводит команду /move1 и номер поля.
То же самое делает игрок 2, только с командой /move2.
Игрок 1 по умолчанию вводит "х", а игрок 2 - "о".

Удачи {emoji.emojize(":smiling_face_with_sunglasses:")}''')

    time.sleep(1)
    bot.send_message(message.chat.id, f"""
 ---------------
| {a[0]} | {a[1]} | {a[2]} |
 ---------------
| {a[3]} | {a[4]} | {a[5]} |
 ---------------
| {a[6]} | {a[7]} | {a[8]} |
 ---------------""")

@bot.message_handler(commands=['move1'])
def move1(message):
    text = message.text
    try:
        array = text.split()
        move1 = int(array[1])
        if move1 >= 1 and move1 <= 9:
            a[move1 - 1] = "x"
            bot.send_message(message.chat.id, f"""
 ---------------
| {a[0]} | {a[1]} | {a[2]} |
 ---------------
| {a[3]} | {a[4]} | {a[5]} |
 ---------------
| {a[6]} | {a[7]} | {a[8]} |
 ---------------""")
            if CheckWinner(a) == True: bot.send_message(message.chat.id, "Игрок 1 выиграл! Поздравляем с победой!")
            elif a[0] != " " and a[1] != " " and a[2] != " " and a[3] != " " and a[4] != " " and a[5] != " " and a[6] != " " and a[7] != " " and a[8] != " ": bot.send_message(message.chat.id, f'У нас ничья. Может, сыграем еще? {emoji.emojize(":smiling_face_with_sunglasses:")}')
        else: bot.send_message(message.chat.id, "Число введено неправильно. Попробуйте ещё раз.")
    except: bot.send_message(message.chat.id, "Число введено неправильно. Попробуйте ещё раз.")

@bot.message_handler(commands=['move2'])
def move2(message):
    text = message.text
    try:
        array = text.split()
        move2 = int(array[1])
        if move2 >= 1 and move2 <= 9:
            a[move2 - 1] = "o"
            bot.send_message(message.chat.id, f"""
 ---------------
| {a[0]} | {a[1]} | {a[2]} |
 ---------------
| {a[3]} | {a[4]} | {a[5]} |
 ---------------
| {a[6]} | {a[7]} | {a[8]} |
 ---------------""")
            if CheckWinner(a) == True: bot.send_message(message.chat.id, "Игрок 2 выиграл! Поздравляем с победой!")
            elif a[0] != " " and a[1] != " " and a[2] != " " and a[3] != " " and a[4] != " " and a[5] != " " and a[6] != " " and a[7] != " " and a[8] != " ": bot.send_message(message.chat.id, f'У нас ничья. Может, сыграем еще? {emoji.emojize(":smiling_face_with_sunglasses:")}')
        else: bot.send_message(message.chat.id, "Число введено неправильно. Попробуйте ещё раз.")
    except: bot.send_message(message.chat.id, "Число введено неправильно. Попробуйте ещё раз.")

@bot.message_handler(content_types="text")
def cantUnderstand(message):
    bot.send_message(message.chat.id, '''Не могу тебя понять.
Введи любую команду из списка:
/start - начать игру;
/move1 "номер ячейки" - для хода первого игрока;
/move2 "номер ячейки" - для хода второго игрока;''')

bot.polling()