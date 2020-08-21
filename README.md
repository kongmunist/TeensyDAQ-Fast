# TeensyDAQ-Fast
TeensyDAQ-Fast is a Python application for visualizing and recording analog signals with a [Teensy micro-controller](https://www.pjrc.com/store/teensy40.html). If you need to get an analog signal from the real world into a text file on your computer, you'll need a DAQ (Data AcQuisition device). However, a standalone DAQ costs upwards of $100, and restricts the GUI/output file types you can use. Because the Teensy's analog-to-digital converter can output 12-bit samples at up to 400kHz, I figured I'd give this a try before buying something new. There's already another project like it [here](https://github.com/JorenSix/TeensyDAQ), but they only get 8kHz out of their Teensy. 

I used the fast ADC library on the teensy side to output a continuous stream of readings from pin 18 to Serial, then used the pySerial library to decode it on the computer side. Then I adapted a GUI from @szeloof to record into a specific file. The visualization of the data stream appears after the recording finishes, to show you any egregious errors. The files are saved as .txts, but are actually CSVs. Go crazy!

![GUI picture](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/GUI.png)
 
 # How to Use
1. Clone the repo.  
2. Your <b>Python</b> instance is going to need PyQt5, pySerial, and matplotlib (I ran it in Python 3.6). 
3. Push the Teensy code to the <b>Teensy</b> however you would like (I'm using Teensy 4.0)
4. Plug your Teensy into your computer. Connect your signal to pin 18.
5. Run SerialGUI.py. 
6. Click the "Start Recording" button to start and stop the recording. If you want a custom file name, type it in the box and hit enter. (The GUI does not always update when I tell it to).
 
 # Speed Check
The Teensy toggles pin 10 whenever it outputs a measurement to the computer, allowing me to time it. The frequency in this case is halved, so the actual Teensy free-running ADC speed is around 2*167kHz = 334 kHz. 
 
![ADC output speed](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/ADCoutput.JPG)

The python on the computer checks the timer when it starts and stops receiving data points, so we can clock the computer's receive rate as well. It gets close, but not exactly up to the Teensy's 334 kHz.

![Computer serial receive speed](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/GUIoutput.png)



# Example images
# Output file
![output file](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/recordingExample.png)

# Various waves
![Sine wave on oscilloscope and computer](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/Sine.JPG)
![Square wave on oscilloscope and computer](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/Square.JPG)
![Ramp on oscilloscope and computer](https://github.com/kongmunist/TeensyDAQ-Fast/blob/master/ims/Ramp.JPG)
