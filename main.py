import telebot
import sqlite3

token = '5062396153:AAHb0ooMOoMDw8imXBQjDSwHQMDewwf78DA'
bot = telebot.TeleBot(token)

connection = sqlite3.connect('contacts.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(name TEXT PRIMARY KEY, contactNumber text, note text);""")

connection.commit()

state = 0

def get_state():
    return state

class PhoneContact:
    def __init__(self, name, contactNumber, note):
        self.name = name
        self.contactNumber = contactNumber
        self.note = note
    def strtranslate(self):
        self.name = str(self.name)
        self.contactNumber = str(self.contactNumber)
        self.note = str(self.note)
        return self.name, self.contactNumber, self.note



@bot.message_handler(commands=['start'])
def adduser(message):
    bot.send_message(message.chat.id, 'Введите имя, номер и заметку через запятую')
    global state
    state = 1

@bot.message_handler(func=lambda message: get_state() == 1)
def adduser2(message):
    inf = message.text
    m = str(inf).split(', ')
    add = PhoneContact(m[0], m[1], m[2])
    n = add.strtranslate()
    try:
        local_connection = sqlite3.connect('contacts.db')
        local_cursor = local_connection.cursor()
        local_cursor.execute("INSERT INTO contacts VALUES(?, ?, ?);", (n[0],n[1],n[2]))
        local_connection.commit()
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка подключения к базе даных. Возмжно пользователь с таким именем уже существует.')
    global state
    state = 0


@bot.message_handler(commands=['get'])
def getContactByName(message):
    bot.send_message(message.chat.id, 'Введите имя')
    global state
    state = 2

@bot.message_handler(func=lambda message: get_state() == 2)
def getContactByName2(message):
    textname = message.text
    local_connection = sqlite3.connect('contacts.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute(f"SELECT * from contacts where name = '{str(textname)}';")
    all_results = local_cursor.fetchall()
    for i in all_results[0]:
        bot.send_message(message.chat.id, i)
    global state
    state = 0


bot.polling(none_stop=True, interval=0)