import wx
import wx.lib.masked as masked
import utils
from config import WledSettings, WledSettingsData
from task_bar import WledTaskBarIcon
import wx.lib.agw.hyperlink as hl


# TODO разметка и окно по контенту

# TODO
class SettingsFrame(wx.Frame):

    def __init__(self, parent, title):
        super(SettingsFrame, self).__init__(parent, title=title, size=(450, 600))

        self.available_speeds = ['0.5', '1', '2']

        self.settings = WledSettings.load_settings()

        # Фикс размытых шрифтов
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
        except:
            pass

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.task_bar = WledTaskBarIcon(self)

        self.statusbar = self.CreateStatusBar(1)
        self.parentsizer = wx.BoxSizer(wx.VERTICAL)

        # Главные настройки
        self.main_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Главные настройки")
        self.main_sizer = wx.StaticBoxSizer(self.main_staticbox, wx.VERTICAL)
        self.main_cb_on = wx.CheckBox(self, label='Включено', pos=(10, 10))
        self.wled_hiperlink = hl.HyperLinkCtrl(self, wx.ID_ANY, 'Настройки wled',
                                               URL="Открыть в браузере")

        self.main_sizer.Add(self.main_cb_on)
        self.main_sizer.Add(self.wled_hiperlink)
        # Скорость обновления

        self.speed_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Скорость обновления, секунд")
        self.speed_sizer = wx.StaticBoxSizer(self.speed_staticbox, wx.VERTICAL)
        self.speed_choise = wx.Choice(self, choices=self.available_speeds)
        self.speed_sizer.Add(self.speed_choise)

        # Ip адрес контроллера
        self.ip_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Ip адрес контроллера")
        self.ip_sizer = wx.StaticBoxSizer(self.ip_staticbox, wx.VERTICAL)
        self.ip_rb_auto = wx.RadioButton(self, wx.ID_ANY, label='Автоматически', style=wx.RB_GROUP)
        self.ip_rb_manual = wx.RadioButton(self, wx.ID_ANY, label='В ручную')
        self.ip_text = masked.IpAddrCtrl(self, size=(140, -1))
        self.ip_sizer.Add(self.ip_rb_auto)
        self.ip_sizer.Add(self.ip_rb_manual)
        self.ip_sizer.Add(self.ip_text)

        # Led панель
        self.led_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Led панель")
        self.led_sizer = wx.StaticBoxSizer(self.led_staticbox, wx.VERTICAL)

        # Ширина сегмента(в светодиодах)
        self.led_x_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Ширина сегмента(в светодиодах)")
        self.led_x_sizer = wx.StaticBoxSizer(self.led_x_staticbox, wx.VERTICAL)
        self.led_x_text = masked.NumCtrl(self, wx.ID_ANY, size=(50, -1))
        self.led_x_sizer.Add(self.led_x_text)
        # Высота сегмента(в светодиодах)
        self.led_y_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Высота сегмента(в светодиодах)")
        self.led_y_sizer = wx.StaticBoxSizer(self.led_y_staticbox, wx.VERTICAL)
        self.led_y_text = masked.NumCtrl(self, wx.ID_ANY, size=(50, -1))
        self.led_y_sizer.Add(self.led_y_text)

        # Цвет индикатора процессора
        self.led_proc_staticbox = wx.StaticBox(self, wx.ID_ANY, label="Цвет индикатора загрузки процессора R,G,B")
        self.led_proc_sizer = wx.StaticBoxSizer(self.led_proc_staticbox, wx.HORIZONTAL)
        self.led_proc_r_text = wx.TextCtrl(self, wx.ID_ANY, size=(100, -1), value="R")
        self.led_proc_g_text = wx.TextCtrl(self, wx.ID_ANY, size=(100, -1), name="G")
        self.led_proc_b_text = wx.TextCtrl(self, wx.ID_ANY, size=(100, -1), name="B")
        self.led_proc_sizer.Add(self.led_proc_r_text)
        self.led_proc_sizer.Add(self.led_proc_g_text)
        self.led_proc_sizer.Add(self.led_proc_b_text)

        # Цвет индикатора озу
        self.led_ram_staticbox = wx.StaticBox(self, wx.ID_ANY,
                                              label="Цвет индикатора загрузки оперативной памяти R,G,B")
        self.led_ram_sizer = wx.StaticBoxSizer(self.led_ram_staticbox, wx.HORIZONTAL)
        self.led_mem_r_text = wx.TextCtrl(self, wx.ID_ANY, size=(100, -1), name="R")
        self.led_mem_g_text = wx.TextCtrl(self, wx.ID_ANY, size=(100, -1), name="G")
        self.led_mem_b_text = wx.TextCtrl(self, wx.ID_ANY, size=(100, -1), name="B")
        self.led_ram_sizer.Add(self.led_mem_r_text)
        self.led_ram_sizer.Add(self.led_mem_g_text)
        self.led_ram_sizer.Add(self.led_mem_b_text)

        # Led панель
        self.led_sizer.Add(self.led_proc_sizer)
        self.led_sizer.Add(self.led_ram_sizer)
        self.led_sizer.Add(self.led_x_sizer)
        self.led_sizer.Add(self.led_y_sizer)

        # Сохранить
        self.save_btn = wx.Button(self, wx.ID_ANY, "Сохранить")
        self.save_btn.Bind(wx.EVT_BUTTON, self.OnSaveClicked)

        # Родительский вертикальный контейнер
        self.parentsizer.Add(self.main_sizer)
        self.parentsizer.Add(self.speed_sizer)
        self.parentsizer.Add(self.ip_sizer)
        self.parentsizer.Add(self.led_sizer)
        self.parentsizer.Add(self.save_btn, 0, wx.ALIGN_CENTER)

        self.SetSizer(self.parentsizer)

        self.set_ui_settings()

        # TODO optimize
        self.SetIcon(wx.Icon(utils.resource_path('bitmaps/icon.png'), wx.BITMAP_TYPE_PNG))

        self.Layout()
        self.Centre()

    def OnSaveClicked(self, event):
        try:
            new_settings = self.get_ui_settings()
            need_reboot = self.settings.on and not new_settings.on
            self.settings = new_settings
            WledSettings.save_settings(self.settings)
            if need_reboot:
                self.worker.api.reboot()
            wx.MessageBox('Настройки сохранены', 'Wled sysinfo assistant',
                          style=wx.OK | wx.ICON_INFORMATION)

        except Exception as e:
            print(e)
            wx.MessageBox(str(e), 'Проверьте правильность настроек',
                          style=wx.OK | wx.ICON_ERROR)

    def OnClose(self, event):
        self.Hide()

    def set_ui_settings(self):
        try:
            self.led_proc_r_text.SetValue(str(self.settings.proc_color[0]))
            self.led_proc_g_text.SetValue(str(self.settings.proc_color[1]))
            self.led_proc_b_text.SetValue(str(self.settings.proc_color[2]))
            self.led_mem_r_text.SetValue(str(self.settings.mem_color[0]))
            self.led_mem_g_text.SetValue(str(self.settings.mem_color[1]))
            self.led_mem_b_text.SetValue(str(self.settings.mem_color[2]))
            self.main_cb_on.SetValue(self.settings.on)
            self.ip_text.SetValue(self.settings.ip)
            self.ip_rb_auto.SetValue(self.settings.ip_auto)
            self.ip_rb_manual.SetValue(not self.settings.ip_auto)
            self.speed_choise.SetSelection(self.settings.refresh_speed)  # numer 1
            self.led_x_text.SetValue(self.settings.segment_x)
            self.led_y_text.SetValue(self.settings.segment_y)
        except Exception as e:
            print(e)
            wx.MessageBox(WledSettings.config_file(), 'Проверьте правильность настроек в конфиге',
                          style=wx.OK | wx.ICON_ERROR)

    def get_ui_settings(self) -> WledSettingsData:
        return WledSettingsData(
            proc_color=[int(self.led_proc_r_text.GetValue()),
                        int(self.led_proc_g_text.GetValue()),
                        int(self.led_proc_b_text.GetValue())],
            mem_color=[int(self.led_mem_r_text.GetValue()),
                       int(self.led_mem_g_text.GetValue()),
                       int(self.led_mem_b_text.GetValue())],
            on=self.main_cb_on.GetValue(),
            ip=self.ip_text.GetValue(),
            ip_auto=self.ip_rb_auto.GetValue(),
            refresh_speed=self.speed_choise.GetSelection(),
            segment_x=self.led_x_text.GetValue(),
            segment_y=self.led_y_text.GetValue(),
            is_zig_zag=False #TODO ui
        )

    def set_worker(self, worker):
        self.worker = worker

    def set_status(self, text):
        print(text)
        self.statusbar.SetStatusText(text)

    def set_hiperlink(self, ip, port):
        self.wled_hiperlink.SetURL('http://{}:{}'.format(ip, port))
# ex = wx.App()
# SettingsFrame(None, 'Настройки')
# ex.MainLoop()
