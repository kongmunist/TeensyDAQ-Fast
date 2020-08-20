import serial
import sys
import threading
import os
import time
import copy



# Taken from my friend Sam, god bless his soul
# fast serial readline from https://github.com/pyserial/pyserial/issues/216#issuecomment-369414522
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)




# stoppable thread for serial tx/rx
class SerialThread(threading.Thread):
    def __init__(self, port, dataHolder, baud):
        super(SerialThread, self).__init__()
        self._stop = threading.Event()
        self.port = port

        # Receiving data variables
        self.serialData = ""
        self.dataHolder = dataHolder
        self.data = []
        self.baud = baud

        # Serial printing data variables
        self.RTS = False # Ready To Send
        self.message = ""

        # Recording data variables
        self.recording = False
        self.recordingNum = 0
        self.basefilename = "recording"
        self.recordingfilename = ""
        self.saveDir = "output"
        self.startRecordTime = 0
        self.stopRecordTime = 0

        os.makedirs(self.saveDir, exist_ok=True)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


    def start_recording(self, filename=None):
        # If input filename, take it. Otherwise make a default one from recordingNum
        if filename is None:
            self.recordingfilename = os.path.join(self.saveDir,
                                         self.basefilename + str(self.recordingNum) + ".txt")
            print("filename not supplied, recording into", self.recordingfilename)
        else:
            self.recordingfilename = os.path.join(self.saveDir, filename)
            print("recording into", self.recordingfilename)

        # Set variables and tell Teensy to start recording
        self.recording = True
        self.send_message("h")
        self.startRecordTime = time.time()


    def stop_recording(self):
        # Turn off teensy recording
        self.send_message("h")

        # write into file
        tmp = copy.copy(self.data)
        tmp = b''.join(tmp)
        tmp = tmp.strip().split(b'\r\n')
        tmp = [x.decode("utf-8").strip() for x in tmp]
        with open(self.recordingfilename, "w+") as f:
            f.write(",".join(tmp))

        # Add data to the graph
        try:
            self.dataHolder = [int(x) for x in tmp]
        except Exception as e:
            print("error:", e)
            print('graph failed')

        print("Done recording: Saved", len(tmp), "numbers in", round(self.stopRecordTime-self.startRecordTime,2) ,
              "s, at frequency", round(len(tmp)/(self.stopRecordTime-self.startRecordTime)/1000,2), "kHz")

        # Reset variables and iterate the default file num
        self.data = []
        self.recording = False
        self.recordingNum += 1



    def send_message(self, message):
        self.RTS = True
        self.message = message
        t1 = threading.Thread(target=self.threadSendMess)
        t1.start()

    def threadSendMess(self):
        self.com.write(self.message.encode('utf-8'))
        self.stopRecordTime = time.time()
        # print("Sent in thread", self.message)
        self.RTS = False
        self.message = ""


    def run(self):
        try:
            self.com = serial.Serial(self.port, self.baud, timeout = 0.5)
            self.rl = ReadLine(self.com)
        except Exception as e:
            print("\nSERIAL PORT ERROR:", e)
            sys.exit()

        while True:
            if self.stopped():
                return

            # While there are bytes to be read, keep reading and recording
            # Do not record if there's a pending message to be sent
            if self.recording and not self.RTS:
                while self.com.in_waiting:
                    self.data.append(self.com.read(1000))
                    # print(self.com.in_waiting) # shows num bytes backed up in buffer