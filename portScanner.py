import sys 
import socket
from datetime import datetime
import time #use this to test the efficiency of the multithread
import concurrent.futures
import itertools

#TODO impelemnt a method that multithreads the portscan if the range is larger than x ports;
    #Use a queue to schedule the scans for the threads

#Small Scan method used for scans under 20 ports
def smallScan(ipaddress, portFirst, portLast):
    try:
        for port in range(portFirst, portLast + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket object AF_INET = ipv4, SOCKSTREAM = port
            socket.setdefaulttimeout(1)
            result = s.connect_ex((ipaddress,port))
            if result == 0:
                print("Port {} is open".format(port))
            else:
                print("Port {} is closed".format(port))
            s.close()
        print("Scan Complete")

    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit

    except socket.error:
        print("Could not connect to server.")
        sys.exit

#Single Port Scan
def singlePortScan(ipaddress, portNumber):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ipaddress,portNumber))
    if result == 0:
        portState = ("Port {} is open".format(portNumber))
    else:
        portState = ("Port {} is closed".format(portNumber))
    s.close()
    return portState
    
#Multithreaded Scan
def multiThreadScan(ipaddress, portFullList):
    with concurrent.futures.ThreadPoolExecutor() as executor:           #Context Manager
        results = executor.map(singlePortScan, itertools.repeat(ipaddress), portFullList) #map returns the results in the order they are started, not a future object
        print(*results, sep = "\n")
        
#Banner
def printBanner():
    print("-" * 50)
    print("Scanning target " + ipaddress + " Port Range: " + str(portFirst) + ", " + str(portLast))
    now = datetime.now()
    print("Time started: " + now.strftime("%m-%d-%Y %H:%M:%S"))
    print("-" * 50)

#MAIN METHOD---------------------------------------------------------------------------------------------------------------------
    
#get hostname from user and convert to IPv4
print("Enter an IPv4 address or Hostname")
hostname = input()
try:
    ipaddress = socket.gethostbyname(hostname)

except:
    print("Hostname could not be resolved")
    sys.exit()


#Get the range of ports. (Messing with functions to seperate the string, rather then having the user just input the numbers seperatly)
print("Enter the range of ports you would like to scan ex: 1,65535")
portString = input()
portList = portString.split(',') #splits the input at the comma; saves as list
portFirst = int(portList[0])
portLast = int(portList[1])
portFullList = list(range(portFirst, portLast + 1))


#run the scan
printBanner()
start = time.perf_counter()
if (portLast - portFirst) < 25:
    smallScan(ipaddress, portFirst, portLast)
else:
    multiThreadScan(ipaddress, portFullList)

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')

