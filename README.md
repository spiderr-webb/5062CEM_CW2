# 5062CEM_CW2

## Introduction

Welcome to the repository for my coursework 2 for the module <b><i>5062CEM 
Programming and Algorithms 2</i></b>

## What It Does

This coursework consists of two programs, a <b>controller</b> with a 
graphical user interface that enables the user to issue a command, and a 
<b>client</b> that receives instructions from the controller, executes 
them on the machine, and sends back the relevant information.

Both the controller and client programs are designed to be run on a linux 
system.

## How To Use

To use this program, first the <b>controller</b> and <b>client</b> 
directories need to be downloaded.

The <b>controller</b> directory should contain the following files:
- <i>controller.py</i>
- <i>controller_gui.py</i>
- <i>controller_test.py</i>

The <b>client</b> directory should contain the following files:
- <i>client.py</i>

### Module Requirements

The following modules will need to be installed for all parts of the 
program to run correctly:

#### Modules imported in <i>controller.py</i>
- [Socket](https://docs.python.org/3/library/socket.html)
- [Threading](https://docs.python.org/3/library/threading.html)

#### Modules imported in <i>controller_gui.py</i>
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Threading](https://docs.python.org/3/library/threading.html)
- [Subprocess](https://docs.python.org/3/library/subprocess.html)

#### Modules imported in <i>controller_test.py</i>
- [Unitttest](https://docs.python.org/3/library/unittest.html)
- [Socket](https://docs.python.org/3/library/socket.html)
- [Threading](https://docs.python.org/3/library/threading.html)

#### Modules imported in <i>client.py</i>
- [Socket](https://docs.python.org/3/library/socket.html)
- [Subprocess](https://docs.python.org/3/library/subprocess.html)

### Testing

The file <i>controller_test.py</i>, in the <b>controller</b> directory, 
contains tests for <i>controller.py</i>.

It contains five tests which can be run from the CLI by navigating to the
<b>controller</b> directory where <i>controller_test.py</i> and 
<i>controller.py</i> are located and running the following commands:

`python3 -m unittest controller_test.Tests.test_client_connect`

`python3 -m unittest controller_test.Tests.test_receive_info`

`python3 -m unittest controller_test.Tests.test_send_info`

`python3 -m unittest controller_test.Tests.test_multiple_clients_receive`

`python3 -m unittest controller_test.Tests.test_multiple_clients_send`

### Running the program

The program consists of two parts, the controller and the client.

The controller needs to be started first, and can be run from the CLI by 
navigating to the <b>controller</b> directory where <i>controller.py</i>,
and <i>controller_gui.py</i> are located and running the command:

`python3 controller_gui.py`

Once the controller is running, on any device that is connected to the same 
network that the device running the controller is on, the client program can 
be started by navigating to the <b>client</b> directory where <i>client.py</i> 
is located and running the command:

`python3 client.py`

The client will request for the user to input the IP address of the controller 
to connect to, which should be displayed at the top of the controller's GUI 
window.

After inputting the controller's IP address into the client program, press the 
button on the controller GUI that is labelled "Check for clients", and the 
new client should appear on the list of currently connected clients.

Multiple clients can be connected to one controller by running 
<i>client.py</i> multiple times and connecting them to the IP address of the 
same controller.

## Documentation

The developer documentation for this program is provided in the form of 
docstrings and comments in the source-code.

Ideas for how the software could be extended by a developer in the future 
can be found in the wiki.