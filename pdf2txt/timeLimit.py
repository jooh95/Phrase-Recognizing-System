import signal


def signal_handler(signum, frame):
    raise Exception("Timed out!")


def time_limit(sec):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(sec)   # Ten seconds


'''
try:
    time_limit(15)
except
'''