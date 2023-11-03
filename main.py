from server import create_app
# from flask_socketio import SocketIO


if __name__ == '__main__':
    server_app = create_app()

    # socketio = SocketIO(server_app)
    # socketio.run(server_app, debug=True)

    server_app.run(debug=True)
