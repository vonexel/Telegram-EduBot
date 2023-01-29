#!/usr/local/bin/python3.8
import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('TOKEN')

db = sqlite3.connect('baza.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Utilisateur(
    surname TEXT,
    firstname TEXT,
    middlename TEXT,
    telephone TEXT,
    nickname TEXT,
    mail TEXT
)""")

db.commit()

user_data = {}


class User:
    def __init__(self, surname):
        self.surname = surname
        self.firstname = ''
        self.middlename = ''
        self.telephone = ''
        self.nickname = ''
        self.mail = ''


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg=bot.send_message(message.chat.id,"Здравствуйте!Мы рады приветствовать Вас в одной из главнейших частей нашего курса!Этот бот отвечает за многое: тесты, лекции и навигацию по всей экосистеме, но обо всем по порядку.Для начала давайте познакомимся) Чат-бот довольно сложная система и для того, чтобы он грамотно с Вами взаимодействовал, ему нужны некоторые данные")
    msg = bot.send_message(message.chat.id, "Начнем с простого- напишите фамилию")
    bot.register_next_step_handler(msg, process_surname_step)


def process_surname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        print(type(user_data))
        msg = bot.send_message(message.chat.id, "Теперь введите свое полное имя")
        bot.register_next_step_handler(msg, process_firstname_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.firstname = message.text
        print(type(user.firstname))
        msg = bot.send_message(message.chat.id, "И отчество тоже! ")
        bot.register_next_step_handler(msg, process_middlename_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_middlename_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.middlename = message.text
        print(type(user.middlename))

        msg = bot.send_message(message.chat.id, "Введите свой телефонный номер")
        bot.register_next_step_handler(msg, process_telephone_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_telephone_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.telephone = message.text
        print(type(user.telephone))

        msg = bot.send_message(message.chat.id, "Нам уже не терпится показать Вам, что находится внутри! Осталось только ввести свой никнейм в Telegrame, чтобы ваши успехи точно не потерялись")
        bot.register_next_step_handler(msg, process_nickname_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_nickname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.nickname = message.text
        print(type(user.nickname))

        msg = bot.send_message(message.chat.id, "Ой, чуть не забыли,укажите свою почту ")
        bot.register_next_step_handler(msg, process_mail_step)
    except Exception as e:
        bot.reply_to(message, e)


def process_mail_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.mail = message.text
        print(type(user.mail))
        cursor.execute(
            f"INSERT INTO Utilisateur (surname,firstname,middlename,telephone,nickname,mail) VALUES(?,?,?,?,?,?)",
            (user.surname, user.firstname, user.middlename, user.telephone, user.nickname, user.mail))
        print(f"INSERT INTO Utilisateur (surname,firstname,middlename,telephone,nickname,mail) VALUES(?,?,?,?,?,?)",
              (user.surname, user.firstname, user.middlename, user.telephone, user.nickname, user.mail))
        db.commit()
        db.close

        msg = bot.send_message(message.chat.id,"Вы успешно зарегистрированны! Введите любое сообщение,чтобы приступить к работе! ")
        bot.register_next_step_handler(msg, first)
    except Exception as e:
        bot.reply_to(message, e)


def first(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Меню')
    send = bot.send_message(message.chat.id,"Здравствуйте! Вы наконец-то добрались до самого сердца нашего курса – заветной кнопки «Меню». Как только Вы нажмете на нее, Вам откроется уйма вкладок, которые будут заполнены, когда Вы присоединитесь к нам. Но хватит слов! Нажимайте на кнопку и смотрите все сами.",reply_markup=keyboard)
    bot.register_next_step_handler(send, second)


def second(message):
    if message.text == 'Меню':
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Тесты', 'Лекции')
        keyboard.add('Ссылки', 'Навигация')
        keyboard.add('Актуальное')
        send = bot.send_message(message.chat.id, 'Что Вас интересует?? ', reply_markup=keyboard)
        bot.register_next_step_handler(send, third)
    else:
        bot.send_message(message.chat.id, 'Извините,я Вас не понял')


def third(message):
    if message.text == 'Тесты':
        keyboard = types.ReplyKeyboardMarkup(True, False)
        send = bot.send_message(message.chat.id,"Здесь Вы сможете пройти тесты по химиии ,не переходя на стороние ресурсы!Все тесты будут доступны в нашем чат-боте!")
        send =bot.send_message(message.chat.id,"[Собеседование и тест](https://docs.google.com/forms/d/e/1FAIpQLSdAIzzOti7wS6CpNOmidX1f3PTFYH3Q4MJmotavCReYZe6DNA/viewform)",parse_mode='Markdown')
    elif message.text == 'Лекции':
        #send = bot.send_message(message.chat.id,"Здесь, по мере освоения программы, будут публиковаться ссылки на лекции.")
        keyboard3 = types.ReplyKeyboardMarkup(True, False)
        markup = types.InlineKeyboardMarkup()
        lessonz = types.InlineKeyboardButton(text='Лекция в Zoom', url='https://us04web.zoom.us/j/73091577424?pwd=VFRxTFdMeEptSi9TeG43aTFvdm5GUT09')
        markup.add(lessonz)
        send = bot.send_message(message.chat.id, "Нажмите на кнопку,чтобы перейти на лекционное занятие.Пароль от конференции :vxwqu6",reply_markup=markup)
    elif message.text == 'Навигация':
        send = bot.send_message(message.chat.id,"Сейчас Вы находитесь чат-боте, связывающем механизме во всей нашей экосистеме. Здесь Вы сможете найти все необходимые ссылки и материалы для изучения химии. Клавиатура - Ваш главный друг. При нажатии на нее, Вы получите все необходимые данные!")
    elif message.text == 'Актуальное':
        send = bot.send_message(message.chat.id,"Желаете приобрести курс?")
    elif message.text == 'Ссылки':
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Литература', 'Социальные сети')
        keyboard.add('Отмена')
        send = bot.send_message(message.chat.id, 'Что Вас интересует?', reply_markup=keyboard)
    if message.text == 'Литература':
        send = bot.send_message(message.chat.id,"Здесь Вы сможете ознакомится с необходимыми литературными источниками для углубленного изучения материала,а также найти их в виде файлов для скачивания")
    elif message.text == 'Социальные сети':
        keyboard = types.ReplyKeyboardMarkup(True, False)
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Мы в Instagram', url='https://www.instagram.com/cham4v/')
        markup.add(btn_my_site)
        send = bot.send_message(message.chat.id, "Нажмите на кнопку,чтобы перейти в наш инстаграм.",reply_markup=markup)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        markup = types.InlineKeyboardMarkup()
        btn_my_sitee = types.InlineKeyboardButton(text='Мы в Telegram', url='t.me/HJIEBUIIIEK')
        markup.add(btn_my_sitee)
        send = bot.send_message(message.chat.id, "Нажмите на кнопку,чтобы перейти в наш телеграм.",reply_markup=markup)

    elif message.text == 'Отмена':
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Тесты', 'Лекции')
        keyboard.add('Ссылки', 'Навигация')
        keyboard.add('Актуальное')
        send = bot.send_message(message.chat.id, "Вы вернулись в основное меню", reply_markup=keyboard)
    send = bot.send_message(message.chat.id, "Я к вашим услугам!")
    bot.register_next_step_handler(send, third)


# sql=db.cursor.close()
# db.commit()
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.infinity_polling()
