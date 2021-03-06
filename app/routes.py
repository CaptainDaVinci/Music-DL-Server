from flask import abort, request, jsonify
from app import app
from os import path
import youtube_dl
import eyed3
import requests
import json


def add_cover_art(yt_id):
    file_path = path.join(app.config['STORAGE_DIR'], yt_id + '.mp3')
    thumbnail_path = path.join(app.config['STORAGE_DIR'], yt_id + '.jpg')
    
    app.logger.info('Setting cover art file path: {}, thumbnail: {}'.format(file_path, thumbnail_path))

    eyed3.log.setLevel('ERROR')
    mFile = eyed3.load(file_path)
    try:
        thumbnail = open(thumbnail_path, 'rb').read()
        mFile.tag.images.set(eyed3.id3.frames.ImageFrame.FRONT_COVER, thumbnail, 'image/jpeg', u'front cover')
        mFile.tag.images.set(eyed3.id3.frames.ImageFrame.BACK_COVER, thumbnail, 'image/jpeg', u'back cover')
        mFile.tag.save() 
    except FileNotFoundError as e:
        app.logger.debug('File not found ' + thumbnail_path)


def download_file(yt_id, encoding, quality):
    ytdl_opts = dict()
    if encoding == 'mp3':
        ytdl_opts = app.config['MP3_OPTS']
        if quality == 'low':
            ytdl_opts['postprocessors'][0]['preferredquality'] = '124'
    else:
        ytdl_opts = app.config['MP4_OPTS']
        if quality == 'low':
            ytdl_opts['format'] = 'worst' 

    app.logger.info('Options {}'.format(ytdl_opts))
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
         ytdl.download([yt_id])

    if encoding == 'mp3':
        add_cover_art(yt_id)


@app.route('/')
def index():
    return '<h3>Music-dl</h3>'


@app.route('/download/', methods=['GET'])
def download():
    yt_id = request.args.get('id')
    encoding = request.args.get('format', 'mp3')
    quality = request.args.get('quality', 'high')

    app.logger.info('Request: {} {} {}'.format(yt_id, encoding, quality))

    if yt_id == None:
        abort(400)

    if encoding not in ['mp3', 'mp4']:
        abort(415)

    try:
        download_file(yt_id, encoding, quality)
        download_path = path.join(request.url_root, app.config['STORAGE_DIR'], yt_id + '.' + encoding)
        resp = {
            'download_link': '{}'.format(download_path) 
        }
        app.logger.info('download_link: {}'.format(download_path))
        return jsonify(resp)
    except Exception as e:
        app.logger.critical(str(e))
        abort(500) 


@app.route('/id', methods=['GET'])
def get_id():
    query = request.args.get('q')

    app.logger.info('Get ID for: {}'.format(query))

    yt_api_url = 'https://www.googleapis.com/youtube/v3/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/74.0'
    }
    payload = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 1,
        'key': app.config['YT_API_KEY']
    }
    
    try:
        resp = requests.get(yt_api_url, headers=headers, params=payload)
        if resp.status_code != 200:
            raise Exception('YouTube API returned with {} status code and body, \n{}'.format(
                                resp.status_code, 
                                json.dumps(resp.json(), indent=2, sort_keys=True)))
        data = resp.json()
        data_item = data.get('items')[0]
        resp = {
            'id': data_item['id']['videoId'],
            'title': data_item['snippet']['title'],
            'thumbnailUrl': data_item['snippet']['thumbnails']['default']['url']
        }
        return jsonify(resp)
    except Exception as e:
        app.logger.debug('API key: ' + os.environ.get('YT_API_KEY'))
        app.logger.debug('Requested URL: ' + resp.url)
        app.logger.critical(str(e))
        abort(500)

