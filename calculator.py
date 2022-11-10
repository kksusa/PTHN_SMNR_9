import telebot
import time
import json
import numpy

API_TOKEN='5775895145:AAHFBY_06oYIfZBMwfrOgb7fmpE4lkTTiIU'
bot = telebot.TeleBot(API_TOKEN)

def ReadData():
    with open("log.json") as dataStorage:
        array = json.load(dataStorage)
    return array

def SaveData(data):
    with open("log.json", "w", encoding = "utf-8") as dataStorage:
        dataStorage.write(json.dumps(data, ensure_ascii = False))
        dataStorage.close()

def FindElements(expression):
    elements = []
    element = ""
    i = 0
    if "+" or "-" or "/" or "*" in expression:
        while i < len(expression):
            if expression[i] != "+" and expression[i] != "-" and expression[i] != "*" and expression[i] != "/":
                element += expression[i]
                i += 1
                continue
            else:
                elements.append(element)
                element = ""
                element += expression[i]
                elements.append(element)
                i += 1
                element = ""
        elements.append(element)
    i = 0
    if "" in elements:
        while "" in elements:
            if elements[i] == "" and elements[i + 1] == "-":
                elements[i + 2] = str((-1)*float(elements[i + 2]))
                elements.pop(i + 1)
                elements.pop(i)
            i += 1
    return elements

def FindBrackets(expression):
    startBracket = None
    endBracket = None
    newExpression = ""
    if "(" and ")" in expression:
        for i in range(len(expression)):
            if expression[i] == "(": startBracket = i
            if expression[i] == ")":
                endBracket = i
                break
        for i in range(startBracket + 1, endBracket):
            newExpression = newExpression + expression[i]
        expression = newExpression
    return expression, startBracket, endBracket 

def Calculation(elements):
    i = 0
    while "*" in elements or "/" in elements:
        if elements[i] == "*":
            elements[i] = str(float(elements[i - 1]) * float(elements[i + 1]))
            elements.pop(i + 1)
            elements.pop(i - 1)
        elif elements[i] == "/":
            elements[i] = str(float(elements[i - 1]) / float(elements[i + 1]))
            elements.pop(i + 1)
            elements.pop(i - 1)
        else: i += 1
    i = 0
    while "+" in elements or "-" in elements:
        if elements[i] == "+":
            elements[i] = str(float(elements[i - 1]) + float(elements[i + 1]))
            elements.pop(i + 1)
            elements.pop(i - 1)
        elif elements[i] == "-":
            elements[i] = str(float(elements[i - 1]) - float(elements[i + 1]))
            elements.pop(i + 1)
            elements.pop(i - 1)
        else: i += 1
    return elements[0]

def BaseFunctionRational(expression):
    result = 0
    if FindBrackets(expression)[1] == None: result = Calculation(FindElements(FindBrackets(expression)[0]))
    else:
        while "(" in expression and ")" in expression:
            IMexpression = FindElements(FindBrackets(expression)[0])
            result = Calculation(IMexpression)
            expression = expression[:FindBrackets(expression)[1]] + result + expression[(FindBrackets(expression)[2] + 1):]
    out = Calculation(FindElements(expression))
    roundNumber = round(float(out), 2)
    if roundNumber % 1 * 100 == 0:
        roundNumber = int(roundNumber)
    return roundNumber

@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(message.chat.id, '''Это калькулятор рациональных и комплексных чисел.

Если желаете выполнить какое-то действие, то введите соответствующую команду:

/rat "выражение со скобками или без" - расчет выражения с рациональными числами без пробелов;
/comp "выражение со скобками или без в формате "A±Bj" - расчет выражения с комплексными числами без пробелов;
/log - вывод лога вычислений.''')

@bot.message_handler(commands=['rat'])
def rat(message):
    text = message.text
    try:
        array = text.split()
        result = BaseFunctionRational(array[1])
        answer = str(array[1]) + "=" + str(result)
        bot.send_message(message.chat.id, answer)
        array1 = ReadData()
        array1.append(answer)
        SaveData(array1)
        time.sleep(1)
    except: bot.send_message(message.chat.id, "Выражение введено неправильно. Попробуйте ещё раз.")

@bot.message_handler(commands=['comp'])
def comp(message):
    text = message.text
    try:
        array = text.split()
        result = numpy.round(eval(array[1]), 2)
        answer = str(array[1]) + "=" + str(result)
        bot.send_message(message.chat.id, answer)
        array1 = ReadData()
        array1.append(answer)
        SaveData(array1)
        time.sleep(1)
    except: bot.send_message(message.chat.id, "Выражение введено неправильно. Попробуйте ещё раз.")

@bot.message_handler(commands=['log'])
def log(message):
    if ReadData() == []: bot.send_message(message.chat.id, "\nЛог пустой. Сначала выполните какое-нибудь вычисление.")
    else:
        arrayLog = ReadData()
        bot.send_message(message.chat.id, "\nИстория вычислений:\n")
        for i in range(len(arrayLog)): bot.send_message(message.chat.id, f"{i + 1}: {arrayLog[i]}")
    time.sleep(1)

@bot.message_handler(content_types="text")
def cantUnderstand(message):
    bot.send_message(message.chat.id, '''Не могу тебя понять.
Введи любую команду из списка:

/rat "выражение со скобками или без" - расчет выражения с рациональными числами без пробелов;
/comp "выражение со скобками или без в формате "A±Bj" - расчет выражения с комплексными числами без пробелов;
/log - вывод лога вычислений.''')

bot.polling()