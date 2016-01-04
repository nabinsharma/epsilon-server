import os

from flask import flash, redirect, render_template, \
    request, send_from_directory, url_for
from werkzeug import secure_filename

from dejavu import app, config, djv, log_file

@app.route("/")
def home():
    app.logger.info("home: replying with song list")
    songs = djv.db.get_songs()
    return render_template('list.html', songs=songs)

@app.route("/recognize", methods=['GET', 'POST'])
def recognize():
    if request.json:
        content = request.json
        app.logger.info("recognize: received recognize request from a client")
        app.logger.info("recognize: %s, %s" % (content.get("length"), content.get("channels")))
    else:
        app.logger.info("recognize: no json data in request")
    return "Recognize not yet implemented!"

@app.route("/log", methods=['GET'])
def log():
    try:
        with open(log_file, 'r') as f:
	    log_lines = reversed(f.readlines())
        if not log_lines:
            log_lines = ["Log file is empty"]
        return render_template('log.html', log_lines=log_lines)
    except:
        return render_template('log.html', log_lines=["Can't read %s" % log_file])

@app.route("/webtest", methods=['GET', 'POST'])
def webtest():
    app.logger.info("webtest: received a web test request")
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename, config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            full_filename = os.path.join(config['UPLOAD_FOLDER'], filename)
            file.save(full_filename)
            from dejavu.recognize import FileRecognizer
            song = djv.recognize(FileRecognizer, full_filename)
            flash('Recognized [%s]' % song['song_name'])
            app.logger.info('webtest: recognized [%s]' % song['song_name'])
            return redirect(url_for('home', song=song['song_name']))
    return render_template('webtest.html')


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_extensions
