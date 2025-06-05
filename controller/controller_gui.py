import tkinter as tk
from tkinter.font import Font
from threading import *
import subprocess

from controller import Controller


class ControllerWindow:

    def __init__(self):
        """
        function to initialise GUI
        """

        self.win = tk.Tk()
        # create window

        self.fonts_def()
        # call function to declare fonts for GUI

        self.control = Controller()
        # create controller object

        self.control.create_socket()
        # call function to create socket and start listening for connections

        self.main_window()
        # call function to display GUI

        self.close_all()
        # once GUI is closed, close all client connections and socket

    def fonts_def(self):
        """
        function to create fonts to use in GUI
        """

        # create font 1 (used for header)
        self.font_1 = Font(
            family='Helvetica',
            size=25,
            weight='bold',
            slant='roman',
            underline=1,
            overstrike=0
        )

        # create font 2 (used for labels)
        self.font_2 = Font(
            family='Helvetica',
            size=13,
            weight='bold',
            slant='roman',
            underline=0,
            overstrike=0
        )

        # create font 3 (used for buttons and ip address text)
        self.font_3 = Font(
            family='Helvetica',
            size=13,
            weight='normal',
            slant='roman',
            underline=0,
            overstrike=0
        )

    def main_window(self):
        """
        function to design and display GUI
        """

        # clear all elements from window
        for w in self.win.winfo_children():
            w.destroy()

        self.win.geometry("400x600")
        # set size of window

        self.win.resizable(False, True)
        # window can only be resized along y axis

        # ----- scroll -----

        canvas = tk.Canvas(self.win)
        # create canvas in window

        main_frame = tk.Frame(canvas)
        # create main_frame in canvas

        scrollbar = tk.Scrollbar(self.win, orient='vertical', command=canvas.yview)
        # create vertical scrollbar in window, scrolls y axis of canvas

        canvas.configure(yscrollcommand=scrollbar.set)
        # add scrollbar y axis scroll to canvas

        scrollbar.pack(side='right', fill='y')
        # add scrollbar to right side of main_frame, fill window in y direction

        canvas.pack(side='left')
        # add canvas to left side of main_frame

        # bind canvas and main_frame
        canvas.create_window(0, 0, window=main_frame, anchor='nw', width=400)
        self.win.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox("all"), width=400,
                                                                    height=1000))

        # ----- header -----

        # create header_frame and add to main_frame, fill in x direction
        header_frame = tk.Frame(main_frame, height="50")
        header_frame.pack(fill="x")

        # create header_label and add to header_frame, display text "CONTROLLER" in font 1
        header_label = tk.Label(header_frame, text="CONTROLLER", font=self.font_1)
        header_label.pack(pady=25)

        # ----- ip address -----

        # create ip_frame and add to main_frame, fill in x direction
        ip_frame = tk.Frame(main_frame)
        ip_frame.pack(fill="x", padx=50)

        self.get_ip()
        # call function to get controller ip address

        # create ip_label_frame and add to ip_frame, display text "IP address:" in font 2, fill in x direction
        ip_label_frame = tk.LabelFrame(ip_frame, text="IP address:", font=self.font_2)
        ip_label_frame.pack(fill="x")

        # create ip_label and add to ip_label_frame, display ip address of controller in font 3
        ip_label = tk.Label(ip_label_frame, text=self.ip_addr, font=self.font_3)
        ip_label.pack(pady=10)

        # ----- listen button -----

        # create listen_frame and add to main_frame, fill in x and y directions
        listen_frame = tk.Frame(main_frame)
        listen_frame.pack(fill="both", pady=25)

        # create listen_button and add to listen_frame, set height to 2, display text "Check for clients" in font 2
        # if listen_button is pressed, call function to check for new connections
        listen_button = tk.Button(listen_frame, height="2", text="Check for clients", font=self.font_2,
                                  command=lambda: self.sock_listen())
        listen_button.pack()

        # ----- labels -----

        # create labels_frame and add to main_frame, fill in x and y directions
        labels_frame = tk.Frame(main_frame)
        labels_frame.pack(fill="both", pady=5)

        # create buttons_label and place in labels_frame grid column 0 row 0, display text "Commands:" in font 2
        buttons_label = tk.Label(labels_frame, text="Commands:", font=self.font_2)
        buttons_label.grid(column=0, row=0, pady=10)

        # create clients_label and place in labels_frame grid column 1 row 0, display text "Clients:" in font 2
        clients_label = tk.Label(labels_frame, text="Clients:", font=self.font_2)
        clients_label.grid(column=1, row=0, pady=10)

        # configure both columns in labels_frame grid to take up half the width of labels_frame
        labels_frame.grid_columnconfigure(0, weight=1)
        labels_frame.grid_columnconfigure(1, weight=1)

        # ----- command option frames -----

        # create commands_frame and add to main_frame, fill in x direction
        commands_frame = tk.Frame(main_frame)
        commands_frame.pack(fill="x", pady=10)

        # create buttons_frame and add to left side of commands_frame, fill in x and y directions
        buttons_frame = tk.Frame(commands_frame)
        buttons_frame.pack(expand=True, side="left", fill="both")

        # create clients_frame and add to right side of commands_frame, fill in x and y directions
        clients_frame = tk.Frame(commands_frame)
        clients_frame.pack(expand=True, side="right", fill="both")

        # ----- buttons ------

        # create users_button and place in buttons_frame grid column 0 row 0
        # set size to 10x3, display text "Get user accounts" in font 3
        # if users_button is pressed, call function to send message to client with command "get_users"
        users_button = tk.Button(buttons_frame, height=3, width=10, text="Get user\naccounts", font=self.font_3,
                                 command=lambda: self.send_command("get_users"))
        users_button.grid(column=0, row=0, pady=5)

        # create sys_button and place in buttons_frame grid column 0 row 1
        # set size to 10x3, display text "Get system information" in font 3
        # if sys_button is pressed, call function to send message to client with command "sys_info"
        sys_button = tk.Button(buttons_frame, height=3, width=10, text="Get system\ninformation", font=self.font_3,
                               command=lambda: self.send_command("sys_info"))
        sys_button.grid(column=0, row=1, pady=5)

        # create procs_button and place in buttons_frame grid column 0 row 2
        # set size to 10x3, display text "Get running processes" in font 3
        # if procs_button is pressed, call function to send message to client with command "running_proc"
        procs_button = tk.Button(buttons_frame, height=3, width=10, text="Get running\nprocesses", font=self.font_3,
                                 command=lambda: self.send_command("running_proc"))
        procs_button.grid(column=0, row=2, pady=5)

        # create disconn_button and place in buttons_frame grid column 0 row 3
        # set size to 10x3, display text "Disconnect" in font 3
        # if sys_button is pressed, call function to send message to client with command "sys_info"
        disconn_button = tk.Button(buttons_frame, height=3, width=10, text="Disconnect", font=self.font_3,
                                   command=lambda: self.send_command("disconn_req"))
        disconn_button.grid(column=0, row=3, pady=5)

        # configure column in buttons_frame grid to take up entire width of buttons_frame
        buttons_frame.grid_columnconfigure(0, weight=1)

        # ----- clients -----

        count = 1
        # set count to 1

        self.checked = []
        # create checked array

        # for each client connected
        for client in self.control.clients:

            self.checked.append(tk.IntVar())
            # add variable to checked array representing whether checkbox is checked

            # create checkbox and place in clients_frame grid column 0 with each checkbox in new row
            # display hostname of client in font 3
            cb = tk.Checkbutton(clients_frame, text=str(client[1]), font=self.font_3, variable=self.checked[count-1])
            cb.grid(column=0, row=count, pady=5)

            count += 1
            # increment count

        # configure column in clients_frame grid to take up entire width of clients_frame
        clients_frame.grid_columnconfigure(0, weight=1)

        # ----- results -----

        # create result_frame and add to main_frame, fill in x direction
        result_frame = tk.Frame(main_frame, height="50")
        result_frame.pack(fill="x", padx=25)

        # create result_label_frame and add to result_frame, display text "Results:" in font 2, fill in x direction
        result_label_frame = tk.LabelFrame(result_frame, text="Results:", font=self.font_2)
        result_label_frame.pack(fill="x", pady=25)

        # create result_box and add to result_label_frame, fill in x and y directions
        self.result_box = tk.Text(result_label_frame)
        self.result_box.pack(fill="both", padx=10, pady=10)

        # ----- loop -----

        self.win.mainloop()
        # display window

    def get_ip(self):
        """
        function to get IP address of device controller is currently running on
        """

        self.ip_addr = subprocess.check_output("hostname -I", shell=True).decode("utf-8")
        # ip address is value returned from running the command

    def sock_listen(self):
        """
        function to connect new clients
            - checks for any new clients to connect
            - sets up new client connections if there are
            - re-displays GUI window with updated client list
        """

        client_to_connect = True
        # assume there is at least one client waiting to connect

        # while there could be more clients waiting to connect
        while client_to_connect:

            client_to_connect, c = self.control.new_conn_check()
            # call function to check for new connections

            # if a new client has been connected
            if client_to_connect:

                # create new thread for new client connection
                # call function to get hostname of client and add to clients list
                thread = Thread(target=self.control.new_conn, args=[c], daemon=True)
                thread.start()

        self.main_window()
        # call function to display GUI to update clients list

    def send_command(self, message):
        """
        function to send a command to and receive and display information from clients

        :param message: command to send to clients
        :type message: string
        """

        count = 0
        # set count to 0

        send = False
        # assume no checkboxes are checked

        # for each checkbox
        for x in self.checked:

            # if checkbox is checked
            if x.get() == 1:

                send = True
                # there is at least one client to send command to

        # if there is at least one client to send command to
        if send:

            output = ""
            # no results to display yet

            # for each client connected
            for client in self.control.clients:

                c = client[2]
                # set c to connection info of current client from clients list

                # if checkbox for current client is checked
                if self.checked[count].get() == 1:

                    self.control.send_request(c, message)
                    # call function to send message passed into function (depends on which button was pressed)

                    data = self.control.receive_info(c)
                    # call function to receive data from client

                    # if data received indicates that command sent was invalid
                    if data == "invalid_comm":

                        data = "Error: Could not execute command"
                        # set data as error message to be displayed

                    output = output + client[1] + ":\n\n" + data + "\n\n"
                    # add data to output string to be displayed

                    # if client has confirmed disconnect
                    if data == "disconnect":

                        self.control.conn_close(c)
                        # call function to close current connection

                        self.sock_listen()
                        # update current connections

                    # if data received is anything else
                    else:

                        self.result_box.delete(1.0, tk.END)
                        # clear contents of result_box

                        self.result_box.insert(tk.END, output)
                        # display output to result_box

                count += 1
                # increment count

    def close_all(self):
        """
        function to close all current client connections
        """

        # while clients are still connected
        while not len(self.control.clients) == 0:

            c = self.control.clients[0][2]
            # set c to connection info of first client from clients list

            self.control.send_request(c, "shutdown")
            # call function to send shutdown message to client

            self.control.receive_info(c)
            # call function to receive client response

            self.control.conn_close(c)
            # call function to close current connection

        self.control.sock_close()
        # call function to close socket


if __name__ == '__main__':

    win = ControllerWindow()
    # create controller GUI
