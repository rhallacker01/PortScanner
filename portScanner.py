import sys 
import socket
from datetime import datetime

#TODO impelemnt a method that multithreads the portscan if the range is larger than x ports;
    #Use a queue to schedule the scans for the threads

#Small Scan method used for scans under 20 ports
def smallScan(ipaddress, portFirst, portLast):
    try:
        for port in range(portFirst, portLast):
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

#Banner
def printBanner():
    print("-" * 50)
    print("Scanning target " + ipaddress + " Port Range: " + str(portFirst) + ", " + str(portLast))
    now = datetime.now()
    print("time started: " + now.strftime("%m-%d-%Y %H:%M:%S"))
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
portList = portString.split(',') #splits the input at the comma
portFirst = int(portList[0])
portLast = int(portList[1])


#run the scan
if (portLast - portFirst) < 25:
    smallScan(ipaddress, portFirst, portLast)
else:
    print("Wait for large scan to be implemented")
    sys.exit

