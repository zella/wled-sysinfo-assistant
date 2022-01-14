import wx
from wx.adv import TaskBarIcon


class WledTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        TaskBarIcon.__init__(self)

        self.frame = frame

        self.SetIcon(wx.Icon('./bitmaps/icon.png', wx.BITMAP_TYPE_PNG), 'Wled sysinfo assistant')

        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=1)
        self.Bind(wx.EVT_MENU, self.OnTaskBarDeactivate, id=2)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=3)

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnTaskBarActivate)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, 'Show')
        menu.Append(2, 'Hide')
        menu.Append(3, 'Close')

        return menu

    def OnTaskBarClose(self, event):
        self.Destroy()

        self.frame.Destroy()

    def OnTaskBarActivate(self, event):
        if not self.frame.IsShown():
            self.frame.Show()

    def OnTaskBarDeactivate(self, event):
        if self.frame.IsShown():
            self.frame.Hide()
