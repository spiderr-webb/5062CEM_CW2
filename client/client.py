import socket
import subprocess


class ClientConnection:

    def __init__(self):
        """
        function to initialise client
        """

        self.connect()
        # call function to connect to controller

    def connect(self):
        """
        function to interact with controller
            - connect to controller
            - receive commands
            - get relevant information depending on command received and send back to controller
            - when disconnect is requested by controller, close connection
        """

        s = socket.socket()
        # create socket object

        port = 12345
        # define port number

        ipaddr = self.input_ip()
        # call function to get ip address of controller from user

        s.connect((ipaddr, port))
        # connect to the controller

        message = socket.gethostname()
        # set message to send as hostname of current device

        s.send(message.encode())
        # send message to controller

        stop = False
        # connection has not been closed yet

        # keep connection open until controller sends message asking to disconnect
        while not stop:

            data = s.recv(1024).decode()
            # receive data stream, won't accept data packet greater than 1024 bytes

            print('Received from server: ' + data)
            # print command received from controller

            # if controller requested user account information
            if data == "get_users":

                message = self.get_users()
                # call function to get user account info and set message to returned value

            # if controller requested system information
            elif data == "sys_info":

                message = self.get_sys_info()
                # call function to get system info and set message to returned value

            # if controller requested running processes
            elif data == "running_proc":

                message = self.get_procs()
                # call function to get running processes and set message to returned value

            # if controller requested to disconnect
            elif data == "disconn_req":

                message = "disconnect"
                # set message to confirm disconnect

                stop = True
                # end loop keeping connection open

            # if controller has closed
            elif data == "shutdown":

                message = "shutdown"
                # set message to confirm disconnect

                stop = True
                # end loop keeping connection open

            else:
                message = "invalid_comm"

            s.send(message.encode())
            # send message to controller

        s.close()
        # close connection

    def get_users(self):
        """
        function to get information about user accounts on the system

        :return: information about user accounts from /etc/passwd
        :rtype: string
        """

        users = subprocess.check_output("cat /etc/passwd", shell=True).decode("utf-8")
        # read information from /etc/passwd

        return users
        # return /etc/passwd

    def get_sys_info(self):
        """
        function to get information about the current system

        :return: information about current system
        :rtype: string
        """

        ports = subprocess.check_output("uname -a", shell=True).decode("utf-8")
        # read results of command 'uname -a'

        return ports
        # return 'uname -a' results

    def get_procs(self):
        """
        function to get names of processes currently running on the system from /proc directory

        :return: names of running processes from /proc directory
        :rtype: string
        """

        procs = subprocess.check_output("ls /proc | grep '[0-9]' | while read -r dir ; do cat /proc/$dir/comm ; done", shell=True).decode("utf-8")
        # for each numbered directory in /proc read the process name

        return procs
        # return running processes

    def input_ip(self):
        """
        function to get IP address of controller to connect to from user input

        :return: user input of IP address of controller
        :rtype: string
        """

        print("Input IP address of controller (127.0.0.1 for localhost): ")
        ipaddr = input()
        # get ip address of controller from user input

        return ipaddr
        # return ip address


if __name__ == '__main__':

    conn = ClientConnection()
    # create client
