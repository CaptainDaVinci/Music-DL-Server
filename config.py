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
    SECRET_KEY = os.environ.get('SECRET_KEY', 'abcdefghijklmnopqrstuvwxyz')
    STORAGE_DIR = 'media'
    STORAGE_DIR_PATH = os.path.join(base_dir, STORAGE_DIR, '%(id)s.%(ext)s')
    YT_API_KEY = os.environ.get('YT_API_KEY', 'no_api_key')
    

    MP3_OPTS = {
        'writethumbnail': True,
        'no_warnings': True,
        'quiet': True,
        'outtmpl': STORAGE_DIR_PATH,
        'format': 'bestaudio/best',
        'logger': music_dl_log(),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegMetadata',
        }],
    }

    MP4_OPTS = {
        'no_warnings': True,
        'quiet': True,
        'outtmpl': STORAGE_DIR_PATH,
        'format': 'best',
        'logger': music_dl_log()
    }
