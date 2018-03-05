import subprocess


def shell_cmd(bot, update, permission_data):
    if permission_data["admin"] == update.message.chat_id:
        cmd = parse_command(update.message.text)
        result = run_cmd(cmd)
        bot.sendMessage(chat_id=update.message.chat_id, text=result)
    else:
        print("Unauthorized account")


def parse_command(message):
    msg = message.split("/shellcmd ")[1].split()
    return msg


def run_cmd(cmd):
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    if result.stdout:
        return result.stdout.decode('utf-8')
    else:
        return result
