import sys


def signal_handler(sig, frame):
    print('Bot stoped')
    sys.exit(0)
