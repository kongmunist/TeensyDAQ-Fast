# TeensyDAQ-Fast
TeensyDAQ-Fast is a Python application + [Teensy](https://www.pjrc.com/store/teensy40.html) script for recording and visualizing analog signals. Jitter-free operation at 100kHz sampling rate on the Teensy 3.5, and possibly higher for more recent Teensy releases. 

## Motivation
Usually, converting an analog signal into a digital file on your computer rqeuires a DAQ (Data AcQuisition device). However, a standalone DAQ costs upwards of $100, and restricts the GUI and output file types. Because the Teensy's built-in ADC can digitize 12-bits at up to 400kHz, I figured I'd give this a try before buying something new. 

## Brief summary
I'm using the [ADC library](https://github.com/pedvide/ADC) by pedvide on the Teensy to output a continuous stream of recordings to the serial port. On the python side, I use pySerial to connect to the serial port and read it into a text file. I modified a GUI from another project to give a nice visualization of the recorded data — this graph only appears after the recording finishes to show you any egregious errors. The files are saved as txt, but are actually CSVs. Have fun!

![GUI picture](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/GUI.png)

The old version of this program could reach a 300kHz sampling rate (13 bit, Teensy 4.0) with no regard for jitter in the sampling time. In the interest of stable sampling, the sampling rate has come down to 100kHz (13 bit, Teensy 3.5) with little to no jitter in the digitization/communication time. See update notes for more info.

There's already another project like this [here](https://github.com/JorenSix/TeensyDAQ), but they only get 8kHz out of their Teensy. 


 # Usage
1. Clone this repo. 
2. Your <b>Python</b> instance is going to need PyQt5, pySerial, and matplotlib (I ran it in Python 3.6). 
3. Push the Teensy code to the <b>Teensy</b> however you would like (I'm using Teensy 4.0)
4. Plug your Teensy into your computer. Connect your signal to pin 14
5. Run SerialGUI.py. 
6. Click the "Start Recording" button to start and stop the recording. If you want a custom file name, type it in the box and hit enter. (The GUI does not always update when I tell it to).
 
Alternatively, you can use just the Teensy code and record the serial output on the computer any way you want. I recently found a very neat way to do it on Mac/Linux computers [here](https://medium.com/@kongmunist/serial-logging-in-processing-using-shell-commands-183ea8be6791).

 # Speed Check
The Teensy toggles pin 11 whenever it sends a measurement to the computer, allowing me to time it. Currently, the ADC speed is fixed at 100kHz stably. We can access the free-running speed by dialing the two timer delays down to 1 on lines 40-41, accessing a jittery speed of ~400kHz. 

I have also improved the Python side by turning rtscts=True. I do not know why this isn't on by default since we lose data without it, but hopefully now we don't lose data anymore

# Updates
### 6/12/23 Update 2.0
I switched to using timers for sampling and printing data to serial in a more stable way. This has fixed a lot of jitter in the sampling rate, which is a problem for certain types of data. I also added rtscts=True to Python. 

Here is the jitter in output data rate using v1, approximately 6uS on a 154kHz signal (which takes ~6uS to sample). ADC resolution is set to 13 bits, Serial set to 2000000, data output with Serial.println()

https://github.com/kongmunist/TeensyDAQ-Fast/assets/29759597/acf605ef-2906-4921-ac4d-cc0a98a16c8e

Here's the jitter now, using v2. Settings same as above, we get 100kHz with low jitter.

https://github.com/kongmunist/TeensyDAQ-Fast/assets/29759597/85333d69-af3e-42a8-b334-c11a5becdd34

Same settings as above, v2, using Serial.write() instead of println. Even better!

https://github.com/kongmunist/TeensyDAQ-Fast/assets/29759597/b8cef35f-3d08-412a-880c-80fa9c1c72ff

# Example images
# Output file
![output file](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/recordingExample.png)

# Various waves
![Sine wave on oscilloscope and computer](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/Sine.JPG)
![Square wave on oscilloscope and computer](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/Square.JPG)
![Ramp on oscilloscope and computer](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/Ramp.JPG)
