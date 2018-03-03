import subprocess


def shell_cmd_run(bot, update):
    cmd = parse_command(update.message.text)
    result = run_cmd(cmd)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)


def parse_command(message):
    msg = message.split("/shellcmd ")[1].split()
    return msg


def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    if result.stdout:
        return result.stdout.decode('utf-8')
    else:
        return result
