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
        connection.setblocking(0)
        connections.append({
            "connection": connection,
            "username": None
            })
        connection.send("server: Input username.\n")

def main():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# tells us it's IPv4 and TCP <- abstraction, don't have to touch!
        print "Socket successfully created"

    except socket.error as err:
        print "Socket creation failed with error s." %(err)

    soc.bind(('', PORT))        
    print "Socket binded to %s." %(PORT)

    soc.listen(5)
    print "Socket is listening."

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

