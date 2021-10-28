# WA Terminal

WA Terminal is a CLI application that allows us to login and send message with WhatsApp with a single command.

```plaintext
usage: sendwa [-h] -c {login,message} [-f] [-d DESTINATION] [-t TEXT] phone

positional arguments:
  phone                 Your phone number

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -c {login,message}, --command {login,message}
                        A command you want to run

login optional arguments:
  -f, --force           If you want to force logged in

message required arguments:
  -d DESTINATION, --destination DESTINATION
                        Phone number you want to send a message to
  -t TEXT, --text TEXT  A message that you want to send
```

### NOTE

- Before you run the app, make sure you have geckodriver and firefox in your path, if you don't have them in your path variable, then export it before running the program.
- When you run login command, this app will take a screenshot of the QR Code and store it to qr_codes folder. So you guys can scan it to login into your new session. After the first login there is no need to login again to send message.
- When you run into issue like timeout or something when sending message, please try to login again with options `-f` to forcely generate new session.
- This packages can be install and import in python, the example use of this package in [Telegram Bot](http://t.me/SendWaBot)
