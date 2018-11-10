import config
import app_vision

app = app_vision.create_app(config)
app.secret_key = config.SECRET_KEY

# Run app
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(host='127.0.0.1', port=8080, debug=True)

