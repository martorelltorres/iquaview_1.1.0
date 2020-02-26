# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Iqua Robotics SL

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.
"""

"""
 Process running into the AUV from boot time.
 It provides communication with the interface and allows to start launch files.
 The launch files that can be started are configured through the launch_list.xml.
"""

import socket
import sys
import os
import subprocess

from _thread  import *
from lxml import etree as ET

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8585 # Arbitrary non-privileged port
TIMEOUT = 5 # timeout connection 

class serverProcess(object):
    def __init__(self,name = None, process = None):
        self.name = name
        self.process = process
        
    def terminateProcess(self):
        if self.process is not None:
            #send 'terminate' to process
            self.process.terminate()
            #wait to finish
            self.process.wait()
    
    def get_name(self):
        return self.name

#find process 'launchName' in 'serverProcessList'
#return process if found, else None
def findProcess(serverProcessList, launchName):
    process = None
    n = 0
    while n<len(serverProcessList):
        pr = serverProcessList[n]
        if launchName == pr.name:
            process = pr
            break
        n += 1

    return process
    
def clientthread(connection):
    try:
        print( 'Client connected:', client_address)
        while True:
            recived = connection.recv(4096)
            data = recived.decode('utf-8')
            data_list = data.split()
            print (data_list)
            print( 'Received "%s"' % data)

            if data == "watchdog":
                connection.sendall("watchdogack".encode('utf-8'))
            #restart
            elif data == "restart":
                print( 'The client wants to restart the server')

                #connection.sendall("ATENTION! You are about to restart the server. Are you sure? (yes/no)")
                #data = connection.recv(1024)
                #if data == "yes":
                #    print( "Let's do it...")
                connection.sendall("The reboot process is in progress. Wait.".encode('utf-8'))
                #command to restart server
                subprocess.call("reboot")
                #else:
                #    aborted = "The reboot process has been aborted."
                #    print( "%s" % aborted)
                #    connection.sendall(aborted)
            #list of launchs in xml
            elif data =="list":

                #data = "List of launchs: \n"
                data = ""
                for launch in launches:
                    data = data + (launch[0].text+ ",")
                    #launch_data = "Description: "+ launch[0].text+ " Name: "+launch[1].text+ "\n"
                    #data = data + launch_data

                connection.sendall(data.encode('utf-8'))
            #list processes on
            elif data == "on":
                #data = "Processes ON: \n"
                data = ""
                if len(processes) == 0:
                    data = "No running processes."
                else:
                    for pr in processes:
                        #process_data = "Process Name: "+ pr.get_name() +"\n"
                        data = data + pr.get_name() + ","

                connection.sendall(data.encode('utf-8'))

            elif data:
                #TODO comprovar que nomes es vol matar un proces? o potser varis?
                if data_list[0] == "terminate":
                    if processes:
                        if len(data_list)>1:
                            tProcess = findProcess(processes, data_list[1])

                            if tProcess is not None:
                                tProcess.terminateProcess()
                                processes.remove(tProcess)
                                connection.sendall(("Launch  " + tProcess.get_name() + " is finished.").encode('utf-8'))

                            else:
                                connection.sendall("This process is not launched.".encode('utf-8'))
                        else:
                            connection.sendall("Please, enter launch to terminate.".encode('utf-8'))
                    else:
                        connection.sendall("There are no processes on.".encode('utf-8'))
                else:
                    n = 0
                    sameLaunch = False
                    while not sameLaunch and n<len(launches):
                        launch = launches[n]
                        #if launch is in xml
                        if data == launch[0].text:
                            sameLaunch = True
                            #check process in processes list
                            sProcess = findProcess(processes, data)
                            #if not exist, it can run
                            if sProcess is None:
                                message = "Running roslaunch... %s " % data
                                print( message)
                                connection.sendall(message.encode('utf-8'))
                                command = launch[1].text
                                command_list  = command.split()
                                p = subprocess.Popen(command_list)

                                sProcess = serverProcess(data, p)
                                processes.append(sProcess)
                                #,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            else:
                                connection.sendall("You can not launch that process, it's already running".encode('utf-8'))
                        n += 1

                    if not sameLaunch:
                        message = "You can't run roslaunch with: %s   " % data
                        print( message)
                        connection.sendall(message.encode('utf-8'))

            #if the client send no data, let's break while and close connection
            else:
                break
    except socket.timeout:
        print( 'Timeout error')
        connection.close()
    except socket.error as ex:
        print( ex)
        connection.close()

    finally:
        print( 'Closing the connection with client:', client_address)
        connection.close()

if __name__ == "__main__":

    #get pathname of current script
    path = os.path.realpath(__file__)
    # get dir of current script
    directory = os.path.dirname(path)
    #default launch_list path
    launch_list_path = directory + "/launch_list.xml"
    #if argument passed
    if len(sys.argv) > 1:
        # path passed as argument
        launch_list_path = sys.argv[1]
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address given on the command line
    server_address = (HOST, PORT)
    sock.bind(server_address)
    print( 'Starting up on %s port %s' % sock.getsockname())
    sock.listen(5) #5 denotes the number of clients can queue

    #parser
    parser = ET.XMLParser(remove_comments=True)
    #tree
    tree = ET.parse(launch_list_path,parser=parser)
    #root
    root = tree.getroot()
    #all matches launches
    launches = root.findall("launch")

    processes = list()
    while True:
        print( 'Waiting for a connection')
        connection, client_address = sock.accept()
        connection.settimeout(TIMEOUT)
        #creating new thread. 1st argument is a function to run, 2n argument is the tuple of arguments to the function
        start_new_thread(clientthread,(connection,))
        
