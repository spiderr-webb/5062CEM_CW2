import unittest
import socket
from threading import *

from controller import Controller

# tests have all run successfully individually

# running them all together causes "OSError: [Errno 98] Address already in use" in con.create_socket
# this sometimes also happens when run individually without waiting enough time between them

# tests also sometimes aren't successful the first time they're run
# run successfully every time after though


class Tests(unittest.TestCase):

    def test_client_connect(self):
        """
        test to check that controller can recognise a new client wanting to connect
        """

        con = Controller()
        # create controller object

        # create new thread for controller
        # call function to create socket and start listening for connections
        thread = Thread(target=con.create_socket())
        thread.start()


        s = socket.socket()
        # create client socket object

        port = 12345
        # define port number

        s.connect(("127.0.0.1", port))
        # connect client socket to the controller

        message = "Client1"
        # set message to send as client name

        s.send(message.encode())
        # send message from client to controller

        new_client, c = con.new_conn_check()
        # call controller function to check for new connections

        self.assertTrue(new_client)
        # check that new client connection has been found

        con.conn_close(c)
        # call controller function to close client connection

        con.sock_close()
        # call controller function to close socket

        s.close()
        # close client socket

    def test_receive_info(self):
        """
        test to check that controller can receive info from a connected client
        """

        con = Controller()
        # create controller object

        # create new thread for controller
        # call function to create socket and start listening for connections
        thread = Thread(target=con.create_socket())
        thread.start()

        s = socket.socket()
        # create client socket object

        port = 12345
        # define port number

        s.connect(("127.0.0.1", port))
        # connect client socket to the controller

        message = "Client1"
        # set message to send as client name

        s.send(message.encode())
        # send message from client to controller

        new_client, c = con.new_conn_check()
        # call controller function to check for new connections

        # create new thread for new client connection
        # call function to get name of client and add to clients list
        thread = Thread(target=con.new_conn, args=[c], daemon=True)
        thread.start()

        message = "Test message 1"
        # set message to send

        s.send(message.encode())
        # send message from client to controller

        received = con.receive_info(c)
        # call controller function to receive message from client

        self.assertEqual(received, message)
        # check that message sent by client is the same is message received by controller

        message = "Test message 2"
        # set message to send

        s.send(message.encode())
        # send message from client to controller

        received = con.receive_info(c)
        # call controller function to receive message from client

        self.assertEqual(received, message)
        # check that message sent by client is the same is message received by controller

        con.conn_close(c)
        # call controller function to close client connection

        con.sock_close()
        # call controller function to close socket

        s.close()
        # close client socket

    def test_send_info(self):
        """
        test to check that controller can send info to a connected client
        """

        con = Controller()
        # create controller object

        # create new thread for controller
        # call function to create socket and start listening for connections
        thread = Thread(target=con.create_socket())
        thread.start()

        s = socket.socket()
        # create client socket object

        port = 12345
        # define port number

        s.connect(("127.0.0.1", port))
        # connect client socket to the controller

        message = "Client1"
        # set message to send as client name

        s.send(message.encode())
        # send message from client to controller

        new_client, c = con.new_conn_check()
        # call controller function to check for new connections

        # create new thread for new client connection
        # call function to get name of client and add to clients list
        thread = Thread(target=con.new_conn, args=[c], daemon=True)
        thread.start()

        message = "Test message 1"
        # set message to send

        con.send_request(c, message)
        # call controller function to send message to client

        received = s.recv(5120).decode()
        # client receive message from controller

        self.assertEqual(received, message)
        # check that message sent by controller is the same is message received by client

        message = "Test message 2"
        # set message to send

        con.send_request(c, message)
        # call controller function to send message to client

        received = s.recv(5120).decode()
        # client receive message from controller

        self.assertEqual(received, message)
        # check that message sent by controller is the same is message received by client

        con.conn_close(c)
        # call controller function to close client connection

        con.sock_close()
        # call controller function to close socket

        s.close()
        # close client socket

    def test_multiple_clients_receive(self):
        """
        test to check that controller can connect to and receive info from multiple clients
        """

        con = Controller()
        # create controller object

        # create new thread for controller
        # call function to create socket and start listening for connections
        thread = Thread(target=con.create_socket())
        thread.start()

        s1 = socket.socket()
        # create first client socket object

        port = 12345
        # define port number

        s1.connect(("127.0.0.1", port))
        # connect first socket to the controller

        message = "Client1"
        # set message to send as first client name

        s1.send(message.encode())
        # send message from first client to controller

        new_client, c1 = con.new_conn_check()
        # call controller function to check for new connections

        # create new thread for new client connection
        # call function to get name of client and add to clients list
        thread = Thread(target=con.new_conn, args=[c1], daemon=True)
        thread.start()

        s2 = socket.socket()
        # create second client socket object

        port = 12345
        # define port number

        s2.connect(("127.0.0.1", port))
        # connect second socket to the controller

        message = "Client2"
        # set message to send as second client name

        s2.send(message.encode())
        # send message from second client to controller

        new_client, c2 = con.new_conn_check()
        # call controller function to check for new connections

        # create new thread for new client connection
        # call function to get name of client and add to clients list
        thread = Thread(target=con.new_conn, args=[c2], daemon=True)
        thread.start()

        message = "Test message 1"
        # set message to send

        s1.send(message.encode())
        # send message from first client to controller

        received = con.receive_info(c1)
        # call controller function to receive message from first client

        self.assertEqual(received, message)
        # check that message sent by first client is the same is message received by controller

        message = "Test message 2"
        # set message to send

        s2.send(message.encode())
        # send message from second client to controller

        received = con.receive_info(c2)
        # call controller function to receive message from second client

        self.assertEqual(received, message)
        # check that message sent by second client is the same is message received by controller

        con.conn_close(c1)
        # call controller function to close first client connection

        con.conn_close(c2)
        # call controller function to close second client connection

        con.sock_close()
        # call controller function to close socket

        s1.close()
        # close first client socket

        s2.close()
        # close second client socket

    def test_multiple_clients_send(self):

        con = Controller()
        # create controller object

        # create new thread for controller
        # call function to create socket and start listening for connections
        thread = Thread(target=con.create_socket())
        thread.start()

        s1 = socket.socket()
        # create first client socket object

        port = 12345
        # define port number

        s1.connect(("127.0.0.1", port))
        # connect first socket to the controller

        message = "Client1"
        # set message to send as first client name

        s1.send(message.encode())
        # send message from first client to controller

        new_client, c1 = con.new_conn_check()
        # call controller function to check for new connections

        # create new thread for new client connection
        # call function to get name of client and add to clients list
        thread = Thread(target=con.new_conn, args=[c1], daemon=True)
        thread.start()

        s2 = socket.socket()
        # create second client socket object

        port = 12345
        # define port number

        s2.connect(("127.0.0.1", port))
        # connect second socket to the controller

        message = "Client2"
        # set message to send as second client name

        s2.send(message.encode())
        # send message from second client to controller

        new_client, c2 = con.new_conn_check()
        # call controller function to check for new connections

        # create new thread for new client connection
        # call function to get name of client and add to clients list
        thread = Thread(target=con.new_conn, args=[c2], daemon=True)
        thread.start()

        message = "Test message 1"
        # set message to send

        con.send_request(c1, message)
        # call controller function to send message to first client

        received = s1.recv(5120).decode()
        # first client receive message from controller

        self.assertEqual(received, message)
        # check that message sent by controller is the same is message received by first client

        message = "Test message 2"
        # set message to send

        con.send_request(c2, message)
        # call controller function to send message to second client

        received = s2.recv(5120).decode()
        # second client receive message from controller

        self.assertEqual(received, message)
        # check that message sent by controller is the same is message received by second client

        con.conn_close(c1)
        # call controller function to close first client connection

        con.conn_close(c2)
        # call controller function to close second client connection

        con.sock_close()
        # call controller function to close socket

        s1.close()
        # close first client socket

        s2.close()
        # close second client socket


if __name__ == '__main__':

    unittest.main()
    # start tests
