from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import templates, statparser, config, time, threading


app = Flask(__name__)
app.statparser = statparser.NginxRtmpStatParser(config.site)
def update():
    while True:
        app.statparser.update_stat()
        time.sleep(config.update_interval)
t = threading.Thread(target=update)
t.start()


@app.route('/')
def index():
    # if 'username' not in session:
    #     return 'You are not logged in'
    return redirect(url_for('list_stream', app_name=config.app_name))

@app.route('/<app_name>/streams')
def list_stream(app_name):
    return jsonify(**templates.render_application(app.statparser.stat.application(app_name=app_name)))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)