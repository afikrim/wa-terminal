import argparse

from login import login
from message import message


def main():
    parser = argparse.ArgumentParser("sendwa")
    parser.add_argument("phone", help="Your phone number")

    default_group = parser.add_argument_group("required arguments")
    default_group.add_argument(
        "-c",
        "--command",
        dest="command",
        help="A command you want to run",
        choices=["login", "message"],
        required=True,
    )

    login_group = parser.add_argument_group("login optional arguments")
    login_group.add_argument(
        "-f",
        "--force",
        dest="force",
        help="If you want to force logged in",
        action="store_true",
    )

    send_message_group = parser.add_argument_group("message required arguments")
    send_message_group.add_argument(
        "-d",
        "--destination",
        dest="destination",
        help="Phone number you want to send a message to",
    )
    send_message_group.add_argument(
        "-t", "--text", dest="text", help="A message that you want to send"
    )

    args = parser.parse_args()

    command = args.command
    phone = args.phone

    [program_message, error] = [None, None]
    if command == "login":
        force = args.force

        [program_message, error] = login(phone, force)
    elif command == "message":
        destination = args.destination
        text = args.text

        [program_message, error] = message(phone, destination, text)

    print(program_message)
    if error:
        raise error


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\rProgram stop running!")
