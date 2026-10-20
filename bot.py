import telebot
from telebot import types

TOKEN = 'ВАШ_ТОКЕН'
bot = telebot.TeleBot(TOKEN)

INFO = {
    'Русалка': 'Русалка — мифическое существо, обитающее в воде, с телом женщины и рыбьим хвостом вместо ног. Встречается в фольклоре многих культур.',
    'Дракон': 'Дракон — крылатое огнедышащее существо, напоминающее огромного ящера. Символизирует силу, мудрость и испытание в легендах.',
    'Феникс': 'Феникс — бессмертная птица, способная сжигать себя и снова возрождаться из пепла. Символ вечного обновления.',
    'Единорог': 'Единорог — волшебный конь с одним рогом на лбу, символизирующий чистоту, грацию и светлую магию.'
}

game_steps = {}

def make_yes_no_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
    return kb

def make_start_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton('Начать заново'))
    return kb

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    text = (
        "Привет! Загадай одно из существ:\n"
        "Дракон, Единорог, Феникс или Русалка.\n"
        "Отвечай только Да или Нет, и я попробую угадать."
    )
    bot.send_message(message.chat.id, text, reply_markup=make_start_kb())

@bot.message_handler(func=lambda message: message.text == 'Начать заново')
def start_game(message):
    uid = message.chat.id
    game_steps[uid] = 'q1'
    bot.send_message(uid, "Вопрос 1: Это существо живет в воде?", reply_markup=make_yes_no_kb())

@bot.message_handler(func=lambda message: message.text in ['Да', 'Нет'])
def send_reply(message):
    uid = message.chat.id
    ans = message.text

    if uid not in game_steps:
        bot.send_message(uid, "Нажмите кнопку ниже, чтобы играть.", reply_markup=make_start_kb())
        return

    step = game_steps[uid]

    if step == 'q1':
        if ans == 'Да':
            end_game(uid, 'Русалка')
        else:
            game_steps[uid] = 'q2'
            bot.send_message(uid, "Вопрос 2: Оно умеет летать?", reply_markup=make_yes_no_kb())

    elif step == 'q2':
        if ans == 'Да':
            game_steps[uid] = 'q3'
            bot.send_message(uid, "Вопрос 3: Оно дышит огнем?", reply_markup=make_yes_no_kb())
        else:
            end_game(uid, 'Единорог')

    elif step == 'q3':
        if ans == 'Да':
            end_game(uid, 'Дракон')
        else:
            end_game(uid, 'Феникс')

def end_game(uid, creature):
    desc = INFO.get(creature, "")
    text = f"Я угадал! Вы загадали: {creature}.\n\n{desc}"
    bot.send_message(uid, text, reply_markup=make_start_kb())
    if uid in game_steps:
        del game_steps[uid]

if __name__ == '__main__':
    bot.infinity_polling()