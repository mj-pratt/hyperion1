import serial
import time
import csv
from multiprocessing import Process, Queue
import sys
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

fulldatastrings = []
timedata = []
timevect = []
tc1list = []
tc2list = []
tc3list = []
tc4list = []
pt1list = []
pt2list = []
pt3list = []
pt4list = []
forcelist = []
avgs = []
newlist = []
num = 0
qmain=1
numbbitsthermocouple = 16
numbbitspt = 16
tempsensorrange = 2440
pressuresensorrange = 5000
q = Queue()


def establishserial(comport, baud):
    try:
        ser = serial.Serial(comport, baudrate=baud, parity=serial.PARITY_NONE, stopbits=1, timeout=4)
        return ser
    except:
        print(Fore.RED + "serial no go OwO")
        print(Fore.WHITE)



#def getdata(ser,testnumb, comportlogging, baudratecontrol,q):
#    num = 0
#    print(Fore.YELLOW + 'Data Gathering Start')
#    print(Fore.WHITE)
#    r = True
#
#    while r == True:
#        try:
#            data = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
#            utfdata = str(time.time())+" "+data.decode("utf-8")
#            fulldatastrings.append(utfdata)
#
#        except KeyboardInterrupt:
#            print(Fore.YELLOW + num)
#            print(Fore.WHITE)
#            r = False
#            with open('AspenDaqdata.txt', 'w', newline='') as f:
#                writer = csv.writer(f, dialect='excel')
#                for row in fulldatastrings:
#                    newrow=row.split(' ')
#                    writer.writerow(newrow)

def liveplotting(ser, numbbitsthermocouple):
    num = 0
    print(Fore.YELLOW + 'Data Gathering Start')
    print(Fore.WHITE)
    r = True
    line1=[]
    fig = plt.figure()
    ax1 = fig.add_subplot(331)
    ax1.set_title('TC 1')
    ax1.set_ylim([0, 1000])
    ax2 = fig.add_subplot(332)
    ax2.set_title('TC 2')
    ax2.set_ylim([0, 1000])
    ax3 = fig.add_subplot(333)
    ax3.set_title('TC 3')
    ax3.set_ylim([0, 1000])
    ax4 = fig.add_subplot(334)
    ax4.set_title('TC 4')
    ax4.set_ylim([0, 1000])
    ax5 = fig.add_subplot(335)
    ax5.set_title('PT 1')
    ax5.set_ylim([0, 1200])
    ax6 = fig.add_subplot(336)
    ax6.set_title('PT 2')
    ax6.set_ylim([0, 1200])
    ax7 = fig.add_subplot(337)
    ax7.set_title('PT 3')
    ax7.set_ylim([0, 1200])
    ax8 = fig.add_subplot(338)
    ax8.set_title('PT 4')
    ax8.set_ylim([0, 1200])
    ax9 = fig.add_subplot(339)
    ax9.set_title('FORCE 1')
    ax8.set_ylim([0, 10])
    print("Subplots added")
    try:
        print("attempting subplot")
        ani = animation.FuncAnimation(fig, animate, fargs=(ser, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9), interval=200, repeat=False)
        plt.show()
    #while r == True:
    #    try:
    #        data = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
    #        utfdata = str(time.clock())+" "+str(data, 'utf-8', errors='ignore')
    #        fulldatastrings.append(utfdata)
    #       tim, tc1, tc2, tc3, tc4, pt1, pt2, pt3, pt4, forc = splitdata(utfdata, numbbitsthermocouple)
    #       timevect.append(tim)
    #        tc1list.append(tc1)
    #        tc2list.append(tc2)
    #        tc3list.append(tc3)
    #        tc4list.append(tc4)
    #        pt1list.append(pt1)
    #        pt2list.append(pt2)
    #        pt3list.append(pt3)
    #        pt4list.append(pt4)
    #       forcelist.append(forc)
    except:
        printerror("animation failed")



def animate(i,ser, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9):
    starttime = time.clock()
    intertc1 = []
    intertc2 = []
    intertc3 = []
    intertc4 = []
    interpt1 = []
    interpt2 = []
    interpt3 = []
    interpt4 = []
    interforce = []
    tim = time.perf_counter()
    while(time.perf_counter() < starttime+.03):
        try:
            data = ser.readline()[:-2]  # the last bit gets rid of the new-line chars
            utfdata = str(time.clock()) + " " + str(data, 'utf-8', errors='ignore')
            fulldatastrings.append(utfdata)
            tim, tc1inter, tc2inter, tc3inter, tc4inter, pt1inter, pt2inter, pt3inter, pt4inter, forcinter = splitdata(utfdata, numbbitsthermocouple)
            intertc1.append(tc1inter)
            intertc2.append(tc2inter)
            intertc3.append(tc3inter)
            intertc4.append(tc4inter)
            interpt1.append(pt1inter)
            interpt2.append(pt2inter)
            interpt3.append(pt3inter)
            interpt4.append(pt4inter)
            interforce.append(forcinter)
        except:
            pass
    try:
        tc1 = sum(intertc1) / len(intertc1)
        tc2 = sum(intertc2) / len(intertc2)
        tc3 = sum(intertc3) / len(intertc3)
        tc4 = sum(intertc4) / len(intertc4)
        pt1 = sum(interpt1) / len(interpt1)
        pt2 = sum(interpt2) / len(interpt2)
        pt3 = sum(interpt3) / len(interpt3)
        pt4 = sum(interpt4) / len(interpt4)
        forc = sum(interforce)/len(interforce)
    except:
        pass
    try:
        tc1new = processtemp(tc1, numbbitsthermocouple)
        tc2new = processtemp(tc2, numbbitsthermocouple)
        tc3new = processtemp(tc3, numbbitsthermocouple)
        tc4new = processtemp(tc4, numbbitsthermocouple)
        pt1new = processpressure1(pt1)
        pt2new = processpressure2(pt2)
        pt3new = processpressure3(pt3)
        pt4new = processpressure4(pt4)
        forcenew = processforce(forc)
        timevect.append(tim)
        tc1list.append(tc1new)
        tc2list.append(tc2new)
        tc3list.append(tc3new)
        tc4list.append(tc4new)
        pt1list.append(pt1new)
        pt2list.append(pt2new)
        pt3list.append(pt3new)
        pt4list.append(pt4new)
        forcelist.append(forcenew)
        xar = timevect
        ax1.clear()
        ax1.plot(xar, tc1list, linewidth=.5)
        ax1.annotate(str(tc1new), xy=(tim, tc1new))
        ax1.set_title('TC 1')
        ax1.set_ylim([0, 1000])
        ax2.clear()
        ax2.plot(xar, tc2list, linewidth=.5)
        ax2.annotate(str(tc2new), xy=(tim, tc2new))
        ax2.set_title('TC 2')
        ax2.set_ylim([0, 1000])
        ax3.clear()
        ax3.plot(xar, tc3list, linewidth=.5)
        ax3.set_title('TC 3')
        ax3.set_ylim([0, 1000])
        ax3.annotate(str(tc3new), xy=(tim, tc3new))
        ax4.clear()
        ax4.plot(xar, tc4list, linewidth=.5)
        ax4.set_title('TC 4')
        ax4.set_ylim([0, 1000])
        ax4.annotate(str(tc4new), xy=(tim, tc4new))
        ax5.clear()
        ax5.plot(xar, pt1list, linewidth=.5)
        ax5.annotate(str(pt1new), xy=(tim, pt1new))
        ax5.set_ylim([0, 1200])
        ax5.set_title('PT 1')
        ax6.clear()
        ax6.plot(xar, pt2list, linewidth=.5)
        ax6.set_ylim([0, 1200])
        ax6.annotate(str(pt2new), xy=(tim, pt2new))
        ax6.set_title('PT 2')
        ax7.clear()
        ax7.plot(xar, pt3list, linewidth=.5)
        ax7.annotate(str(pt3new), xy=(tim, pt3new))
        ax7.set_ylim([0, 1200])
        ax7.set_title('PT 3')
        ax8.clear()
        ax8.plot(xar, pt4list, linewidth=.5)
        ax8.annotate(str(pt4new), xy=(tim, pt4new))
        ax8.set_ylim([0, 1200])
        ax8.set_title('PT 4')
        ax9.clear()
        ax9.plot(xar, pt4list, linewidth=.5)
        ax9.annotate(str(forcenew), xy=(tim, forcenew))
        ax9.set_ylim([0, 10])
        ax9.set_title('Force 1')
    except:
        pass


def sendtest(ser, testpath):
    filepath = testpath
    try:
        comList = [line.rstrip('\n') for line in open(filepath)]
        numcommands = len(comList)
        print(Fore.YELLOW + comList)
        print(Fore.WHITE)
        try:
            for com in comList:
                ser.write((com+'\n'))
                time.sleep(20)  # waits so that board can catch up
            ser.write("00000000000")
        except:
            printerror("Commands Where Not Sent Please Exit Program")
    except:
        printerror("couldnt get commands from command file")


def splitdata(utfval,numbbitsthermocouple):
    try:
        val = utfval.split()
        time = float(val[0])
        tc1new = float(val[1])
        tc2new = float(val[2])
        tc3new = float(val[3])
        tc4new = float(val[4])
        pt1new = float(val[5])
        pt2new = float(val[6])
        pt3new = float(val[7])
        pt4new = float(val[8])
        forcenew = float(val[9])
    except:
        return
    return time, tc1new, tc2new, tc3new, tc4new, pt1new, pt2new, pt3new, pt4new, forcenew


def processtemp(utfvaltemp, numbbitsthermocouple):
    v = (3.3*utfvaltemp)/(2 ** 16)
    newval= (v-1.25)/(5*(10**-3))
    return newval


def processpressure1(utfvalpressure):
    maxval = 4.996
    voltage = (utfvalpressure/(2 ** 16))*3.3
    newval=((voltage*603.34657082)-33.20529496)
    return newval


def processpressure2(utfvalpressure):
    maxval = 4.988
    voltage = (utfvalpressure / (2 ** 16)) * 3.3
    newval = ((voltage*642.91697145) - 19.16682956)
    return newval

def processpressure3(utfvalpressure):
    maxval = 5.008
    voltage = (utfvalpressure / (2 ** 16)) * 3.3
    newval = ((voltage*667.90201473) - 20.17582263)
    return newval

def processpressure4(utfvalpressure):
    maxval = 5.005
    voltage = (utfvalpressure / (2 ** 16)) * 3.3
    newval = ((voltage * 585.55952032) - 13.50447115)
    return newval


def processforce(utfvalforce):
    #newval = utfvalforce*(pressuresensorrange/(2 ^ numbbitspt))
    newval = 0
    return newval


def getconfigfile(filepath):
    #Is coming in as string figure out how to split back into list
    lineList = [line.rstrip('\n') for line in open(filepath)]
    configdata = [lineList[1], lineList[3], lineList[5], lineList[7], lineList[9], lineList[11], lineList[13],
                  lineList[15], lineList[17], lineList[19], lineList[21], lineList[23], lineList[25], lineList[27]]
    print(Fore.YELLOW + configdata[0])
    print(Fore.WHITE)
    return configdata


def printerror(val):
    print(Fore.RED + val)
    print(Fore.YELLOW)


def printdatarecorded(val):
    print(Fore.CYAN + val)
    print(Fore.YELLOW)


def main(configpath):
    print(configpath)
    try:
        os.system('color')
    except:
        print("No Color")
    print(Fore.YELLOW + "Starts\n")
    print(Fore.YELLOW + configpath)
    try:
        try:
            print(Fore.YELLOW + "Starting command and")
            configdata = getconfigfile(configpath)
            print(Fore.YELLOW + "Config Gotten By Display And Control")
            print(Fore.WHITE)
            comportcontrol = configdata[5]
            baudratecontrol = configdata[6]
            numbbitsthermocouple = configdata[7]
            numbbitspressure = configdata[8]
            tempsensorrange = configdata[9]
            pressuresensorrange = configdata[10]
            forcesensorrange = configdata[11]
            numbbitsforce = configdata[12]
            testpath = configdata[13]
        except:
            printerror("Config File Could Not Be Read By Display And Control")
        try:
            ser = establishserial(comportcontrol, baudratecontrol)
            print(Fore.YELLOW + "Serial Started")
            print(Fore.WHITE)
        except:
            printerror("Serial Did Not Start")
        try:
            sendtest(ser, testpath)
        except:
            printerror("Test Not Sent")
        try:
            liveplotting(ser, numbbitsthermocouple)
        except:
            printerror("live plotting failed")
    except:
        printerror("Data Display And Control Did Not Function")


if __name__ == '__main__':
    main(sys.argv[1])
