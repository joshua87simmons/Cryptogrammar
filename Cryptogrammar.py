import os
import wx
import random
import re
from random import shuffle

#/------------------ Quote Encryption -----------------\

#This is the stock alphabet that will be shuffled.
alphabet = ["z","y","x","w","v","u","t","s","r","q","p","o","n","m","l","k","j","i","h","g","f","e","d","c","b","a"]

def alpha_scramble(alpha): #This is a small function that scrambles an input alphabet.
	shuffle(alpha)
	return alpha
	
def encrypt_key(alpha): #Foil for reference; takes input scrambled alphabet
	foil = ["z","y","x","w","v","u","t","s","r","q","p","o","n","m","l","k","j","i","h","g","f","e","d","c","b","a"]
	encrypt_dict = {"a" : "a",
    			"b" : "b",
					"c" : "c",
					"d" : "d",
					"e" : "e",
					"f" : "f",
					"g" : "g",
					"i" : "i",
          				"h" : "h",
					"j" : "j",
					"k" : "k",
					"l" : "l",
					"m" : "m",
					"n" : "n",
					"o" : "o",
					"p" : "p",
					"q" : "q",
					"r" : "r",
					"s" : "s",
					"t" : "t",
					"u" : "u",
					"v" : "v",
					"w" : "w",
					"x" : "x",
					"y" : "y",
					"z" : "z"}
	x = 0
	for i in alpha:
		encrypt_dict[i] = foil[x]
		x += 1
	return encrypt_dict

def quote_grabber(quote_dict): 
	k = random.randint(1, len(quotes))
	quote = quote_dict[k]
	return quote

def crypt_generator(quote, key):
	string_list = []
	encryp_list = []
	null_list = ["*", " ", ",", ".", "?", "'", ";", "!", "", "-",":"] #list of characters not to be encrypted
	for i in quote:
		string_list.append(i) #splits the string so that we may mutate it
	for l in string_list:
		if l not in null_list:
			encryp_list.append(key[l.lower()].upper())
		else:
			encryp_list.append(l)
	return "".join(encryp_list)
			
	
	
quotes = { 1 : "That which I cannot create, I cannot understand. **Richard Feynman**",
		   2 : "Nobody cares how much you know, until they know how much you care. **Theodore Roosevelt**",
		   3 : "Courage is what it takes to stand up and speak; courage is also what it takes to sit down and listen. **Winston Churchill**",
		   4 : "Guests are like fish, they wear out their welcome after three days. **Benjamin Franklin**",
		   5 : "I do not feel obliged to believe that the same God who has endowed us with sense, reason, and intellect has intended us to forgo their use. **Galileo Galilei**",
		   6: "Fear cannot be without hope, nor hope without fear. **Baruch Spinoza**"
}

#print crypt_generator(quote_grabber(quotes), encrypt_key(alpha_scramble(alphabet)))
quote = []
quote.append(quote_grabber(quotes))
cryp = []
base = []

HOW_TO = 1


#wxPython GUI
class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title="Cryptogrammar", size=(1000, 200))
		self.CreateStatusBar()

		self.txt = wx.StaticText(self, -1, "".join(cryp), (20,30), (40,40))
		self.txt.SetForegroundColour("WHITE")

		#Menu
		filemenu = wx.Menu()
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
		menuHow = filemenu.Append(HOW_TO, "&How to Play", " How to play Cryptogrammar")
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit", " Close Cryptogrammar")
		#menuGenerate = filemenu.Append(wx.ID_NONE, "&Generate New", "Generate a new cryptogram")

		#Menubar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)


		#Buttons
		GenButton = wx.Button(self, -1, "&Generate Cryptogram")
		DecButton = wx.Button(self, -1, "&Decode Letter")
		ClearButton = wx.Button(self, -1, "&Clear Changes")
		AnswerButton = wx.Button(self, -1, "Show &Answer")
		but_list = [GenButton, DecButton, ClearButton, AnswerButton]

		#Sizers
		self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		for i in range(0, 4):
			self.sizer2.Add(but_list[i], 1, wx.EXPAND)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.txt, 1, wx.EXPAND)
		self.sizer.Add(self.sizer2, 0, wx.EXPAND)

		#Events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnHow, menuHow)
		self.Bind(wx.EVT_BUTTON, self.OnGen, GenButton)
		self.Bind(wx.EVT_BUTTON, self.OnDec, DecButton)
		self.Bind(wx.EVT_BUTTON, self.OnAnswer, AnswerButton)
		self.Bind(wx.EVT_BUTTON, self.OnClear, ClearButton)


		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.SetTitle("Cryptogrammar")
		self.Centre()

	def OnAbout(self, e):
		dlg = wx.MessageDialog(self, "A program for generating random cryptograms.\n\n\n\nCopyright 2014 Joshua Simmons\nVersion 0.1.0", "About Cryptogrammar", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self, e):
		self.Close(True)

	def OnHow(self, e):
		dlg = wx.MessageDialog(self, "HOW TO PLAY:\n\n\n--\tPress the 'Generate Cryptogram' to spawn a cryptogram.\n\n--\tUse the 'Decode Letter' to replace an encrypted letter with a letter of your choice. 'Decoded' letters will be lowercase to distinguish them.\n\n--\tUse the 'Clear Changes' button to reset the puzzle.\n\n--\t'Show Answer' solves the puzzle!", "How to play Cryptogrammar", wx.OK) 
		dlg.ShowModal()
		dlg.Destroy()

	def OnDec(self, e):
		global cryp
		dlg = wx.TextEntryDialog(self, "Which letter do you wish to change? Use format: 'a=e'", "Decode Letter", "")
		dlg.ShowModal()
		decode = dlg.GetValue()
		#Text entry filter
		match = re.search(r'\w+=\w+|^\d*$', decode)
		if not match:
			err = wx.MessageDialog(self, "That is not a correct entry format.", "Entry Error", style=wx.ICON_HAND)
			err.ShowModal()
			#Letter replacement
		else:
			origin = decode[0].upper()
			replace = decode[2].upper()
			for n in range(0, len(cryp)):
				if cryp[n] == origin:
					cryp[n] = replace.lower()
			self.txt.SetLabel("".join(cryp))
			self.sizer.Layout()

		dlg.Destroy()

	def OnGen(self, e):
		global crpqut
		global cryp
		global base

		quote.pop()
		quote.append(quote_grabber(quotes))
		crpqut = crypt_generator(quote[0], encrypt_key(alpha_scramble(alphabet)))
		cryp = []
		base = []
		for i in crpqut:
			cryp.append(i)
			base.append(i)
		self.txt.SetLabel("".join(cryp))
		self.txt.SetForegroundColour("WHITE")
		self.sizer.Layout()

	def OnAnswer(self, e):
		global base
		if len(base) == 0:
			err = wx.MessageDialog(self, "You haven't generated a puzzle yet, doofus!", "Encryption Error", style=wx.ICON_HAND)
			err.ShowModal()
		else:
			self.txt.SetLabel(quote[0])
			self.txt.SetForegroundColour("BLUE")
			self.sizer.Layout()

	def OnClear(self, e):
		global base
		self.txt.SetLabel("".join(base))
		self.txt.SetForegroundColour("WHITE")
		self.sizer.Layout()

app = wx.App(False)
frame = MainWindow(None, "Cryptogrammar")
frame.Show()
app.MainLoop()
