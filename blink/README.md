#Miniproject 0

##Running the Blink Code on a PIC24

*This document explains the necessary steps to start running code on a PIC24 microcontroller. This setup uses the command line bootloader, rather than the GUI.*

*This documentation utilizes the elecanisms git repository that can be found [here](https://github.com/OlinElecanisms/elecanisms).*

###Installing Build Tools
1. Download the installer for your desired operating system [here](http://www.microchip.com/compilers).
2. For 64-bit Linux, you may need to install some libraries to allow for 32-bit compatibility. Follow the commands [here](http://askubuntu.com/questions/297151/how-to-run-32-bit-programs-on-a-64-bit-system).
3. Run the installer and select the default options.
4. You will also need to install a build system. **SCons** is a simple build automation tool. The command *$ sudo apt-get install scons* should take care of this.

###Compiling C Code
1. In the terminal, navigate to the **blink** directory in the elecanisms folder.
2. Run *scons*.
3. Check to see that blink.hex has been created.

###Uploading Code to the Microcontroller
1. Connect the PIC24 to your computer using a microusb.
2. To put the microcontroller in bootloader mode, hold SW1 while pressing the RESET button.
3. In the terminal, navigate to the **site_scons** directory.
4. Run *python bootloadercmd.py* to check that the microcontroller is connected properly.
5. Run *python bootloadercmd.py -i ../blink/blink.hex -w* to write the blink program to the PIC24.
6. Reset the board to verify that the program is running properly.

Changes can be made to the program by editing the blink.c file. This will need to be saved and recompiled as above. To view the help documentation for the command line bootloader, run *python bootloadercmd.py -h*.