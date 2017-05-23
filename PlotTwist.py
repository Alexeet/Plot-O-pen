# coding: utf8

from PIL import Image
import tkinter as tk
from tkinter.filedialog import askopenfilename
import math
import serial
from serial.tools import list_ports


sqrt = lambda x:x**0.5


#Initialisation de la liaison série
n=0
print("Ports disponibles :")
for i in list_ports.comports():
	n+=1
	print(str(n)+" : "+i.description)
	
ser = serial.Serial(input("Port :"), 9600, timeout=0)
ser.open()

print("Connexion établie.")

def findStartingPoint(a,b,c):
		#Cherche un point à l'extrémité d'un segment dans l'image
	for x in range(1,b-1):
		for y in range(1,c-1):
			if a[x,y] is 0:
				pass
			elif sum(a[x-1+b%3,y-1+b//3] for b in range(0,9))>=3:
				pass
			else:
				return x,y
	return None


def findRoute(a,b,c):
	order = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
	for d in order:
		if a[b+d[0],c+d[1]]==1:
			return (b+d[0],c+d[1])
	return None

def findPoint(a,b,c,d,e):
	x_,y_,dist=0,0,math.inf	#On utilise de grands nombres au début
	for x in range(1,b-1):
		for y in range(1,c-1):
			if border_img[x,y]==0:  #Recherche d'un pixel de bordure
				pass
			elif max(abs(d-x),abs(e-y))<dist:
				dist=max(abs(d-x),abs(e-y))
				x_,y_=x,y
		
		return x_,y_
	return None #Aucun pixel trouvé, l'image est vide


root = tk.Tk()
root.withdraw()
file_path = askopenfilename()   #Demande d'un fichier

img = Image.open(file_path)
print("Image size : {}×{}".format(img.size[0],img.size[1]))
image = img.load()      #Chargement de l'image en pixelarray

border = Image.new("1",(img.size[0],img.size[1]))
border_img = border.load()      #Création d'une image vide "border" et chargement de cette image

#Génération des bordures
print("Génération des bordures...")
for x in range(img.size[0]):
	for y in range(img.size[1]):
		if(image[max(x-1,0),y]+image[x,max(y-1,0)]+image[min(x+1,img.size[0]-1),y]+image[x,min(y+1,img.size[1]-1)])<4 and image[x,y]==1:
		 #Si un pixel n'est pas entouré de quatre autres pixels du même type
			border_img[x,y]=1

start = findPoint(border_img,border.size[0],border.size[1],border.size[0]//2,border.size[1]//2)

finished = False

route = [start]
x,y = start
print("Génération chemin..")

while not finished:
	result = findRoute(border_img,x,y)  #Recherche d'un point adjacent
	if result is not None:
		border_img[x,y] = 0
		route.append(result)
		x,y = result
	else:
		result = findStartingPoint(border_img,border.size[0],border.size[1])    #Sinon, recherche d'un trait "brisé"
		if result is not None:
			border_img[x,y] = 0
			route.append(result)
			x,y = result
		else:
			result = findPoint(border_img,border.size[0],border.size[1],x,y)    #Sinon, recherche d'un pixel dans l'image
			if result is not None:
				border_img[x,y] = 0
				route.append(result)
				x,y = result
			else:
				finished = True

#Maintenant, la liste route contient les coordonnées à visiter.

route = [(0,0)]+route
travel=[]
x_,y_=route[0]
altroute = list()

for i in range(len(route)-1):
	x,y=route[i]
	altroute.append((x-x_,y-y_))
	if sqrt((x-x_)**2+(y-y_)**2)>sqrt(2):
		travel.append(True)
	else:
		travel.append(False)
	x_,y_=x,y

infill = img
for x in range(img.size[0]):
	for y in range(img.size[1]):
		0


#READER

from tkinter import *
from time import sleep

master = Tk()
quit = lambda :master.destroy()
master.protocol('WM_DELETE_WINDOW', quit)

c = Canvas(master, width=border.size[0], height=border.size[1], bg="#131313")
c.pack()

sleep(1)
y,x=route[0]
travellen=0
for i in range(len(altroute)):

	ser.write("X{} Y{} E{}".format(point[0],point[1],travel[i]))

	point=altroute[i]
	if travel[i]:
		color="#BBBB55"
		travellen+=sqrt((x-point[0])**2+(y-point[1])**2)
	else:
		color="white"
	c.create_line(y,x,y+point[0],x+point[1],fill=color)
	y+=point[0]
	x+=point[1]
	master.update()
	sleep(0.001)

print("Travel length:%s"%travellen)
master.mainloop()
input()
