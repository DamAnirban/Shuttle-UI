import socket
import pickle
from tkinter import *
from tkinter import scrolledtext


cart = 0
count = 0
goal_flag = 0
cart_flag = 0
waypoint_x = []
waypoint_y = []
delta = []
goals = [4, 4, 4]
carts = ["192.168.43.159", "192.168.43.159", "192.168.43.159"]
IP = "127.0.0.1"
UDP_PORT = 2055

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock.sendto(MESSAGE, (UDP_IP1, UDP_PORT))
window = Tk()
window.title("INTERFACE")
window.geometry('500x500')

#*****************************************radio button 1********************************************
def clicked1():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	cart_flag = 0
	print ("cart_flag =  ", cart_flag)
	txt.insert(INSERT , "Cart chosen = ")
	txt.insert(INSERT , str(cart_flag) + '\n')
	
def clicked2():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	cart_flag = 1
	print ("cart_flag =  ", cart_flag)
	txt.insert(INSERT , "Cart chosen = ")
	txt.insert(INSERT , str(cart_flag) + '\n')
	
def clicked3():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	cart_flag = 2
	print ("cart_flag =  ", cart_flag)
	txt.insert(INSERT , "Cart chosen = ")
	txt.insert(INSERT , str(cart_flag)+ '\n')
#*****************************************radio button 2********************************************	
def clicked4():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	goal_flag = 0
	print ("goal_flag =  ", goal_flag)
	waypoint_x = [0 , 0 , 0   , -4 ]
	waypoint_y = [2 , 6 , 8.5 , 12 ]
	delta =      [0 , 0 , 0   , 180]
	txt.insert(INSERT , "Route chosen = ")
	txt.insert(INSERT , str(goal_flag)+ '\n')
		
def clicked5():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	goal_flag = 1
	print ("goal_flag =  ", goal_flag)
	waypoint_x = [0 , 0 , 0   , -4 ]
	waypoint_y = [2 , 6 , 8.5 , 12 ]
	delta =      [0 , 0 , 0   , 180]
	txt.insert(INSERT , "Route chosen = ")
	txt.insert(INSERT , str(goal_flag)+ '\n')
	
def clicked6():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	goal_flag = 2
	print ("goal_flag =  ", goal_flag)
	waypoint_x = [0 , 0 , 0   , -4 ]
	waypoint_y = [2 , 6 , 8.5 , 12 ]
	delta =      [0 , 0 , 0   , 180]
	txt.insert(INSERT , "Route chosen = ")
	txt.insert(INSERT , str(goal_flag)+ '\n')
#*****************************************box buttons***********************************************	
def clicked7():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	txt.insert(INSERT , "\t ******Initialized****** \n ")
	nop = 0

def clicked8():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	
	if count < goals[goal_flag]:
		print (" ", count)
		print (" ", goal_flag)
		print (" ", goals[goal_flag])
		print (" waypoint_x[count] = ", waypoint_x[count])
		print (" waypoint_Y[count] = ", waypoint_y[count])
		print (" carts[cart_flag] ", carts[cart_flag])
		message1 = []
		message1.append(waypoint_x[count])
		message1.append(waypoint_y[count])
		message1.append(delta[count])
		MESSAGE = pickle.dumps(message1)
		sock.sendto(MESSAGE, (IP, UDP_PORT))
		txt.insert(INSERT , "message sent as follows : \n ")
		txt.insert(INSERT , '\t' + str(waypoint_x[count])+ '\n')
		txt.insert(INSERT , '\t' + str(waypoint_y[count])+ '\n')
		txt.insert(INSERT , '\t' + str(delta[count])+ '\n')
		txt.see("end")
		count += 1
	else:
		txt.insert(INSERT , "Goal overflow \n ")

def clicked9():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	nop = 0
	print ("###goal_flag =  ", goal_flag)
	print ("###cart_flag =  ", cart_flag)
	
def clicked10():
	global cart, count, goal_flag, cart_flag, waypoint_x, waypoint_y, delta
	nop = 0
	
rad1 = Radiobutton(window,text=' CART1', value=1, width = 10, variable = 1, command = clicked1).grid(column=1, row=0)
rad2 = Radiobutton(window,text=' CART2', value=2, width = 10, variable = 1, command = clicked2).grid(column=2, row=0)
rad3 = Radiobutton(window,text=' CART3', value=3, width = 10, variable = 1, command = clicked3).grid(column=3, row=0)

rad4 = Radiobutton(window,text=' ROUTE1', value=4, width = 10, variable = 2, command = clicked4).grid(column=1, row=2)
rad5 = Radiobutton(window,text=' ROUTE2', value=5, width = 10, variable = 2, command = clicked5).grid(column=2, row=2)
rad6 = Radiobutton(window,text=' ROUTE3', value=6, width = 10, variable = 2, command = clicked6).grid(column=3, row=2)

btn = Button(window, text="START",  command=clicked7).grid(column=2, row=3)
btn = Button(window, text="NEXT_GOAL",  command=clicked8).grid(column=1, row=4)
btn = Button(window, text="SKIP_GOAL",  command=clicked9).grid(column=3, row=4)
btn = Button(window, text="STOP",  command=clicked10).grid(column=2, row=5)

txt = scrolledtext.ScrolledText(window,width=40,height=10)
txt.grid(column=2,row=6)
txt.see("end")

window.mainloop()

