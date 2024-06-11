from connection.connectionconfig import TCPConnectionConfig
from connection.message import Message
from connection.c_socket import ClientSocket

if __name__ == "__main__":
    config = TCPConnectionConfig("localhost", 11115)
    print("Client started")
    client_socket = ClientSocket(config)
    client_socket.open()

    print("Client ready")

    while True:
        message = input("Write something to reverse (q to quit): ")
        message = message.strip()

        if message == "q":
            break
        else:

            client_socket.send_message(Message("Request", message))
            response = client_socket.receive_message()
            print(response.title)
            print(response.content)
