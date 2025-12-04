class Language:
    SANTA = "santa"
    SANTA_SUCKS = "santa_sucks"

class MessageSanta:
    GROUP_CHAT_NOTICE = "Так-так, бачу це груповий чат. Можете написати /participants щоби отримати список тих хто вже зареєструвався."
    WELCOME = """\
Привіт, {}! Вітаю в Боті для Таємного... Якщо ви микита, перед початком виконайте команду /santa_sucks
/name <ВеселаПіпірка> - щоб змінити своє ім'я, якщо є бажання... Тільки щоби понятно було, ок?
/register - щоби зареєструватися в грі
"""

class MessageSantaSucks(MessageSanta):
    pass
