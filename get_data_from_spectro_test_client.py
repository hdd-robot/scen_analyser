#!/usr/bin/python3
import base64
import socket
import json

IP = socket.gethostbyname(socket.gethostname())

PORT = 5566
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 100000

def main():
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    client.connect(ADDR)

    """ Sending the filename to the server. """
    client.send("GET_DATA".encode(FORMAT))


    msg = client.recv(SIZE).decode(FORMAT)
    recv_data = msg
    while (len(msg)):
        msg = client.recv(SIZE).decode(FORMAT)
        recv_data = recv_data + msg

    print(f"[SERVER]: {str(len(recv_data))} chars")
    """ Sending the file data to the server. """

    json_obj = json.loads(recv_data)
    image_specter = json.dumps(json_obj['image_specter'])

    with open("specter.png", "wb") as fh:
        img = base64.b64decode(image_specter)
        fh.write(img)

    image_graphe = json.dumps(json_obj['image_graphe'])

    with open("graph.png", "wb") as fh:
        img = base64.b64decode(image_graphe)
        fh.write(img)

    data_array = json.dumps(json_obj['data_array'])
    print(data_array)
    client.close()

if __name__ == "__main__":
    main()