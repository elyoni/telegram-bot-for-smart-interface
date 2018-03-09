import subprocess
import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler

permission_file_path = os.path.abspath(__file__).rsplit(os.sep, 2)[0] + os.sep + "permission.json"
print(permission_file_path)

class ShellCmd:
    def __init__(self):
        self.readPermissionFile()
        self.SSH_MENU, self.CHOCICE= range(2)
        self.keyboard = { "main_menu": [
                            [InlineKeyboardButton(u"ssh -R", callback_data='ssh -R'),
                            InlineKeyboardButton(u"Exit", callback_data='Exit')]
                            ],
                          "ssh_menu": [
                            [InlineKeyboardButton(u"Kill ssh", callback_data='kssh')]
                            ]
                        }


    def readPermissionFile(self):
        # Read the file permission.ini and read the users number and permission
        with open(permission_file_path, 'r') as file:
            self.permission_data = json.load(file)

    def build_conversation_handler(self):
        return ConversationHandler(
                entry_points=[CommandHandler('ssh', self.start)],
                states={
                    self.CHOCICE: [CallbackQueryHandler(self.choice)],
                    self.SSH_MENU: [CallbackQueryHandler(self.ssh_menu)]
                },
                fallbacks=[CommandHandler('ssh', self.start)]
            )
        


    def start(self, bot, update):
        reply_markup = InlineKeyboardMarkup(self.keyboard["main_menu"])
        update.message.reply_text(
            u"Start handler, Press next",
            reply_markup=reply_markup
        )
        return self.CHOCICE 

    def choice(self, bot, update):
        return_value = self.CHOCICE
        keyboard = []
        text = None

        query = update.callback_query
        if query.data == "ssh -R":
            print("running ssh")
            a = self.run_cmd(query.message.chat_id, "ssh -R 19998:localhost:22 yoni@yoni.dns")
            print(a)
            text = "Running \"ssh -R 19998:localhost:22 yoni@-----.dns\"" + "\n\n" + a
            keyboard = self.keyboard["ssh_menu"]
            return_value = self.SSH_MENU
        elif query.data == "Exit":
            keyboard = []
            text = "Done"

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              reply_markup=reply_markup,
                              message_id=query.message.message_id)

        return return_value
    
    def ssh_menu(self, bot, update):
        query = update.callback_query
        keyboard = self.keyboard["main_menu"]
        text = None
        if query.data == "kssh":
            print("run killall ssh")
            text = "The ssh is close"
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              reply_markup=reply_markup,
                              message_id=query.message.message_id)
        return self.CHOCICE

    def run_cmd(self, chat_id, cmd):
        if self.permission_data["admin"] == chat_id:
            try:
                result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                if result.stdout:
                    return result.decode('utf-8')
                else:
                    return result
            except Exception as e:
                return str(e)
        else:
            print("Unauthorized account")
            return None


    '''

    def execute(self, update):
        if self.permission_data["admin"] == update.message.chat_id:
            print("shell_cmd", update.message.text)
            cmd = parse_command(update.message.text)
            result = run_cmd(cmd)
            print("result:", result)
            bot.sendMessage(chat_id=update.message.chat_id, text=result)
        else:
            print("Unauthorized account")

    def parse_command(self, message):
        msg = message.split("/shellcmd ")[1].split()
        return msg

    '''
