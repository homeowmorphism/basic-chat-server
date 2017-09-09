# Basic Chat Server

*Status: done.*

An easy to understand socket-based Python chat server with minimal threading and basic functionalities (you can input a username, that's pretty much it). This is built on top of a minimal server built in Python. You can find the code, as well as a great explanatory tutorial [here](https://pythontips.com/2013/08/06/python-socket-network-programming/) -- normally I would upload self-written code with an accompanied explaination on Github, but I have nothing to add to this excellent tutorial.

## Run

Make sure you have a version of Python that is compatible with Python 2.7.

You will need at least three shells to really run the chat server. 

The first one will serve as the server. 

```
# Server shell.
$ python chatserv.py
Socket successfully created
Socket binded to port 1337.
Socket is listening.
```

Now you will have to create two shells that connect to localhost through port 1337. 

```
# Alice's shell.
$ telnet localhost 1337
server: Input username.
> Alice
server: Your username is Alice.
```

```
# Bob's shell.
$ telnet localhost 1337
server: Input username.
> Bob 
server: Your username is Bob.
> Hello Alice!
```

Now Alice's shell should display 

```
# Alice's shell.
Bob : Hello Alice!
```

We're done! You can play with this very basic chat server 😄!

## Essential upgrades from basic server: threading and non-blocking. 

*This is a conceptual explanation, not an exposition of added features.*

In a basic server, we have a server and a client. The server waits for the client to connect and sends back a message to the client telling the client he has successfully connected, then closes the connection.

```
# Basic server (client side)
Thank you for connecting to mah servah!
Connection closed by foreign host.
```

A chat server is only a tiny bit more complicated. It has a central server and multiple clients. It accepts connections from all clients without closing them. For each client, the server waits for a message. When it gets that message, it sends it to all the other clients. 

The essential upgrades from a basic server are **threading** and **non-blocking**. In the [minimal server scheme](https://pythontips.com/2013/08/06/python-socket-network-programming/), you can afford to wait for your client to connect to accept the connection and display a message. 

In a server, you can't afford to do that because you want to handle *multiple* connections and don't want to wait for one client to connect before you respond to an already-connected client! Running the code to accept connections in parallel 

```
thread.start_new_thread(accept_conns, (soc,))
```

to the code which receives and sends messages to already connected clients fixes the problem between clients wanting to connect and already-connected clients.

The second problem that arises is managing the client-server response for already-connected clients. A basic way to get inputs from each client is to iterate through all of them in a `for` loop (while is nested in a `while True` statement so we keep cycling through each user). The problem with this method is that the server will have to wait for Alice to send a message before Bob can send a message, and then wait for Alice to send another message and so on. *Non-blocking* 

```
connection.setblocking(0)
```

fixes the problem because the server doesn't wait for a connection to be made anymore. It just accepts whatever, even if the message is empty (i.e. Alice doesn't send any message). If the server accepts an empty message, it will throw an exception, which we have to handle through a try-catch block. This looks like a good explanation of [blocking vs non-blocking](http://www.scottklement.com/rpg/socktut/nonblocking.html) if you'd like to learn more about that!

There are other small details in the implementation (like `BUFSIZE`), but they matter little conceptually so I won't go into them. 

## Acknowledgements

This project was really interesting in that I was exposed to a new set of bugs I had no experience with. It was written in the company of [Jinny Cho](https://github.com/eunjincho503) and [Wesley Aptekar-Cassels](https://github.com/WesleyAC) at the [Recurse Center](https://www.recurse.com/). I couldn't have done this without their energy and Wesley knowing what to Google. 
