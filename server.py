import socket
from time import sleep
import toml
from threading import Thread
import sys, os
import json

# Setup the config file
config = toml.load("db_config.toml")
host = socket.gethostname()

save_time = config["GENERAL"]["SAVE_TIME"]
save_file = config["GENERAL"]["SAVE_FILE"]


data = {"a":23, "b":34}
try:
    with open(save_file, "rb") as f:
        data = json.loads(f.read().decode().replace("'", '"'))
except Exception as e:
    with open(save_file, "wb") as f:
        f.write(str(data).encode('utf-8'))
        print("No save file found, created new one")


#load up the config file
if config["GENERAL"]["HOST"] != "default":
    host = config["GENERAL"]["HOST"]
port = config["GENERAL"]["PORT"]
threads = {}

#setup the socket
s = socket.socket()   

# The command line interface thread function
def cmd_interface() -> None:
    while True:
        cm = input(">")
        if cm == "FORCE CLOSE SERVER":
            os._exit(1);
        if cm == "LIST CONNECTIONS":
            print(threads)


# The function that is called when a new client connects
def on_new_client(clientsocket: object, addr: object) -> None:

    while True:
        msg = clientsocket.recv(1024)
        command = msg.decode().split(" ",2);
        match command[0]:
            case "END_CONNECTION":
                clientsocket.send("CONNECTION_ON_SERVER_ENDED".encode())
                threads.pop(str(addr))
                print("connection from", addr, "ended")
                return 1
            case "GET":
                clientsocket.send(str(data[command[1]]).encode())
            case "SET":
                data.update({command[1]:command[2]})
                clientsocket.send("SET".encode())
            case "DELETE":
                pass
            case "LIST":
                pass  
            case other:
                print("Unknown command from", addr, ":", command[0])
                clientsocket.send("RECIVED AN UNKNOWN COMMAND".encode())

        clientsocket.send("TEMP".encode())
        # after the command is executed, send a message to the client
        # clientsocket.send("RECIVED".encode()).
    clientsocket.close()


def save() -> None:
    while True:
        sleep(save_time)
        with open(save_file, "wb") as f:
            f.write(str(data).encode())


# the main function
def main() -> None:
    print('Server started!')
    print('Waiting for clients...')
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    # Start the command line interface thread
    cmd = Thread(target=cmd_interface, name="MASTER_COMMAND_LINE_DO_NOT_CLOSE")
    cmd.start()
    
    save_t = Thread(target=save, name="SAVE_THREAD")
    save_t.start()

    # Start the main loop for establishing new connections
    while True:
        c, addr = s.accept()     # Establish connection with client.
        temp = Thread(target=on_new_client, args=(c, addr), name=str(addr))
        temp.start()
        threads[str(addr)] = temp
        # Note it's (c, addr) not (addr) because second parameter is a tuple
        # that's how you pass arguments to functions when creating new threads using thread module.
    s.close()


if __name__ == '__main__':
    main()