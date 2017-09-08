import socket 
import time
import thread 

BUFSIZE = 4096
PORT = 1337 
users = {}
connections = []

def accept_conns(soc):
    while True:
        connection, addr = soc.accept()

        # `setblocking(0)` allows to set the connection to not halt if there's no an input from the user . As a side effect, every connection.recv call needs to be in a try-catch block so that the server doesn't crash because of lack of input.
        connection.setblocking(0)

        connections.append({
            "connection": connection,
            "username": None
            })
        connection.send("server: Input username.\n")

def main():
    try:
        # Set the socket to be IPv4, TCP respectively.
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        print "Socket successfully created"

    except socket.error as err:
        print "Socket creation failed with error s." %(err)

    soc.bind(('', PORT))        
    print "Socket binded to port %s." %(PORT)

    soc.listen(5)
    print "Socket is listening."

    # Accepting connections runs on a concurrent thread so that we don't have to wait to accept a new connection to run basic server functions.
    thread.start_new_thread(accept_conns, (soc,))

    while True:
        for blob in connections:
            connection = blob["connection"]
            try:
                if not connections[-1]["username"]:
                        user = connection.recv(BUFSIZE)
                        user = user.strip()
                        connections[-1]["username"] = user
                        connection.send("server: Your username is " + user + ".\n")
               
                mess =  connection.recv(BUFSIZE)
                for send_blob in connections:
                   send_connect = send_blob["connection"]
                   if send_connect != connection:
                       send_mess = blob["username"] + " : " + mess
                       send_connect.send(send_mess)
               
            except socket.error:
                "server: Message not received."
                
if __name__ == "__main__":
    main()

