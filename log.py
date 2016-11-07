import logging

app_log = logging.getLogger('app')
app_log.setLevel(logging.DEBUG)

f = logging.Formatter(
    '[L:%(lineno)d]# %(levelname)-4s [%(asctime)s]  %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
app_log.addHandler(ch)