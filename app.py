from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import templates, statparser, config, time, threading, db


app = Flask(__name__)
app.statparser = statparser.NginxRtmpStatParser(config.site)
def update():
    while True:
        try:
            app.statparser.update_stat()
        except:
            pass
        finally:
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
    return jsonify(**templates.render_application(app.statparser.get_stat().application(app_name=app_name)))

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

@app.route('/auth_publish')
def auth_publish():
    username = request.args.get('username', 'anonymous')
    token = request.args.get('token', '')
    app_name = request.args.get('app', '')
    if app_name == '':
        return '', 400
    stream_name = request.args.get('name', '')
    if stream_name == '':
        return '', 400

    if db.token.auth_token(username, token, app_name, stream_name):
        return '', 200
    else:
        return 'auth failed', 400

if __name__=="__main__":
    app.run(debug=True)