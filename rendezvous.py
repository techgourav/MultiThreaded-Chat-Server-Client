import wx

class Rendezvous(object):
    def __init__(self, wxConnected, wxDisplay, wxLost):
        self.wxConnected = wxConnected
        self.wxDisplay = wxDisplay
        self.wxLost = wxLost

    def connected(self):
        wx.CallAfter(self.wxConnected)

    def display(self, msg):
        wx.CallAfter(self.wxDisplay, msg)

    def lost(self, msg):
        wx.CallAfter(self.wxLost, msg)
