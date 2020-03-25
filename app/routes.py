from flask import abort, request, jsonify
from app import app
from os import path
import youtube_dl
import eyed3


def add_cover_art(yt_id):
    file_path = path.join(app.config['STORAGE_DIR'], yt_id + '.mp3')
    thumbnail_path = path.join(app.config['STORAGE_DIR'], yt_id + '.jpg')
    
    app.logger.info('Setting cover art file path: {}, thumbnail: {}'.format(file_path, thumbnail_path))

    eyed3.log.setLevel('ERROR')
    mFile = eyed3.load(file_path)
    thumbnail = open(thumbnail_path, 'rb').read()
    mFile.tag.images.set(eyed3.id3.frames.ImageFrame.FRONT_COVER, thumbnail, 'image/jpeg', u'front cover')
    mFile.tag.images.set(eyed3.id3.frames.ImageFrame.BACK_COVER, thumbnail, 'image/jpeg', u'back cover')
    mFile.tag.save() 


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
