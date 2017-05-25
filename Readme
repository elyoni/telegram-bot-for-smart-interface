# Telegram Bot For Smart Interface with MQTT Support

The purpose of this project is to use Telegram as a GUI for a various Smart
House projects I'm building (this gives me a more secure way to control them
remotely).

## Getting Started

First you need to create a Telegram bot.

You can do that by adding the "Bot Father" bot to your Telegram user list (click
on https://telegram.me/botfather).

The process is very simple, see the tutorial at
https://core.telegram.org/bots#6-botfather (once you're done you'll have a
telegram bot token that you can use for the app).

Next you need to install the following libraries using pip:

```
pip install python-telegram-bot
pip install lxml
pip install paho-mqtt
```

The last step is optional, if you don't use MQTT you can skip it.

You need to to run a MQTT Server (Broker). I am using mosquitto as my broker
since it runs on the RPi (I used this [tutorial][1] to install it).

[1]: https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04)

## Development

I'm working on a few ideas to improve the bot:

1. Access a router via SSH (using Tomato firmware). The idea is to inform you
   on disconnections / reconnections and unknown network devices.
2. Use OpenCV to take a picture and send it to my Telegram account.
3. Israel Train Schedule Bot - You can ask the bot for train schedules and get
   that information fast and with a minimal use of the mobile data plan.
