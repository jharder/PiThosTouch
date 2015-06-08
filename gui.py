from tkinter import *
from PIL import Image, ImageTk
from sys import platform as _platform
from functools import partial

import sys
import math
import collections
import settings
import tkinter.font as Font

# this cool class adapted from
# http://code.activestate.com/recipes/578887-text-widget-width-and-height-in-pixels-tkinter/
class Button2(Frame):
    def __init__(self, master, width = 0, height = 0, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, master, width = self.width, height = self.height)
        self.buttonWidget = Button(self, **kwargs)
        self.buttonWidget.pack(expand = YES, fill = BOTH)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

class FullscreenPithosPandora:
    def __init__(self):
        # some global settings.
        # do not adjust unless you enjoy breaking things
        self.paddingPercent = 0.05 # padding on all sides of a button
        self.maxButtonsPerRow = 3

        # screen res will only be used if we can't figure it out
        self.maxScreenHeight = 320
        self.maxScreenWidth = 240

        # set up the program window
        # it is fullscreen and cannot be closed (except by alt+f4)
        self.tk = Tk()
        self.tk.configure(background = "white")
        self.tk.attributes('-fullscreen', True)
        self.mainFrame = Frame(self.tk)
        self.mainFrame.configure(background = "white")
        self.mainFrame.pack(expand = YES, fill = BOTH)
        self.state = False

    def loadDisplaySettings(self):
        if _platform == "linux" or _platform == "linux2":
            self.screenHeight = self.tk.winfo_height()
            self.screenWidth = self.tk.winfo_width()
        elif _platform == "win32": # used for dev only
            from win32api import GetSystemMetrics
            self.screenWidth = GetSystemMetrics(0)
            self.screenHeight = GetSystemMetrics(1)

        if (int(self.screenHeight) == 1):
            self.screenHeight = self.maxScreenHeight

        if(int(self.screenWidth) == 1):
            self.screenWidth = self.maxScreenWidth

        #print(self.screenHeight, self.screenWidth)

    def displayLoginInterface(self):
        # perhaps a bit of a kludge, but I get the values of the screen
        # dimensions here because this is the initial entry-point that will
        # always be displayed
        self.loadDisplaySettings()

        self.loadUsers()
        numRows = self.countRows(self.orderedUsers)

        self.createButtonRows(numRows, self.orderedUsers)

    def countRows(self, entries):
        return math.ceil(len(entries) / self.maxButtonsPerRow)

    def createButtonRows(self, numRows, data):
        bigFont = Font.Font(size = 40)
        buttonPadHeight = int(self.screenHeight * self.paddingPercent)
        buttonPadWidth = int(self.screenWidth * self.paddingPercent)
        buttonHeight = int(self.screenHeight / numRows) - (2 * buttonPadHeight)
        buttonWidth = int(self.screenWidth / self.maxButtonsPerRow) - (2 * buttonPadWidth)
        #print(buttonPadHeight, buttonPadWidth, buttonHeight, buttonWidth)

        rows = 0
        inserted = 0
        self.frameArray = []
        colorArray = ["yellow", "red", "green", "blue"]

        while (rows < numRows):
            tempFrame = Frame(self.mainFrame)
            tempFrame.configure(background = colorArray[rows])
            tempFrame.pack(expand = YES, fill = BOTH)
            self.frameArray.append(tempFrame)
            rows += 1

        selectedRow = 0
        for key, value in data.items():
            print(key, value)
            if (inserted >= self.maxButtonsPerRow):
                selectedRow += 1
                inserted = 0

            Button2(self.frameArray[selectedRow], width = buttonWidth, \
                height = buttonHeight, text = key, \
                command = partial(self.displayStationInterface, key, value), \
                anchor = CENTER, font = bigFont, wraplength = buttonWidth
                ).pack(side = LEFT, padx = buttonPadWidth, \
                    pady = buttonPadHeight, fill = BOTH)
            inserted += 1

    def clearFrame(main, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def displayStationInterface(self, user, userSettings):
        self.clearFrame(self.mainFrame)
        numRows = self.countRows(settings.fakeStations[user])
        self.createButtonRows(numRows, settings.fakeStations[user])

    def loadUsers(self):
        self.numUsers = len(settings.userSettings)
        self.orderedUsers = collections.OrderedDict(sorted(settings.userSettings.items(), key = lambda t: t[0]))

app = FullscreenPithosPandora()
app.displayLoginInterface()
app.tk.mainloop()
