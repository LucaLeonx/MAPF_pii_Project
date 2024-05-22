from connection.message import Message
from connection.serversocket import ServerSocket
from connection.tcpconnectionconfig import TCPConnectionConfig

if __name__ == '__main__':
    print('Server started', flush=True)

    server_socket = ServerSocket(TCPConnectionConfig("localhost", 11115))
    server_socket.start()

    while True:
        request = server_socket.receive_message()
        response = Message("Reversed message", str(request.get_content())[::-1])
        server_socket.send_message(response)