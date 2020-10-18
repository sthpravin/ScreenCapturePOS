#!/usr/bin/python

import socket
import time
import sys
import threading
from PyQt5 import QtCore, QtWidgets
#calculate LRC
#Set LRC = 0
#For each character c in the string 
#Do
#Set LRC = LRC XOR c
#End Do

#str
def h_lrc(s):
    lrc = 0
    #remove STX
    if s[:4] == "[02]":
        s = s[4:]
    #calculate LRC
    for i in range(len(s)):
        j = s[:2]
        if not j:
            break
        if j[:1] == '[' and s[3:4] == ']':
            temp_i = int(s[1:3],16)
            lrc ^= temp_i
            s = s[4:]
        else:
            lrc ^= ord(s[:1])
            s = s[1:]
    return chr(lrc)

class ecrDemo(QtCore.QThread):

    response_signal = QtCore.pyqtSignal(str)
    status_signal = QtCore.pyqtSignal(str)
    #init
    def __init__(self):
        super().__init__()
        self.ecrVersion = "1.30"
        self.STX = "[02]"
        self.ETX = "[03]"
        self.FS = "[1c]"
        self.US = "[1f]"
        
        self.posurl = ""
        self.posport = ""
        self.response = ""
        self.amount = 0
        self.CommandIdex = 4

    def run(self):
        req = ''
        CommandIdex = self.CommandIdex
        amount = self.amount
        print("amt in run:::", amount)
        if(CommandIdex == 1):
            req = self.pack_message(self.pack_initCommand())
        elif(CommandIdex == 2):
            req = self.pack_message(self.pack_transCommand("CREDIT", "SALE", amount))
        elif(CommandIdex == 3):
            req = self.pack_message(self.pack_transCommand("CREDIT", "ADJUST", amount))
        elif(CommandIdex == 4):
            req = self.pack_message(self.pack_transCommand("DEBIT", "SALE", amount))
        elif(CommandIdex == 5):
            req = self.pack_message(self.pack_transCommand("EBT", "SALE", amount))
        elif(CommandIdex == 6):
            req = self.pack_message(self.pack_transCommand("GIFT", "SALE", amount))
        elif(CommandIdex == 7):
            req = self.pack_message(self.pack_transCommand("LOYALTY", "SALE", amount))
        else:
            pass

        if(req):
            self.sendMessagetopos(req.encode())

        # terminate the thread
        # self.exit()

    def pack_initCommand(self):
        return "A00" + self.FS + self.ecrVersion

    def pack_transCommand(self, edcType, transType, amount):
        
        message = ""
        
        if(edcType == "CREDIT"):
            if(transType == "SALE"):
                message = "T00" + self.FS + self.ecrVersion + self.FS + "01" + self.FS
            elif(transType == "ADJUST"):
                message = "T00" + self.FS + self.ecrVersion + self.FS + "06" + self.FS
            else:
                message = "T00" + self.FS + self.ecrVersion + self.FS + "01" + self.FS

            #message += Amount Information
            message += amount #--Amount
            message += self.FS
            ##message += Account Information
            message += self.FS
            #message += Trace Information
            message += "1"   #--ECR reference number
            message += self.FS
            ##message += AVS Information
            message += self.FS
            ##message += Cashier Information
            message += self.FS
            ##message += Commercial Information Information
            message += self.FS
            ##message += MOTO/E-commerce
            message += self.FS
            ##message += Additional Information
        #debit, ebt, gift, loyalty
        else:
            if(edcType == "DEBIT"):
                message = "T02"
            elif(edcType == "EBT"):
                message = "T04"
            elif(edcType == "GIFT"):
                message = "T06"
            elif(edcType == "LOYALTY"):
                message = "T08"
            else:
                message = "T02"
            
            message += self.FS + self.ecrVersion + self.FS + "01" + self.FS
            #message += Amount Information
            message += amount #--Amount
            message += self.FS
            ##message += Account Information
            message += self.FS
            #message += Trace Information
            message += "1"   #--ECR reference number
            message += self.FS
            ##message += Cashier Information
            message += self.FS
            ##message += Additional Information
            print("message in pack_transCommand:::", message)
        return message

    #ecr ---> request message  ---> pos terminal
    #ecr <--- ACK              <--- pos terminal
    #ecr <--- response message <--- pos terminal
    #ecr ---> ACK              ---> pos terminal
    #ecr <--- EOT              <--- pos terminal
    def sendMessagetopos(self, message):
        data = ''
        response = ""
        #resend times
        t_resend = 0
        try:
            stage_value=0
            # print('Send===>: ',message)
            print("socket address {}:{}".format(self.posurl, self.posport))
            connstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # make a TCP/IP socket object
            connstream.settimeout(60) #60 seconds
            connstream.connect((self.posurl, self.posport)) # connect to server machine + port
            connstream.send(message) # send message to server over socket
            stage_value += 1

            while True:
                self.status_signal.emit("Processing!!!")

                #wait to receive
                data = connstream.recv(1024) # receive line from server: up to 1k
                print('===>Receive: ',data) # bytes are quoted, was `x`, repr(x)
                
                if t_resend > 3:
                    break
                
                #wait ack
                if stage_value == 1:
                    if data == b'\x06':
                        stage_value += 1
                    else:
                        connstream.send(message)
                        t_resend += 1
                    
                #wait response, and send ack to pos terminal
                elif stage_value == 2:
                    if data[:1] == b"\x02":
                        stage_value += 1
                        connstream.send(b'\x06')
                        print('Send===>: ',r'b\x06')
                        print("true ::", data, type(data))
                        res = data.decode()
                        print("res:::", res)
                        sp = len("\x020\x1cT03\x1c1.44\x1c100001\x1c")
                        res = res[sp:]
                        ep = res.index("\x03")
                        response = res[:ep]
                        print("response:::", response)
                    else:
                        #send NAK
                        connstream.send(b'\x15')
                        print('Send===>: ',r'b\x15')
                        t_resend += 1
                        

                #wait EOT
                elif stage_value == 3:
                    if data == b'\x04':
                        stage_value += 1
                        break
                    else:
                        connstream.send(b'\x06')
                        print('Send===>: ',r'b\x06')
                        t_resend += 1
                    
                else:
                    pass
                
            
        except socket.timeout:
            pass
        finally:
            # close socket
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()

            self.status_signal.emit(response)

    #pack message
    def pack_message(self, s_part):
        #STX ... ETX + LRC
        s = self.STX + s_part[:] + self.ETX
        #get LRC
        lrc = h_lrc(s)
        
        s_header = "\x02"
        s_trailer = "\x03"
        s_fs = "\x1c"
        s_us = "\x1f"
        s = s.replace("[1c]",s_fs)
        s = s.replace("[1f]",s_us)
        s = s.replace("[02]",s_header)
        s = s.replace("[03]",s_trailer)
        
        s += lrc
        return s

def main():
    # myEcrDemo = ecrDemo("192.168.5.121", 10009)
    myEcrDemo = ecrDemo("127.0.0.1", 10009)
    ##init
    #myEcrDemo.processCommand(1)
    ##credit sale
    #myEcrDemo.processCommand(2)
    ##credit adjust tip
    #myEcrDemo.processCommand(3)
    ##debit sale
    myEcrDemo.processCommand(4, 100)
    ##ebt sale
    #myEcrDemo.processCommand(5)
    ##gift redeem
    #myEcrDemo.processCommand(6)

#run
if __name__ == "__main__":
    main()

# 192.168.20.252 , 9013
# st.1directconnect.com ,  443


# '\x020\x1cT03\x1c1.44\x1c100001\x1cTIMEOUT\x03 '
# '\x020\x1cT03\x1c1.44\x1c100003\x1cAMOUNT INVALID\x03\x04'
# '\x020\x1cT03\x1c1.44\x1c100019\x1cTRACK INVALID\x03L'