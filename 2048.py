#!/usr/bin/env python

import tkinter as tk
from tkinter import font
from tkinter import messagebox
import tkMessageBox
import random
import numpy as np
import sys

CELL_COLOR_DICT = { 2:"#82c3b8", 4:"#d6ad7c", 8:"#ffc125", 16:"#d89000", \
                    32:"#a04c03", 64:"#704013", 128:"#990000", 256:"#800000", 512:"#4b052e", \
					1024:"#4d0203", 2048:"#101010" }

window=tk.Tk()
window.title("2048")
window.geometry("400x400")
canvas = tk.Canvas(window,height=400,width=400)

def initial():
	for i in range(4):
		for j in range(4):
			tile = canvas.create_rectangle(0+i*100,0+j*100,100+i*100,100+j*100,fill='white')
	text=[]
	for i in range(4):
		text.append([None] * 4)
	c=0
	while(True):
		x=random.randint(0,15)
		i,j=x%4,x/4
		if text[i][j]==None:
			tex = canvas.create_text((50+j*100,50+i*100),font=fo,text=str(2))
			text[i][j]=2
			c+=1
		if(c==2):
			break
	return text

def move_left(event):
	global text
	text=compress(text)
	text=merge(text)
	text=compress(text)
	text=grid(text)
	
	text=add_one(text)
	color()
	check()

def move_right(event):
	global text
	mat=np.fliplr(text)
	mat=compress(mat)
	mat=merge(mat)
	mat=clear(mat)
	mat=compress(mat)
	mat=np.fliplr(mat)
	mat=clear(mat)
	text=grid(mat)

	text=add_one(text)
	color()
	check()

def move_up(event):
	global text
	mat=transpose(text)
	mat=compress(mat)
	mat=merge(mat)
	mat=clear(mat)
	mat=compress(mat)
	mat=transpose(mat)
	mat=clear(mat)
	text=grid(mat)

	text=add_one(text)
	color()
	check()

def move_down(event):
	global text
	mat=transpose(text)
	mat=np.fliplr(mat)
	mat=compress(mat)
	mat=merge(mat)
	mat=clear(mat)
	mat=compress(mat)
	mat=np.fliplr(mat)
	mat=transpose(mat)
	mat=clear(mat)
	text=grid(mat)

	text=add_one(text)
	color()
	check()

def color():
	for i in range(4):
		for j in range(4):
			if text[i][j]!=None:
				tile = canvas.create_rectangle(0+j*100,0+i*100,100+j*100,100+i*100,fill=CELL_COLOR_DICT[text[i][j]])
				tex = canvas.create_text((50+j*100,50+i*100),font=fo,text=str(text[i][j]))

def add_one(mat):
	k=0
	while(True):
		x=random.randint(0,15)
		i,j=x%4,x/4
		if mat[i][j]==None:
			tex = canvas.create_text((50+j*100,50+i*100),font=fo,text=str(2))
			mat[i][j]=2
			k+=1
		if(k==1):
			return mat

def transpose(mat):
	new=[]
	for i in range(len(mat[0])):
		new.append([])
		for j in range(len(mat)):
			new[i].append(mat[j][i])
	return new

def clear(mat):
	for i in range(4):
		for j in range(4):
			if mat[i][j]==None:
				tile = canvas.create_rectangle(0+j*100,0+i*100,100+j*100,100+i*100,fill='white')
	return mat

def compress(mat):
	new=[[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
	done=False
	for i in range(4):
		count=0
		for j in range(4):
			if mat[i][j]!=None:
				new[i][count]=mat[i][j]
				tile = canvas.create_rectangle(0+j*100,0+i*100,100+j*100,100+i*100,fill='white')
				if j!=count:
					done=True
				count+=1
	return new

def merge(mat):
	done=False
	for i in range(4):
		for j in range(3):
			if mat[i][j]==mat[i][j+1] and mat[i][j]!=None:
				mat[i][j]*=2
				tile = canvas.create_rectangle(0+j*100,0+i*100,100+j*100,100+i*100,fill='white')
				tile = canvas.create_rectangle(0+(j+1)*100,0+i*100,100+(j+1)*100,100+i*100,fill='white')
				mat[i][j+1]=None
				done=True
	return mat

def grid(mat):
	for i in range(4):
		for j in range(4):
			if(mat[i][j]!=None):
				tex = canvas.create_text((50+j*100,50+i*100),text=str(mat[i][j]))
	return mat

def check():
	global text
	x=0
	for i in range(4):
		for j in range(4):
			if(text[i][j]==2048):
				tkMessageBox.showinfo("Congrats! You completed the game.","Phir se karo")
				text=initial()
			if text[i][j]!=None:
				x+=1
	if x==16:
		answer = messagebox.askyesno("Congrats! You completed the game.","Do you want to try again?")
		if answer==True:
			text=initial()
			color()
		else:
			sys.exit(0)

fo=font.Font(family='Purisa',size=14,weight='bold')


text = initial()
color()

window.bind('<Left>',move_left)
window.bind('<Right>',move_right)
window.bind('<Up>',move_up)
window.bind('<Down>',move_down)

canvas.pack()
window.mainloop()
