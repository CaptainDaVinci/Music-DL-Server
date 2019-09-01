import os
import logging


base_dir = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(
	filename='music-dl.log',
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S')


class music_dl_log(object):
    def debug(self, msg):
        if 'ETA' not in msg:
            logging.debug(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)


class Config(object):
    SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz'
    STORAGE_DIR = 'media'
    STORAGE_DIR_PATH = os.path.join(base_dir, STORAGE_DIR, '%(id)s.%(ext)s')

    MP3_OPTS = {
        'no_warnings': True,
        'quiet': True,
        'outtmpl': STORAGE_DIR_PATH,
        'format': 'bestaudio/best',
        'logger': music_dl_log(),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    MP4_OPTS = {
        'no_warnings': True,
        'quiet': True,
        'outtmpl': STORAGE_DIR_PATH,
        'format': 'best',
        'logger': music_dl_log()
    }
