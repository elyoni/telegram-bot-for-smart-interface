import json
import os
# For the Telegram lib
from telegram.ext import Updater, ConversationHandler
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.inlinekeyboardbutton import InlineKeyboardButton
import telegram
# MQTT
from mqttClass import mqttClass
from modules.shell_cmd import ShellCmd

config_file_path = os.path.abspath(__file__).rsplit(os.sep, 1)[0] + os.sep + "config.json"
permission_file_path = os.path.abspath(__file__).rsplit(os.sep, 1)[0] + os.sep + "permission.json"

with open(config_file_path, 'r') as file:
    config = json.load(file)

Telegram_PORT = config["telegram_port"]
Telegram_TOKEN = config["telegram_token"]
MQTT_Server_IP = config["mqtt_server"]

class TelegramServer:
    def __init__(self):
        self.shell_cmd = ShellCmd()
        self.readPermissionFile()
        self.telegram_server_configure()  # Connect To Telegram Server
        # self.mqttConnection = mqttClass(MQTT_Server_IP)
        # self.mqttConnection.mqttSubscribeHandler = self.mqttSubscribeHandler
        # self.mqttConnection.startLoopMQTT()
    def mqttSubscribeHandler(self):
        self.mqttConnection.subscribe("downloadFiles", self.downloadFiles)
        self.mqttConnection.subscribe("sendRawToTelegram", self.sendRawToTelegram)


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

        # # Functions Configure
        # Headel the '/' commandes to function
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('whatmyid', self.whatMyID))
        self.dispatcher.add_handler(self.shell_cmd.build_conversation_handler())

        # Handel regular message
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))

        # Handel button querys
        #self.dispatcher.add_handler(CallbackQueryHandler(self.button))

        updater.start_polling()  # Need to change webhook

    # ------ The Commands function ---------
    def start(self, bot, update):
        print("start")
        bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        for i in range(len(self.permission_data["users"])):
            if self.permission_data["users"][i] == update.message.from_user.id:
                print("Everything Is ok i know the user")
                update.message.reply_text('HI How Are You')
                break
        else:
            # Make sure to write the right ID for the admin user
            print(self.admin_user_data[2])
            bot.send_message(chat_id=self.admin_user_data[2],
                             text="An unauthorized account send a /start command \
                             to the bot.\n The accound data is:\n" +
                             str(update.message.from_user))
            print("An unauthorized account send a /start command to the bot.\n \
                  The accound data is" + str(update.message.from_user))

    def whatMyID(self, bot, update):
        update.message.reply_text("Your ID is: " + str(update.message.chat_id))

    def shell_cmd_run(self, bot, update):
        shell_cmd(bot, update, self.permission_data)
    
    def echo(self, bot, update):
        # This function is for debug, To see if the code is working
        print("echo function:", update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    # ------ The mqtt function ---------

    def downloadFiles(self, msg):
        # When the program finish download it run a script that connect
        # to the MQTT server and send me a message
        # the message is in the form of "The Name Of the File;
        # The Path Of the file;Label name"
        # I am using the label to know to who to send the file
        msgList = msg.split(';')
        msgToSend = ('New Download:  ' + msgList[1] + ', Path: ' +
                     msgList[2] + ', Label: ' + msgList[0])
        for user in msgList[0].split('@'):
            print(user)
            try:
                userID = filter(lambda x: user in x, self.permissionsList)[0][2]
                self.bot.sendMessage(chat_id=userID, text=msgToSend,
                                     reply_markup=telegram.ReplyKeyboardRemove())
            except:
                unknownUser = "The User " + user + " Is unknown, Sending message to admin"
                print(unknownUser)
                msgToSendTemp = unknownUser + "\n" + msgToSend
                self.bot.sendMessage(chat_id=self.admin_user_data[2],
                                     text=msgToSendTemp,
                                     reply_markup=telegram.ReplyKeyboardRemove())

    def sendRawToTelegram(self, msg):
        # This function is more for debug,
        # when publish a message it will be send to the admin
        self.bot.send_message(chat_id=self.admin_user_data[2], text=msg)


telegramserver = TelegramServer()
