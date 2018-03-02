#For the Telegram lib
from telegram.ext import Updater
from telegram.ext import CommandHandler,CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.inlinekeyboardbutton import InlineKeyboardButton
import telegram


permission_file_path = "permission.json"

Telegram_PORT   =   8443
Telegram_TOKEN  =   'EnterYourTOEKN HERE'
#MQTT_Server_IP	=		'192.168.1.12' # Uncomment if the borker is not on the local computer

from lxml import html

# MQTT
from mqttClass import mqttClass

# 


class user:
    def __init__(self):
        self.userName
        self.permission_data
        self.telegramID

class TelegramServer:
    def mqttSubscribeHandler(self):
        self.mqttConnection.subscribe("downloadFiles",self.downloadFiles)
        self.mqttConnection.subscribe("sendRawToTelegram",self.sendRawToTelegram)

    def __init__(self):
        self.readPermissionFile()
        self.telegram_server_configure() #Connect To Telegram Server
        self.mqttConnection = mqttClass(MQTT_Server_IP)
        self.mqttConnection.mqttSubscribeHandler = self.mqttSubscribeHandler
        self.mqttConnection.startLoopMQTT()

    def readPermissionFile(self):
        # Read the file permission.ini and read the users number and permission
        with open(permission_file_path, 'r') as file:
            self.permission_data = json.load(file)

    def telegram_server_configure(self):
        # General Configure
        self.PORT = Telegram_PORT
        self.TOKEN = Telegram_TOKEN
        updater = Updater(token=self.TOKEN)
        self.bot = telegram.Bot(self.TOKEN)
        self.dispatcher = updater.dispatcher

        ##Functions Configure
        #Headel the '/' commandes to function
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('whatmyid', self.whatMyID))

        # Handel regular message
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))

        # Handel button querys
        self.dispatcher.add_handler(CallbackQueryHandler(self.button))        

        updater.start_polling() # Need to change webhook    
    # ------ The Commands function ---------
    def start(self,bot, update):
        update.message
        bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        for i in range(len(self.permission_data["users"])):
            if self.permission_data["users"][i] == update.message.from_user.id:
                print("Everything Is ok i know the user")
                update.message.reply_text('HI How Are You')
                break
        else:
            # Make sure to write the right ID for the admin user
            print(self.admin_user_data[2])
            bot.send_message(chat_id = self.admin_user_data[2], text = "An unauthorized account send a /start command to the bot.\n The accound data is:\n" + str(update.message.from_user))
            print("An unauthorized account send a /start command to the bot.\n The accound data is"    + str(update.message.from_user)) 

    def whatMyID(self,bot,update):
        update.message.reply_text("Your ID is: " + str(update.message.chat_id))

    def button(self,bot, update):
        query = update.callback_query
        print(query.message.text)

    def echo(self,bot,update):
        # This function is for debug, To see if the code is working
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    # ------ The mqtt function ---------

    def downloadFiles(self,msg):
        # When the program finish download it run a script that connect to the MQTT server and send me a message
        # the message is in the form of "The Name Of the File;The Path Of the file;Label name"
        # I am using the label to know to who to send the file
        msgList = msg.split(';')
        msgToSend = ('New Download:  ' + msgList[1] + ', Path: ' + msgList[2] + ', Label: ' + msgList[0])
        for user in msgList[0].split('@'):
            print(user)
            try:
                userID = filter(lambda x: user in x, self.permissionsList)[0][2]
                self.bot.sendMessage(chat_id=userID,text=msgToSend,reply_markup=telegram.ReplyKeyboardRemove())
            except:
                unknownUser =  "The User " + user + " Is unknown, Sending message to admin"
                print(unknownUser)
                msgToSendTemp =  unknownUser + "\n" + msgToSend
                self.bot.sendMessage(chat_id=self.admin_user_data[2],text=msgToSendTemp,reply_markup=telegram.ReplyKeyboardRemove())
                
    def sendRawToTelegram(self,msg):
        # This function is more for debug, when publish a message it will be send to the admin
        self.bot.send_message(chat_id=self.admin_user_data[2], text=msg)

telegramserver = TelegramServer()
