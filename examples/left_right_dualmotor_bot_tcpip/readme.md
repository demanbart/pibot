#Left right dual motor bot
##Setup
The robot was made out of [K'nex](https://en.wikipedia.org/wiki/K%27Nex) which already has DC motor building blocks. To make the DC motors controllable I've disconnected the power source (2x1.5AA batteries) from the motor and placed a DC motor driver inbetween. The DC motor driver is connected to a Raspberry PI. The RPi is powered by a USB powerbank. On the RPi the receive.py is executed serving as a TCP/IP server. The controller is run on a Win10 PC sending commands to the RPi via TCP/IP.

##Reproduction
1. You should change the motor driver class to the one that fits Yours.
2. The IP addresses in the control.py and receive.py script should be changed to reflect Your situation.
