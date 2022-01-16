import wx

from config import WledSettings
from settings_frame import SettingsFrame
from worker import WledWorker


class WledApp(wx.App):

    def OnInit(self):
        self.settings = WledSettings.load_settings()

        frame = SettingsFrame(None, 'Настройки')
        frame.Show(False)
        self.SetTopWindow(frame)

        self.worker = WledWorker(self, frame)
        frame.set_worker(self.worker)

        self.worker.start()

        return True

    def OnExit(self):
        self.worker.api.reboot()
        return 0


app = WledApp(0)
app.MainLoop()
