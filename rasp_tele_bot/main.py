from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import picamera
import threading
import RPi.GPIO as GPIO

# GPIO INITIALIZED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
sensor = 20
led = 21
buzzer = 16

# GPIO SETUP
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(led, GPIO.LOW)
GPIO.output(buzzer, GPIO.LOW)
time.sleep(2)
print("Detecting Motion")

# Given a token for Telegram Chatting Bot
TOKEN = '751327134:AAER637xGXY8GtlvZtPeeizNA4T--oWjd9g'
bot=telegram.Bot(token="751327134:AAER637xGXY8GtlvZtPeeizNA4T--oWjd9g")

# This function is always running until this program is stoped.
# This function is running by thread.
# If a sensor detected a person, take and send photo to main user.
def readData():
    # this code is for Timer
    timeCount = 0
    timerBool = False

    # Below this Code is detecting Perosn using sensor.
    while True:
        if GPIO.input(sensor):
                print("Motion Detected")
                timerBool = True
                if timeCount >= 30 or timeCount == 0:
                        print('Call Function')
                        global set_id
                        bot.send_message(chat_id=set_id, text="사람을 감지했습니다!\n\n")
                        with picamera.PiCamera() as camera:
                                camera.start_preview()
                                time.sleep(3)
                                camera.capture('image.jpg')
                                camera.stop_preview()
                        bot.send_message(chat_id=set_id, text="사진을 보내는 중입니다! 잠시만 기다려주세요!\n\n")
                        bot.send_photo(chat_id = set_id, photo=open('image.jpg', 'rb'))
                        timeCount = 0
        else:
                print("finding...")
        # This code exists to send pictures once every 30 seconds.
        if timerBool:
                timeCount += 2
        time.sleep(2)    

    
def check_id(bot, update):
    try:
        id = update.message.chat.id
        print('Chat ID', id)
        return id
    except:
        id = update.channel_post.chat.id
        return id

def check_nickname(bot, update):
    try:
        nickname = update.message.from_user.first_name
        print('Chat NickName', nickname)
        return nickname
    except:
        nickname = update.channel_post.from_user.first_name
        return nickname


# There functions exist to control led.
def on_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    bot.send_message(chat_id=id, text="안녕하십니까, " + nickname + "님, led의 전원을 켜드리겠습니다!\n\n")
    GPIO.output(led, GPIO.HIGH)
    GPIO.output(buzzer, GPIO.HIGH)

def off_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    bot.send_message(chat_id=id, text="안녕하십니까, " + nickname + "님, led의 전원을 꺼드리겠습니다!\n\n")
    GPIO.output(led, GPIO.LOW)
    GPIO.output(buzzer, GPIO.LOW)

# This code exists to set the alarm and sets the main user to receive pictures from the readData() function.
def alarm_set(bot, update):
    global set_id
    set_id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    bot.send_message(chat_id=set_id, text="이제" + nickname + "님으로 알람이 설정 되었습니다.\n\n")
    t = threading.Thread(target=readData, args=())
    t.start()

updater = Updater(TOKEN)

#LED ON / OFF COMMAND HANDLER
updater.dispatcher.add_handler(CommandHandler('on', on_command))
updater.dispatcher.add_handler(CommandHandler('off', off_command))

# ALARM SET COMMAND HANDLER
updater.dispatcher.add_handler(CommandHandler('set', alarm_set))

updater.start_polling(timeout=3, clean=True)

# Run Function: readData() using thread
updater.idle()
