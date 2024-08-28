from app import app, socketio

if __name__ == '__main__':
    # socketio.run(app=app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    socketio.run(app=app, host='0.0.0.0', port=5001, debug=True)
