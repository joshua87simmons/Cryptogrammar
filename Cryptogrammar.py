import os
import random
import wx
import re
from random import shuffle, randrange

#Fisher-Yates Shuffle Implementation. 'encrypt_key' will take the output of
#'shuffle_alphabet' as its argument. 'encrypt_key' will then create a different
#encryption key each time it's called. When 'generate_cryptoquote' is fed
#a quote and an encryption key from 'encrypt_key', it will generate a new
#random cryptogram each time.

def shuffle_alphabet():
	alphabet = ["z","y","x","w","v","u","t","s","r","q","p","o","n",
	"m","l","k","j","i","h","g","f","e","d","c","b","a"]

	i = len(alphabet)
	while i > 1:
		i = i -1
		j = randrange(i)
		alphabet[j], alphabet[i] = alphabet[i], alphabet[j]
	return alphabet

def encrypt_key(alphabet):
	encrypt_dict = {		"a" : "a",
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
											"z" : "z"
			}
	x = 0
	for i in encrypt_dict:
		encrypt_dict[i] = alphabet[x]
		x += 1
	return encrypt_dict

def quote_fetch(quote_dict): #Grab a random quote from supplied dictionary.
	k = random.randint(1, len(quotes))
	quote = quote_dict[k]
	return quote

def generate_cryptogram(quote, key):
	string_list = []
	encryp_list = []
	null_list = ["*", " ", ",", ".", "?", "'", ";", "!", "", "-",":"] #List of characters not to be encrypted
	for character in quote:
		string_list.append(character) #Splits the string to mutate.
	for i in string_list:
		if i not in null_list:
			encryp_list.append(key[i.lower()].upper())
		else:
			encryp_list.append(i)
	return "".join(encryp_list)



quotes = { 1 : "That which I cannot create, I cannot understand. **Richard Feynman**",
			2 : "Nobody cares how much you know, until they know how much you care. **Theodore Roosevelt**",
			3 : "Courage is what it takes to stand up and speak; courage is also what it takes to sit down and listen. **Winston Churchill**",
			4 : "Guests are like fish, they wear out their welcome after three days. **Benjamin Franklin**",
			5 : "I do not feel obliged to believe that the same God who has endowed us with sense, reason, and intellect has intended us to forgo their use. **Galileo Galilei**",
			6: "Fear cannot be without hope, nor hope without fear. **Baruch Spinoza**"
}


HOW_TO = 1


class MainWindow(wx.Frame):

	quote = []
	quote.append(quote_fetch(quotes))
	cryptoquote = []
	split_cryptoquote = []
	base_copy = []
	split_buffer = []
	buffer_origin = None
	buffer_replace = None
	quote_altered = False #Becomes true after first decoding change.

	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title="Cryptogrammar", size=(1000, 200))
		self.CreateStatusBar()

		self.txt = wx.StaticText(self, -1, "".join(MainWindow.base_copy), (20,30), (40,40))
		self.txt.SetForegroundColour("WHITE")

		#Menu
		filemenu = wx.Menu()
		menu_about = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
		menu_how = filemenu.Append(HOW_TO, "&How to Play", " How to play Cryptogrammar")
		menu_exit = filemenu.Append(wx.ID_EXIT,"E&xit", " Close Cryptogrammar")
		#menuGenerate = filemenu.Append(wx.ID_NONE, "&Generate New", "Generate a new cryptogram")

		#menu_bar
		menu_bar = wx.MenuBar()
		menu_bar.Append(filemenu, "&File")
		self.SetMenuBar(menu_bar)


		#Buttons
		generate_button = wx.Button(self, -1, "&Generate Cryptogram")
		decode_button = wx.Button(self, -1, "&Decode Letter")
		clear_all_button = wx.Button(self, -1, "&Clear All Changes")
		clear_last_button = wx.Button(self, -1, "Clear &Last Change")
		answer_button = wx.Button(self, -1, "Show &Answer")
		but_list = [generate_button, decode_button, clear_all_button, clear_last_button, answer_button]

		#Sizers
		self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		for i in range(0, 5):
			self.sizer2.Add(but_list[i], 1, wx.EXPAND)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.txt, 1, wx.EXPAND)
		self.sizer.Add(self.sizer2, 0, wx.EXPAND)

		#Events
		self.Bind(wx.EVT_MENU, self.on_about, menu_about)
		self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
		self.Bind(wx.EVT_MENU, self.on_how, menu_how)
		self.Bind(wx.EVT_BUTTON, self.on_generate_quote, generate_button)
		self.Bind(wx.EVT_BUTTON, self.on_decode, decode_button)
		self.Bind(wx.EVT_BUTTON, self.on_answer, answer_button)
		self.Bind(wx.EVT_BUTTON, self.on_clear_all, clear_all_button)
		self.Bind(wx.EVT_BUTTON, self.on_clear_last, clear_last_button)


		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.SetTitle("Cryptogrammar")
		self.Centre()

	def on_about(self, e):
		dialogue = wx.MessageDialog(self, "A program for generating random cryptograms.\n\n\n\nCopyright 2014 Joshua Simmons\nVersion 0.1.0", "About Cryptogrammar", wx.OK)
		dialogue.ShowModal()
		dialogue.Destroy()

	def on_exit(self, e):
		self.Close(True)

	def on_how(self, e):
		dialogue = wx.MessageDialog(self, "HOW TO PLAY:\n\n\n--\tPress the 'Generate Cryptogram' to spawn a cryptogram.\n\n--\tUse the 'Decode Letter' to replace an encrypted letter with a letter of your choice. 'Decoded' letters will be lowercase to distinguish them.\n\n--\tUse the 'Clear Changes' button to reset the puzzle.\n\n--\t'Show Answer' solves the puzzle!", "How to play Cryptogrammar", wx.OK)
		dialogue.ShowModal()
		dialogue.Destroy()

	def on_decode(self, e):
		dialogue = wx.TextEntryDialog(self, "Which letter do you wish to change? Use format: 'a=e'", "Decode Letter", "")
		dialogue.ShowModal()
		decode = dialogue.GetValue()
		#Text entry filter
		match = re.search(r'\w+=\w+|^\d*$', decode)
		if not match:
			err = wx.MessageDialog(self, "That is not a correct entry format.", "Entry Error", style=wx.ICON_HAND)
			err.ShowModal()
			#Letter replacement
		else:
			origin = decode[0].upper()
			replace = decode[2].upper() #For resetting changes one at a time.
			MainWindow.split_buffer.append(MainWindow.split_cryptoquote[:])
			for n in range(0, len(MainWindow.split_cryptoquote)):
				if MainWindow.split_cryptoquote[n] == origin:
					MainWindow.split_cryptoquote[n] = replace.lower()
			MainWindow.quote_altered = True
			origin = None
			replace = None
			self.txt.SetLabel("".join(MainWindow.split_cryptoquote))
			self.sizer.Layout()


		dialogue.Destroy()

	def on_generate_quote(self, e):

		MainWindow.quote.pop()
		MainWindow.quote.append(quote_fetch(quotes))
		MainWindow.cryptoquote = generate_cryptogram(MainWindow.quote[0], encrypt_key(shuffle_alphabet()))
		MainWindow.split_cryptoquote = []
		MainWindow.base_copy = []
		for i in MainWindow.cryptoquote:
			MainWindow.split_cryptoquote.append(i)
			MainWindow.base_copy.append(i)
		self.txt.SetLabel("".join(MainWindow.split_cryptoquote))
		self.txt.SetForegroundColour("BLACK")
		self.sizer.Layout()

	def on_answer(self, e):
		if len(MainWindow.base_copy) == 0:
			err = wx.MessageDialog(self, "You haven't generated a puzzle yet, doofus!", "Encryption Error", style=wx.ICON_HAND)
			err.ShowModal()
		else:
			self.txt.SetLabel(MainWindow.quote[0])
			self.txt.SetForegroundColour("BLUE")
			self.sizer.Layout()

	def on_clear_last(self, e):
		if len(MainWindow.split_buffer) > 0:
			previous_cryptoquote = MainWindow.split_buffer.pop()
			self.txt.SetLabel("".join(previous_cryptoquote))
			MainWindow.split_cryptoquote = previous_cryptoquote[:]
		self.txt.SetForegroundColour("BLACK")
		self.sizer.Layout()


	def on_clear_all(self, e):
		MainWindow.split_cryptoquote = MainWindow.base_copy[:]
		MainWindow.quote_altered = False
		MainWindow.split_buffer = []
		self.txt.SetLabel("".join(MainWindow.base_copy))
		self.txt.SetForegroundColour("BLACK")
		self.sizer.Layout()


app = wx.App(False)
frame = MainWindow(None, "Cryptogrammar")
frame.Show()
app.MainLoop()
