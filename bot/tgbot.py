import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
bot = telebot.TeleBot("7295152486:AAEZm0KAOSiIG8SZrEWzwCjzgcr9yLa6va4")
GROUP_CHAT_ID = '@f_registrar'  

bot.remove_webhook()

students = {}
message_ids = {}
def is_valid_phone_number(phone_number):
    pattern = re.compile(r"^\+2519\d{8}$|^09\d{8}$|^07\d{8}$")
    return pattern.match(phone_number) is not None
def is_valid_integer(value):
    return value.isdigit()
def is_valid_sex(value):
    return value.lower() in ['male', 'female', 'ወንድ', 'ሴት', 'ወ', 'ሴ', 'm', 'f', 'M', 'F']
def is_valid_string(value):
    return isinstance(value, str) and re.match(r"^[\u0041-\u005A\u0061-\u007A\u0020\u1200-\u137F\u200C\u200D]+$", value) is not None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ይህ የፍኖተ ሕይወት ሰንብት ት/ቤት መመዝገቢያ bot ነው! እባኮትን የተመዝጋቢውን ሙሉ ስም እስከ ሃያት ይጻፉ:")

@bot.message_handler(func=lambda message: True)
def collect_student_info(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in students:
        students[chat_id] = {}

    if 'name' not in students[chat_id]:
        if is_valid_string(text):
            students[chat_id]['name'] = text
            bot.reply_to(message, "እባኮትን ስልክ ቁጥር ያስገቡ:")
        else:
            bot.reply_to(message, "ስም ትክክለኛ እንዲሆን እባኮትን እንደገና ይጻፉ፡፡")
    elif 'phone_number' not in students[chat_id]:
        if is_valid_phone_number(text):
            students[chat_id]['phone_number'] = text
            bot.reply_to(message, "እባኮትን የሚኖሩበትን ክፍለ ከተማውን ያስገቡ:")
        else:
            bot.reply_to(message, "ትክክል ያልሆነ ስልክ ቁጥር አስገብተዋል፤ እባክዎን ትክክለኛውን ስልክ ያስገቡ፡፡")
    elif 'kifle_ketema' not in students[chat_id]:
        if is_valid_string(text):
            students[chat_id]['kifle_ketema'] = text
            bot.reply_to(message, "እባኮትን ወረዳውን ያስገቡ:")
        else:
            bot.reply_to(message, "እባኮትን ትክክለኛ ክፍለ ከተማ ያስገቡ፡፡")
    elif 'woreda' not in students[chat_id]:
        if is_valid_integer(text):
            students[chat_id]['woreda'] = int(text)
            bot.reply_to(message, "እባኮትን ቀበሌውን ያስገቡ:")
        else:
            bot.reply_to(message, "ወረዳው ቁጥር መሆን አለበት፤ እባኮትን ትክክለኛ ወረዳ ያስገቡ፡፡")
    elif 'kebele' not in students[chat_id]:
        if is_valid_integer(text):
            students[chat_id]['kebele'] = int(text)
            bot.reply_to(message, "እባኮትን እድሜውን ያስገቡ:")
        else:
            bot.reply_to(message, "ቀበሌው ቁጥር መሆን አለበት፤ እባኮትን ትክክለኛ ቀበሌ ያስገቡ፡፡")
    elif 'age' not in students[chat_id]:
        if is_valid_integer(text):
            students[chat_id]['age'] = int(text)
            bot.reply_to(message, "እባኮትን ፆታውን ያስገቡ (male/female):")
        else:
            bot.reply_to(message, "እድሜው ቁጥር መሆን አለበት፤ እባኮትን ትክክለኛ እድሜ ያስገቡ፡፡")
    elif 'sex' not in students[chat_id]:
        if is_valid_sex(text):
            students[chat_id]['sex'] = text.lower()
            if chat_id in message_ids:
                bot.delete_message(GROUP_CHAT_ID, message_ids[chat_id])

            name = students[chat_id]['name']
            phone_number = students[chat_id]['phone_number']
            kifle_ketema = students[chat_id]['kifle_ketema']
            woreda = students[chat_id]['woreda']
            kebele = students[chat_id]['kebele']
            age = students[chat_id]['age']
            sex = students[chat_id]['sex']
            sent_message = bot.send_message(GROUP_CHAT_ID, f"New Student Registered:\nስም: {name}\nስልክ ቁጥር: {phone_number}\nክፍለ ከተማ: {kifle_ketema}\nወረዳ: {woreda}\nቀበሌ: {kebele}\nእድሜ: {age}\nፆታ: {sex}")
            
            message_ids[chat_id] = sent_message.message_id
            bot.reply_to(message, f"የተቀመጠው መረጃ:\nስም: {name}\nስልክ ቁጥር: {phone_number}\nክፍለ ከተማ: {kifle_ketema}\nወረዳ: {woreda}\nቀበሌ: {kebele}\nእድሜ: {age}\nፆታ: {sex}")
        
            markup = InlineKeyboardMarkup()
            edit_button = InlineKeyboardButton("Edit", callback_data="edit")
            register_another_button = InlineKeyboardButton("Register Another", callback_data="register_another")
            markup.add(edit_button, register_another_button)
            bot.send_message(chat_id,"ስለተመዝገቡ ከልብ እናመሰግናለን! ")
            bot.send_message(chat_id,"መረጃዎትን ማስተካከል ይፈልጋሉ ወይም ሌላ ሰው ማስመዝገብ?", reply_markup=markup)
            students[chat_id]['confirming'] = True
        else:
            bot.reply_to(message, "ፆታው male ወይም female መሆን አለበት፤ እባኮትን ትክክለኛ ፆታ ያስገቡ፡፡")
@bot.callback_query_handler(func=lambda call: call.data == "edit")
def edit_student_info(call):
    chat_id = call.message.chat.id
    if chat_id in students:
        students.pop(chat_id) 
        bot.send_message(chat_id, "እባኮትን የተመዝጋቢውን ስም ይጻፉ እንደገና መመዝገብ ይጀምሩ፡፡")

@bot.callback_query_handler(func=lambda call: call.data == "register_another")
def register_another_student(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "እባኮትን የሌላ ተመዝጋቢ ስም ይጻፉ:")
    students[chat_id] = {} 
bot.polling()
