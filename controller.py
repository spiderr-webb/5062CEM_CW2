import socket
from threading import *


class Controller:

    def __init__(self):
        """
        function to initialise controller
        """

        self.clients = []
        # no clients connected yet

    def create_socket(self):
        """
        function to create socket
        """

        self.s = socket.socket()
        # create socket object

        port = 12345
        # define port number

        self.s.settimeout(0.2)
        # set timeout for listening

        self.s.bind(('', port))
        # bind socket to port
        # no ip to make the server listen to all requests from other computers on the network

        self.s.listen(5)
        # put socket into listening mode

    def new_conn_check(self):
        """
        function to check for and accept new client connections
        """

        c = ""
        # no new connections found yet

        # see whether there are any new client connections to accept
        try:

            c, ipaddr = self.s.accept()
            # accept client connection

            client_to_connect = True
            # as one connection has been made there could be more clients waiting to connect

        # if there are no new clients to connect
        except socket.timeout:

            client_to_connect = False
            # new client connection was not made

        return client_to_connect, c
        # return whether new client connection was made and if it was, connection info

    def new_conn(self, c):
        """
        function to set up new client connection
            - gets hostname of new client
            - adds newly connected client to list of currently connected clients
            - keeps connection open

        :param c: connection information of new client
        """

        thread_id = current_thread().ident
        # get id of current thread

        data = self.receive_info(c)
        # call function to receive data from client
        # first message received from client will be hostname of client

        self.clients.append([thread_id, data, c])
        # add new client to list of clients
        # include id of thread connection is on, hostname of client, and connection info

        # keep connection open
        while True:
            pass

    def send_request(self, c, message):
        """
        function to send message to client

        :param c: connection information of client to send to
        :param message: message to send to client
        :type message: string
        """

        c.send(message.encode())
        # send message to client connection that was passed into the function

    def receive_info(self, c):
        """
        function to receive data from client

        :param c: connection information of client to receive from
        """

        data = c.recv(5120).decode()
        # receive data stream, won't accept data packet greater than 5120 bytes
        # this causes problems with commands sent and results displayed getting out of sync if data is larger
        # 5120 bytes of info will be read, then on next command sent next 5120 bytes of prev info will be read

        # if no data is received from client
        if not data:

            data = "Error: No data received"
            # set data as error message to be displayed

        return data
        # return data received from client (or error message)

    def conn_close(self, c):
        """
        function to close client connection

        :param c: connection information of client to close
        """

        c.close()
        # close connection

        num = len(self.clients)
        # set num to length of clients list

        # if there are clients currently connected
        if num > 0:

            # for each client connected
            for client in self.clients:

                # if connection info of current client in list matches info of client connection that was closed
                if client[2] == c:

                    self.clients.remove(client)
                    # remove closed client connection from list of clients

    def sock_close(self):
        """
        function to close socket
        """

        self.s.close()
        # close socket
