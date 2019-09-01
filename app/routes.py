from flask import abort, request, jsonify
from app import app
import youtube_dl


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

    ytdl_opts = dict()
    if encoding == 'mp3':
        ytdl_opts = app.config['MP3_OPTS']
        if quality == 'low':
            ytdl_opts['postprocessors'][0]['preferredquality'] = '124'
    else:
        ytdl_opts = app.config['MP4_OPTS']
        if quality == 'low':
            ytdl_opts['format'] = 'worst' 

    try:
        app.logger.info('Options {}'.format(ytdl_opts))
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
             ytdl.download([yt_id])
        resp = {
            'download_link': '{}{}/{}.{}'.format(request.url_root, app.config['STORAGE_DIR'], yt_id, encoding)
        }
        return jsonify(resp)
    except Exception as e:
        app.logger.critical(str(e))
        abort(500)
