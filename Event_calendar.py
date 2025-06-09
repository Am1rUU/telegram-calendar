import telebot
from datetime import datetime, timedelta
import schedule
import time
import threading# Настройки бота
TOKEN = '7955350057:AAESM5fA1w9w_8X4k9eEVPFfCO5V_-SAw08'
CHAT_ID = '142652390'  # Ваш Chat ID (узнать через @userinfobot)

bot = telebot.TeleBot(TOKEN)f405 = {
    '28.05.2025':'сдача 405й формы за апрель',
    '25.06.2025':'сдача 405й формы за май',
    '22.07.2025':'сдача 405й формы за июнь',
    '22.08.2025':'сдача 405й формы за июль',
    '22.09.2025':'сдача 405й формы за август',
    '22.10.2025':'сдача 405й формы за сетябрь',
    '25.11.2025':'сдача 405й формы за октябрь',
    '22.12.2025':'сдача 405й формы за ноябрь'
}

ocenka_PB = {
    '06.06.2025':'оценка платежного баланса',
    '07.07.2025':'оценка платежного баланса',
    '07.08.2025':'оценка платежного баланса',
    '05.09.2025':'оценка платежного баланса',
    '07.10.2025':'оценка платежного баланса',
    '10.11.2025':'оценка платежного баланса',
    '05.12.2025':'оценка платежного баланса'
}

MIP = {
    '10.06.2025':'Расчет МИП',
    '10.09.2025':'Расчет МИП',
    '10.12.2025':'Расчет МИП'
}
def send_reminder(event_name, days_left):
    """Отправка напоминания в Telegram"""
    emoji = '⚠️' if days_left > 3 else '🔔'
    message = f"{emoji} Напоминание: {event_name} через {days_left} {get_day_word(days_left)}!"
    bot.send_message(CHAT_ID, message)

def get_day_word(days):
    """Склонение слова 'день'"""
    if days % 10 == 1 and days % 100 != 11:
        return 'день'
    elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
        return 'дня'
    return 'дней'

def check_upcoming_holidays():
    """Проверка предстоящих праздников"""
    today = datetime.now().date()
    
    for date_str, event_name in f405.items():
        event_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        days_until_event = (event_date - today).days
        
        # Отправляем напоминания
        if days_until_event == 14:
            send_reminder(event_name, 14)
        elif days_until_event == 7:
            send_reminder(event_name, 7)
        elif days_until_event == 3:
            send_reminder(event_name, 3)
        elif days_until_event == 1:
            send_reminder(event_name, 1)

    for date_str, event_name in ocenka_PB.items():
        event_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        days_until_event = (event_date - today).days
        
        # Отправляем напоминания
        if days_until_event == 14:
            send_reminder(event_name, 14)
        elif days_until_event == 7:
            send_reminder(event_name, 7)
        elif days_until_event == 3:
            send_reminder(event_name, 3)
        elif days_until_event == 1:
            send_reminder(event_name, 1)

    for date_str, event_name in MIP.items():
        event_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        days_until_event = (event_date - today).days
        
        # Отправляем напоминания
        if days_until_event == 14:
            send_reminder(event_name, 14)
        elif days_until_event == 7:
            send_reminder(event_name, 7)
        elif days_until_event == 3:
            send_reminder(event_name, 3)
        elif days_until_event == 1:
            send_reminder(event_name, 1)

def schedule_checker():
    """Запуск ежедневной проверки в фоне"""
    while True:
        schedule.run_pending()
        time.sleep(1)
from telebot import apihelper
# Настройка расписания
schedule.every().day.at("09:00").do(check_upcoming_holidays)  # Проверка каждый день в 9:00

# Запуск планировщика в отдельном потоке
thread = threading.Thread(target=schedule_checker)
thread.daemon = True
thread.start()

# Команды для бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я буду напоминать о праздниках за 2 недели, неделю, 3 дня и 1 день.")


@bot.message_handler(commands=['today'])
def send_today_events(message):
    today = datetime.now().date()
    merged_events = {**f405, **ocenka_PB, **MIP}  # Объединяем словари
    
    found_events = False
    
    for date_str, name in merged_events.items():  # Используем .items() для словаря
        # Предполагаем, что ключи в словаре - строки в формате 'YYYY-MM-DD'
        event_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        
        if event_date == today:
            bot.send_message(message.chat.id, name)
            found_events = True
    
    if not found_events:
        bot.send_message(message.chat.id, "На сегодня событий нет")
    

@bot.message_handler(commands=['events'])
def send_holidays_list(message):
    """Отправка списка всех праздников"""
    response = "📅 Важные даты в 2025 году:\n\n"
    merged_events = {**f405, **ocenka_PB, **MIP}
    for date, name in sorted(merged_events.items(), 
                           key=lambda x: datetime.strptime(x[0], '%d.%m.%Y')):
        response += f"{date}: {name}\n"
    bot.send_message(message.chat.id, response)

# Удаляем вебхук перед запуском polling
apihelper.delete_webhook(bot.token)

# Теперь можно запускать polling
bot.polling(none_stop=True)