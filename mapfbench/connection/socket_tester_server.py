from connection.c_socket import ServerSocket
from connection.connectionconfig import TCPConnectionConfig
from connection.message import Message

if __name__ == '__main__':
    print('Server started', flush=True)

    server_socket = ServerSocket(TCPConnectionConfig("localhost", 11115))
    server_socket.open()

    while True:
        try:
            request = server_socket.receive_message()
            response = Message("Reversed message", str(request.content)[::-1])
            server_socket.send_message(response)
        except KeyboardInterrupt:
            print("Ctrl+C pressed")
            server_socket.close()
            break

    print("Finished")

