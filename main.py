
# coding: utf8
__version__ = '0.2'
from kivy.config import Config

import sys
import time
from plyer import notification as notf
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.utils import platform
import json
from random import randint
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial
from kivy.graphics import Rectangle, Canvas, Color, Ellipse, RoundedRectangle
import os
import uuid
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from datetime import datetime
from plyer import gps
import threading
import ftplib
try:
    from jnius import autoclass
except:
    pass
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from kivy.config import Config
from kivy.logger import Logger           ##  Logger.info("GalleryApp: Opening gallery.")

from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDRoundFlatButton, MDTextButton, MDFlatButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
import pickle
import pathlib
from plyer import notification
import asyncio
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget


if platform == 'android':
    from jnius import autoclass, java_method, cast    #  PythonJavaClass,
    from android import activity
    from plyer import vibrator

    # PythonScanCallback = autoclass('org.kivy.emergency.PythonScanCallback')

    # PythonActivity = autoclass('org.kivy.android.PythonActivity')
    # Camera = autoclass('android.hardware.Camera')
    # SurfaceView = autoclass('android.view.SurfaceView')
    # SurfaceHolder = autoclass('android.view.SurfaceHolder')
    # Surface = autoclass('android.view.Surface')

    from android.permissions import request_permissions, Permission,  check_permission

    # if not check_permission('android.permission.RECORD_AUDIO'):
    #     request_permissions([Permission.BLUETOOTH_SCAN, Permission.BLUETOOTH_ADMIN, Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH])

    request_permissions([ Permission.BLUETOOTH_SCAN, Permission.BLUETOOTH, Permission.BLUETOOTH_ADMIN,
                         Permission.BLUETOOTH_CONNECT, Permission.BLUETOOTH_ADVERTISE, Permission.CAMERA, Permission.ACCESS_FINE_LOCATION, Permission.RECORD_AUDIO, Permission.ACCESS_COARSE_LOCATION,
                         Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    # if not check_permission('android.permission.RECORD_AUDIO'):



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Window.softinput_mode="below_target"
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

RRR=[]
PASS="0"
service,mActivity=None,None

def dr():
    try:
        from jnius import autoclass
        Env = autoclass('android.os.Environment')
        sd0 = Env.getExternalStorageDirectory().getAbsolutePath()
        directory = "Documents/org/SOS/"
        sd = os.path.join(sd0, directory)
        if not os.path.isdir(sd + "New_temp/"): #dr()+"New_temp/"
            os.mkdir(sd + "New_temp/")
            if not os.path.exists(sd):
                os.makedirs(sd)
            if not os.path.isdir(sd + "conf/"):
                os.mkdir(sd + "conf/")
            if not os.path.isdir(sd + "contacts/"):
                os.mkdir(sd + "contacts/")
            if not os.path.isdir(sd + "Items/"):
                os.mkdir(sd + "Items/")
            if not os.path.isdir(sd + "Activities/"): #
                os.mkdir(sd + "Activities/")

        return sd
    except:
        sd="SD/"
        if not os.path.isdir(sd + "New_temp/"): #dr()+"New_temp/"
            os.mkdir(sd + "New_temp/")
            if not os.path.isdir(sd + "conf/"):
                os.mkdir(sd + "conf/")
            if not os.path.isdir(sd + "contacts/"):
                os.mkdir(sd + "contacts/")
            if not os.path.isdir(sd + "Items/"):
                os.mkdir(sd + "Items/")
            if not os.path.isdir(sd + "Activities/"): #
                os.mkdir(sd + "Activities/")

        return sd
Config.set('kivy','log_dir',dr()+'SOS/')
if not os.path.isdir("HST/"):
    os.mkdir("HST/")


async def ASYNC(msg):
    from SERVICE import offline as snd
    try:
        await snd(msg)
    except:
        pass

def send(data):  # This is for sending   client.send_message( b'/ping', [asctime(localtime()).encode('utf8'), ],)
    print("sending...")
    if not os.path.isfile(dr() + "Temp/" + data.get("sidd", "") + ".json"):
        json.dump(data, open(dr() + "Temp/" + data.get("sidd", "") + ".json", "w"))

    # if platform == "android" :
    #     data=json.dumps(data)
    #     client.send_message( b'/To_server', [data.encode('utf8'), ],)
    # else:
    #     asyncio.run(ASYNC(data))

def SEARCH(message):
    global RRR
    dc = json.loads(message.decode('utf8'))
    RRR.append(dc)

def display_message(message):  # This receives also from bind
    global RRR
    dc=json.loads(message.decode('utf8'))
    RRR.append(dc)

    cl=RM()
    cl.receive(rx=dc)
    pass

def RECEIVER(message):  # This receives also  from  bind
    global PASS
    try:
        MESS = json.loads(message.decode('utf8'))
        # PASS = "1"
        CLASS = RM()
        if MESS["action"] == "cht":
            CLASS.MSG(B=None, update_new=MESS)
        if MESS["action"] == "zone":
            CLASS.zchat(POS=None, ME=MESS)
        if MESS["action"] == "inbx":
            CLASS.PROFILE(iddd=None, update_new=MESS)

        print("RECEIVER: ",MESS)

        if MESS.get("mess", 0) == "home":
            PASS = "0"
            XA = RM()
            XA.home()
    except Exception as e :
        for file in os.listdir(dr()+"New_temp/"):
            MESS=json.load(open(dr()+"New_temp/"+file))
            os.remove(dr()+"New_temp/"+file)
            # PASS = "1"                           #   close the gate to avoid reopening new app layer
            CLASS = RM()
            if MESS["action"] == "cht":
                CLASS.MSG(B=None, update_new=MESS)
            if MESS["action"] == "zone":
                CLASS.zchat(POS=None, ME=MESS)
            if MESS["action"] == "inbx":
                CLASS.PROFILE(iddd=None, update_new=MESS)
            print("RECEIVER: ", MESS)

    PASS= "0"

    # Clock.schedule_once(lambda cl:RECEIVER(cl))

def to_back(path,data):
    ndata=json.dumps({"data":data,"path":path})
    client.send_message(b'/from_main', [ndata.encode('utf8'), ], )

try:
    server = OSCThreadServer()
    server.listen(address=b'localhost', port=3002, default=True, )
    server.bind(b'/message', display_message)
    # server.bind(b'/RECEIVER', RECEIVER)
    server.bind(b'/SEARCH', SEARCH)
    client = OSCClient(b'localhost', 3000)
except Exception as e :
    print("OSC server: ",e)

#####################################################
def underground(x="0"):   #     0 : start service        1 : close & open App      2 : restart phone    3 : manualy start service
    global service, mActivity
    SERVICE_NAME = u'{packagename}.Service{servicename}'.format( packagename=u'org.kivy.emergency',servicename=u'Sos')
    if platform == 'android':
        if x == "0" :                                                 #    This is manually
            if not service:
                service = autoclass(SERVICE_NAME)
                mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
                print(">>>>>>>",mActivity,"<<<<<<<<<<<<<<<<<<<")
                argument = ''
                service.start(mActivity, argument)
        elif x == "1" :
            if service:
                service.stop(mActivity)
        elif x == "3" :
            if service:
                service.stop(mActivity)

            service = autoclass(SERVICE_NAME)
            mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            print(">>>>>>>", mActivity, "<<<<<<<<<<<<<<<<<<<")
            argument = ''
            service.start(mActivity, argument)

# class CameraPreview(Widget):
#     def __init__(self, **kwargs):
#         """
#         layout = BoxLayout(orientation='vertical')
#
#         # Create a camera preview widget
#         self.camera_preview = CameraPreview(size_hint=(1, 0.8))
#         layout.add_widget(self.camera_preview.surface_view)
#
#         # Button to capture an image
#         capture_button = Button(text='Capture Image', size_hint=(1, 0.2))
#         capture_button.bind(on_press=self.capture_image)
#         layout.add_widget(capture_button)
#
#         return layout
#
#         :param kwargs:
#         """
#         super(CameraPreview, self).__init__(**kwargs)
#         self.surface_view = SurfaceView(PythonActivity.mActivity)
#         self.holder = self.surface_view.getHolder()
#         self.holder.addCallback(self)
#         self.camera = Camera.open()
#
#     def surfaceChanged(self, holder, format, width, height):
#         self.camera.stopPreview()
#         self.camera.setPreviewDisplay(holder)
#         self.camera.startPreview()
#
#     def surfaceCreated(self, holder):
#         self.camera.setPreviewDisplay(holder)
#         self.camera.startPreview()
#
#     def surfaceDestroyed(self, holder):
#         self.camera.stopPreview()
#         self.camera.release()
#
#     def capture(self):
#         # Implement capturing image from the camera
#         self.camera.takePicture(None, None, self.picture_callback)
#
#     def picture_callback(self, data, camera):
#         # Save the captured image
#         filepath = os.path.join(App.get_running_app().user_data_dir, 'captured_image.jpg')
#         with open(filepath, 'wb') as file:
#             file.write(data)
#         print(f'Image saved to {filepath}')
#         # Restart preview after capture
#         self.camera.startPreview()

from kivy.graphics import Ellipse, Color, StencilPush, StencilUse, StencilUnUse, StencilPop, Rectangle

from kivy.uix.image import AsyncImage
from kivy.uix.stencilview import StencilView
from kivy.graphics import Ellipse, Color, Rectangle


class CircularImage(StencilView):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.image = AsyncImage(source=self.source, allow_stretch=True, keep_ratio=True)
        self.bind(size=self.update_shape, pos=self.update_shape)
        self.add_widget(self.image)

    def update_shape(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Set the circular clipping area using an Ellipse
            Color(1, 1, 1, 1)
            min_size = min(self.size)
            x = self.center_x - min_size / 2
            y = self.center_y - min_size / 2
            Ellipse(pos=(x, y), size=(min_size, min_size))

        # Update the image size and position to fit within the circular area
        self.image.size = (min_size, min_size)
        self.image.pos = (x, y)

class CustomTB(MDFlatButton):
    toggled=BooleanProperty(False)
    def __int__(self,**kwargs):
        super().__int__(**kwargs)
        self.md_bg_color=(.9,.9,1,1)
        self.bind(on_release=self.toggle)

    def toggle(self):
        self.toggled = not self.toggled
        if self.toggled:
            self.md_bg_color=(0,1,0,.6)
        else:
            self.md_bg_color = (0, 1, 0, .6)

class ImageProcessor:
    def compress(self, src, targ):
        from PIL import Image
        base_width = 1080
        image = Image.open(src)
        width_percent = (base_width / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((base_width, hsize), Image.ANTIALIAS)
        image.save(targ)
        return targ

    def cut(self, IN, OUT):
        import os
        from PIL import Image, ImageDraw, ImageOps
        # Open the image and apply EXIF orientation fix
        imge = Image.open(IN)
        imge = ImageOps.exif_transpose(imge).convert("RGBA")

        width, height = imge.size

        # Create an alpha mask for the circular cut
        alpha = Image.new('L', imge.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.ellipse((0, 0, width, width), fill=255)

        # Apply the alpha mask to the image
        imge.putalpha(alpha)

        # Save the resulting image
        imge.save(OUT)
        if os.path.getsize(OUT) > 1000000:
            return self.compress(OUT, OUT)
        else:
            return OUT

    def fdir(d):
        import os
        """
        This finds the directory path without the file name.
        """
        return os.path.dirname(d)

    def fnam(d):
        import os
        """
        This finds the file name from the path.
        """
        return os.path.basename(d)


def S_TextInputApp(Text="",BG=(0, 0, 0, 1) , FG=(1, 1, 1, .6)):
    global rect__, _S_TextInputApp
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.textinput import TextInput
    from kivy.graphics import Color, Rectangle

    def _update_rect(instance, value):
        global rect__
        """ Update the background rectangle size and position """
        rect__.size = instance.size
        rect__.pos = instance.pos
    def on_text_input_focus(instance, value):
        """Handle focus event for the TextInput"""
        if value:  # If the TextInput is focused
            print("TextInput is focused")
            # Window.request_keyboard(self._keyboard_closed, instance)
        else:
            print("TextInput focus lost")
    def _keyboard_closed(self):
        """Handle keyboard closing event."""
        print("Keyboard has been closed")
    def typed(w,t):
        global _S_TextInputApp
        _S_TextInputApp =w.text

    R = BG[0]
    G = BG[1]
    B = BG[2]
    O = BG[3]

    main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    # Create a ScrollView
    scroll_view = ScrollView(
        size_hint=(1, 1),
        bar_width=30,  # Customize the scrollbar width
        bar_inactive_color=(0,0,0,.8),
        scroll_type=['bars', 'content'],  # Enable both scrollbar and content dragging
        do_scroll_x=False,  # Disable horizontal scrolling
        do_scroll_y=True  # Enable vertical scrolling
    )

    # font_size=20,  # Increase font size for readability
    text_input = TextInput(
        text=Text,
        hint_text='Text...',
        multiline=True,
        size_hint_y=None,  # Disable auto-resize
        height=500,  # Set a height to enable scrolling

        background_color=BG,  # White background for TextInput
        foreground_color=FG,  # Black text color
        padding=[10, 10, 10, 10]  # Add padding for better UX
    )

    # Set the height of the TextInput dynamically
    text_input.bind(minimum_height=text_input.setter('height'))

    # Add the TextInput to the ScrollView
    scroll_view.add_widget(text_input)

    # Add the ScrollView to the main layout
    main_layout.add_widget(scroll_view)

    # Custom background for ScrollView
    with scroll_view.canvas.before:
        Color(R,G,B,O)#(0.9, 0.9, 0.9, 1)  # Light gray background for ScrollView
        rect__ = Rectangle(size=scroll_view.size, pos=scroll_view.pos)
        scroll_view.bind(size=_update_rect, pos=_update_rect)

    # Bind touch_down event to focus the TextInput
    text_input.bind(focus=on_text_input_focus)

    return main_layout

class ExText(TextInput):
    def __init__(self,**kwargs):
        super(ExText,self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))


# from jnius import autoclass
# import logging
#
# # Initialize logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Import Java classes
# ScanCallback = autoclass('android.bluetooth.le.ScanCallback')
# BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
# ScanSettings = autoclass("android.bluetooth.le.ScanSettings")
# ScanSettingsBuilder = autoclass("android.bluetooth.le.ScanSettings$Builder")
# ScanFilter = autoclass("android.bluetooth.le.ScanFilter")
# ScanFilterBuilder = autoclass("android.bluetooth.le.ScanFilter$Builder")
#
# class BLEScanCallback(ScanCallback):
#     def onScanResult(self, callback_type, result):
#         """
#         Called when a BLE device is found.
#         """
#         device = result.getDevice()
#         name = device.getName()
#         address = device.getAddress()
#         logger.info(f"Found device: {name} - {address}")
#
#     def onBatchScanResults(self, results):
#         """
#         Called when batch scan results are available.
#         """
#         for result in results:
#             self.onScanResult(0, result)
#
#     def onScanFailed(self, error_code):
#         """
#         Called when the scan fails.
#         """
#         logger.error(f"Scan failed with error code: {error_code}")
#
# class BLEScanner:
#     def __init__(self):
#         self.adapter = BluetoothAdapter.getDefaultAdapter()
#
#         if self.adapter is None or not self.adapter.isEnabled():
#             logger.error("Bluetooth is not enabled or available.")
#             raise RuntimeError("Bluetooth is not enabled or available.")
#
#         self.le_scanner = self.adapter.getBluetoothLeScanner()
#         self.scan_callback = BLEScanCallback()
#
#         # Configure ScanSettings
#         settings_builder = ScanSettingsBuilder()
#         settings_builder.setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
#         self.settings = settings_builder.build()
#
#         # Configure ScanFilter
#         filter_builder = ScanFilterBuilder()
#         self.filter = filter_builder.build()
#
#     def start_scanning(self):
#         if not self.le_scanner:
#             logger.error("LE Scanner is not initialized.")
#             return
#
#         filters = [self.filter]
#         try:
#             self.le_scanner.startScan(filters, self.settings, self.scan_callback)
#             logger.info("Started scanning...")
#         except Exception as e:
#             logger.error(f"Failed to start scanning: {e}")
#
#     def stop_scanning(self):
#         if not self.le_scanner:
#             logger.error("LE Scanner is not initialized.")
#             return
#
#         try:
#             self.le_scanner.stopScan(self.scan_callback)
#             logger.info("Stopped scanning.")
#         except Exception as e:
#             logger.error(f"Failed to stop scanning: {e}")
#
# class BLEAdvertiser:
#     def __init__(self, uuid_str="12345678-1234-5678-1234-567812345678", message="I sell electronics"):
#         self.adapter = BluetoothAdapter.getDefaultAdapter()
#
#         if self.adapter is None or not self.adapter.isEnabled():
#             raise RuntimeError("Bluetooth is not enabled or available.")
#
#         self.le_advertiser = self.adapter.getBluetoothLeAdvertiser()
#
#         settings_builder = AdvertiseSettingsBuilder()
#         settings_builder.setAdvertiseMode(AdvertiseSettingsBuilder.ADVERTISE_MODE_LOW_POWER)
#         settings_builder.setConnectable(True)
#         settings_builder.setTimeout(0)
#         settings_builder.setTxPowerLevel(AdvertiseSettingsBuilder.ADVERTISE_TX_POWER_MEDIUM)
#         self.settings = settings_builder.build()
#
#         data_builder = AdvertiseDataBuilder()
#         uuid = UUID.fromString(uuid_str)
#         parcel_uuid = ParcelUuid(uuid)
#
#         data_builder.addServiceUuid(parcel_uuid)
#         data_builder.addServiceData(parcel_uuid, message.encode('utf-8'))
#         self.data = data_builder.build()
#
#     def start_advertising(self):
#         if not self.le_advertiser:
#             logger.error("LE Advertiser is not initialized.")
#             return
#         try:
#             self.le_advertiser.startAdvertising(self.settings, self.data, None)
#             logger.info("Started advertising...")
#         except Exception as e:
#             logger.error(f"Failed to start advertising: {e}")
#
#     def stop_advertising(self):
#         if not self.le_advertiser:
#             logger.error("LE Advertiser is not initialized.")
#             return
#         try:
#             self.le_advertiser.stopAdvertising(None)
#             logger.info("Stopped advertising.")
#         except Exception as e:
#             logger.error(f"Failed to stop advertising: {e}")

class RM(Screen):
    def __init__(self,**kwargs):
        super(RM,self).__init__(**kwargs)
        if PASS == "1" :
            return
        Window.bind(on_touch_down=self.down)
        self.SLD=[]
        self.HIDE= -.2
        try:
            self.Items=json.load(open("Shp.json"))
        except:
            self.Items={}
        try:
            URL=json.load(open("SD/conf/server.json", "r"))
            self.URL=URL["ch_url"] + ":" + URL["port"]
            self.PWD=URL.get("pwd","12435687")
            self.PORT=URL["port"]
            self.ip=URL["ch_url"]
            print(self.URL)
            del URL
        except:
            pass
        ###################################################################################################

        if not os.path.isdir("offline"):
            os.mkdir("offline")

        if not os.path.isdir("tokens/"):
            os.mkdir("tokens/")

        if not os.path.isdir("REMINDERS/"):
            os.mkdir("REMINDERS/")

        if not os.path.isdir("Temp/"):      #  ("SD/conf/server.json","r")
            os.mkdir("Temp/")

        if not os.path.isdir("SD/conf/"):
            os.makedirs("SD/conf/")

        if  not os.path.isfile(dr()+"/conf/server.json"):      #  ("SD/conf/server.json","r")
            try:
                json.dump(json.load(open("SD/conf/server.json", "r")), open(dr()+"conf/server.json", "w"))
            except:
                pass

        # with self.canvas.before:
        #     Color(0,0,0, 1)
        #     self.rideau = Rectangle(pos=self.pos, size=(Window.width, Window.height))  # source=SD + "pn/w5.jpg",

        if not os.path.isfile("SD/conf/me.json"):
            """ USE GPS IN GUI TO FIND COUNTRY AND CITY .   THATS IS THE BEST.      I MAY FIND KYAKA II ALSO"""
            IDD=str(uuid.uuid4())

            dic={"Name": ["Emergency", "x"+str(randint(0,100000))], "pseudo": "Unknown", "busy": "Job/Trading", "adress": ["World", "Unclassified"],
                 "idd": IDD,"perm":[IDD[:8]],"LIKE":[0,1],"lk":11}
            self.ME=dic
            self.JOBTALENT=IDD[:8]
            self.PAIDADDS=IDD[:16]
            self.ORG=IDD[:24]
            json.dump(dic, open("SD/conf/me.json", "w"))

            if not os.path.isdir(dr() + "contacts/" + IDD ):
                os.mkdir(dr() + "contacts/" + IDD )

            if not os.path.isdir(dr() + "contacts/" + IDD + "/chats/"):
                os.mkdir(dr() + "contacts/" + IDD + "/chats/")

            if not os.path.isfile(dr() + "contacts/" + IDD + "/" + IDD + ".json"):
                json.dump({"schm": "Activities/JobTalent/" + IDD, "action": "B_U", "org": self.ME["Name"][0], "msg": "hello",
                           "zone": self.ME["adress"], "day": time.strftime("%d/%m/%y %H:%M:%S"),
                           'subject': self.ME["busy"], "BUSY": [], "pht": [], "sidd": IDD[:5], "idd": IDD},
                          open(dr() + "contacts/" + IDD + "/" + IDD + ".json","w"))

            if not os.path.exists(self.ME["adress"][1] + "/LOOKING FOR"):  # "LOOKING FOR"    "OFFERING"
                os.makedirs(self.ME["adress"][1] + "/LOOKING FOR")
                os.makedirs(self.ME["adress"][1] + "/LOOKING FOR" + "/jobs")
                os.makedirs(self.ME["adress"][1] + "/LOOKING FOR" + "/bagainers")
                os.makedirs(self.ME["adress"][1] + "/LOOKING FOR" + "/given")

            if not os.path.exists(self.ME["adress"][1] + "/OFFERING"):  # "LOOKING FOR"    "OFFERING"
                os.makedirs(self.ME["adress"][1] + "/OFFERING")
                os.makedirs(self.ME["adress"][1] + "/OFFERING" + "/jobs")
                os.makedirs(self.ME["adress"][1] + "/OFFERING" + "/bagainers")
                os.makedirs(self.ME["adress"][1] + "/OFFERING" + "/given")


            Clock.schedule_once(self.new, 0)
            underground(x="0")
            snd={"action":"N_user","data":dic,"sidd": str(uuid.uuid4())[:5]}
            send(snd)
            Clock.schedule_once(self.BS, 1)

        else:
            if json.load(open("SD/conf/me.json", "r"))["adress"][0] == "World" :
                self.ME = json.load(open("SD/conf/me.json", "r"))
                self.JOBTALENT = self.ME["idd"][:8]
                self.PAIDADDS = self.ME["idd"][:16]
                self.ORG = self.ME["idd"][:24]
                underground(x="0")
                Clock.schedule_once(self.BS, 1)
                # Clock.schedule_once(self.home)
                Clock.schedule_once(self.new, 20)
            else:
                self.ME = json.load(open("SD/conf/me.json", "r"))
                self.JOBTALENT = self.ME["idd"][:8]
                self.PAIDADDS = self.ME["idd"][:16]
                self.ORG = self.ME["idd"][:24]
                underground(x="0")
                Clock.schedule_once(self.BS, 1)

    def down(self,touch,what):
        Window.bind(on_touch_up=lambda touch,what: Clock.unschedule(self.IP))
        self.cnt=0
        Clock.schedule_interval(self.IP,1)

    def IP(self,x, pm=None):
        self.cnt+=1
        print(self.cnt)
        if self.cnt == 45 :
            Clock.schedule_once(self.new, 0)
        if self.cnt == 50 :
            if platform == "android":
                sz=(.5, .13)
            else:
                sz=(.5, .4)
            if os.path.isfile("SD/conf/server.json"):
                d=json.load(open("SD/conf/server.json", "r"))
                tx=d["ch_url"]+":"+str(d["port"])
            else:
                tx=""
            T=TextInput(text=tx,size_hint=(.9, .5),background_color=(0,0,0,.91),foreground_color=(1,1,1,1),multiline=False, hint_text="ip adress",pos_hint={"center_x": .3, "center_y": .5})
            T.bind(focus=self.saveip)
            T.bind(on_text_validate=self.saveip)
            new_popup = Popup(title="Adress :", title_size=Window.size[1] / 50, title_align="center",
                              separator_color=(1, 1, 1, 0), size_hint=sz, content=T, disabled=False)
            new_popup.open()
        if self.cnt == 55 or pm:
            Clock.unschedule(self.IP)
            if platform == "android":
                sz=(.5, .13)
            else:
                sz=(.5, .4)
            if os.path.isfile("SD/conf/me.json"):
                d=json.load(open("SD/conf/me.json", "r"))
                tx="".join(d["perm"])
            else:
                tx=""
            T=TextInput(text=tx,size_hint=(.9, .5),background_color=(0,0,0,.91),foreground_color=(1,1,1,1),multiline=False, hint_text="Permission code",pos_hint={"center_x": .3, "center_y": .5})
            T.bind(focus=self.save_perm)
            T.bind(on_text_validate=self.save_perm)
            T.bind(text=self.save_perm)
            new_popup = Popup(title="Adress :", title_size=Window.size[1] / 50, title_align="center",
                              separator_color=(1, 1, 1, 0), size_hint=sz, content=T, disabled=False)
            new_popup.open()
            self.cnt=0

    def saveip(self,w,v=None):
            if ":" in w.text:
                if w.text.endswith("."):
                    ipl=w.text[:-1].split(":")
                    json.dump({"ch_url": ipl[0], "port": ipl[1]}, open("SD/conf/server.json", "w"))
                    underground(x="3")
                    # sys.exit("The app should restart to connect to new adress. exiting...")

    def save_perm(self,w,v=None):
        if w.text.endswith("."):
            d = json.load(open("SD/conf/me.json", "r"))
            if w.text[:-1] in d["idd"]:
                w.foreground_color=(0,1,0,1)
                if not w.text in d["perm"]:
                    d["perm"].append(w.text[:-1])
                json.dump(d, open("SD/conf/me.json", "w"))
            else:
                w.foreground_color = (1, 0, 0, 1)
        if "#...*#" in w.text:
            # d = json.load(open("SD/conf/me.json", "r"))
            # w.text=d["idd"]
            w.background_color=(0,1,0,1)
            d = json.load(open("SD/conf/me.json", "r"))
            if not d["idd"][:8] in d["perm"]:
                d["perm"].append(d["idd"][:8])
            if not d["idd"][8:16] in d["perm"]:
                d["perm"].append(d["idd"][8:16])
            if not d["idd"][16:24] in d["perm"]:
                d["perm"].append(d["idd"][16:24])
            json.dump(d, open("SD/conf/me.json", "w"))
            # w.text=d["idd"]

    def new(self, x,idd=None):
        def submited( butn):
            global r_n, r_pn, PS, ad1, ad2, ad3, new_popup, g_new, ok

            w_l = [r_n, r_pn, PS, ad1, ad2, ad3]
            cm = len(w_l)

            if r_n.text == "" or len(r_n.text) <= 2:
                r_n.background_color = (1, 0, 0, .4)
                cm = cm - 1

            if r_pn.text == "" or len(r_pn.text) <= 2:
                r_pn.background_color = (1, 0, 0, .4)
                cm = cm - 1

            if PS.text == "":
                PS.background_color = (1, 0, 0, .4)
                cm = cm - 1

            if ad1.text == "choose country":
                ad1.color = (1, 0, 0, 1)
                cm = cm - 1

            if ad2.text == "choose city":
                ad2.color = (1, 0, 0, 1)
                cm = cm - 1

            if len(w_l) == cm:
                if idd:
                    ID=idd
                    if self.ME.get("perm",0):
                        perm=self.ME["perm"]

                    else:
                        perm=[ID[:8]]

                    lk = self.ME.get("lk", 21)
                    LIKE = self.ME.get("LIKE", [0, 1])
                    jb=self.ME.get("jb", None)

                else:
                    ID=str(uuid.uuid4()).replace("-", "").replace(" ", "").replace("_", "").replace(":", "").replace("/","").lower() + "ONE"
                    perm = [ID[:8]]
                    lk=21
                    LIKE=[0,1]
                    jb=None


                me = {"Name": [r_n.text, r_pn.text], "pseudo": PS.text, "busy": ad3.text,
                      "adress": [ad1.text, ad2.text], "idd": ID, "perm": perm, "LIKE": LIKE,"lk":lk}
                if jb:
                    me["jb"]=jb
                self.ME = me
                self.JOBTALENT = ID[:8]
                self.PAIDADDS = ID[:16]
                self.ORG = ID[:24]

                if not os.path.isdir(dr() + "Activities/" + me["adress"][1]):
                    os.mkdir(dr() + "Activities/" + me["adress"][1])
                json.dump(me, open("SD/conf/me.json", "w"))

                if not idd:
                    if not os.path.exists(dr() + "contacts/" + ID + "/chats/"):
                        os.makedirs(dr() + "contacts/" + ID + "/chats/")

                    json.dump({"schm":"Activities/JobTalent/"+ID,"action": "B_U","org":r_n.text,"msg":"hello","zone": [ad1.text, ad2.text],"day": time.strftime("%d/%m/%y %H:%M:%S"),
                       'subject':ad3.text ,"BUSY":[],"pht":[],"sidd":ID[:5], "idd": ID},
                              open(dr()+"contacts/"+ID+"/"+ID+".json","w"))

                if not os.path.exists(self.ME["adress"][1] + "/LOOKING FOR"):  # "LOOKING FOR"    "OFFERING"
                    os.makedirs(self.ME["adress"][1] + "/LOOKING FOR" )
                    os.makedirs(self.ME["adress"][1] + "/LOOKING FOR"  + "/jobs")
                    os.makedirs(self.ME["adress"][1] + "/LOOKING FOR" + "/bagainers")
                    os.makedirs(self.ME["adress"][1] + "/LOOKING FOR"  + "/given")

                if not os.path.exists(self.ME["adress"][1] + "/OFFERING"):  # "LOOKING FOR"    "OFFERING"
                    os.makedirs(self.ME["adress"][1] + "/OFFERING")
                    os.makedirs(self.ME["adress"][1] + "/OFFERING" + "/jobs")
                    os.makedirs(self.ME["adress"][1] + "/OFFERING" + "/bagainers")
                    os.makedirs(self.ME["adress"][1] + "/OFFERING" + "/given")

                Clock.schedule_once(lambda x: underground(x="3"), 5)

                new_popup.dismiss()
                for _ in w_l:
                    del _
                del new_popup
                del w_l
                del cm
                del ID
                # del me
                del g_new
                del ok
                self.ME = json.load(open("SD/conf/me.json", "r"))

                try:
                    to_back("conf/me.json",me)
                except:
                    pass
                sen = {"action": "N_user", "data": me, "sidd": str(uuid.uuid4())[:5]}
                send(sen)
                self.clear_widgets()
                Clock.schedule_once(self.BS, 1)

        def city(sp, tx):
            global ad2
            ad2.values = tuple(PAYS[tx])
        global ad2, r_n, r_pn, PS, ad1, ad2, ad3, new_popup, g_new, ok
        """
        pseudo,idd,url_ch,port,real_names, unkown name,
        """
        olD=json.load(open("SD/conf/me.json", "r") )
        dd = open("SD/countries.json", "r")
        PAYS = json.load(dd)
        g_new = GridLayout(cols=1, spacing=Window.size[0] / 180)  ##  ,col_default_width=Window.width/1.5,col_force_default=True,row_default_height=Window.height/9,row_force_default=True
        PS = TextInput(hint_text="Unknown name")
        r_n = TextInput(hint_text="Real name")
        r_pn = TextInput(hint_text="Real Post name")
        g_new.add_widget(PS)
        g_new.add_widget(r_n)
        g_new.add_widget(r_pn)

        ad1 = Spinner(text="choose country", values=tuple(PAYS.keys()))
        ad2 = Spinner(text="choose city")
        ad1.bind(text=city)
        ad3 = Spinner(text="Job/Trading", values=("Job","Trading","Leader","Talent","Org"))
        if len(olD) > 4 :
            PS.text=olD["pseudo"]
            r_n.text=olD["Name"][0]
            r_pn.text = olD["Name"][1]
            ad1.text = olD["adress"][0]
            ad2.text = olD["adress"][1]
            ad3.text = olD["busy"]


        g_new.add_widget(ad1)
        g_new.add_widget(ad2)
        g_new.add_widget(ad3)

        ok = Button(text="Submit", on_press=submited)
        g_new.add_widget(ok)

        new_popup = Popup(title="Welcome Dear", title_size=Window.size[1] / 80, title_align="center",
                          separator_color=(1, 1, 1, 0), size_hint=(.4, .4), content=g_new, disabled=False)
        new_popup.open()

    def KEYS(self,window, key, *largs):

        if key == 27 :
            if len(self.SLD) == 0:
                return False
            else:
                try:
                    self.call_slid2()
                except:
                    pass
                return True

    def home(self, x=None):
        global wl

        Window.bind(on_keyboard=self.KEYS)
        # if "rideau2" in dir(self):
        #     print("self.rideau2.source: ",self.rideau2.source)
        #     wl=self.rideau2.source
        # else:
        #     lt = os.listdir("Temp/")
        #     wl = "Temp/" + lt[randint(0, len(lt) - 1)]

        self.Desktop = RelativeLayout(size_hint=(None,None),size=(Window.width/1.5,Window.height/2))
        with self.Desktop.canvas.before:
            Color(0,0,0,1)
            self.rideau2 = Rectangle( pos=(0, 0), size=(Window.width, Window.height))

        self.keys=Label(text="IDD MPAKA 20")

        self.scrol_domain=ScrollView(size_hint=(.24, .8), pos_hint={'center_x': .15, 'center_y': .45}, do_scroll_x=False,
                                do_scroll_y=True, scroll_timeout=55, scroll_distance=20,
                                scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)

        familly=os.listdir("REMINDERS/")

        self.damain=GridLayout(row_default_height=Window.size[1]/11,pos_hint={"center_x":.01,"center_y":.89},
                                  row_force_default=True,cols=1,size_hint=(1,None),size=(1,((Window.size[1]/100)* 20)* len(familly)) )

        self.damain.add_widget(Button(text="...",bold=True,font_size=40,on_release=self.New,background_normal="data/icos/bb.png",background_color=(.65,0,.2,.8)))

        self.filter={}

        for x in familly :
            name = x[x.index("@") + 1:x.index(".json")]
            if not name.upper() in self.filter.keys():
                self.filter[name.upper()]=[x]
            else:
                self.filter[name.upper()].append(x)

        for x in self.filter.keys():
            self.damain.add_widget(Button(text=x[:8].replace(" ","\n"),ids={"idd":self.filter[x]},background_color=(1,.7,0,.8),background_normal="data/icos/bb.png",size_hint=(1,.15),on_release=lambda w:self.return_widget(w,w.text)))

        self.scrol_domain.add_widget(self.damain)
        self.Desktop.add_widget(self.scrol_domain)

        # self.add_widget(self.Desktop)
        self.moveer(self.Desktop,pos=(50,50))

        if platform == "android":
            print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            # gps.configure(on_location=self.locator)
            # gps.start()

        # threading.Thread(target=self._Alarm).start()
        Clock.schedule_interval(self.INC,2)

        if os.path.isdir(dr()+"ready/"):
            ready=os.listdir(dr()+"ready/")
            if len(ready)>0 :
                self.front()
        else:
            os.mkdir(dr()+"ready/")

    def locator(self, lat, lon, speed, bearing, Altitude, accurancy):
        # Environment = autoclass('android.os.Environment')
        # storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
        # file_path = os.path.join(storage_path, "data/test")  # Adjust the path as needed
        notf.notify(title='GPS', message='lat: ')   #   + lat + ' lon: ' + lon
        # open(file_path, "a").write('lat: {lat}, lon: {lon}'.format(**kwargs))

    def front(self):
        dirc=dr()+"ready/"
        for x in os.listdir(dirc):
            dc=json.load(open(dirc+x))
            if dc.get("data",0):
                self.wid_detail(dc["data"],file=x)
            else:
                self.wid_detail(dc,file=x)

    def gp(self,w):
        import pickle

        from jnius import autoclass
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = autoclass('android.content.Context')
            intent = Intent(context, PythonActivity.mActivity.getClass())
            context.startActivity(intent)

            # Toast = autoclass('android.widget.Toast')
            # toast = Toast.makeText(mActivity.getApplicationContext(), 'Hello, Android!', Toast.LENGTH_LONG)
            # toast.show()

        except Exception as e:
            notf.notify(title="Emergency", message=f"Notification creation failed: {e}",toast=True)


        # pickle.dump({"mActivity": mActivity},open("pickled","wb"))
        # to_back("conf/server2.json", {"ch_url": 3, "port": 8080})

    def INC(self,x):
        a=os.listdir("tokens/")
        if len(a)==0 :
            return
        else:
            # filter = {}

            for x in a:
                name = x[x.index("@") + 1:x.index(".json")]
                if not name.upper() in self.filter.keys():
                    self.filter[name.upper()] = [x]
                else:
                    self.filter[name.upper()].append(x)
                os.remove("tokens/" + x)

            for x in self.filter.keys():
                for i in self.domain.children:
                    if i.text== x[:8].replace(" ", "\n"):
                        pass
                    else:
                        self.damain.add_widget(Button(text=x[:8].replace(" ", "\n"), ids={"idd": self.filter[x]}, background_color=(1, .89, 0, .8),
                                   background_normal="data/icos/bb.png", size_hint=(1, .15),on_release=lambda w: self.return_widget(w, w.text)))

    def pppp(self,B):
        new_popup_ = Popup(title="TOKENS:", background_color=(0, 0, 0, 0), background="", title_size=Window.size[1] / 25,
                           title_align="center", separator_color=(1, 0, 0, 0), size_hint=(.4, .35),
                           content=Label(text=B.ids["id"]), disabled=False)
        new_popup_.open()

    def return_widget(self,w,tx):
        if len(self.SLD) > 0 :
            self.call_slid2()

        All= w.ids["idd"]

        self.SUP=ScrollView(size_hint=(.78, .8), pos_hint={'center_x': self.HIDE, 'center_y': .5},do_scroll_x=False, do_scroll_y=True, scroll_type=['bars', 'content'],
                                      bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
        self.retrned = GridLayout(cols=1,size_hint=(.78, None), size=(1,(Window.size[1]/4)*len(All)),pos_hint={'center_x': .32, 'center_y': .5}) # BIG UP DOWN           SET SIZE AFTER

        for dom in All :
            DD=json.load(open("REMINDERS/"+dom,"r"))

            srt = ScrollView(size_hint=(.8, None),size=(1,Window.size[1]/6), pos_hint={'center_x': .6, 'center_y': .5}, do_scroll_x=True,
                                  do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)

            l_r = GridLayout(cols=7,spacing=15, size_hint=(None, .7),size=(Window.size[0]*3,1) ,pos_hint={'center_x': .5,'center_y': .5})  # left right          SET SIZE AFTER

            begin=GridLayout(cols=1,size_hint=(.17, .35))
            domain=Button(text=DD["domain"],markup=True,halign="center",valign="middle",pos_hint={'center_x': .1,'center_y': .5},background_color = (0, 0, 0, .5))

            title=Button(on_release=self.pppp,text=DD["Title"],ids={"id":DD["idd"][:3]+DD["idd"][-3:]},markup=True,halign="center",valign="middle",font_size=self.height/80,
                         text_size=(self.width/4,self.height/9),pos_hint={'center_x': .1,'center_y': .2},background_color = (1,.7,0,.5))
            begin.add_widget(domain)
            begin.add_widget(title)

            detail=Button(text=DD["Details "][:70]+"...",ids={"src":DD},size_hint=(.28, .85),pos_hint={'center_x': .25,'center_y': .2},
                          markup=True, halign="center", valign="middle", font_size=self.height / 80,
                          on_release=lambda w:self.wid_detail(w),background_color = (0, 0, 0, .6))

            ws=ScrollView(size_hint=(.12, .91), pos_hint={'center_x':.415, 'center_y': .2},do_scroll_x=False, do_scroll_y=True, scroll_type=['bars', 'content'],
                                      bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
            ws.add_widget(self.wsee(DD))  #self.MAIN

            wt = ScrollView(size_hint=(.12, .91), pos_hint={'center_x': .555, 'center_y': .2}, do_scroll_x=False,
                            do_scroll_y=True, scroll_type=['bars', 'content'],bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
            wt.add_widget(self.wtr(DD))

            frequenc=Spinner(text="Remind "+DD["reminder frequency"], values=("once", "Repeated"),size_hint=(.10, .4),pos_hint={'center_x': .67,'center_y': .5},background_color=(0,0,0,.78))
            frequenc.bind(text=lambda w,t :self.freq(w,t,MAIN=DD))

            wR = ScrollView(size_hint=(.12, .91), pos_hint={'center_x': .79, 'center_y': .2}, do_scroll_x=False,
                            do_scroll_y=True, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1),
                            bar_margin=0)
            wR.add_widget(self.wRC(DD))

            ED_TM=Button(text="Edit time", size_hint=(.10, .4),pos_hint={'center_x': .913,'center_y': .5},background_color=(0,0,0,.78))
            ED_TM.bind(on_release=lambda e:self.freq(w,fq=DD["reminder frequency"],MAIN=DD,edit=100))    #DD["reminder frequency"]

            #   REMEMBER TIME   AND     TITLES ABOVE

            # l_r.add_widget(domain)
            l_r.add_widget(begin)
            l_r.add_widget(detail)
            l_r.add_widget(ws)
            l_r.add_widget(wt)
            l_r.add_widget(frequenc)
            l_r.add_widget(wR)
            l_r.add_widget(ED_TM)


            srt.add_widget(l_r)
            self.retrned.add_widget(srt)
        self.SUP.add_widget(self.retrned)

        self.SLD.append([self.SUP, self])
        self.call_slid(wid=self.SUP,point=.65)
        self.add_widget(self.SUP)
        # return self.SUP

    def wid_detail(self,ddd,file=None):
        """PREVIOUS TEXT       SCROLLABLE TEXT"""
        car = Carousel(direction="right", size_hint=(1., 1.))  # , loop=True

        self.BW=0
        if file :
            dd = ddd
            txt = dd["Details "]
        else:
            dd = ddd.ids["src"]
            txt = dd["Details "]

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)


        scroll_view = ScrollView(
            size_hint=(1, .8),
            bar_width=10,  # Customize the scrollbar width
            scroll_type=['bars', 'content'],  # Enable both scrollbar and content dragging
            do_scroll_x=False,  # Disable horizontal scrolling
            do_scroll_y=True  # Enable vertical scrolling
        )

        # Create a TextInput with multiline and size_hint set
        b = TextInput(
            text=txt,
            multiline=True,
            size_hint_y=None,  # Disable auto-resize
            height=500,  # Set a height to enable scrolling
            font_size=35,  # Increase font size for readability
            background_color=(1, 1, 1, .9),  # White background for TextInput
            foreground_color=(0, 0, 0, .9),  # Black text color
            padding=[10, 10, 10, 10] , # Add padding for better UX
            ids={"src": dd}
        )
        # Set the height of the TextInput dynamically
        b.bind(minimum_height=b.setter('height'))

        b.bind(text=lambda w, tx: self.Edit(dd, tx))
        Window.bind(on_touch_down=lambda w, t: self.opo(self.new_popup, b))
        Window.bind(on_touch_up=lambda w, t: Clock.unschedule(self.C_SCH))  # error not difined

        scroll_view.add_widget(b)


        main_layout.add_widget(scroll_view)

        with scroll_view.canvas.before:
            Color(0, 0, 0, 0.5)
            self.rect = Rectangle(size=scroll_view.size, pos=scroll_view.pos)
            scroll_view.bind(size=self._update_rect, pos=self._update_rect)


        b.bind(focus=self.on_text_input_focus)

        car.add_widget(main_layout)
        hist = os.listdir("HST/")
        if len(hist) > 0:
            for H in hist :
                dcto=json.load(open("HST/"+H,"r"))
                car.add_widget(S_TextInputApp(Text=dcto["Details "],BG=(1,.0,.2,.7),FG=(1,1,1,.9)))

        if file:
            self.new_popup = Popup(title=dd["domain"] + " => " + dd["Title"], background_color=(0, 0, 0, .3),
                              background="", title_size=Window.size[1] / 25, title_align="center",
                              separator_color=(1, 0, 0, .5), size_hint=(1, .65), content=car, disabled=False)
            self.new_popup.open()

            os.remove(dr() + "ready/" + file)
        else:
            self.new_popup = Popup(title=dd["domain"] + " / " + dd["Title"], background_color=(0, 0, 0, .3),
                              background="", title_size=Window.size[1] / 25, title_align="center",
                              separator_color=(1, 0, 0, .5), size_hint=(1, .45), content=car, disabled=False)
            self.new_popup.open()

    def _update_rect(self, instance, value):
        """ Update the background rectangle size and position """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def on_text_input_focus(self, instance, value):
        """Handle focus event for the TextInput"""
        if value:  # If the TextInput is focused
            print("TextInput is focused")
            self.new_popup.pos_hint = {"center_x": .5, "center_y": .85}
            # Window.request_keyboard(self._keyboard_closed, instance)
        else:
            print("TextInput focus lost")
            self.new_popup.pos_hint = {"center_x": .5, "center_y": .6}

    def _keyboard_closed(self):
        """Handle keyboard closing event."""
        print("Keyboard has been closed")

    #?????/////////////////////////////////////////////////////////////////////////////

    def opo(self,pop,w):
        self.C_SCH=Clock.schedule_interval(lambda x: self.oppo(pop, w),1)
        w.bind(on_touch_up=lambda w, t: Clock.unschedule(self.C_SCH))

    def oppo(self,pop,w):
        if self.BW == 2:
            Clock.unschedule(self.C_SCH)
            if w.background_color==[0, 0, 0, 0.98] :
                w.background_color = (1, 1, 1, 1)
                w.foreground_color=(0,0,0,.98)
                pop.background_color=(0,0,0,.98)
                pop.title_color=(1,1,1,.98)
            else:
                w.background_color = (0, 0, 0, .98)
                w.foreground_color= (1, 1, 1, .98)
                pop.background_color = (1, 1, 1, .98)
                pop.title_color = (0, 0, 0, .98)
            self.BW=0
        else:
            self.BW+=1

    def Edit(self,MAIN,tx):
        json.dump(MAIN, open("HST/" + MAIN["idd"] + "@" + MAIN["domain"].upper() + '.json', "w"))
        if tx.endswith((" ", ".", ",", "\n", "\r") ):
            MAIN["Details "] = tx
            json.dump(MAIN, open("REMINDERS/" + MAIN["idd"] + "@" + MAIN["domain"].upper() + '.json', "w"))
            send(MAIN)

    def goten(self,w,v):
        if w.text != "" :
            self.MAIN[w.hint_text[:w.hint_text.index("*")]]= w.text

    def BASE(self):
        dir=self.MAIN["idd"]+"@"+self.MAIN["domain"].upper()

        # if not os.path.isdir( "REMINDERS/"+dir ):
        #     os.mkdir(  "REMINDERS/"+dir  )

        json.dump(self.MAIN,open("REMINDERS/"+dir+".json","w"))
        # json.dump({"recipients":[]},open("REMINDERS/"+dir+"/"+"."+self.MAIN["domain"].upper()+".json","w"))
        send(self.MAIN)
        Clock.schedule_once(self.home)

    def New(self,gri):
        if len(self.SLD) > 0 :
            self.call_slid2()

        self.addgr = GridLayout(cols=1, spacing=Window.size[1] / 35, size_hint=(.2,.2),pos_hint={"center_x": .5, "center_y": .53})

        new = Button(text="New", background_normal="data/icos/bb.png",background_color=(.65,0,.2,.8), on_release=self.make)
        join = Button(text="Join", background_normal="data/icos/bb.png",background_color=(.65,0,.2,.8),on_release=self.token)
        Del = Button(text="Delete", background_normal="data/icos/bb.png", background_color=(.65, 0, .2, .8),on_release=self.Delete)

        new.bind(on_release= lambda w: self.remove_widget(self.addgr ))
        join.bind(on_release= lambda w: self.remove_widget(self.addgr ))
        Del.bind(on_release=lambda w: self.remove_widget(self.addgr))

        self.addgr.add_widget(new)
        self.addgr.add_widget(join)
        self.addgr.add_widget(Del)
        self.add_widget(self.addgr)

        self.SLD.append([self.addgr,self])

    def Delete(self,x):
        def CUT(st):
            if len(st)<=5:
                return st
            else:
                return st[:5]+"..."
        def confirm(Btn):
            if not Btn.ids["fl"] in DELETABLE:
                DELETABLE.append(Btn.ids["fl"])
            else:
                DELETABLE.remove(Btn.ids["fl"])
            print(DELETABLE)
        DELETABLE=[]
        files=os.listdir("REMINDERS/")
        r = RelativeLayout(size_hint=(1, .9), pos_hint={"center_x":.5, "center_y": .5})
        s = ScrollView(size_hint=(.95, .99), do_scroll_x=False, do_scroll_y=True, scroll_timeout=55, scroll_distance=20,
                       scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
        layout = GridLayout(cols=1, size_hint=(1, None), row_default_height=Window.size[1] /13,row_force_default=True,size=(1, (Window.size[1] / 7) * len(files)))
        layout.add_widget(Label(text=" "))
        # r.add_widget(Label(text="Choose Reminders to delete : \n ", pos_hint={"center_x": .5, "center_y": .97}))
        for i in files:
            DC=json.load(open("REMINDERS/"+i,"r"))
            button = ToggleButton(text=CUT(DC["domain"].upper()) + "/" + CUT(DC["Title"].upper()),ids={"fl":i},background_normal="data/icos/bb.png",background_color=(.65,0,.2,.8))
            # button.bind(on_release=lambda w:DELETABLE.append(i))
            button.bind(on_release=confirm)
            layout.add_widget(button)

        s.add_widget(layout)
        r.add_widget(s)

        okbt = Button(background_normal="data/icos/ok.png", background_down="data/icos/k.png", size_hint=(None, None),
                      size=(Window.size[0] / 9, Window.size[0] / 9), pos_hint={"center_x": .89, "center_y": .05},
                      on_release=lambda w: [os.remove("REMINDERS/"+file) for file in DELETABLE])
        r.add_widget(okbt)

        new_popup = Popup(title="Choose Reminders to delete :", title_size=Window.size[1] / 40, title_align="center",
                          separator_color=(1, 1, 1, 1), size_hint=(.5, .5), content=r,disabled=False)

        new_popup.open()

        okbt.bind(on_release=lambda w: new_popup.dismiss())
        okbt.bind(on_release=lambda w: Clock.schedule_once(self.home) )


    def make(self,w):
        if len(self.SLD) > 0 :
            self.call_slid2()
        idd=str(uuid.uuid4())[:5]
        me_name=" ".join(json.load( open("SD/conf/me.json","r")  )["Name"])
        iddd=json.load( open("SD/conf/me.json","r")  )["idd"]
        self.MAIN = {"domain": "",
                     "Title": "",
                     "Details ": "",
                     "Responsible": "",
                     "idd": idd,
                     "sender": iddd,
                     "Who can see": [me_name],
                     "viewers":[me_name],
                     "who can remind": [me_name],
                     "trigers":[],
                     "reminder frequency": "",
                     "who receive same reminder": [me_name],
                     "receivers":[me_name],
                     "recipients": [iddd],
                     "start date": "",
                     "action":"New Alarm"}


        self.DOMAIN = TextInput(multiline=False,hint_text="domain* ex: school, family, job, church, ...")
        self.DOMAIN.bind(focus=self.goten)
        self.DOMAIN.bind(on_text_validate=self.DICT)
        self.box1 = GridLayout(cols=1, size_hint=(.6, .05))
        self.box1.add_widget(self.DOMAIN)

        self.SLD.append([self.box1, self])
        self.call_slid(wid=self.box1)
        self.add_widget(self.box1)


        self.resp = TextInput(hint_text="Responsible* / OVERSEER",multiline=False)
        self.resp.bind(focus=self.goten)
        self.resp.bind(on_text_validate=self.DICT)
        self.box2 = GridLayout(cols=1, size_hint=(.6, .05),pos_hint={"center_x": self.HIDE, "center_y": .5})
        self.box2.add_widget(self.resp)

        self.title = TextInput(hint_text="Title* ex: study, sport, debt ,payment...",multiline=False)
        self.title.bind(focus=self.goten)
        self.title.bind(on_text_validate=self.DICT)
        self.box3 = GridLayout(cols=1, size_hint=(.6, .05),pos_hint={"center_x": self.HIDE, "center_y": .5})
        self.box3.add_widget(self.title)

        self.details = TextInput(hint_text="Details * or plans,scennario ex: i may need 2 concret nail",multiline=False)
        self.details.bind(focus=self.goten)
        self.details.bind(on_text_validate=self.DICT)
        self.box4 = GridLayout(cols=1, size_hint=(.6, .05),pos_hint={"center_x": self.HIDE, "center_y": .5})
        self.box4.add_widget(self.details)

        self.who_see = self.who_sees(self.MAIN)

        self.who_remind = self.Who_rec(self.MAIN)

        self.schedule = Spinner(text="Scheduled", values=("once", "Repeated"),size_hint=(.7, .05))
        self.schedule.bind(text=lambda w,t :self.freq(w,t))
        self.schedule.bind(text=self.DICT)

        self.who_receive_same_remind = self.Trigers(self.MAIN)

        self.BT = [self.box2,self.box3,self.box4, self.who_see, self.who_remind, self.schedule,self.who_receive_same_remind]

    def token(self,x):
        if len(self.SLD) > 0 :
            self.call_slid2()

        self.DOMAIN = TextInput(background_color=(0,0,0,.91),foreground_color=(1,1,1,1),multiline=False, hint_text="    Tokens   ",pos_hint={"center_x": self.HIDE, "center_y": .5})
        self.DOMAIN.bind(focus=self._tok)
        self.DOMAIN.bind(text=self._tok)
        self.box1 = GridLayout(cols=1, size_hint=(.6, .05))
        self.box1.add_widget(self.DOMAIN)

        self.SLD.append([self.box1, self])
        self.call_slid(wid=self.box1)
        self.add_widget(self.box1)

    def _tok(self,w,t=None):
        if not w.text or len(w.text)> 6:
            w.text=w.text[:-1]
            return
        if len(w.text) ==6 :
            self.call_slid2()
            #  loading function
            # self.loading()
            Clock.schedule_once(self.loading)
            me_name = " ".join(json.load(open("SD/conf/me.json", "r"))["Name"])
            idd= " ".join(json.load(open("SD/conf/me.json", "r"))["idd"])
            di={"action":"token","token":w.text,"recipients":[],"name":me_name,"idd":idd}
            send(di)
            Clock.schedule_once(lambda d:self.loading(1,stop=10),3)

    def loading(self,b,stop=None):
        if stop :
            # Clock.unschedule()
            try:
                self.remove_widget(self.srt)
            except:
                pass
        else:
            self.srt = ScrollView(size_hint=(1,.07),  pos_hint={'center_x': .5, 'center_y': .1},
                             do_scroll_x=True,do_scroll_y=False, scroll_type=['bars', 'content'],bar_width=1, bar_color=(1, 1, 0, 0))

            l_r = GridLayout(cols=12, spacing=5, size_hint=(None, .7), size=(Window.size[0] * 5, 1),
                             pos_hint={'center_x': .5, 'center_y': .5})
            for x in range(12):
                l_r.add_widget(Label(color=(0,1,0,.2),text="1010101010101010101010101010101010101010101010101010101"))        #str(uuid.uuid4())
                l_r.add_widget(Label(color=(0, 1, 0, .2), text="0101010101010101010101010101010101010101010101010101"))

            self.srt.add_widget(l_r)
            self.add_widget(self.srt)

            self.SLD.append([self.srt,self])

            Clock.schedule_once(lambda x: self.auto_scroll(self.srt, "x", 0.02))

    def DICT(self,WID,txt=None):
        if len(self.BT) == 0 :
            self.call_slid2()
            return

        self.call_slid2()
        self.SLD.append([self.BT[0], self])
        self.call_slid(wid=self.BT[0])
        self.add_widget(self.BT[0])

        del self.BT[0]

    def save(self,ok):
        print("ok: ",ok)
        # disponible=[]
        alow={}
        for i in ok.keys():
            if ok[i] == "" :
                pass
            else:
                alow[i]=ok[i]
                # disponible.append(i)
        # ok["dispo"] =disponible

        self.MAIN["time"] =alow
        # del disponible
        # del alow

    def receive(self,rx):
        new_popup = Popup(title=rx["tt"], title_size=Window.size[1] / 50, title_align="center",
                          separator_color=(1, 1, 1, 0), size_hint=(.4, .4), content=Label(text=rx["msg"]), disabled=False)
        new_popup.open()

    def wsee(self,dd):
        # r=RelativeLayout(size_hint=(.35,.4),pos_hint={"center_x": self.HIDE, "center_y": .5})

        layout = GridLayout(cols=1,size_hint=(1,None),size=(1,(Window.size[1]/20)*len(dd["Who can see"])))
        layout.add_widget(Label(text="Who can see \n"))
        for i in dd["Who can see"]:   # list
            button = ToggleButton(text=i)
            if i in dd["viewers"] :
                button.state = 'down'
            button.bind(on_release=lambda w:self.ws_press(w,dd))
            layout.add_widget(button)

        return layout

    def ws_press(self, button,MAIN):
        if button.state == 'down' :
            MAIN["viewers"].append(button.text)
        else:
            try:
                MAIN["viewers"].remove(button.text)
            except:
                pass
        json.dump(MAIN, open("REMINDERS/" + MAIN["idd"] + "@" + MAIN["domain"].upper() + '.json', "w"))
        send(MAIN)
        # print(f"{button.text} {'selected' if button.state == 'down' else 'deselected'}")
        print(MAIN)

    def wtr(self,dd):

        r=RelativeLayout(size_hint=(.35,.4),pos_hint={"center_x": self.HIDE, "center_y": .5})

        layout = GridLayout(cols=1,size_hint=(1,None),size=(1,(Window.size[1]/15)*len(dd["Who can see"])))
        layout.add_widget(Label(text="who can remind \n"))
        # Create ToggleButtons
        for i in dd["who can remind"]:   # list
            button = ToggleButton(text=i)
            if i in dd["trigers"] :
                button.state = 'down'
            button.bind(on_release=lambda w:self.wt_press(w,dd))
            layout.add_widget(button)

        return layout

    def wt_press(self, button,MAIN):
        if button.state == 'down' :
            MAIN["trigers"].append(button.text)
        else:
            try:
                MAIN["trigers"].remove(button.text)
            except:
                pass
        json.dump(MAIN,open("REMINDERS/"+MAIN["idd"]+"@"+MAIN["domain"].upper()+'.json',"w") )
        send(MAIN)
        # print(f"{button.text} {'selected' if button.state == 'down' else 'deselected'}")
        print(MAIN)

    def wRC(self,dd):

        r=RelativeLayout(size_hint=(.35,.4),pos_hint={"center_x": .5, "center_y": .5})

        layout = GridLayout(cols=1,size_hint=(1,None),size=(1,(Window.size[1]/20)*len(dd["who receive same reminder"])))
        layout.add_widget(Label(text="who receives \n"))
        # Create ToggleButtons
        for i in dd["who receive same reminder"]:   # list
            button = ToggleButton(text=i)
            if i in dd["receivers"] :
                button.state = 'down'
            button.bind(on_release=lambda w:self.wRC_press(w,dd))
            layout.add_widget(button)

        return layout

    def wRC_press(self, button,MAIN):
        if button.state == 'down' :
            MAIN["receivers"].append(button.text)
        else:
            try:
                MAIN["receivers"].remove(button.text)
            except:
                pass
        json.dump(MAIN,open("REMINDERS/"+MAIN["idd"]+"@"+MAIN["domain"].upper()+'.json',"w") )
        send(MAIN)
        # print(f"{button.text} {'selected' if button.state == 'down' else 'deselected'}")
        print(MAIN)

    def join(self,x):
        pass

    def edited(self,MAIN,ED):
        MAIN["time"]=ED
        json.dump(MAIN, open("REMINDERS/" + MAIN["idd"] + "@" + MAIN["domain"].upper() + '.json', "w"))
        send(MAIN)

    def freq(self,w,fq,MAIN={},edit=None):
        print(fq, MAIN, edit)
        if len(MAIN) > 0 and not edit:
            MAIN["reminder frequency"] = fq.split(" ")[-1]
            json.dump(MAIN, open("REMINDERS/" + MAIN["idd"] + "@" + MAIN["domain"].upper() + '.json', "w"))
            send(MAIN)
            return

        ys = list(range(int(time.strftime("%Y")), 2041))
        for i in ys:
            ys[ys.index(i)] = str(i)

        dy = list(range(1, 32))
        for i in dy:
            if len(str(i)) == 1:
                dy[dy.index(i)] = "0" + str(i)
            else:
                dy[dy.index(i)] = str(i)

        hr = list(range(0, 24))
        for i in hr:
            if len(str(i)) == 1:
                hr[hr.index(i)] = "0" + str(i)
            else:
                hr[hr.index(i)] = str(i)

        MIN = list(range(0, 60))
        for i in MIN:
            if len(str(i)) == 1:
                MIN[MIN.index(i)] = "0" + str(i)
            else:
                MIN[MIN.index(i)] = str(i)

        cl_o = ["Year", "Month", "Date", "Day", "Hour", "Min"]
        cl_i = ["Month", "Date", "Day", "Hour", "Min"]
        if fq == "once" or MAIN.get("reminder frequency", 0) == "once":
            self.grido = GridLayout(pos_hint={"center_x": self.HIDE, "center_y": .5}, size_hint=(1, .3), cols=6,
                                    row_default_height=Window.height / 15, row_force_default=True,
                                    col_default_width=Window.size[0] / 6, col_force_default=True)
            for x in cl_o:
                self.grido.add_widget(
                    TextInput(text=x, background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1), readonly=True))
            year = Spinner(text=time.strftime("%Y"), values=tuple([""] + ys))
            mounth = Spinner(text=time.strftime("%B"), values=tuple(
                ["", 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']))
            date = Spinner(text=time.strftime("%d"), values=tuple([""] + dy))
            day = Spinner(text=time.strftime("%A"),
                          values=("", "Monday", "Tuesday", "Wednesday", "Thurday", "Friday", "Saturday", "Sunday"))
            hour = Spinner(text=time.strftime("%H"), values=tuple([""] + hr))
            min = Spinner(text=time.strftime("%M"), values=tuple([""] + MIN))
            wid = [year, mounth, date, day, hour, min]
            all = {"Y": year.text, "B": mounth.text, "d": date.text, "A": day.text, "H": hour.text, "M": min.text}
            for x in wid:
                # x.bind(text= lambda w,t: self.valid(all))
                self.grido.add_widget(x)
            if not edit:
                self.MAIN["reminder frequency"] = fq

            r = RelativeLayout(size_hint=(1, .3), pos_hint={"center_x": .5, "center_y": .5})
            okbt = Button(background_normal="data/icos/ok.png", background_down="data/icos/k.png",
                          size_hint=(None, None),
                          size=(Window.size[0] / 7, Window.size[0] / 7), pos_hint={"center_x": .5, "center_y": .05})

            if edit:
                okbt.bind(on_release=lambda w: self.edited(MAIN, {"Y": year.text, "B": mounth.text, "d": date.text,
                                                                  "A": day.text, "H": hour.text, "M": min.text}))
                okbt.bind(on_release=lambda w: self.remove_widget(self.grido))
            else:
                okbt.bind(on_release=lambda w: self.DICT(self.grido))
                okbt.bind(on_release=lambda w: self.save(
                    {"Y": year.text, "B": mounth.text, "d": date.text, "A": day.text, "H": hour.text, "M": min.text}))

            r.add_widget(okbt)
            self.grido.add_widget(r)

        elif fq == "Repeated" or MAIN.get("reminder frequency", 0) == "Repeated":
            if not edit:
                self.MAIN["reminder frequency"] = fq
            self.grido = GridLayout(pos_hint={"center_x": self.HIDE, "center_y": .5}, size_hint=(1, .45), cols=5,
                                    row_default_height=Window.height / 15, row_force_default=True,
                                    col_default_width=Window.size[0] / 6, col_force_default=True)
            for x in cl_i:
                self.grido.add_widget(
                    TextInput(text=x, background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1), readonly=True))
            # year = Spinner(text="", values=tuple(ys))  #  NO YEAR  REPEATS
            mounth = Spinner(text=time.strftime("%B"), values=(
            "", 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
            'November', 'December'))
            date = Spinner(text=time.strftime("%d"), values=tuple([""] + dy))
            day = Spinner(text=time.strftime("%A"),
                          values=("", "Monday", "Tuesday", "Wednesday", "Thurday", "Friday", "Saturday", "Sunday"))
            hour = Spinner(text=time.strftime("%H"), values=tuple([""] + hr))
            min = Spinner(text=time.strftime("%M"), values=tuple([""] + MIN))

            wid = [mounth, date, day, hour, min]
            all = {"B": mounth.text, "d": date.text, "A": day.text, "H": hour.text, "M": min.text}
            for x in wid:
                # x.bind(text=lambda w, t: self.valid(all))
                self.grido.add_widget(x)

            r = RelativeLayout(size_hint=(1, .3), pos_hint={"center_x": .5, "center_y": .5})

            okbt = Button(background_normal="data/icos/ok.png", background_down="data/icos/k.png",
                          size_hint=(None, None),
                          size=(Window.size[0] / 7, Window.size[0] / 7), pos_hint={"center_x": .5, "center_y": .05})
            if edit:
                okbt.bind(on_release=lambda w: self.edited(MAIN, {"B": mounth.text, "d": date.text, "A": day.text,
                                                                  "H": hour.text, "M": min.text}))
                okbt.bind(on_release=lambda w: self.remove_widget(self.grido))
            else:
                okbt.bind(on_release=lambda w: self.DICT(self.grido))
                okbt.bind(on_release=lambda w: self.save(
                    {"B": mounth.text, "d": date.text, "A": day.text, "H": hour.text, "M": min.text}))

            r.add_widget(okbt)
            self.grido.add_widget(r)
            if not edit:
                self.MAIN["reminder frequency"] = fq

        # self.BT.append(self.grido)
        if edit:
            self.add_widget(self.grido)
            self.grido.pos_hint = {"center_x": .5, "center_y": .5}
        else:
            self.BT.insert(0, self.grido)

    def valid(self,dc):
        st = dc["A"] + "," + dc["B"] + " " + dc["d"] + " " + dc["Y"]
        try:

            datetime.datetime.strptime(st,'%A,%B %d %Y')
            print("valid",st)
            return True
        except:
            print("invalid",st)
            return False

    def who_sees(self,dd):

        r=RelativeLayout(size_hint=(.6,.4),pos_hint={"center_x": self.HIDE, "center_y": .5})
        s=ScrollView(size_hint=(.55, .8), do_scroll_x=False,
                                do_scroll_y=True, scroll_timeout=55, scroll_distance=20,
                                scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
        layout = GridLayout(cols=1,size_hint=(1,None),size=(1,(Window.size[1]/20)*len(dd["Who can see"])))
        # layout.add_widget(Label(text=" \n"))
        r.add_widget(Label(text="Share with : \n ",pos_hint={"center_x": .5, "center_y": .97}))

        # Create ToggleButtons
        for i in dd["Who can see"]:   # list
            button = ToggleButton(text=i)
            button.bind(on_press=self.on_button_press)
            layout.add_widget(button)
        s.add_widget(layout)
        r.add_widget(s)

        okbt = Button(background_normal="data/icos/ok.png", background_down="data/icos/k.png", size_hint=(None, None),
                              size=(Window.size[0] / 7, Window.size[0] / 7),pos_hint={"center_x": .5, "center_y": .05},
                      on_release=lambda w : self.DICT(r))
        r.add_widget(okbt)
        return r

    def on_button_press(self, button):
        if button.state == 'down' :
            self.MAIN["viewers"].append(button.text)
        else:
            try:
                self.MAIN["viewers"].remove(button.text)
            except:
                pass
        # print(f"{button.text} {'selected' if button.state == 'down' else 'deselected'}")
        print(self.MAIN)

    def Who_rec(self,dd):
        r = RelativeLayout(size_hint=(.6, .4), pos_hint={"center_x": self.HIDE, "center_y": .5})
        s=ScrollView(size_hint=(.55, .8),  do_scroll_x=False,
                                do_scroll_y=True, scroll_timeout=55, scroll_distance=20,
                                scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
        layout = GridLayout(cols=1,size_hint=(1,None),size=(1,(Window.size[1]/20)*len(dd["who receive same reminder"])))
        # layout.add_widget(Label(text=" "))
        r.add_widget(Label(text="Who to remind : \n ",pos_hint={"center_x": .5, "center_y": .97}))

        # Create ToggleButtons
        for i in dd["who receive same reminder"]:   # list
            button = ToggleButton(text=i)
            button.bind(on_press=self.on_button_press2)
            layout.add_widget(button)
        s.add_widget(layout)

        r.add_widget(s)

        okbt = Button(background_normal="data/icos/ok.png", background_down="data/icos/k.png", size_hint=(None, None),
                      size=(Window.size[0] / 9, Window.size[0] / 9), pos_hint={"center_x": .5, "center_y": .05},
                      on_release=lambda w: self.DICT(r))
        r.add_widget(okbt)
        return r

    def on_button_press2(self, button):
        if button.state == 'down' :
            self.MAIN["receivers"].append(button.text)
        else:
            try:
                self.MAIN["receivers"].remove(button.text)
            except:
                pass
        print(f"{button.text} {'selected' if button.state == 'down' else 'deselected'}")

    def Trigers(self,dd):
        r = RelativeLayout(size_hint=(.6, .4), pos_hint={"center_x": self.HIDE, "center_y": .5})
        s=ScrollView(size_hint=(.55, .8), do_scroll_x=False,
                                do_scroll_y=True, scroll_timeout=55, scroll_distance=20,
                                scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)
        layout = GridLayout(cols=1,size_hint=(1,None),size=(1,(Window.size[1]/20)*len(dd["who can remind"])))
        layout.add_widget(Label(text=" "))
        r.add_widget(Label(text="Allowed to trigger : \n ",pos_hint={"center_x": .5, "center_y": .97}))

        # Create ToggleButtons
        for i in dd["who can remind"]:   # list
            button = ToggleButton(text=i)
            button.bind(on_press=self.on_button_press3)
            layout.add_widget(button)

        s.add_widget(layout)
        r.add_widget(s)

        okbt = Button(background_normal="data/icos/ok.png", background_down="data/icos/k.png", size_hint=(None, None),
                      size=(Window.size[0] / 7, Window.size[0] / 7), pos_hint={"center_x": .5, "center_y": .05},
                      on_release=lambda w: self.DICT(r))
        okbt.bind(on_release=lambda w: self.BASE())
        r.add_widget(okbt)
        return r

    def on_button_press3(self, button):
        if button.state == 'down' :
            self.MAIN["trigers"].append(button.text)
        else:
            try:
                self.MAIN["trigers"].remove(button.text)
            except:
                pass
        print(f"{button.text} {'selected' if button.state == 'down' else 'deselected'}")

    def call_slid2(self):
        wid=self.SLD[-1][0]
        self.PARENT=self.SLD[-1][1]

        self.stp2 = -.2  #point
        self.WIDG2 = wid

        print("wid",wid.ids)
        if wid.pos_hint=={} :
            print(wid.pos)
            self.insid2 = wid.pos[0]
            self.trace = self.insid2
            Clock.schedule_interval(self.slid_new_acc2, 1 / 100)
        else:
            self.insid2 = wid.pos_hint["center_x"]
            self.trace = self.insid2
            print(wid.pos_hint)
            Clock.schedule_interval(self._slid_new_acc2, 1 / 100)

    def slid_new_acc2(self,x):
        if self.WIDG.pos[0] <= self.WIDG.ids.get('x',0):
            Clock.unschedule(self.slid_new_acc2)
            self.PARENT.remove_widget(self.WIDG2)
            del self.SLD[-1]
            print("done")

        else:
            if self.WIDG.pos[0] >= self.WIDG.ids['x']/1.5:
                self.WIDG.pos=(self.WIDG.pos[0]-1,self.WIDG.pos[1])

            else:
                self.WIDG.pos=(self.WIDG.pos[0]-4,self.WIDG.pos[1])

    def _slid_new_acc2(self,x):
        if self.insid2 < self.stp2 :
            Clock.unschedule(self._slid_new_acc2)
            self.PARENT.remove_widget(self.WIDG2)
            try:
                del self.SLD[-1]
            except:
                pass

            print("done")

        else:
            if self.insid2 < self.trace/2 :
                self.WIDG2.pos_hint = {"center_x": self.insid2, "center_y": .5}
                self.insid2 -= 0.07
            else:
                self.WIDG2.pos_hint={"center_x":self.insid2,"center_y":.5}
                self.insid2-= 0.01

    def call_slid(self,wid,point=.52):
        print(wid.pos)
        self.stp1=point
        self.WIDG=wid
        self.insid = - .2
        if wid.pos_hint== {} :
            Clock.schedule_interval(self.slid_new_acc, 0)
        else:
            Clock.schedule_interval(self._slid_new_acc, 0)

    def slid_new_acc(self,x):

        if self.WIDG.pos[0] >= self.WIDG.ids['x']:
            Clock.unschedule(self.slid_new_acc)
            # self.call_slid2()
        else:
            if  self.WIDG.pos[0] >= self.WIDG.ids['x']/1.5:
                self.WIDG.pos=(self.WIDG.pos[0]+3,self.WIDG.pos[1])

            else:
                self.WIDG.pos=(self.WIDG.pos[0]+17,self.WIDG.pos[1])

    def _slid_new_acc(self,x):

        if self.insid >= self.stp1 :
            Clock.unschedule(self._slid_new_acc)
            # self.call_slid2()
        else:
            if self.insid > self.stp1/1.1  :
                self.WIDG.pos_hint = {"center_x": self.insid}
                self.insid += 0.001
            else:
                self.WIDG.pos_hint={"center_x":self.insid}
                self.insid+=0.03

    def auto_scroll(self, wid, xy, speed):
        global star_scl_plus, star_scl_minus
        try:
            Clock.unschedule(star_scl_plus)
            Clock.unschedule(star_scl_minus)
        except:
            pass

        self.end = 0
        star_scl_plus = Clock.schedule_interval(lambda x: self.star_scroll(wid, xy, speed), speed)

    def star_scroll(self, wid, xy, speed):
        st = self.end
        global star_scl_minus


        if os.path.isfile("stop_auto_scroll") :
            Clock.unschedule(star_scl_plus)
            Clock.unschedule(star_scl_minus)
            Clock.schedule_once(lambda w: self.loading(3,stop=3))
            os.remove("stop_auto_scroll")

        if self.end >= 1:
            Clock.unschedule(star_scl_plus)  # Clock.unschedule(star_scl_minus)
            star_scl_minus = Clock.schedule_interval(lambda x: self.back_scroll(wid, xy, speed), speed)
        else:
            if xy == "y":
                wid.scroll_y = st
                self.end += 0.009
            else:
                wid.scroll_x = st
                self.end += 0.009

    def back_scroll(self, wid, xy, speed):
        # print("BACK SCROLL")
        global star_scl_plus

        if os.path.isfile("stop_auto_scroll") :
            Clock.unschedule(star_scl_plus)
            Clock.unschedule(star_scl_minus)
            Clock.schedule_once(lambda w: self.loading(3, stop=3))
            os.remove("stop_auto_scroll")

        st = self.end
        if self.end <= 0:
            Clock.unschedule(star_scl_minus)
            star_scl_plus = Clock.schedule_interval(lambda x: self.star_scroll(wid, xy, speed), speed)
        else:
            if xy == "y":
                wid.scroll_y = st
                self.end -= 0.009
            else:
                wid.scroll_x = st
                self.end -= 0.009

   #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////









































































    def BS(self,x):

        Window.bind(on_keyboard=self.KEYS)
        #################################
        if "rideau2" in dir(self):
            print("self.rideau2.source: ", self.rideau2.source)
            wl = self.rideau2.source
        else:
            lt = os.listdir("Temp/")
            wl = "Temp/" + lt[randint(0, len(lt) - 1)]
    #########################################################


        self.Desktop = RelativeLayout(size_hint=(1., 1.))

        with self.Desktop.canvas.before:
            Color(1, 1, 1, 1)
            self.rideau2 = RoundedRectangle(source=wl, pos=(0, 0), size=(Window.width, Window.height),radius=[20])
        self.add_widget(self.Desktop)
         #333333333333333333333333333333333333333333333333333333333333333333333333333333333

        self.dustbin()
        self.add_widget(self.Add_item())
        print("#  KEEP DELETING EXPIRED VARIABLES FOR FAST MEMORY")

        for directory in ["org", "JobTalent", "paidAdds", self.ME["adress"][1]]:
            if not os.path.isdir(dr()+"Activities/"+directory):
                os.makedirs(dr()+"Activities/"+directory)


        self.DIST=(Window.size[1] /6)
        Clock.schedule_once(lambda cc: threading.Thread(target=self.org).start(), 1)
        Clock.schedule_once(lambda cc: threading.Thread(target=self.MME).start(), 1)

        self.OPTIONS()
        if not self.ME.get("jb",0) or len(self.ME.get("jb",[])) == 0:
            Clock.schedule_once(lambda cl: self.WORK(cl,msg="You have not selected any job! \nYou can choose up to 5:\n"),20)

        if platform != "android" :
            from SERVICE import start as ST
            threading.Thread(target=ST, args=(1,)).start()
        THR=threading.Thread(target= self.RECEIVER,args=(4,))
        THR.start()
        Clock.schedule_once(self.SIDEBAR,4)
        Clock.schedule_once(self.LOCAL_JOB, 4)
        # THR = threading.Thread(target=self.LOCAL_JOB, args=(4,))
        # THR.start()
        try:
            server.bind(b'/RECEIVER', self.RECEIVER)
        except:
            pass
        self.rn = 0

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   BLUETOOTH

        Clock.schedule_once(self.Bluetooth_receiver, 2)
        # Clock.schedule_once(self.Bluetooth_expose, 3)

    def Bluetooth_receiver(self, x):

        if platform == "android":

            try:

                import traceback
                from jnius import autoclass

                def received(sender=None, date=None):
                    discovered_devices_dir = os.path.join(activity.getFilesDir().getPath(), "service")
                    HERE = os.listdir(activity.getFilesDir().getPath())
                    Logger.info(f"HERE: {HERE}")

                    devices = {}

                    if os.path.exists(discovered_devices_dir):
                        HERE = os.listdir(discovered_devices_dir)
                        Logger.info(f"IN SERVICE: {HERE}")
                        for filename in os.listdir(discovered_devices_dir):
                            Logger.info(f"FILENAME: {filename}")
                            devices[filename] = eval(open(filename, 'r').read())

                    Logger.info(f"Received data: {devices}")
                    # return devices

                    discovered_devices_dir = os.path.join(activity.getFilesDir().getPath(), "Received_data")
                    HERE3 = os.listdir(discovered_devices_dir)
                    Logger.info(f"Received_data: {HERE3}")

                    devices2 = {}

                    if os.path.exists(discovered_devices_dir):
                        # HERE2 = os.listdir(discovered_devices_dir)
                        # Logger.info(f"HERE3: {HERE3}")
                        for filename3 in os.listdir(discovered_devices_dir):
                            Logger.info(f"FILENAME: {filename3}")
                            devices2[filename3] = eval(open(filename3, 'r').read())

                    Logger.info(f"Received data: {devices2}")
                    # return devices

                BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
                adapter = BluetoothAdapter.getDefaultAdapter()

                if not adapter.isEnabled():
                    adapter.enable()

                if not os.path.isdir("service"):
                    os.mkdir("service")
                    open("service/me", "w").write(str(self.ME))

                # Get the Android Context
                Context = autoclass("android.content.Context")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                activity = PythonActivity.mActivity

                # Access Java classes
                BLEAdvertiser = autoclass("org.kivy.emergency.BLEAdvertiser")
                BLEService = autoclass("org.kivy.emergency.BLEService")

                # Initialize BLEAdvertiser
                ble_advertiser = BLEAdvertiser(activity)

                # Start advertising
                service_uuid = "0000180f-0000-1000-8000-00805f9b34fb"  # Replace with your actual UUID
                data_key = "exampleKey"
                data_value = "exampleValue"
                # Combine service_uuid, data_key, and data_value into one string
                dictionary_entry = f"{service_uuid}:{data_key}:{data_value}"
                ble_advertiser.startAdvertising(dictionary_entry)
                # ble_advertiser.startAdvertising(service_uuid, data_key, data_value)

                # Initialize BLEService
                ble_service = BLEService(activity)

                # Start scanning
                ble_service.startScanning()


                Clock.schedule_interval(received, 2)
            except Exception as ex:
                Logger.info(f"BLUERROR: {ex} \n {traceback.format_exc()}")

        elif platform == "ios":
            print("ios")
            pass

        elif platform == "win":
            print("win")
            pass
            # import bluetooth
            #
            # def bluetooth_server():
            #     server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            #     server_socket.bind(("", bluetooth.PORT_ANY))
            #     server_socket.listen(1)
            #
            #     print("Waiting for connection...")
            #     client_socket, address = server_socket.accept()
            #     print(f"Connected to {address}")
            #
            #     with open("received_file.txt", "wb") as file:
            #         while True:
            #             data = client_socket.recv(1024)
            #             if not data:
            #                 break
            #             file.write(data)
            #
            #     print("File received successfully.")
            #     client_socket.close()
            #     server_socket.close()
            # try:
            #     bluetooth_server()
            # except:
            #     pass

        elif "mac" in platform:
            print("ios")
            pass

    def Bluetooth_expose(self,x):
        from jnius import autoclass
        BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        adapter = BluetoothAdapter.getDefaultAdapter()

        if not adapter.isEnabled():
            adapter.enable()

        try:
            import json
            import os
            from jnius import autoclass
            from kivy.clock import Clock
            from kivy.logger import Logger

            # Load the BLEService class
            BLEService = autoclass('org.kivy.emergency.BLEService')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            # Initialize BLEService
            context = PythonActivity.mActivity
            ble_service = BLEService(context)

            # Function to start scanning for BLE devices
            def start_scanning():
                ble_service.startScanning()

            # Function to read discovered devices from their respective files
            def read_discovered_devices(dt):
                discovered_devices_dir = os.path.join(context.getFilesDir().getPath(),
                                                      "Discovered_devices")  # "Received_data"
                # here=os.path.dirname(__file__)
                # DIR=os.path.abspath(os.path.join(here,dt))
                # ici=os.listdir(DIR)
                # parent_dir+="../"
                if os.path.isdir(context.getFilesDir().getPath()):
                    ici = os.listdir(context.getFilesDir().getPath())
                else:
                    ici = os.listdir("/")

                devices = []

                if os.path.exists(discovered_devices_dir):
                    # Logger.info(f"FOLDER EXISTS")
                    for date_dir in os.listdir(discovered_devices_dir):
                        # Logger.info(f"DATE_DIR:{date_dir}")
                        date_path = os.path.join(discovered_devices_dir, date_dir)
                        if os.path.isdir(date_path):
                            # Logger.info(f"DATE_DIR EXISTS:{date_dir}")
                            for filename in os.listdir(date_path):
                                # Logger.info(f"FILES:{filename}")
                                if filename.endswith('.txt'):
                                    devices.append(filename[:-4])  # Append address without .txt
                                    send({"message":"Aime shabani"},filename[:-4])

                Logger.info(f"Discovered devices: {devices},ici: {ici}")
                return devices

            # Function to send data to a device
            def send(data, address):
                try:
                    data_json = json.dumps(data)  # Convert dictionary to JSON string
                    ble_service.sendData(data_json, address)
                    Logger.info(f"Sent data to {address}: {data_json}")
                except Exception as e:
                    Logger.error(f"Error sending data: {e}")

            # Function to handle received data
            def received(sender=None, date=None):
                global parent_dir

                discovered_devices_dir = os.path.join(context.getFilesDir().getPath(), "Received_data")
                HERE=os.listdir(discovered_devices_dir)
                Logger.info(f"HERE: {HERE}")

                devices = {}

                if os.path.exists(discovered_devices_dir):
                    # Logger.info(f"FOLDER EXISTS")
                    for date_dir in os.listdir(discovered_devices_dir):
                        Logger.info(f"DATE_DIR:{date_dir}")
                        # if date and date_dir == date:
                        date_path = os.path.join(discovered_devices_dir, date_dir)
                        if os.path.isdir(date_path):
                            Logger.info(f"DATE_DIR EXISTS:{date_dir}")
                            for filename in os.listdir(date_path):
                                Logger.info(f"FILES:{filename}")
                                devices[filename] = eval(open(filename, 'r').read())

                Logger.info(f"Received data: {devices}")
                # return devices

            # Start scanning for devices
            start_scanning()
            parent_dir = "../"
            Clock.schedule_interval(read_discovered_devices, 2)
            Clock.schedule_interval(received, 2)


        except Exception as ex:
            Logger.info(f"BLUERROR: {ex}")
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    BLUETOOTH

    def SIDEBAR(self,clo):
        def disp(cl):
            nonlocal clock
            clock = Clock.schedule_interval(DIS, 1 / 100)

        def DIS(cl):
            nonlocal SB, clock
            if SB.opacity <=0 :
                Clock.unschedule(clock)
                self.remove_widget(SB)
            else:
                SB.opacity=SB.opacity-0.03

        def APEAR(cl):
            nonlocal SB, clock

            if SB.opacity >= 0.95:
                Clock.unschedule(clock)
                Clock.schedule_once(disp,8)
            else:
                SB.opacity = SB.opacity + 0.03

        def FIRST():
            Clock.schedule_once(lambda cc: CONTC())

        def CONTC():
            mov = ScrollView(size_hint=(1, .5), do_scroll_x=False, do_scroll_y=True, scroll_timeout=200,
                             scroll_distance=40,
                             scroll_type=['bars', 'content'], bar_width=1, bar_color=(1, 0, 0, 1), bar_margin=0
                             , pos_hint={"center_x": .5, "center_y": .3})
            Gmov = GridLayout(cols=1, size_hint=(1, None), spacing=5,
                              size=(3, ((Window.width / 100) * 16) * len(contacts) + 450))

            for z in contacts:
                if z != self.ME["idd"]:
                    cnct = MDIconButton(md_bg_color=(0, 0, 0, 0), icon_size=(Window.width / 100) * 8,
                                        ids={"idd": z, "schm": dr() + "contacts/" + z}, on_release=self.PROFILE)
                    if os.path.isfile(dr() + "contacts/" + z + "/" + z + ".png"):
                        cnct.icon = dr() + "contacts/" + z + "/" + z + ".png"
                    else:
                        cnct.icon = "photos/user.png"
                    Gmov.add_widget(cnct)

            mov.add_widget(Gmov)
            GR.add_widget(mov)

        SB=Widget(opacity=0,pos=(4,0),size_hint=(.08,1))  #          pos_hint={"center_x":.01,"center_y":.7}
        GR=GridLayout(cols=1,size_hint=(None,1),pos_hint={"center_x":.0,"center_y":.0},spacing=10,size=((Window.width/100)*8,Window.size[1]))
        with GR.canvas.before:
            Color(randint(2,100)/100,randint(2,100)/100,randint(2,100)/100, randint(50,101)/100)
            RoundedRectangle(pos=SB.pos,radius=[10],size=((Window.width/100)*12,Window.size[1]))

        me =MDIconButton(md_bg_color=(0,0,0,0),icon_size=(Window.width/100)*8,
                         ids={"idd":self.ME["idd"],"schm":dr()+"contacts/"+self.ME["idd"]})
        if self.ME["Name"][0]== "Emergency" :
            me.bind(on_release=self.new)
        else:
            me.bind(on_release=lambda bn:self.PROFILE(iddd=bn,update_new=None,mine=4))

        if os.path.isfile(dr()+"contacts/"+self.ME["idd"]+"/"+self.ME["idd"]+".png"):
            if os.path.getsize(dr()+"contacts/"+self.ME["idd"]+"/"+self.ME["idd"]+".png") > 2000 :
                me.icon=dr()+"contacts/"+self.ME["idd"]+"/"+self.ME["idd"]+".png"
            else:
                me.icon = "photos/user.png"
        else:
            me.icon="photos/user.png"
        work=MDIconButton(md_bg_color=(0,0,0,0),icon="photos/pay2.png",icon_size=(Window.width/100)*8,on_release=self.WORK) #pay2, r.png

        remi = MDIconButton(md_bg_color=(0, 0, 0, 0), icon="photos/remi.png", icon_size=(Window.width / 100) * 8,
                          ids={"idd": self.ME["idd"], "schm": dr() + "contacts/" + self.ME["idd"]},
                          on_release=self.home)
        msg = {"schm": ".", "sidd": str(uuid.uuid4()).replace("-", "").replace(" ", "").replace("_", "")[:5],
               "action": "5555", "idd": self.ME["idd"]}
        remi.bind(on_release=lambda w: send(msg))

        GR.add_widget(me)
        GR.add_widget(work)
        GR.add_widget(remi)

        contacts=self._files(dr()+"contacts/")

        con=Label(text="Contacts: "+str(len(contacts)-1),underline=True,size_hint=(None,None),size=((Window.width/100)*12,(Window.width/100)*3))
        con.font_size=con.font_size-6
        GR.add_widget(con)

        print("THE CONTACTS BELOW SHOULD BE IN      SCROLLVIEW       IN NEXT UPDATE.")
        Clock.schedule_once(lambda cc: threading.Thread(target=FIRST).start(), 2)
        SB.add_widget(GR)
        self.add_widget(SB)

        clock=Clock.schedule_interval(APEAR,1/100)

    def DOWNN(self, x, y):
        """  GOING UP   """
        def down(x):
            x = randint(0, Window.size[0] // 1.4)
            y = randint(0, Window.size[1] // 1.5)
            self.CLOCK=Clock.schedule_interval(lambda Clo: self.UPP(x, y), 1 / 1000)
        if self.Skat.pos[0] >= x or self.Skat.pos[1] >= y:
            # print(self.Skat.pos[0])
            Clock.unschedule(self.CLOCK)

            Clock.schedule_once(down, 10)
        else:
            self.Skat.pos = (self.Skat.pos[0] + 8, self.Skat.pos[1] + 8)

    def UPP(self, x, y):
        """  GOING DOWN  """
        def upp(x):
            try:
                posit=eval(open("offposition","r").read())
                x=posit[0]
                y=posit[1]
            except:
                x = Window.size[0] - 80
                y = Window.size[1] - 60

            try:
                Clock.unschedule(self.CLOCK)
            except:
                pass
            self.CLOCK=Clock.schedule_interval(lambda Clo: self.DOWNN( x, y), 1 / 1000)

        if self.Skat.pos[0] < x and self.Skat.pos[1] < y:
            if self.Skat.pos[0] < 0 :
                self.Skat.pos=(0,self.Skat.pos[1] )
            if self.Skat.pos[0] < 0 :
                self.Skat.pos=(0,self.Skat.pos[1] )
            # print(self.Skat.pos)
            Clock.unschedule(self.CLOCK)

            Clock.schedule_once(upp, 10)
        else:
            self.Skat.pos = (self.Skat.pos[0] - 8, self.Skat.pos[1] - 8)

    def DISAP(self,widg,pos=(Window.size[0]/3,Window.size[1]/4)):
        def save_pos(widg,touch):
            open("offposition", "w").write(str(widg.pos))
            # try:
            #     pos = eval(open("offposition", "r").read())
            # except:
            #     pos=(Window.size[0] - 80,Window.size[1] - 60)
            #
            # if widg.pos==pos:
            #     pass
            # else:
            #     open("offposition", "w").write(str(widg.pos))
            # print(widg.pos)
        def clocK(x):
            try:
                posit = eval(open("offposition", "r").read())
                x = posit[0]
                y = posit[1]
            except:
                x = Window.size[0] - 80
                y = Window.size[1] - 60
            try:
                Clock.unschedule(self.CLOCK)
            except:
                pass
            self.CLOCK=Clock.schedule_interval(lambda clo: self.UPP( x, y), 1 / 1000)

        try:
            pos = eval(open("offposition", "r").read())
        except:
            pos=(Window.size[0] - 80,Window.size[1] - 60)
        self.Skat = Scatter(size_hint=(None, None),ids={"x":pos[0]},pos=pos)
        with self.Skat.canvas.before:
            Color(0,0,1,1)
            rect=RoundedRectangle(pos=(0,0),radius=[10],size=(Window.size[0]/20,Window.size[0] /30))

        self.Skat.add_widget(widg)

        # skat.size=(Window.width, Window.size[1] / 6)
        self.Skat.size =(widg.size[0]+70,widg.size[1])
        widg.pos=(self.Skat.size[0]/20,0)

        self.call_slid(wid=self.Skat)
        self.SLD.append([self.Skat, self])
        self.add_widget(self.Skat)
        self.Skat.bind(on_touch_up=self.TOUCH)
        self.Skat.bind(on_touch_up=save_pos)
        Window.bind(on_keyboard=self.KEYS)

        try:
            Clock.unschedule(self.CLOCK)
            Clock.unschedule(clocK)
        except:
            pass
        Clock.schedule_once(clocK, 1)

    def interested(self,btn,TP,TC):
        "  Send message to poster, then reserve changes to clients, on click, opens a popup with list of takers a their prices"
        try:
            sidd=btn.ids["sidd"]
            idd=btn.ids["idd"]
            ac = btn.ids["ac"]
            price=TP[sidd]
            comment=TC.get(sidd,"")
            sidd2=str(uuid.uuid4()).replace("-", "").replace(" ", "").replace("_", "")[:5]
            sent={"action":"GVM","a2":ac,"idd":self.ME["idd"],"sidd":sidd2,"jb":sidd,"prc":price,"recipients":[idd],"schm":"no","COMM":comment}
            send(sent)
        except:
            pass

    def given(self,sidd,choise):
        if sidd in self._files(self.ME["adress"][1] + "/" + choise + "/given/") :
            return (0,.8,0,1)
        else:
            return (0,0,0,1)

    def Price(self,sidd,txt,OF_ND,wid):
        prices=[]
        pf=self._files(self.ME["adress"][1] + "/" + OF_ND + "/bagainers/"+sidd+"/")
        for j in pf :
            N=eval(open(self.ME["adress"][1] + "/" + OF_ND + "/bagainers/"+sidd+"/"+j , "r").read())
            prices.append(  [int( N.get("prc","0") ) ,N.get("COMM","No comment") ]  )
        if len(prices) :
            wid.background_color=(.8,1,.8,.9)
            prices.sort()
            return prices[0]
            # return str(max(prices) ) + "??"
        else:
            return [txt,"No comemnts"]

    def CMNT(self,sidd,txt,OF_ND,wid):
        prices=[]
        pf=self._files(self.ME["adress"][1] + "/" + OF_ND + "/bagainers/"+sidd+"/")
        for j in pf :
            N=eval(open(self.ME["adress"][1] + "/" + OF_ND + "/bagainers/"+sidd+"/"+j , "r").read())
            prices.append(  int( N.get("prc","0") )   )
        if len(prices) :
            wid.background_color=(.8,1,.8,.9)
            return str(max(prices) ) + "??"
        else:
            return txt

    def LOCAL_JOB(self,x,OF_ND="LOOKING FOR"):
        """Need       OR     OFFER
        START and STOP BUTTON
        FROM LIST and CUSTOM INPUT
        LAYOUT OF WHO ARE NEEDED IN EMERGENCY THIS TIME
        LAYOUT OF WHOS OFFERING IN EMERGENCY THIS TIME
        TIMEOUT ? 24HOURS ?

        ONCE YOU START YOUR AVAILLABILITY, THATS WHEN YOU START INCREASINGING RESPONSE LIST LIKE SEARCH

        REPLY WITH AMOUNT INT ONLY,    POSTER SEES AMOUNT AND HISTORY COLORS     THEN CLICKS ON ONE                           [poster_idd, in_geven,  in_hist,   sidd,   sidd_dir for int proposals,  text(20)  ]

        GREEN: GIVEN       ORANGE:  NOT FIRST TIME
        """
        def GONE(LOC,PRC,OF_ND,comm,tmes,TS,DEL=None):
            if not LOC :
                return
            if DEL :
                sidd = str(uuid.uuid4())[:5].replace("_", "").replace("-", "")
                d = {"schm": "ab", "action": OF_ND.replace(" ", "_"), "receiver": self.ME["jb"],
                     "zone": self.ME["adress"], 'sidd': sidd, 'idd': self.ME["idd"],"delete":DEL.ids["sidd"]}
                send(d)
                return
            if TS.text=="Mins" :
                tm= 60* int(tmes.text)
            if TS.text=="Hours" :
                tm= 3600* int(tmes.text)
            if TS.text=="Days" :
                tm= 86400* int(tmes.text)
            sidd=str(uuid.uuid4())[:5].replace("_","").replace("-","")
            d={"schm":"ab","action":OF_ND.replace(" ","_"),"receiver":self.ME["jb"],"zone":self.ME["adress"],'sidd': sidd,
               'pr': PRC.text, 'idd': self.ME["idd"], 'txt': LOC.text.replace("\n",""), 'tm': tm,"COMM":comm.text,}                         # real schm ?

            send(d)
            # open(self.ME["adress"][1]+"/"+OF_ND+"/"+sidd,"w").write(str(d))
            self.LOCAL_JOB(x=5,OF_ND=OF_ND)

        def tping(widg,tex):
            nonlocal TP
            TP[widg.ids["sidd"]]=widg.text
            # print(TP)

        def COMMENT(widg,tx):
            nonlocal TC
            TC[widg.ids["sidd"]] = widg.text

        def txtime(sp,tx):
            try:
                int(tx)
                pass
            except:
                sp.text = sp.text[:-1]

        def focused(w,v):
            Clock.unschedule(self.CLOCK)

        def unfocused(w):
            x = randint(0, Window.size[0] // 1.4)
            y = randint(0, Window.size[1] // 1.5)
            self.CLOCK=Clock.schedule_interval(lambda Clo: self.UPP(x, y), 1 / 1000)

        if not os.path.exists(self.ME["adress"][1]+"/"+OF_ND):    #   "LOOKING FOR"    "OFFERING"
            os.makedirs(self.ME["adress"][1]+"/"+OF_ND)
            os.makedirs(self.ME["adress"][1] + "/" + OF_ND+"/jobs")
            os.makedirs(self.ME["adress"][1] + "/" + OF_ND + "/bagainers")
            os.makedirs(self.ME["adress"][1] + "/" + OF_ND + "/given")

            os.makedirs(self.ME["adress"][1] + "/OFFERING")
            os.makedirs(self.ME["adress"][1] + "/OFFERING/jobs")
            os.makedirs(self.ME["adress"][1] + "/OFFERING/bagainers")
            os.makedirs(self.ME["adress"][1] + "/OFFERING/given")
        try:
            self.remove_widget(self.OFF_NED.parent)
            # self.OFF_NED.clear_widgets()
        except:
            pass
        self.OFF_NED=RelativeLayout(size_hint=(None, None), size=(Window.size[0]/1.3, Window.height / 3.5))
        with self.OFF_NED.canvas.before:
            Color(randint(2,100)/100,randint(2,100)/100,randint(2,100)/100, randint(50,101)/100)
            RCT = RoundedRectangle(pos=(0, 0), size=(Window.size[0]/1.3, Window.size[1] / 3.5))

        HEADS=GridLayout(cols=2, size_hint=(None, None),spacing=self.OFF_NED.size[0]/6, size=(Window.size[0]/1.3, Window.size[1] / 20),pos_hint={"center_x":.5,"center_y":.85})

        NEED=MDRaisedButton(text="I  AM LOOKING FOR: "+str(len(self._files(self.ME["adress"][1] + "/LOOKING FOR/jobs"))),size_hint=(None, None),_min_width=10,_min_height=2,
                            md_bg_color=(randint(20,100)/100,randint(20,100)/100,randint(20,100)/100, 1) if "LOOKING" in OF_ND else (.2,.2,.2,.3),
                            on_release=lambda btn:self.LOCAL_JOB(x=btn,OF_ND="LOOKING FOR"))

        OFFER=MDRaisedButton(text="I AM OFFERING: "+str(len(self._files(self.ME["adress"][1] + "/OFFERING/jobs"))),size_hint=(None, None),_min_width=10,_min_height=2,
                             md_bg_color=(randint(20,100)/100,randint(20,100)/100,randint(20,100)/100, 1) if "OFFERING" in OF_ND else (.2,.2,.2,.3),
                             on_release=lambda btn:self.LOCAL_JOB(x=btn,OF_ND="OFFERING"))

        NEED.font_size = NEED.font_size - 3
        OFFER.font_size = OFFER.font_size - 3
        HEADS.add_widget(NEED)
        HEADS.add_widget(OFFER)

        S_L_C_S  = ScrollView(size_hint=(1,.2), do_scroll_x=True, do_scroll_y=False, scroll_timeout=200, scroll_distance=40,
                          scroll_type=['bars', 'content'], bar_width=1, bar_color=(1, 1, 0, 1), bar_margin=0
                              ,pos_hint={"center_x": .5, "center_y": .13})  #  size=(self.OFF_NED.size[0], Window.size[1] / 20),

        L_C_S = GridLayout(cols=7, size_hint=(None,1),size=(Window.size[0]*2, Window.size[1] / 10), pos=(0,0),row_default_height=Window.size[1] / 20,row_force_default=True)

        LOC = TextInput(hint_text="I am " + OF_ND.lower() + " what ?",ids={"zn":[]} ,foreground_color=(0, 0, 0,  .8), multiline=False,background_color=(1, 1, 1,.8))
        LOC.font_size=LOC.font_size-5
        LOC.bind(focus=focused)
        LOC.bind(on_text_validate=unfocused)

        PRC = TextInput(hint_text="Price ? (Numbers only)", foreground_color=(0, 0, 0, .8),background_color=(1, 1, 1, .8),multiline=False)
        PRC.font_size = PRC.font_size - 5
        PRC.bind(text=txtime)
        PRC.bind(focus=focused)
        PRC.bind(on_text_validate=unfocused)

        CHOOSE = MDRaisedButton(text="...", text_color=(1, 1, 1, 1), md_bg_color=(0, 0, 0, 1),on_release=lambda bt:self.WORK(bt,msg="Choose who receive : ",found=None,zn=LOC))

        comm=TextInput(hint_text="Comment on it ", foreground_color=(0, 0, 0, .8),
                        background_color=(1, 1, 1, .8),multiline=False)
        comm.bind(focus=focused)
        comm.bind(on_text_validate=unfocused)
        comm.font_size = comm.font_size - 5

        tmes = TextInput(hint_text="Time in numbers ", foreground_color=(0, 0, 0, .8),
                         background_color=(1, 1, 1, .8),multiline=False)
        tmes.font_size = tmes.font_size - 5
        tmes.bind(text=txtime)
        tmes.bind(focus=focused)
        tmes.bind(on_text_validate=unfocused)

        TS=Spinner(text="Days", values=tuple(["Days","Hours","Mins"]))
        TS.font_size =  TS.font_size - 5

        START = MDRaisedButton(text="START", text_color=(1, 1, 1, 1), md_bg_color=(0, 0, 0, 1))
        START.font_size = START.font_size - 5
        START.bind(on_release=lambda bt:GONE(LOC,PRC,OF_ND,comm,tmes,TS))
        L_C_S.add_widget(LOC)
        L_C_S.add_widget(CHOOSE)
        L_C_S.add_widget(PRC)
        L_C_S.add_widget(comm)
        L_C_S.add_widget(tmes)
        L_C_S.add_widget(TS)
        L_C_S.add_widget(START)
        S_L_C_S.add_widget(L_C_S)

        scrowller=ScrollView(size_hint=(.98, .7), do_scroll_x=False, do_scroll_y=True, scroll_timeout=200, scroll_distance=40,
                       scroll_type=['bars', 'content'], bar_width=50, bar_color=(.4, 0, 1, .6), bar_margin=0,
                              pos_hint={"center_x": .5, "center_y": .45})


        files = self._files(dir=self.ME["adress"][1] + "/" + OF_ND+"/jobs")
        self.NEED = GridLayout(cols=1,spacing=7,padding=6, size_hint=(None, None), size=(Window.size[0]/1.5, (Window.size[1] / 20)*len(files)+140),row_default_height=Window.size[1] / 20,row_force_default=True,
                               pos_hint={"center_x":.5,"center_y":.5})
        _NEED = GridLayout(cols=4, spacing=7, padding=6, size_hint=(None, 1), size=(Window.size[0] *2,1 ),
                               row_default_height=Window.size[1] / 20, row_force_default=True, pos_hint={"center_x": .5, "center_y": .5})
        TP = {}
        TC = {}

        for n in files :
            ones=ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=False, scroll_timeout=200, scroll_distance=40,
                       scroll_type=['bars', 'content'], bar_width=1, bar_color=(1, 1, 0, 1), bar_margin=0,
                       pos_hint={"center_x": .5, "center_y": .5})

            grio=GridLayout(cols=6, spacing=7, padding=6, size_hint=(None, 1),
                               size=(Window.size[0] *2,1 ),
                               row_default_height=Window.size[1] / 20, row_force_default=True,
                               pos_hint={"center_x": .5, "center_y": .5})

            try:
                N=eval(open(self.ME["adress"][1]+"/"+OF_ND+"/jobs/"+n , "r").read())
            except:
                N={}

            btn=MDRaisedButton(text=N["txt"],text_color=(1, 1, 1, 1), md_bg_color=self.given(N["sidd"],OF_ND),size_hint=(None,None),size=(40,10),_min_height=2)
            btn.font_size = btn.font_size - 5
            # btn.bind(on_release=lambda z: self.interested(idd=N["idd"]))

            btn2 = MDRaisedButton(text="24:00:00",text_color=(1, 1, 1, 1), md_bg_color=(0,0,0, 1),_min_height=2)
            btn2.font_size = btn2.font_size - 5
            counter = self.countdown
            counter(btn2, self.ME["adress"][1] + "/" + OF_ND + "/jobs/" + n)

            btn3 = MDRaisedButton(text="give" if "OFFERING" in OF_ND else "Book", ids={"sidd":N["sidd"],"idd":N["idd"],"ac":OF_ND},text_color=(1, 1, 1, 1), md_bg_color=(0, 0, 0, 1),_min_height=2)
            btn3.font_size = btn3.font_size - 5
            btn3.bind(on_release=lambda btn: self.interested(btn,TP,TC))

            sugst=TextInput(ids={"sidd":N["sidd"]},multiline=False,foreground_color=( 0,0,0, .8),background_color=(1, 1, 1,.8),size_hint=(None,None),size=(60,Window.size[1] / 29))
            sugst.bind(text=tping)
            pc=self.Price(N["sidd"],str(N["pr"])+" ??",OF_ND,sugst)
            sugst.hint_text = str(pc[0])
            sugst.font_size = sugst.font_size - 5
            sugst.size=(30*len(sugst.hint_text),sugst.size[1])
            sugst.bind(focus=focused)
            sugst.bind(on_text_validate=unfocused)

            comment = TextInput(hint_text=pc[1],ids={"sidd": N["sidd"]}, multiline=False, foreground_color=(0, 0, 0, .8),
                                background_color=(1, 1, 1, .8), size_hint=(None, None), size=(60, Window.size[1] / 29))

            comment.bind(text=COMMENT)
            comment.bind(focus=focused)
            comment.font_size = comment.font_size - 5
            comment.size = (30 * len(comment.hint_text), comment.size[1])
            comment.bind(on_text_validate=unfocused)

            Del = MDRaisedButton(text="Delete", ids={"sidd": N["sidd"],"ac": OF_ND}, text_color=(1, 1, 1, 1),
                                  md_bg_color=(0, 0, 0, 1), _min_height=2)
            Del.font_size = Del.font_size - 5
            # Del.bind(on_release=lambda btn: os.remove(self.ME["adress"][1]+"/"+OF_ND+"/jobs/"+n))
            Del.bind(on_release=lambda btn:self.LOCAL_JOB(x=6,OF_ND=OF_ND))
            Del.bind(on_release=lambda btn: GONE(LOC="5",PRC=None,OF_ND=OF_ND,comm=None,tmes=None,TS=None,DEL=btn))

            grio.add_widget(btn)
            grio.add_widget(sugst)
            grio.add_widget(btn3)
            grio.add_widget(btn2)
            grio.add_widget(comment)
            grio.add_widget(Del)
            ones.add_widget(grio)
            self.NEED.add_widget(ones)

        self.OFF_NED.add_widget(HEADS)
        scrowller.add_widget(self.NEED)
        self.OFF_NED.add_widget(scrowller)
        self.OFF_NED.add_widget(S_L_C_S)
        self.DISAP(self.OFF_NED)

    def countdown(self,btn,path_file):
        def minus(R):
            if not os.path.isfile(path_file):
                return
            N = eval(open(path_file, "r").read())
            REMT=int(N.get("tm",str(24*60*60)))
            if REMT > 0:
                REMT -= 1

                HOUR, remainder=divmod(REMT,3600)
                MIN,SEC=divmod(remainder,60)
                btn.text=f"{HOUR:02}:{MIN:02}:{SEC:02}"
                N["tm"]=str(REMT)
                open(path_file, "w").write(str(N))

            else:
                # btn.parent.remove_widget(btn)
                os.remove(path_file)
                self.LOCAL_JOB(x=5)

        Clock.schedule_interval(minus,1)

    def OPTIONS(self):
        TR = Scatter(size_hint=(None, None), ids={"x": 20})
        with TR.canvas.before:
            Color(0,0,0,0)
            rect = RoundedRectangle( pos=(0, 0), radius=[20],size=(Window.size[0] / 8, Window.size[0] / 8))

        OPT = MDIconButton(icon="photos/bum.png", icon_size=Window.size[0] / 7.5, text_color=(0, 0, 1, 1), md_bg_color=(.7, .3, .4, 0),
                           rounded_button=10,size_hint=(None, None),pos=(0,0),on_release=self.SIDEBAR, size = (Window.size[0]/12,Window.size[0]/12))
        OPT.bind(on_release=self.LOCAL_JOB)
        TR.add_widget(OPT)

        TR.size = (Window.size[0] / 5, Window.size[0] / 5)
        self.add_widget(TR)

        TR.pos=(Window.size[0]/5,         (Window.size[1]-(Window.size[1] / 8.2)   )   )

    def MME(self,x=None):
        if not x :
            # self.JOBS = eval(open("JOBS.txt", "r").read())
            return
        dicti=json.load(open("SD/conf/me.json","r"))
        dicti["jb"]=self.professios
        json.dump(dicti,open("SD/conf/me.json", "w"))
        sen = {"action": "N_user", "data": dicti, "sidd": str(uuid.uuid4())[:5]}
        send(sen)
        del dicti
        del x
        del sen

    def WORK(self, bt, msg="Select jobs you can do up to 5. : \n ",found=None,zn=None):
        def ZN(button):
            if not button.text in zn.ids["zn"]:
                if len(zn.ids["zn"]) == 1:
                    try:
                        vibrator.vibrate(1 / 50)
                    except:
                        pass
                    return
                button.md_bg_color = (.7, 1, .7, 1)
                zn.ids["zn"].append(button.text)
                if "textinput" in str(type(zn)) :
                    zn.text = button.text
                else:
                    zn.text="Receivers: "+button.text
            else:
                try:
                    button.md_bg_color = (1, .7, 0, .8)
                    zn.ids["zn"].remove(button.text)
                    zn.text = "Receivers: " + self.ME["adress"][1]
                except:
                    pass

            lab.text=str(len(zn.ids["zn"]))+"/"+limit
        def SELECTION(button):
            if not zn:
                limit = "5"
            else:
                limit = "1"

            if not button.text.replace("\n", "") in self.professios:
                if len(self.professios) == 5:
                    try:
                        vibrator.vibrate(1 / 50)
                    except:
                        pass
                    return
                button.md_bg_color = (.7, 1, .7, 1)
                self.professios.append(button.text.replace("\n", ""))
            else:
                try:
                    button.md_bg_color = (1, .7, 0, .8)
                    self.professios.remove(button.text.replace("\n", ""))
                except:
                    pass
            print(self.professios)
            try:
                lab.text = str(len(self.professios)) + "/" + limit
            except:
                pass
        def Find(wd, ZN):
            tx=wd.text
            goten=[]
            with open("JBS.txt", "r") as JBS:
                for e in JBS:
                    if tx.lower().strip() in e.lower():
                        goten.append(e)

            Clock.schedule_once(lambda dt:self.WORK(bt=None,msg=msg,found=goten,zn=ZN))
        def YIELD():
            nonlocal gen
            try:
                return next(gen)
            except:
                return None
        def GEN():
            self.JBS.scroll_y = 0.001
            self.JBS.scroll_y = 0.001
            self.JBS.scroll_y = 0.001
            with open("JBS.txt", "r") as JBS:
                for i in JBS:
                    yield i
        def FIRST():
            Clock.schedule_once(lambda cc: CONTC())
        def CONTC(klock=None):
            text=YIELD()
            if text:
                lab2.text=str(int(lab2.text)+1)  #+"/374"
                button = CustomTB(text=text, md_bg_color=(.7, 1, .7, 1) if text[:-1] in self.professios else ( 1, .7, 0, .8))
                if zn:
                    button.bind(on_release=ZN)
                else:
                    button.bind(on_release=SELECTION)
                self.JBL.add_widget(button)                                                  #  self.JBL.children[0].text
                self.JBL.size = (self.JBL.size[0], self.JBL.size[1] + Window.size[1] / 10)
                Clock.schedule_once(CONTC)
            else:
                try:
                    vibrator.vibrate(1/40)
                except:
                    pass

        if found == []:
            return

        if found != None :
            for i in found:
                button = CustomTB(text=i, md_bg_color=(.7, 1, .7, 1) if i in self.professios else (1, .7, 0, .8))  # ToggleButton
                if zn:
                    button.bind(on_release=ZN)
                else:
                    button.bind(on_release=SELECTION)
                self.JBL.size = (self.JBL.size[0], self.JBL.size[1] + Window.size[1] / 20)
                self.JBL.add_widget(button,index=len(self.JBL.children))
                self.JBS.scroll_y=1.
            return

        if not zn:
            self.professios = self.ME.get("jb", [])
            limit="5"
        else:
            self.professios=[]                               # dd=pickle.load(open("JOBS.bin","rb"))
            limit="1"

        old = self.ME.get("jb", [])
        self.REL = RelativeLayout(size_hint=(None, None),size=((Window.size[0] / 100) * 81, (Window.size[1] / 100) * 85),
                                  pos_hint={"center_x": .5, "center_y": .5})
        with self.REL.canvas.before:
            Color(randint(0, 100) / 100, randint(0, 100) / 100, randint(0, 100) / 100, .8)  # (.65,0,.2,.8)  (1,.7,0,.8)
            rect = RoundedRectangle(pos=(-10, -5), radius=[10],size=((Window.size[0] / 100) * 81, (Window.size[1] / 100) * 85))

        self.JBS = ScrollView(size_hint=(.84, .85), do_scroll_x=False, do_scroll_y=True, scroll_timeout=55, scroll_distance=20,
                       scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0,
                              pos_hint={"center_x": .5, "center_y": .45})

        self.JBL = GridLayout(cols=1, size_hint=(1, None), spacing=Window.size[1] /50, size=(1, Window.size[1] / 10),
                              pos_hint={"center_x": .5, "center_y": .45})

        find = MDTextField(size_hint_x=.64,hint_text=msg, hint_text_color_normal=(1, 5, .3, .8),icon_right="magnify",text_color_normal=(1, 1, 1, 1), pos_hint={"center_x": .5, "center_y": .91})
        find.bind(on_text_validate=lambda wd:threading.Thread(target=Find,args=(wd,zn,)).start())
        self.REL.add_widget(find)

        gen = GEN()
        Clock.schedule_once(lambda cc: threading.Thread(target=FIRST).start(), 2)

        self.JBS.add_widget(self.JBL)
        self.REL.add_widget(self.JBS)

        okbt = MDIconButton(icon="photos/s1.png", icon_size=Window.size[0] / 7, md_bg_color=(1, 5, .3, .8),
                            size_hint=(None, None),
                            size=(Window.size[0] / 7, Window.size[0] / 7), pos_hint={"center_x": .5, "center_y": .1})

        okbt.bind(on_release=lambda bt: send({"schm": ".", "sidd": str(uuid.uuid4()).replace("-", "").replace(" ", "").replace("_", "")[:5],
             "action": "JB", "idd": self.ME["idd"], "jb": self.professios, "zn": self.ME["adress"], "old": old}))
        okbt.bind(on_release=self.MME)
        okbt.bind(on_release=lambda clic:self.remove_widget(self.REL.parent))
        lab=Label( text=str(len(self.professios))+"/"+limit,pos_hint={"center_x": .85, "center_y": .91})
        self.REL.add_widget(lab)
        lab2 = Label(text="0", color=(1,1,1,.5),pos_hint={"center_x": .85, "center_y": .1})
        self.REL.add_widget(lab2)

        if not zn :
            self.REL.add_widget(okbt)

        self.moveer(self.REL, pos=(100, 50))

        # del s
        # del self.REL
        # del self.JBL
        # del okbt
        # del msg
        # del button
        # del rect
        # self.add_widget(r)

    def RECEIVER(self,xmessage):
        XM=[]
        try:
            MESS = json.loads(xmessage.decode('utf8'))

            if MESS.get("action", 0) == "src":
                if "GG" in dir(self):
                    if not MESS["data"].get("sidd", 0) in XM:
                        Clock.schedule_once(lambda CLO: self._layers(s=MESS["data"]))
                        XM.append(MESS["data"]["sidd"])
                        MESS={}

            if MESS.get("action", 0) in   ["OFFERING" , "LOOKING_FOR"]:
                    if not MESS["data"].get("sidd", 0) in XM:
                        Clock.schedule_once(lambda CLO: self.LOCAL_JOB(OF_ND=MESS.get("action","LOOKING_FOR").replace("_"," ")))
                        XM.append(MESS["data"]["sidd"])
                        MESS={}

            if MESS.get("action", 0) == "cht":
                if "comg" in dir(self):
                    if not MESS.get("sidd", 0) in XM:
                        Clock.schedule_once(lambda CLO: self.MSG(B=None, update_new=MESS))
                        XM.append(MESS["sidd"])

            if MESS.get("action", 0) == "zone":
                if 'l_r' in dir(self):
                    if not MESS.get("sidd", 0) in XM:
                        Clock.schedule_once(
                            lambda CLO: self.zchat(POS=None, schm=MESS["schm"] + "/" + MESS["sidd"], ME=MESS))
                        XM.append(MESS["sidd"])

            if MESS.get("action", 0) == "inbx":
                if "pcomg" in dir(self):
                    if not MESS.get("sidd", 0) in XM:
                        Clock.schedule_once(lambda CLO: self.PROFILE(iddd=None, update_new=MESS))
                        XM.append(MESS["sidd"])

            ###############################################################################################
            if MESS.get("action", 0) == "B_U":
                if not MESS.get("sidd", 0) in XM:
                    if "org" in MESS["schm"]:
                        Clock.schedule_once(lambda CLO: self.Lines_org(dicti=MESS, schm="/org/"))
                        XM.append(MESS["sidd"])

                    if "JobTalent" in MESS["schm"]:
                        Clock.schedule_once(lambda CLO: self.Lines_JobTalent(dicti=MESS, schm="/JobTalent/"))
                        XM.append(MESS["sidd"])

                    if "paidAdds" in MESS["schm"]:
                        Clock.schedule_once(lambda CLO: self.Lines_paidAdds(dicti=MESS, schm="/paidAdds/"))
                        XM.append(MESS["sidd"])


            print("RECEIVER: ", MESS)
            Logger.info(f"FROM OSC SERVER: {MESS}")
        except Exception as e :
            for file in os.listdir(dr()+"New_temp/"):
                try:
                    MESS = json.load(open(dr() + "New_temp/" + file))
                    os.remove(dr()+"New_temp/"+file)
                except:
                    MESS={}
                    pass
                print(MESS)

                if MESS.get("action", 0) == "src":
                    print("MESS ",MESS)
                    if "GG" in dir(self):
                        if not MESS["data"].get("sidd", 0) in XM:
                            Clock.schedule_once(lambda CLO: self._layers(s=MESS["data"]))
                            XM.append(MESS["data"]["sidd"])
                            # MESS = {}

                if MESS.get("action", 0) in ["OFFERING", "LOOKING_FOR"]:
                    if not MESS["data"].get("sidd", 0) in XM:
                        Clock.schedule_once(lambda CLO: self.LOCAL_JOB(x=None,OF_ND=MESS.get("action","LOOKING FOR").replace("_", " ")))
                        XM.append(MESS["data"]["sidd"])
                        MESS = {}

                if MESS.get("action",0) == "cht":
                    if "comg" in dir(self):
                        if not MESS.get("sidd", 0) in XM:
                            Clock.schedule_once(lambda CLO: self.MSG(B=None, update_new=MESS) )
                            XM.append(MESS["sidd"])

                if MESS.get("action",0) == "zone":
                    if 'l_r' in dir(self):
                        if not MESS.get("sidd", 0) in XM:
                            Clock.schedule_once(lambda CLO: self.zchat(POS=None, schm=MESS["schm"]+"/"+MESS["sidd"],ME=MESS))
                            XM.append(MESS["sidd"])

                if MESS.get("action",0) == "inbx":
                    if "pcomg" in dir(self):
                        if not MESS.get("sidd", 0) in XM:
                            Clock.schedule_once(lambda CLO: self.PROFILE(iddd=None, update_new=MESS))
                            XM.append(MESS["sidd"])

                ###############################################################################################
                if MESS.get("action", 0) == "B_U":
                    if not MESS.get("sidd", 0) in XM:
                        if "org" in MESS["schm"]:
                            Clock.schedule_once(lambda CLO: self.Lines_org(dicti=MESS, schm="/org/"))
                            XM.append(MESS["sidd"])

                        if "JobTalent" in MESS["schm"]:
                            Clock.schedule_once(lambda CLO: self.Lines_JobTalent(dicti=MESS, schm="/JobTalent/"))
                            XM.append(MESS["sidd"])

                        if "paidAdds" in MESS["schm"]:
                            Clock.schedule_once(lambda CLO: self.Lines_paidAdds(dicti=MESS, schm="/paidAdds/"))
                            XM.append(MESS["sidd"])

                ##################################################################################################

            if platform != "android" :
                Clock.schedule_once(self.RECEIVER)
        # THR = threading.Thread(target=self.RECEIVER, args=(4,))
        # THR.start()

    def dustbin(self):
        self.TR = Scatter(size_hint=(None, None),ids={"x":20},pos=(Window.size[0]/12,Window.size[1]-(Window.size[1] / 10)))
        with self.TR.canvas.before:
            Color(1,1,1,1)
            rect=RoundedRectangle(source="photos/trash.png",pos=(0,0),radius=[10],size=(Window.size[0]/8,Window.size[0]/8))

        self.TR.size = (Window.size[0]/8,Window.size[0]/8)
        self.call_slid(wid=self.TR)
        self.SLD.append([self.TR, self])
        self.add_widget(self.TR)

    def _files(self,dir,rev=True):
        try:
            FILES = [f.name for f in pathlib.Path(dir).iterdir()]
            FILES.sort(key=lambda x: os.stat(os.path.join(dir, x)).st_mtime, reverse=rev)
            return FILES
        except Exception as e:
            Logger.info(f"COULD NOT GET LIST OF FILES IN _files(). REASON: {e}")
            return []

    def send_message(self,DD,comment=None,inbox=None):
        "paths are diffrent according to device, don't include paths"
        # DD=x.ids
        if inbox :
            schm, msg, pht, sidd = DD["schm"], DD["msg"], DD["pth"], DD["sidd"]
            schm = schm.replace(".bin", "").replace(".json", "")

            if msg is None and pht is None:
                return
            #     inbx, cht, zone
                                                  #          "prfl": dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".png",
            bsn = {"action": "inbx", "zone": self.ME["adress"], "org": self.ME["Name"][0], "sidd": sidd, "schm":schm,"msg": msg,
                   "chats": {}, "bl":self.ME.get("bl","0"),
                   'subject': self.ME["busy"], "BUSY": [], "pht": pht, "idd": self.ME["idd"],
                   "day": time.strftime("%d/%m/%y %H:%M:%S"),"lk":self.ME.get("lk","0")}
            # json.dump(bsn,open(dr()+"Activities/"+schm,"w"))
            pickle.dump(bsn, open(schm +".bin", "wb"))
            if not os.path.isdir(schm):
                os.mkdir(schm)



            try:
                send(bsn)
                # bsn = {"bsn": bsn, "schm": schm}
                self.PROFILE(iddd=None, update_new=bsn)
                self.PROFILE(iddd=None, update_new=bsn)
            except Exception as e:
                print(e)
                Logger.info(f"SHIDA NI (if inbx): {e}")

            return


        if not comment:
            schm,msg , pht,sidd =  DD["schm"], DD["msg"],DD["pth"], DD["sidd"]
            tag=DD["tg"]
            print(DD)
            schm = schm.replace(".bin", "").replace(".json", "")

            if msg is None and pht is None :
                return


            bsn = {"action": "zone", "zone":self.ME["adress"],"org": self.ME["Name"][0],"sidd":sidd, "msg": msg,"chats":{},"schm":schm,"bl":self.ME.get("bl","0"),
                   'subject': self.ME["busy"], "BUSY": [], "pht": pht, "idd": self.ME["idd"],"day":time.strftime("%d/%m/%y %H:%M:%S"),"lk":self.ME.get("lk","0")}
            if tag != [] :
                bsn["tg"]=tag[0].replace("\n","")

            pickle.dump(bsn, open(dr() + "Activities/" + schm+".bin", "wb"))
            if not os.path.isdir(dr()+"Activities/"+schm):
                os.mkdir(dr()+"Activities/"+schm)


            try:
                self.zchat(POS=None, schm=schm,ME=bsn)
                send(bsn)
            except Exception as e:
                print(e)
                Logger.info(f"SHIDA NI (if not comment): {e}")

        else:
            schm,msg , pht, sidd=  DD["schm"], DD["msg"],DD["pth"], DD["sidd"]
            schm = schm.replace(".bin", "").replace(".json", "")

            if msg is None and pht is None:
                return
                                           # "prfl": dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".png",
            bsn = {"action": "cht", "zone": self.ME["adress"], "org": self.ME["Name"][0], "sidd": sidd, "schm":schm, "msg": msg,
                   "chats": {},
                   'subject': self.ME["busy"], "BUSY": [], "pht": pht, "idd": self.ME["idd"],
                   "day": time.strftime("%d/%m/%y %H:%M:%S"),"bl":self.ME.get("bl","0"),"lk":self.ME.get("lk","0")}
            # json.dump(bsn,open(dr()+"Activities/"+schm,"w"))
            pickle.dump(bsn, open(dr() + "Activities/" + schm + ".bin", "wb"))
            if not os.path.isdir(dr() + "Activities/" + schm):
                os.mkdir(dr() + "Activities/" + schm)
            try:
                send(bsn)
                # bsn={"bsn":bsn,"schm":schm}
                self.MSG(B=None,update_new=bsn)
            except Exception as e:
                print(e)
                Logger.info(f"SHIDA NI: {e}")

    def org(self):
        try:
            Clock.schedule_once(lambda cc: self.Lines_org(schm="/org/",pos=(42, self.DIST * 4 + 60)))
            Clock.schedule_once(lambda cc: threading.Thread(target=self.paidAdds).start(), 1 / 2)
        except Exception as e:
            Clock.schedule_once(lambda cc: threading.Thread(target=self.paidAdds).start(), 1 / 2)
            Logger.info(f"ORG: {e}")

    def JobTalent(self):
        try:
            Clock.schedule_once(lambda cc: self.Lines_JobTalent(schm="/JobTalent/",pos=(42, self.DIST * 2 + 20)))
            Clock.schedule_once(lambda cc: threading.Thread(target=self.zone_chats).start(), 1 / 2)
        except Exception as e :
            Clock.schedule_once(lambda cc: threading.Thread(target=self.zone_chats).start(), 1 / 2)
            Logger.info(f"ORG: {e}")

    def paidAdds(self):
        try:
            Clock.schedule_once(lambda cc: self.Lines_paidAdds(schm="/paidAdds/",pos=(42, self.DIST * 3 + 40)))
            Clock.schedule_once(lambda cc: threading.Thread(target=self.JobTalent).start(), 1 / 2)
        except Exception as e :
            Clock.schedule_once(lambda cc: threading.Thread(target=self.JobTalent).start(), 1 / 2)
            Logger.info(f"ORG: {e}")

    def zone_chats(self):
        Clock.schedule_once(lambda cc: self.zchat(schm="/"+self.ME["adress"][1]+"/", POS=(42, self.DIST - (self.DIST / 3.3))))

    def keys_path(self,dc, key, cur_path=[]):
        print("key: ",key," dict: ",dc)
        def dict_paths(DICT, target_key, current_path=[]):
            """
            Example usage
                data = {
                'a': {'location': 'A'},
                'b': [{'location': 'B', "x": {"papa": {"07888": "shabani"}}}, {'location': 'C'}],
                'c': {'d': {'location': 'D'}}
                }
                p=keys_path(data, 'papa')
                out=eval(str(data)+p)
                print(out)            #  {'07888': 'shabani'}

            """

            paths = []
            for key, value in DICT.items():
                new_path = current_path + [key]
                if key == target_key:
                    paths.append(new_path)
                if isinstance(value, dict):
                    paths.extend(dict_paths(value, target_key, new_path))
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, dict):
                            paths.extend(dict_paths(item, target_key, new_path + [index]))
            return paths

        p = dict_paths(dc, key, cur_path)
        ph = ""
        for i in p[0]:
            l = []
            l.append(i)
            ph += str(l)
        return ph

    def ORDER(self,DICT):  #  DICT HAS   WIDGET, MSG,  PROFILE,
        """
        THIS FUNC SERVES TO INSTANT DOWNLOAD IDD.JSON AND 2 MESSAGES DICT WHEN SCROLL DETECTED ON PROFILE2 AND MSG
        """
        print("scrolv.bind on scroll move> if scl.scroll_y==1. : self ORDER")

    def load_image(self):
        global result_ready
        def Gallery():
            global _activity

            request_permissions([Permission.READ_EXTERNAL_STORAGE])


            intent = Intent(Intent.ACTION_PICK)
            intent.setType("image/*")
            android_bind(on_activity_result=on_activity_result)
            _activity = PythonActivity.mActivity
            _activity.startActivityForResult(intent, 0)

        def on_activity_result(request_code, result_code, data):
            global choosen,result_ready
            if result_code == -1:  # RESULT_OK
                uri = data.getData()
                file_path = get_real_path_from_uri(uri)
                Logger.info(f"GalleryApp: File path - {file_path}")
                if file_path and exists(file_path):
                    choosen = file_path
                    result_ready.set()
                    # self.load_image(file_path)
                else:
                    Logger.error("GalleryApp: Failed to get a valid file path.")
            else:
                Logger.warning("GalleryApp: No image selected or operation canceled.")

        def get_real_path_from_uri(uri):
            global _activity
            """Get the real file path from a URI."""
            context = cast(Context, _activity.getApplicationContext())
            file_path = None

            # Handle the URI
            if DocumentsContract.isDocumentUri(context, uri):
                document_id = DocumentsContract.getDocumentId(uri)
                uri_authority = uri.getAuthority()

                # Handle different document URIs
                if uri_authority == "com.android.providers.media.documents":
                    id_parts = document_id.split(":")
                    doc_type = id_parts[0]
                    doc_id = id_parts[1]

                    if doc_type == "image":
                        content_uri = Uri.withAppendedPath(MediaStore_Images_Media.EXTERNAL_CONTENT_URI, doc_id)
                        file_path = get_data_column(content_uri, None, None)

                elif uri_authority == "com.android.providers.downloads.documents":
                    content_uri = Uri.withAppendedPath(Uri.parse("content://downloads/public_downloads"), document_id)
                    file_path = get_data_column(content_uri, None, None)

                elif uri_authority == "com.android.externalstorage.documents":
                    id_parts = document_id.split(":")
                    storage_type = id_parts[0]
                    storage_id = id_parts[1]

                    if storage_type == "primary":
                        file_path = f"{Environment.getExternalStorageDirectory()}/{storage_id}"

            elif uri.getScheme() == "content":
                file_path = get_data_column(uri, None, None)
            elif uri.getScheme() == "file":
                file_path = uri.getPath()

            if not file_path:
                Logger.error("GalleryApp: Could not retrieve file path from URI.")

            return file_path

        def get_data_column(uri, selection, selection_args):
            global _activity
            """Helper function to get the value of the _data column, which is usually the file path."""
            context = cast(Context, _activity.getApplicationContext())
            content_resolver = cast(ContentResolver, context.getContentResolver())
            cursor = None
            column = "_data"
            projection = [column]
            file_path = None

            try:
                cursor = content_resolver.query(uri, projection, selection, selection_args, None)
                if cursor and cursor.moveToFirst():
                    idx = cursor.getColumnIndexOrThrow(column)
                    file_path = cursor.getString(idx)
            except Exception as e:
                Logger.error(f"GalleryApp: Error in get_data_column - {e}")
            finally:
                if cursor:
                    cursor.close()

            return file_path
        def stater():
            global result_ready
            Gallery()
            result_ready.wait()
            Logger.info(f"Loading image from path {choosen}")
            return choosen

        if platform == "android" :
            from android.permissions import request_permissions, Permission
            from android.activity import bind as android_bind
            from jnius import autoclass, cast
            from kivy.logger import Logger
            from os.path import exists

            ContentResolver = autoclass('android.content.ContentResolver')
            Context = autoclass('android.content.Context')
            Environment = autoclass('android.os.Environment')
            MediaStore_Images_Media = autoclass('android.provider.MediaStore$Images$Media')
            DocumentsContract = autoclass('android.provider.DocumentsContract')
            Uri = autoclass('android.net.Uri')
            DocumentsContract = autoclass('android.provider.DocumentsContract')
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Cursor = autoclass('android.database.Cursor')


            result_ready = threading.Event()
            return stater()

    def cut(self, IN,OUT):
        def compress(src,targ):
            from PIL import Image
            import PIL
            base_width = 360
            image = Image.open(src)
            width_percent = (base_width / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(width_percent)))
            image = image.resize((base_width, hsize), PIL.Image.ANTIALIAS)
            image.save(targ)

            return targ

        def fdir(d):
            """
            THis finds pathath, without file name
            """
            p = "/"  # PTH()
            i = len(d)
            for x in range(len(d)):
                if d == "":
                    return d

                else:
                    if d[-1] != p:
                        d = d[:-1]
                    else:
                        break
            return d

        def fnam(d):
            p = "/"  # PTH()
            x = ""
            for i in range(len(d)):
                if d[-1] == p:
                    break
                else:
                    x = d[-1] + x
                    d = d[:-1]
            return x

        import numpy as np
        from PIL import Image, ImageDraw
        from PIL import Image
        import PIL

        imge = Image.open(IN).convert("RGB")
        npImage = np.array(imge)
        h, w = imge.size[0], imge.size[0]
        # Create same size alpha layer with circle
        alpha = Image.new('L', imge.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)
        # Convert alpha Image to numpy array
        npAlpha = np.array(alpha)
        # Add alpha layer to RGB
        npImage = np.dstack((npImage, npAlpha))

        Image.fromarray(npImage).save(OUT)                                       #    ddir + "/" + "_" + fnam(Dir)

        return  OUT                                                               #compress(ddir + "/" + "_" + fnam(Dir))

    def preload_image(self,im=None,BT=None):
        if os.path.exists("SD/contacts/"+self.ME["idd"]) :
            try:
                os.makedirs("SD/contacts/"+self.ME["idd"])
            except:
                pass
        if platform == "android" :
            pth=self.load_image()
            if not im :
                return pth
            else:
                IM=ImageProcessor()
                RP=IM.cut(IN=pth,OUT=dr()+"contacts/"+self.ME["idd"]+"/"+self.ME["idd"]+".png")
                im.source =RP
                im.reload()
                self.Loader(up=RP)
        else:

            def on_selected(ob, val):
                global choosen, result_ready,Im,List
                print('val[0]',val[0])
                if val[0].endswith((".png", ".PNG", ".jpg", ".JPG", "jpeg", "JPEG")):            #   , ".bmp", ".BMP", ".gif", ".GIF"
                    if BT :
                        BT.ids={"pht":val[0] }
                    else:
                        IM = ImageProcessor()
                        profile =IM.cut(IN=val[0], OUT="SD/contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".png")

                        im.source=profile
                        im.reload()
                        self.Loader(up=profile)

            from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
            R, G, B, O = randint(10, 20) / 100, randint(5, 20) / 100, randint(5, 20) / 100, 1
            pg = GridLayout(cols=1, size_hint=(None,None),size=(Window.size[0]/1.5,Window.size[1]/2))
            with pg.canvas.before:
                Color(R,G,B,O)
                rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(pg.size[0]+pg.size[0]/5,pg.size[1]))

            ll = [    FileChooserListView(path=os.path.dirname(os.path.dirname(os.path.dirname(dr())))),
                       FileChooserIconView(  path=os.path.dirname(os.path.dirname(os.path.dirname(dr()))))    ]

            ch = ll[randint(1, 2) - 1]
            ch.dirselect = False
            ch.bind(selection=on_selected)

            pg.add_widget(ch)
            self.moveer(pg,pos=(100,200))

    def profile(self,idd,dir=None):
        print("idd: ",idd)
        def getit(iddd):
            try:
                print(self.URL.split(":")[0])
                ftp = ftplib.FTP()
                ftp.connect(self.URL.split(":")[0], 2121)
                ftp.login("aime shabani", "12435687")
                ftp.cwd("ACCOUNTS/" + iddd + "/")
                if os.path.exists("SD/contacts/" + iddd + "/"):
                    y = open("SD/contacts/" + iddd + "/" + iddd + ".png", "wb")
                    ftp.retrbinary("RETR " + iddd + ".png", y.write)
                else:
                    os.makedirs("SD/contacts/" + iddd + "/")
            except Exception as e:
                Logger.info(f"{e}")

        if dir:
            if os.path.isfile(dr()+dir+"/"  + idd + ".png"):
                return dr()+dir+"/"  + idd + ".png"
            else:
                return 'ftp://aime shabani:' + self.PWD + '@' + self.ip + ":" + "2121" + '/' + "ACCOUNTS/" + idd + "/" + dir+"/" + idd + ".png"

        if os.path.isfile("SD/contacts/"+idd+"/"+idd+".png"):
            return "SD/contacts/"+idd+"/"+idd+".png"
        else:

            if idd is None:
                return
            threading.Thread(target=getit,args=(idd,)).start()

            return 'ftp://aime shabani:'+self.PWD+'@'+self.ip+":"+"2121"+'/'+ "ACCOUNTS/"+idd+"/"+idd + ".png"

    def CARO2(self,DI,schm=None,x=None,clr=None,sx=Window.size[0] / 8,sy=Window.size[1] / 15):
        schm=schm.replace(".bin","").replace(".json","")

        if "contacts/" in schm :
            rep=len(self._files(schm))
            DI= pickle.load(open(schm+".bin", "rb"))
        else:
            rep = len(self._files(dr() + "Activities" + "/" + schm))
            DI = pickle.load(open(dr() + "Activities" + "/" + schm + ".bin", "rb"))
        sms=DI.get("msg","No Message")
        print("sms: ",sms)
        R, G, B, O = randint(80, 100) / 100, randint(30, 100) / 100, randint(30, 100) / 100, 1
        scren = RelativeLayout(size_hint=(1,1))
        with scren.canvas.before:
            if len(DI.get("pht",[])) > 0:
                Color(R, G, B, O)                          #Color(1,1,1,1)
                rect=RoundedRectangle(source=DI["pht"][0],pos=(0,0),radius=[20],size=(sx,sy))    #   DI  dict will have local images, already downloaded
            else:
                Color(R, G, B, O)
                rect = RoundedRectangle( pos=(0, 0), radius=[20], size=(sx, sy))  # DI  dict will have local images, already downloaded

        org=MDRaisedButton(text=DI["org"], icon="pencil",text_color=(1,1,1,1),md_bg_color=(0,0,0,1), rounded_button=20,size_hint=(.25,.1), pos_hint={'center_x': .25,'center_y': .84})

        pht=MDRaisedButton(text=str(len(DI["pht"]))+"phot..", text_color=(0,0,1,1),md_bg_color=(1,1,1,1), rounded_button=20,size_hint=(.1,.1), pos_hint={'center_x': .45,'center_y': .8})

        N_chats=MDFlatButton(text=str(rep)+" reps", text_color=(0,0,0,.7),md_bg_color=(B,R,R,.5),size_hint=(.25,.1),rounded_button=5,
                               pos_hint={'center_x': .75,'center_y': .84})

        date=MDRaisedButton(text=DI.get("day","...../...../20...  H : M : S"), text_color=(1,1,1,1),md_bg_color=(0,0,1,.4), rounded_button=10,size_hint=(.25,.1),
                               pos_hint={'center_x': .75,'center_y': .8})
        msg=TextInput(text=sms[:35]+"...",background_color=(1,1,1,0),foreground_color=(0,0,0,.6),size_hint=(1,.7), pos_hint={'center_x': .54, 'center_y': .34})

        back = MDRaisedButton(md_bg_color=(1, 1, 1, 0), x=3,ids={"schm":schm.replace("bin",""),"dt":DI,"COLOR":[R,G,B,O]},
                              rounded_button=10, size_hint=(.98, .98), pos_hint={'center_x': .5, 'center_y': .5},on_release=self.MSG)

        back.bind(on_press=lambda x: send({"action": "contact", "idd": DI["idd"], "sidd": str(uuid.uuid4())[:5]}))

        #+"/"+DI["sidd"]
        scren.add_widget(org)
        org.font_size=org.font_size-4
        # scren.add_widget(pht)
        scren.add_widget(N_chats)
        scren.add_widget(back)
        scren.add_widget(msg)
        # scren.add_widget(date)

        msg.font_size = msg.font_size - 4


        rect.size = (sx,sy)
        msg.elevation=0
        # date.elevation=0
        N_chats.elevation=0
        N_chats.font_size=N_chats.font_size-6
        back.elevation = 0

        return scren

    def CARO3(self,DI,schm=None,sx=Window.size[0] / 8,sy=Window.size[1] / 15,ORIGINE=None):
        def photo(x):
            nonlocal pht
            if platform == "android" :
                pth.append(self.load_image())
            else:
                l=[]

                self.preload_image(BT=x)
                send.bind(on_press=lambda _:pht.append(x.ids.get("pht","")))

            Logger.info(f"pht.ids: {pht}")
        def SIDD():
            sidd = str(uuid.uuid4()).replace("-","").replace(" ","").replace("_","")
            return sidd[:3]+sidd[-3:]

        pht=[]
        try:
            sms = open("ch", "r").read()
        except:
            sms = ""

        scren = RelativeLayout(size_hint=(None,None),size=(sx,sy))
        with scren.canvas.before:
            Color(1, 1, 1, 1)  # source=DI["pht"][0],
            rect = RoundedRectangle(pos=(0, 0), radius=[20], size=(sx,sy))  # DI  dict will have local images, already downloaded

        org = MDRaisedButton(text=self.ME["Name"][0], text_color=(0, 0, 1, 1), md_bg_color=(1, 1, 1, 1),
                             rounded_button=20,size_hint=(.22, .1), pos_hint={'center_x': .2, 'center_y': .97})

        pic = MDIconButton(icon="photos/gal.png",icon_size=rect.size[0]/4, text_color=(0, 0, 1, 1), md_bg_color=(.7,.3,.4, 0),on_release=photo,
                             rounded_button=10, size_hint=(None,None),size=(rect.size[0]/8,rect.size[0]/8), pos_hint={'center_x': .6, 'center_y': .97})


        send=MDIconButton(icon="photos/v.png",icon_size=rect.size[0]/4, text_color=(1, 1, 1, 1), md_bg_color=(.3,.87,.3, 0),rounded_button=10, size_hint=(None,None),
                           size=(rect.size[0]/8,rect.size[0]/8), pos_hint={'center_x': .9, 'center_y': .97})


        _msg = RelativeLayout(size_hint=(None,1),size=(scren.size[0],scren.size[1]/1.2), pos=(0,5))
        msg = self.S_TextInputApp( Text=sms,S="ch",BG=(0, 0, .3, 0), FG=(0, 0, 0, .6),bw=5)  # size_hint=(.8, .5)
        msg.size_hint=(None,None)
        msg.size=_msg.size
        _msg.add_widget(msg)

        back = MDRaisedButton(md_bg_color=(1, 1, 1, 0), x=3, rounded_button=10, size_hint=(.98, .98),
                              pos_hint={'center_x': .5, 'center_y': .5})

        if DI.get("org", 0) != "Me":
            pass
            # scren.add_widget(back)
        scren.add_widget(_msg)

        rect.size=(sx,sy)

        sidd = []
        send.bind(on_press=lambda bt: sidd.append(SIDD()))

        if "contacts/" in schm:
            send.bind(on_release=lambda c: self.send_message({"schm":schm.replace(".bin","/").replace(".json","/")+"/" +sidd[-1] ,"msg": msg.children[0].text, "recipients":[DI["idd"]],"sidd":sidd[-1], "pth": pht},inbox="ok"))
        else:
            send.bind(on_release=lambda c: self.send_message({"schm": schm.replace(".bin", "/").replace(".json","/") + "/" + sidd[-1], "msg": msg.children[0].text, "recipients":[DI["idd"]],"sidd": sidd[-1], "pth": pht},comment="ok"))

        send.bind(on_release=lambda btn: os.remove("ch"))

        scren.add_widget(org)
        scren.add_widget(pic)
        scren.add_widget(send)

        return scren

    def S_TextInputApp(self,S,Text="", BG=(0, 0, 0, 1), FG=(1, 1, 1, .6),bw=15):
        global rect__, _S_TextInputApp
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.textinput import TextInput
        from kivy.graphics import Color, Rectangle

        def _update_rect(instance, value):
            global rect__
            """ Update the background rectangle size and position """
            rect__.size = instance.size
            rect__.pos = instance.pos

        def on_text_input_focus(instance, value):
            """Handle focus event for the TextInput"""
            if value:  # If the TextInput is focused
                print("TextInput is focused")
                # Window.request_keyboard(self._keyboard_closed, instance)
            else:
                print("TextInput focus lost")

        def _keyboard_closed(self):
            """Handle keyboard closing event."""
            print("Keyboard has been closed")

        def typed(w, t):
            global _S_TextInputApp
            _S_TextInputApp = w.text

        R = BG[0]
        G = BG[1]
        B = BG[2]
        O = BG[3]

        # main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a ScrollView
        scroll_view = ScrollView(
            size_hint=(1, 1),
            bar_width=bw,  # Customize the scrollbar width
            bar_inactive_color=(0, 0, 0, .8),
            scroll_type=['bars', 'content'],  # Enable both scrollbar and content dragging
            do_scroll_x=False,  # Disable horizontal scrolling
            do_scroll_y=True  # Enable vertical scrolling
        )

        # font_size=20,  # Increase font size for readability
        text_input = TextInput(
            text=Text,
            hint_text='Text...',
            multiline=True,
            size_hint_y=None,  # Disable auto-resize
            height=500,  # Set a height to enable scrolling

            background_color=BG,  # White background for TextInput
            foreground_color=FG,  # Black text color
            padding=[10, 10, 10, 10]  # Add padding for better UX
        )

        # Set the height of the TextInput dynamically
        text_input.bind(minimum_height=text_input.setter('height'))

        # Add the TextInput to the ScrollView
        scroll_view.add_widget(text_input)

        # Add the ScrollView to the main layout
        # main_layout.add_widget(scroll_view)

        # Custom background for ScrollView
        with scroll_view.canvas.before:
            Color(R, G, B, O)  # (0.9, 0.9, 0.9, 1)  # Light gray background for ScrollView
            rect__ = Rectangle(size=scroll_view.size, pos=scroll_view.pos)
            scroll_view.bind(size=_update_rect, pos=_update_rect)

        # Bind touch_down event to focus the TextInput
        text_input.bind(focus=on_text_input_focus)
        text_input.bind(text=lambda w,tx:open(S,"w").write(tx))

        return scroll_view  #main_layout

    def PROFILE(self, iddd, update_new=None,mine=None):
        """BIO ON LEFT
        PUBLIC COMMENTS RIGHT              2 message will be downloaded when the scroll reaches the end
        BUSINESS OR TALENT PHOTOS BOTTOM

        """

        if update_new:
            self.pcomg.remove_widget(self.pcomg.children[-1])
            self.pcomg.add_widget(
                self.CARO2(DI=update_new, schm=update_new["schm"], sx=Window.size[0] / 3.5,
                           sy=(Window.size[1] / 10) * 2),
                index=len(self.pcomg.children))
            self.pcomg.size = (self.pcomg.size[0], self.pcomg.size[1] + Window.size[1] / 5)
            self.pcomg.add_widget(
                self.CARO3(DI=update_new, schm=update_new["schm"], sx=Window.size[0] / 3.5,
                           sy=(Window.size[1] / 10) * 2),
                index=len(self.pcomg.children))
            self.pcomg.size = (self.pcomg.size[0], self.pcomg.size[1] + Window.size[1] / 5)
            return

        idd = iddd.ids["idd"]
        schm = iddd.ids["schm"]
        schm2 = iddd.ids["schm"] + "/chats/"
        if not os.path.isfile(schm + "/" + idd + ".json"):
            print()
            if mine:
                self.new(x=None,idd=None)
            return
        DIC = json.load(open(schm + "/" + idd + ".json", "r"))
        FILES = self._files(schm2)

        RL = RelativeLayout(size_hint=(None, None), size=(Window.size[0] - 200, Window.size[1] / 2), ids={"x": 0},
                            pos=(200, 300))
        with RL.canvas.before:
            Color(0, randint(0, 100) / 100, randint(0, 100) / 100, randint(80, 100) / 100)
            rect = RoundedRectangle(pos=(0, 0), radius=[20], size=RL.size)

        with RL.canvas.before:
            Color( randint(0, 100) / 100, randint(0, 70) / 100, randint(0, 30) / 100, 1)
            RCT = RoundedRectangle(pos=(0,0), radius=[20], size=(RL.size[0], RL.size[1] / 2.4))

        prof = RelativeLayout(opacity=.3,size_hint=(None, None), size=(Window.size[0] / 4, Window.size[0] / 4), ids={"x": 0},
                              pos=(0, RL.size[1] - Window.size[0] / 4))
        Im = AsyncImage(source=self.profile(DIC.get("idd","")))  # self.profile checkes in contacts/idd/idd.png  if not idd.png, return link and download it.
        prof.add_widget(Im)
        if idd == self.ME["idd"]:
            open_prfl = MDRaisedButton(md_bg_color=(1, 1, 1, 0), ids={"idd": DIC.get("idd", "")}, rounded_button=10,
                                       size_hint=(.98, .98), pos_hint={'center_x': .5, 'center_y': .5},
                                       on_release=lambda x: self.preload_image(Im))

            Edit = MDIconButton(icon="photos/user.png", icon_size=RL.size[0] / 16, md_bg_color=(0, 0, 0, .3),
                                rounded_button=30, size_hint=(None, None),
                                size=(RL.size[0] / 4, RL.size[0] / 4),
                                pos_hint={'center_x': .15, 'center_y': .1},
                                on_press=lambda bt: self.new(x=bt,idd=DIC["idd"]))

            prof.add_widget(open_prfl)
            prof.add_widget(Edit)
            open_prfl.elevation = 0
        RL.add_widget(prof)

        sx = Window.size[0] / 3.5
        sy = (Window.size[1] / 10) * 2

        coms = ScrollView(size_hint=(None, None), size=(RL.size[0] / 2, RL.size[1] / 2.5),
                          pos=(RL.size[0] / 2, RL.size[1] / 1.8),
                          do_scroll_x=False, do_scroll_y=True, scroll_type=['bars', 'content'], bar_width=10,
                          bar_color=(1, 1, 0, 1), bar_margin=0)

        self.pcomg = GridLayout(cols=1, orientation='bt-lr', spacing=40, size_hint=(1, None),
                                size=(RL.size[0] / 2, (Window.size[1] / 6) * 2), col_default_width=sx,
                                col_force_default=True,
                                row_default_height=sy, row_force_default=True)

        self.pcomg.add_widget(self.CARO3(DI=DIC, schm=schm2, sx=sx, sy=sy))
        hist = ""
        for cht in FILES:
            if cht.replace(".bin", "") != hist.replace(".bin", ""):
                dict = pickle.load(open(schm2 + cht + ".bin", "rb"))
                self.pcomg.add_widget(self.CARO2(DI=dict, schm=schm2 + "/" + cht.replace(".bin", ""), sx=sx, sy=sy))
                self.pcomg.size = (self.pcomg.size[0], self.pcomg.size[1] + Window.size[1] / 4)
            hist = cht

        coms.add_widget(self.pcomg)

        RL.add_widget(coms)
        coms.scroll_y = 0

        sx = RL.size[0] / 2.5
        sy = (Window.size[1] / 10) * 2

        SDW = ScrollView(size_hint=(None, None), size=(RL.size[0]/1.2 , RL.size[1] / 2.5),
                         pos_hint={'center_x': .5, 'center_y': .26},do_scroll_x=True, do_scroll_y=False, scroll_type=['bars', 'content'],
                         bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)


        GDW = GridLayout(rows=2, spacing=5, size_hint=(None, None), size=((RL.size[0] / 1.3)+2000, RL.size[1] / 2.7) )
                                               # col_default_width=RL.size[0] /2, col_force_default=True,
                                            #    row_default_height=(RL.size[1] / 2.5)/2, row_force_default=True

        if DIC.get("BUSY", 0):
            for itm in DIC.get("BUSY", []):
                ph = RelativeLayout(ids={"x": 0})

                if len(itm)>1 :
                    Im = AsyncImage(source=self.profile(itm[1].replace(".png",""),dir="Items"))     #here
                    ph.add_widget(Im)
                    opn = MDRaisedButton(md_bg_color=(1, 1, 1, 0), elevation=0,ids={"idd": DIC.get("idd", "")}, rounded_button=10)
                    ph.add_widget(opn)
                    opn.elevation=0
                    GDW.add_widget(ph)

                    opn2 = MDRaisedButton(text=itm[0], elevation=0, md_bg_color=(randint(0, 30) / 100, randint(0, 30) / 100, randint(0, 30) / 100, 1),
                                         size_hint=(None, None), size=(RL.size[0] / 2, (RL.size[1] / 2.5) / 2),ids={"idd": DIC.get("idd", "")}, rounded_button=10)
                    GDW.add_widget(opn2)
                else :
                    opn = MDRaisedButton(text=itm[0],elevation=0,md_bg_color=(randint(0, 30) / 100, randint(0, 30) / 100, randint(0, 30) / 100, 1),
                                              size_hint=(None, None), size=(RL.size[0] /2, (RL.size[1] / 2.5)/2 ) , ids={"idd": DIC.get("idd", "")}, rounded_button=10)
                    GDW.add_widget(opn)

                GDW.size = (GDW.size[0]+(RL.size[0] /4), GDW.size[1] )


        SDW.add_widget(GDW)
        RL.add_widget(SDW)
        SDW.scroll_y = 1.

        self.RLD(Im)

        self.moveer(RL, pos=(50, randint(50, Window.size[1] // 1.8)))
        print(randint(50, Window.size[1] // 1.8))

    def RLD(self,Im):
        if len(Im.source) < 3:
            Im.reload()
        else:
            pass
            # threading.Thread(target=self.RLD,args=(Im,)).start()

    def _talk(self,idd=None,sidd=None,stop=None):
        if stop :
            try:
                self.mRecorder2.stop()
                self.mRecorder2.release()
            except:
                pass
            try:
                self.mRecorder.stop()
                self.mRecorder.release()
            except:
                pass
            Clock.unschedule( self.clockstop)
            self.rn=0
            vibrator.vibrate(1)
            return
        if platform == 'android':
            self.rn += 1
            # try:
            if not os.path.isdir(dr()+"talking/"):
                os.mkdir(dr()+"talking/")
            MediaRecorder = autoclass('android.media.MediaRecorder')
            AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
            OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
            AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
            Environment = autoclass('android.os.Environment')

            # storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
            output_file = dr()+'talking/'+sidd+'.mp3'

            self.mRecorder = MediaRecorder()
            self.mRecorder.setAudioSource(AudioSource.MIC)
            self.mRecorder.setOutputFormat(OutputFormat.MPEG_4)
            self.mRecorder.setOutputFile(output_file)
            self.mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)
            try:
                self.mRecorder2.stop()
                self.mRecorder2.release()
            except:
                pass
            self.mRecorder.prepare()
            self.mRecorder.start()
            self.clockstop=Clock.schedule_once(lambda cl:self.next_talk(idd,sidd=str(self.rn)+"_"+str(uuid.uuid4())[:8]),4)

        else:
            pass

    def next_talk(self,idd,sidd):
        if platform == 'android':
            self.rn+=1
            if not os.path.isdir(dr()+"talking/"):
                os.mkdir(dr()+"talking/")
            MediaRecorder = autoclass('android.media.MediaRecorder')
            AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
            OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
            AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
            Environment = autoclass('android.os.Environment')

            # storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
            output_file = dr()+'talking/'+sidd+'.mp3'

            self.mRecorder2 = MediaRecorder()
            self.mRecorder2.setAudioSource(AudioSource.MIC)
            self.mRecorder2.setOutputFormat(OutputFormat.MPEG_4)
            self.mRecorder2.setOutputFile(output_file)
            self.mRecorder2.setAudioEncoder(AudioEncoder.AMR_NB)
            try:
                self.mRecorder.stop()
                self.mRecorder.release()
            except:
                pass

            self.mRecorder2.prepare()
            self.mRecorder2.start()

            self.clockstop=Clock.schedule_once(lambda cl:self._talk(idd=idd,sidd=str(self.rn)+"_"+str(uuid.uuid4())[:8]),4)

        else:
            pass

        print(idd,"talking...")

    def MSG(self,B,update_new=None):
        "Each item has its own messages. when deleted, messges goes too"
        "each profile has its private chats,each idd with its chats list and images path"

        def _like(idd,btn):
            print("schm ",schm)
            if not os.path.isdir('.lk'):
                os.mkdir(".lk")
            if idd in self._files(".lk"):
                os.remove(".lk/"+idd)
                btn.text=str(int(btn.text)-1)
                l=int(DIC.get("lk",0))-1
                DIC["lk"]=str(l)
                if "contacts/" in schm:
                    pickle.dump(DIC,open(dr()+schm.replace(".bin","").replace(".json","") + ".bin", "wb"))
                else:
                    pickle.dump(DIC, open(dr() +"Activities/"+ schm.replace(".bin", "").replace(".json", "").replace("Activities", "/") + ".bin", "wb"))

                Dict = {"action": "lk","tg": idd, "sidd": str(uuid.uuid4()).replace("-","").replace("_","")[:12], "schm": schm,
                        "idd": self.ME["idd"], "recipients": [DIC["idd"]],"zone": self.ME["adress"],
                        "N": "-1"}
                send(Dict)

            else:
                open(".lk/"+idd,"w").write(schm)

                btn.text = str(int(btn.text) + 1)
                l = int(DIC.get("lk", 0)) + 1
                DIC["lk"] = str(l)
                if "contacts/" in schm:
                    pickle.dump(DIC, open(dr() + schm.replace(".bin", "").replace(".json", "") + ".bin", "wb"))
                else:
                    pickle.dump(DIC, open(dr() + "Activities/" + schm.replace(".bin", "").replace(".json", "").replace("Activities", "/") + ".bin","wb"))

                Dict = {"action": "lk","tg":idd, "sidd": str(uuid.uuid4()).replace("-", "").replace("_", "")[:12], "schm": schm,
                        "idd": self.ME["idd"], "recipients": [DIC["idd"]],"zone": self.ME["adress"],
                        "N": "-1"}
                send(Dict)
        def _block(idd,btn):
            if not os.path.isdir('.bl'):
                os.mkdir(".bl")
            if idd in self._files(".bl"):
                os.remove(".bl/" + idd)
                btn.text = str(int(btn.text) - 1)
                l = int(DIC.get("bl", 0)) - 1
                DIC["bl"] = str(l)
                if "contacts/" in schm:
                    pickle.dump(DIC, open(dr() + schm.replace(".bin", "").replace(".json", "") + ".bin", "wb"))
                else:
                    pickle.dump(DIC, open(dr() + "Activities/" + schm.replace("Activities/", "").replace(".bin", "").replace(".json", "") + ".bin","wb"))
                Dict={"action": "bl","tg": idd, "sidd": str(uuid.uuid4()).replace("-","").replace("_","")[:12], "schm":schm, "zone": self.ME["adress"], "idd": self.ME["idd"],"recipients":[DIC["idd"]],"N":"-1"}
                send(Dict)
            else:
                open(".bl/" + idd, "w").write(schm)

                btn.text = str(int(btn.text) + 1)
                l = int(DIC.get("bl", 0)) + 1
                DIC["bl"] = str(l)
                if "contacts/" in schm:
                    pickle.dump(DIC, open(dr() + schm.replace(".bin", "").replace(".json", "") + ".bin", "wb"))
                else:
                    pickle.dump(DIC, open(dr() + "Activities/" + schm.replace("Activities/", "").replace(".bin", "").replace(".json", "") + ".bin","wb"))
                Dict = {"action": "bl", "tg": idd,"sidd": str(uuid.uuid4()).replace("-","").replace("_","")[:12], "schm": schm, "zone": self.ME["adress"],"idd": self.ME["idd"], "recipients": [DIC["idd"]],
                        "N": "1"}
                send(Dict)

        def Get(sch,Id,sv):
            # print(sv.scroll_y)
            # check.append(sv.scroll_y)
            if sv.scroll_y > 1  :
                # sv.scroll_y=0.
                try:
                    vibrator.vibrate(1/50)
                    # notification.notify(message="Next", app_icon="photos/s1.png")
                except:
                    pass
                    # notification.notify(title="Next",message="Getting 2 privious messages",app_icon="photos/s1.png")
                dic={"action":"next","zone":self.ME["adress"],"idd":self.ME["idd"],"recipients":[self.ME["idd"]],"schm":sch,"sidd":str(uuid.uuid4())[:3]}# "Id":Id
                send(dic)

        if update_new:
            self.comg.remove_widget(self.comg.children[-1])

            self.comg.add_widget(self.CARO2(DI=update_new,schm=update_new["schm"],sx = Window.size[0] / 3.5,sy=(Window.size[1] / 10)*2),index=len(self.comg.children))
            self.comg.size = (self.comg.size[0], self.comg.size[1] + Window.size[1] / 5)
            self.comg.add_widget(self.CARO3(DI=update_new, schm=update_new["schm"],sx = Window.size[0] / 3.5,sy=(Window.size[1] / 10)*2),index=len(self.comg.children))
            self.comg.size = (self.comg.size[0], self.comg.size[1] + Window.size[1] / 5)
            return

        check=[]
        DIC=B.ids
        schm=DIC["schm"].replace(".bin","/")
        if "contacts/" in schm :
            FILES = self._files(schm)
            DIC = pickle.load(open(B.ids["schm"] + ".bin", "rb"))
        else:
            print("schm: ",B.ids["schm"])
            FILES = self._files(dr() + "Activities/" + schm.replace("Activities/","/"))
            DIC = pickle.load(open(dr() + "Activities" + "/" + B.ids["schm"].replace("Activities/","/").replace(".json","").replace(".bin","") + ".bin", "rb"))

        try:
            DIC["pht"].remove("")
        except:
            pass

        L=len(DIC.get("chats",[]))  # """{chat_idd{org, idd,pht,msg}}"""

        self.RL=RelativeLayout(size_hint=(None,None),size=(Window.size[0]-200, Window.size[1] / 2),ids={"x":0},pos=(0, 0))
        with self.RL.canvas.before:
            Color(B.ids["COLOR"][0],B.ids["COLOR"][1],B.ids["COLOR"][2],1)
            rect = RoundedRectangle(source="back.jpg",pos=(0, 0), radius=[20], size=self.RL.size)  # Window.size[0]-200, Window.size[1]-200

        prof=RelativeLayout(size_hint=(None,None),size=(self.RL.size[0]/2, self.RL.size[0]/2),ids={"x":0},pos=(0, self.RL.size[1]-self.RL.size[0]/2))
        #
        Im=AsyncImage(source=self.profile(DIC["idd"]))      #  self.profile checkes in contacts/idd/idd.png  if not idd.png, return link and download it.
        prof.add_widget(Im)
        open_prfl=MDRaisedButton(md_bg_color=(1, 1, 1, 0),ids={"idd":DIC["idd"],"schm":dr()+"contacts/"+DIC["idd"]},
                                 rounded_button=10, size_hint=(.98, .98), pos_hint={'center_x': .5, 'center_y': .5},on_release=self.PROFILE)
        prof.add_widget(open_prfl)
        open_prfl.elevation=0
        self.RL.add_widget(prof)

        sx = Window.size[0] / 3.5
        sy = (Window.size[1] / 10)*2

        coms = ScrollView(size_hint=(None, None), size=(self.RL.size[0] / 2 ,self.RL.size[1]/2.5 ), pos=(self.RL.size[0]/2, self.RL.size[1]/1.8),
                          do_scroll_x=False,do_scroll_y=True, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1), bar_margin=0)

        coms.bind(on_scroll_stop=lambda w,x:Get(schm,DIC["idd"],coms))

        self.comg = GridLayout(cols=1, orientation='bt-lr',spacing=40, size_hint=(1, None),size=(self.RL.size[0] / 2 , (Window.size[1] / 6)*2),col_default_width=sx,col_force_default=True,
                          row_default_height=sy ,row_force_default=True)



        chats= DIC.get("chats",{})
        if not "chats" in DIC :
            DIC["chats"]={}
        # print("schm: ",schm)


        self.comg.add_widget(self.CARO3(DI=DIC, schm=schm, sx=sx, sy=sy,ORIGINE=B))

        hist=""
        for cht in FILES:
            if cht.replace(".bin","") != hist.replace(".bin","") :
                if "contacts/" in schm:
                    dict=pickle.load(open(schm+".bin","rb"))
                else:
                    dict = pickle.load(open(dr() + "Activities" + "/" + schm + ".bin", "rb"))

                self.comg.add_widget(self.CARO2(DI=dict,schm=schm+"/"+cht.replace(".json", "").replace(".bin", ""),sx=sx,sy=sy))  # cht are file ending witn   .bin
                self.comg.size = (self.comg.size[0], self.comg.size[1] + Window.size[1] / 4)
            hist=cht

        coms.add_widget(self.comg)
        self.RL.add_widget(coms)
        coms.scroll_y=0

        lk=MDRaisedButton(text=str(DIC.get("lk",0)), text_color=(1,1,1, 1), icon_size=self.RL.size[0] / 15,
                     md_bg_color=(0, 0, 1, 0), size_hint=(None, None), size=(self.RL.size[0] / 8, self.RL.size[0] / 4),
                     pos_hint={'center_x': .09, 'center_y': .57})

        like =MDIconButton(text="27",text_color=(1,1,1,1),icon="photos/lk2.png",icon_size=self.RL.size[0] / 15,
                           md_bg_color=(0, 0, 1, .4),size_hint=(None,None),size=(self.RL.size[0] / 8 , self.RL.size[0] / 4),
                           pos_hint={'center_x': .09, 'center_y': .61},on_release=lambda btn:_like(DIC["idd"],lk))


        bl = MDRaisedButton(text=str(DIC.get("bl", 0)),  text_color=(1,1,1, 1),
                            icon_size=self.RL.size[0] / 15, md_bg_color=(0, 0, 1, 0), size_hint=(None, None),
                            size=(self.RL.size[0] / 8, self.RL.size[0] / 4), pos_hint={'center_x': .24, 'center_y': .57})

        block = MDIconButton(icon="photos/bl.png",icon_size=self.RL.size[0] / 15, md_bg_color=(0, 0, 1, .4), rounded_button=30, size_hint=(None,None),
                             size=(self.RL.size[0] / 4 , self.RL.size[0] / 4), pos_hint={'center_x': .24, 'center_y': .61})
        lk.font_size=lk.font_size-3
        bl.font_size = bl.font_size - 3


        talk = MDIconButton(icon="photos/talk.png", icon_size=self.RL.size[0] / 15,md_bg_color=(0, 0, 1, .4), rounded_button=30, size_hint=(None, None),
                             size=(self.RL.size[0] / 4, self.RL.size[0] / 4), pos_hint={'center_x': .39, 'center_y': .61},
                            on_release=lambda bt: self._talk([DIC["idd"]],stop=2),on_press=lambda bt: self._talk([DIC["idd"]],sidd='0_'+str(uuid.uuid4())[:8]))

        bl.bind(on_release=lambda btn: _block(DIC["idd"], bl))

        self.RL.add_widget(like)
        self.RL.add_widget(lk)
        lk.elevation=0
        self.RL.add_widget(block)
        self.RL.add_widget(bl)
        bl.elevation=0
        self.RL.add_widget(talk)

        _msg = RelativeLayout(size_hint=(1, .4), pos_hint={'center_x': .5, 'center_y': .35})
        msg = S_TextInputApp(Text=DIC["msg"], BG=(1, 1, 1, .3), FG=(0, 0, 0, .6))
        _msg.add_widget(msg)

        self.RL.add_widget(_msg)
        L=len(DIC.get("pht",[]))
        PHTs=ScrollView(size_hint=(1,.2), pos=(3,1), do_scroll_x=True,
                         do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1),bar_margin=0)
        P_S=GridLayout(cols=L, spacing=3, size_hint=(None, None),size=((Window.width/4)*L+200,Window.size[1] / 8 ),col_default_width=Window.width/4,col_force_default=True) #

        cnt=0
        for im in DIC.get("pht",[]) :
            print("im :",im)
            if "ACCOUNTS/" in im :
                im='ftp://aime shabani:'+self.PWD+'@'+self.ip+":"+"2121"+'/'+ im
            cnt+=1
            cli=RelativeLayout()
            cli.add_widget(AsyncImage(source=im,pos_hint={'center_x': .5,'center_y': .5}))
            b=MDRaisedButton(ids={"iddd":im},md_bg_color=(1,1,1,0), rounded_button=20,size_hint=(.25,.5), pos_hint={'center_x': .5,'center_y': .5} )
            b.bind(on_release=lambda xi: self.Loader(x=xi.ids["iddd"],name=b.ids["iddd"]+"@"+str(cnt)))
            cli.add_widget(b)
            b.elevation=0
            P_S.add_widget(cli)
        PHTs.add_widget(P_S)
        self.RL.add_widget(PHTs)

        self.RLD(Im)

        self.moveer(self.RL,pos=(50, randint(50,Window.size[1]//1.8)))

    def zchat(self,POS,schm,sig=None,ME=None):

        def SLines(schm, pos, cas=".", color=[],me=None):
            def generator(gr):  # 6
                level = gr.ids["lv"]
                for dic in self._files(dr() + "Activities/" + level):
                    ORG = pickle.load(
                        open(dr() + "Activities/" + level + dic.replace(".bin", "").replace(".json", "") + ".bin",
                             "rb"))
                    yield ORG

            def Get(sch, sv):
                if sv.scroll_x > 1.:
                    try:
                        vibrator.vibrate(1 / 20)
                    except:
                        pass
                    try:
                        DICT = next(self.zchat_Generator)
                        self.l_r.cols = self.l_r.cols + 1
                        self.l_r.size = (self.l_r.size[0] + (Window.width / 1.3), Window.size[1] / 4)  # Window.width / 1.3  size[0]+(Window.width / 1.5)
                        self.l_r.add_widget(self.caro(DICT, schm=self.ME["adress"][1]+ "/" + DICT["sidd"]))
                    except Exception as e:
                        dic = {"action": "next", "zone": self.ME["adress"], "idd": self.ME["idd"],
                               "recipients": [self.ME["idd"]], "schm": self.ME["adress"][1]+"/", "sidd": str(uuid.uuid4())[:3]}  # "Id":Id
                        send(dic)
                        print("END.")
                        return


            if me:
                """
                schm=dicti["schm"]+"/"+dicti["sidd"]     ?????????
                """
                self.l_r.cols = self.l_r.cols + 1
                self.l_r.add_widget(self.caro(DI=me, schm=me["schm"]),index=1)  #  len(self.l_r.children),   + "/" + me["sidd"]
                self.l_r.size = (self.l_r.size[0] + (Window.width / 1.3), Window.size[1] / 4)
                return
            # if me :
            #     Logger.info("INSIDE SLINES() if me 1:")
            #     dicti = {}
            #     FILES=[f.name for f in pathlib.Path(  dr() + "Activities/" + self.ME["adress"][1]   ).iterdir()]
            #     FILES.sort(key= lambda x: os.stat(os.path.join(     dr() + "Activities/" + self.ME["adress"][1]  ,x)).st_mtime,reverse=True)
            #
            #     for dic in FILES:
            #         #""" ch = json.load(open(dr() + "Activities/" + self.ME["adress"][1] + "/" + dic, "r"))"""  # reserved for pickle
            #         if dic.endswith(".bin"):
            #             try:
            #                 ch = pickle.load(open(dr() + "Activities/" + self.ME["adress"][1] + "/" + dic, "rb"))
            #                 dicti[dic] = ch
            #             except Exception as e:
            #                 Logger.info(f"ERROR: {e}")
            #                 # FILES.insert(FILES.index(dic)+1,dic)
            #         else:
            #             try:
            #                 ch = pickle.load(open(dr() + "Activities/" + self.ME["adress"][1] + "/" + dic +".bin", "rb"))
            #                 dicti[dic] = ch
            #             except Exception as e:
            #                 Logger.info(f"ERROR: {e}")
            #                 # FILES.insert(FILES.index(dic)+1,dic)
            #     if isinstance(me,dict):
            #         dicti.update(me)
            #     # for x in self.l_r.children:
            #     #     self.l_r.remove_widget(x)
            #
            #     self.l_r.clear_widgets()
            #     pos=self.___position


            skat = Scatter(size_hint=(None, None), pos=pos)
            with skat.canvas.before:
                Color(1, 1, 1, 1)
                rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(Window.size[0] / 20, Window.size[0] / 30))
            srt = ScrollView(size_hint=(None, None), size=(Window.width, Window.size[1] / 4),
                             pos_hint={'center_x': .2, 'center_y': .5}, do_scroll_x=True,  # 2
                             do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1),
                             bar_margin=0)

            self.l_r = GridLayout(orientation='lr-bt',cols=6 ,ids={"lv":schm}, spacing=5, size_hint=(None, None), col_default_width=Window.width / 1.5,
                             col_force_default=True, size=(Window.width / 1.3, Window.size[1] / 4),
                             pos_hint={'center_x': .5, 'center_y': .5})  # +200)+(Window.width / 1.5)

            scren = RelativeLayout(size_hint=(1., 1.))

            self.zchat_Generator = generator(self.l_r)

            hist=""
            self.l_r.add_widget(caro({}))

            for ii in range(4):  # 3  few first elements
                try:
                    x = next(self.zchat_Generator)
                except Exception as e:
                    DICT = {}
                    # return
                    break
                if x["sidd"] != hist:
                    schm = self.ME["adress"][1] + "/" + x["sidd"]
                    self.l_r.add_widget(self.caro(x, schm=schm))   ##    +"/"+ x["sidd"]
                    self.l_r.size = (self.l_r.size[0] + (Window.width / 1.3),Window.size[1] / 4)
                hist = x["sidd"]
            # self.l_r.add_widget(caro(dicti ))

            srt.add_widget(self.l_r)
            srt.bind(on_scroll_stop=lambda w, x: Get(schm, srt))

            skat.add_widget(srt)

            skat.size = (Window.width, Window.size[1] / 4)
            srt.pos = (skat.size[0] / 20, 0)

            self.add_widget(skat)
            skat.bind(on_touch_up=self.TOUCH)
            self.___position=pos

            THR = threading.Thread(target=self.RECEIVER, args=(4,))
            THR.start()                                             #    AttributeError: 'RM' object has no attribute 'JobTalent_LG'. Did you mean: 'JobTalent'?
            Clock.schedule_once(self.SS,4)
            # self.SS()

        def caro( DI):
            def GAL(x=None):
                try:
                    pht.append(pic.ids["pht"])
                except:
                    threading.Thread(target=GAL).start()
            def CAM(x=None):
                try:
                    pht.append(self.phot.ids["pht"])
                except:
                    threading.Thread(target=CAM).start()
            def cam(x=None):#
                d = str(uuid.uuid4()).replace("-", "").replace(" ", "").replace("_", "")
                n=d[:3]+d[-2:]
                self.PHT(n)
                threading.Thread(target=CAM).start()
            def photo(x):

                if platform == "android":
                    pht.append(self.load_image())
                    # x.ids = {"pht": self.load_image()}
                else:
                    self.preload_image(BT=pic)
                    threading.Thread(target=GAL).start()
            def SIDD():
                sidd=str(uuid.uuid4()).replace("-","").replace(" ","").replace("_","")
                return sidd[:3]+sidd[-2:]

            pht=[]
            try:
                sms=open("Z","r").read()
            except:
                sms=""

            scren = RelativeLayout(size_hint=( None,None),size=(Window.size[0] / 1.5,Window.size[1] / 4))
            with scren.canvas.before:
                Color(1, 1, 1, 1)#  source=DI["pht"][0],
                rect = RoundedRectangle( pos=(0, 0), radius=[20], size=(Window.size[0] / 1.5, Window.size[1] / 6))  # DI  dict will have local images, already downloaded

            org = MDRaisedButton(text=DI.get("org",self.ME["Name"][0]), text_color=(0, 0, 1, 1), md_bg_color=(1, 1, 1, 1), rounded_button=20,
                                 size_hint=(.25, .1), pos_hint={'center_x': .2, 'center_y': .78})

            targ = MDRaisedButton(text="Receivers: "+self.ME["adress"][1], text_color=(0,0,1, .6),
                                     md_bg_color=(0, 0, 0, 0), rounded_button=10, size_hint=(.25, .3),ids={"zn":[]},
                                     pos_hint={'center_x': .6, 'center_y': .59},on_release=lambda bt:self.WORK(bt,msg="Choose who receive : ",found=None,zn=bt))

            pic = MDIconButton(icon="photos/gal.png", icon_size=rect.size[0] / 17, text_color=(0, 0, 1, 1), md_bg_color=(.7, .3, .4, 1),
                               on_release=photo, rounded_button=10, size_hint=(None, None), size=(rect.size[0] / 14, rect.size[0] / 14),pos_hint={'center_x': .45, 'center_y': .78})

            Cam = MDIconButton(icon="photos/cam.png", icon_size=rect.size[0] / 17, text_color=(0, 0, 1, 1),
                               md_bg_color=(.7, .3, .4, 1), on_release=cam, rounded_button=10, size_hint=(None, None),
                               size=(rect.size[0] / 14, rect.size[0] / 14), pos_hint={'center_x': .65, 'center_y': .78})

            send = MDIconButton(icon="photos/v.png",icon_size=rect.size[0]/17, text_color=(1, 1, 1, 1), md_bg_color=(.3,.87,.3, 1),rounded_button=10, size_hint=(None,None),
                           size=(rect.size[0]/14,rect.size[0]/14),pos_hint={'center_x': .85, 'center_y': .78} )

            _msg=RelativeLayout(size_hint=(1, .55),pos_hint={'center_x': .5, 'center_y': .18})
            msg = self.S_TextInputApp(Text=sms , BG=(0, 0, 1, 0), FG=(0, 0, 0, .6),S="ch")      #    size_hint=(.8, .5)
            _msg.add_widget(msg)
            # _msg.children[0].size=scren.size


            back = MDRaisedButton(md_bg_color=(1, 1, 1, 0), x=3, rounded_button=10, size_hint=(.98, .98),
                                  pos_hint={'center_x': .5, 'center_y': .5})

            scren.add_widget(org)
            scren.add_widget(_msg)
            scren.add_widget(targ)
            # if DI.get("org",0) != "Me" :
            #     scren.add_widget(back)

            scren.add_widget(send)
            scren.add_widget(pic)
            scren.add_widget(Cam)

            # msg.size = (Window.size[0] / 3, Window.size[0] / 13)
            # msg.elevation = 0
            send.elevation = 0
            targ.elevation = 0
            # if len(DI["pht"]) > 0:
            #     back.elevation = 0
            rect.size = (Window.size[0] / 1.5, Window.size[1] / 6)

            sidd=[]
            send.bind(on_press=lambda bt:sidd.append(SIDD()))
            send.bind(on_release=lambda c: self.send_message({"tg":targ.ids["zn"],"schm":self.ME["adress"][1]+"/"+sidd[-1],"sidd":sidd[-1],"msg":msg.children[0].text,"pth": pht})) # .children[0]
            try:
                if os.path.isfile("ch"):
                    send.bind(on_release=lambda btn: os.remove("ch"))

            except:
                pass

            return scren
        if ME :
            SLines(pos=None,schm=schm,me=ME)
        else:
            if schm:
                if sig:
                    return caro(chats)
                SLines(schm=schm, pos=POS)
            else:
                if sig:
                    return caro(DI={})
                try:
                    chats = json.load(open("chats.json", "r"))     #make self.zone in case i moved
                except:
                    chats={}

                SLines(schm=schm ,pos=POS)

    def SS(self,clock):
        # NINAANZIA HAPA NA TUMA BARUA
        self.SSR = RelativeLayout( size=(Window.size[0]/2,(Window.size[1]/100)*15),pos_hint={'center_x': .72, 'center_y': .88})   # size_hint=(.5, .09),

        self.seach = MDTextField(hint_text_color_normal=(1,1,1,.8),line_color_normal=(1,1,1,.8),icon_right="magnify",icon_right_color_normal=(1,.6,1,.8),hint_text="Deal ",
                                 foreground_color=(1, 1, 0, 1),pos_hint={'center_x': .5, 'center_y': .5},background_color=(1, 1, 1, .8), multiline=False, allow_copy=True, size_hint=(None, None),
                               size=(Window.width / 2.5, Window.height / 18))
        self.seach.bind(on_text_validate=self._search_client)
        self.seach.bind(focus=self.resiz)
        # self.seach.bind(on_text_validate=self.resiz)

        self.btn = MDRaisedButton( md_bg_color=(.5, .6, 1, .3),size_hint=(1, 1), pos_hint={'center_x': .5, 'center_y': .5},on_release=self.resiz)
        self.SSR.add_widget(self.btn)
        self.SSR.add_widget(self.seach)
        self.moveer(self.SSR,pos=( Window.size[0] / 2.5 , Window.size[1] - (Window.size[1] / 10)))

    def _SS(self):

        self.SSR = RelativeLayout(size_hint=(.5, .09), pos_hint={'center_x': .67, 'center_y': .88})

        self.seach = MDTextField(hint_text_color_normal=(1, 1, 1, .8), line_color_normal=(1, 1, 1, .8),
                                 icon_right="magnify", icon_right_color_normal=(1, .6, 1, .8), hint_text="Deal ",
                                 foreground_color=(1, 1, 0, 1),
                                 pos_hint={'center_x': .67, 'center_y': .5}, background_color=(1, 1, 1, .8),
                                 multiline=False, allow_copy=True, size_hint=(None, None),
                                 size=(Window.width / 2.5, Window.height / 18))
        self.seach.bind(on_text_validate=self._search_client)
        self.seach.bind(focus=self.resiz)
        self.seach.bind(on_text_validate=self.resiz)

        self.btn = MDRaisedButton(md_bg_color=(.5, .6, 1, .3), size_hint=(1, 1), pos_hint={'center_x': .67, 'center_y': .5},
                                  on_release=self.resiz)
        self.SSR.add_widget(self.btn)
        self.SSR.add_widget(self.seach)
        self.Desktop.add_widget(self.SSR)

    def TOUCH(self,widget,touch):
        if platform=="android":
            dist=Window.size[1]/18
        else:
            dist = 30
        if widget.collide_widget(self.TR):
            if widget.pos[1] >= self.TR.pos[1]:
                if widget.pos[1] - self.TR.pos[1] <= dist:
                    self.remove_widget(widget)

            if widget.pos[1] <= self.TR.pos[1]:
                if self.TR.pos[1] - widget.pos[1] <= dist:
                    self.remove_widget(widget)

        # if widget.proximity(self.TR,20):
        #     self.remove_widget(widget)

        # if widget.pos[0] >= self.TR.pos[0]:
        #     if widget.pos[0] - self.TR.pos[0] <=25 :
        #         self.remove_widget(widget)
        #
        # if widget.pos[0] <= self.TR.pos[0]:
        #     if self.TR.pos[0]-widget.pos[0]  <=25 :
        #         self.remove_widget(widget)

        # if widget.pos[1] >= self.TR.pos[1]:
        #     if widget.pos[1] - self.TR.pos[1] <=25 :
        #         self.remove_widget(widget)
        #
        # if widget.pos[1] <= self.TR.pos[1]:
        #     if self.TR.pos[1]-widget.pos[1]  <=25 :
        #         self.remove_widget(widget)

    def moveer(self,widg,pos):
        """
        widg should have size,not size_hint,
        """
        self.skat = Scatter(size_hint=(None, None),ids={"x":pos[0]},pos=(-200,pos[1]))
        with self.skat.canvas.before:
            Color(1,1,1,1)
            rect=RoundedRectangle(pos=(0,0),radius=[10],size=(Window.size[0]/20,Window.size[0] /30))

        self.skat.add_widget(widg)

        # skat.size=(Window.width, Window.size[1] / 6)
        self.skat.size =widg.size
        widg.pos=(self.skat.size[0]/20,0)

        self.call_slid(wid=self.skat)
        self.SLD.append([self.skat, self])
        self.add_widget(self.skat)
        self.skat.bind(on_touch_up=self.TOUCH)
        Window.bind(on_keyboard=self.KEYS)

    def _Lines(self,dicti):    #  deactivate  motions in small settings
        skat = Scatter(size=(Window.size[0],Window.size[0] /3 ), pos_hint={'center_x': .5, 'center_y': .8})   #  RIGHT UP CORNER SMALL SQUARRE TO MOVE SCROLLVIEW                                            1
        srt = ScrollView(size_hint=(1, None), size=(1, Window.size[1] / 6), pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=True, #                           2
                         do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1),bar_margin=0)

        l_r = GridLayout(cols=len(dicti), spacing=5, size_hint=(None, None), col_default_width=Window.width/1.5,col_force_default=True,size=((Window.width/1.5)*len(dicti)+200,Window.size[1] / 6 ),pos_hint={'center_x': .5, 'center_y': .5}) #        3

        scren= RelativeLayout(size_hint=(1., 1.)) #                                                                                                                    4
        for x in dicti.keys() :
            l_r.add_widget( self.caro(dicti[x]) )
        srt.add_widget(l_r)

        # skat.add_widget(srt)
        # srt.center=skat.center
        # self.add_widget(skat)
        self.add_widget(srt)

    def Lines_org(self, pos=None, dicti=None, schm=None, ):
        def generator(gr):  # 6
            level = gr.ids["lv"]
            for dic in self._files(dr() + "Activities/" + level):
                ORG = pickle.load(open(dr() + "Activities/" + level + dic.replace(".bin", "").replace(".json", "") + ".bin", "rb"))
                yield ORG

        def Get(sch, sv):  # 5
            # print("scroll_x >>> ",sv.scroll_x)
            if sv.scroll_x > 1.:
                try:
                    vibrator.vibrate(1 / 20)
                except:
                    pass
                try:
                    DICT = next(self.org_Generator)
                    self.org_LG.cols = self.org_LG.cols + 1
                    self.org_LG.size = (self.org_LG.size[0] + (Window.width / 1.5),
                                        Window.size[1] / 6)  # Window.width / 1.3  size[0]+(Window.width / 1.5)
                    self.org_LG.add_widget(self.caro(DICT, schm=sch + "/" + DICT["sidd"]))
                except Exception as e:
                    dic = {"action": "next", "zone": self.ME["adress"], "idd": self.ME["idd"],
                           "recipients": [self.ME["idd"]], "schm": sch,"sidd": str(uuid.uuid4())[:3]}  # "Id":Id
                    send(dic)
                    print("END.")
                    return

        if dicti:
            """
            schm=dicti["schm"]+"/"+dicti["sidd"]     ?????????
            """
            self.org_LG.add_widget(self.caro(DI=dicti, schm=dicti["schm"]),index=len(self.org_LG.children)) #  + "/" + dicti["sidd"]
            self.org_LG.size = (self.org_LG.size[0] + (Window.width / 1.5), Window.size[1] / 6)
            return

        skat = Scatter(size_hint=(None, None), pos=pos)
        with skat.canvas.before:
            Color(1, 1, 1, 1)
            rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(Window.size[0] / 20, Window.size[0] / 30))
        self.org_srt = ScrollView(size_hint=(None, None), size=(Window.width, Window.size[1] / 6),
                                  pos_hint={'center_x': .2, 'center_y': .5}, do_scroll_x=True,  # 2
                                  do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10,
                                  bar_color=(1, 1, 0, 1),
                                  bar_margin=0)

        self.org_LG = GridLayout(cols=4, ids={"lv": schm}, spacing=5, size_hint=(None, None),
                                 col_default_width=Window.width / 1.5,  # 1 : ids schm
                                 col_force_default=True, size=((Window.width / 1.3) + 200, Window.size[1] / 6),
                                 pos_hint={'center_x': .5, 'center_y': .5})  # 3

        scren = RelativeLayout(size_hint=(1., 1.))
        self.org_Generator = generator(self.org_LG)  # 2

        for x in range(2):  # 3  few first elements
            try:
                DICT = next(self.org_Generator)
            except Exception as e:
                DICT = {}
                # return
                break
            self.org_LG.add_widget(self.caro(DICT, schm=schm + "/" + DICT["sidd"]))
        self.org_srt.add_widget(self.org_LG)

        self.org_srt.bind(on_scroll_stop=lambda w, x: Get(schm, self.org_srt))  # 4

        skat.add_widget(self.org_srt)

        skat.size = (Window.width, Window.size[1] / 6)
        self.org_srt.pos = (skat.size[0] / 20, 0)

        self.add_widget(skat)
        skat.bind(on_touch_up=self.TOUCH)

        # self.org_LG.remove_widget(self.org_LG.children[-1])

    def Lines_JobTalent(self, pos=None, dicti=None, schm=None, ):
        def generator(gr):  # 6
            level = gr.ids["lv"]
            for dic in self._files(dr() + "Activities/" + level):
                ORG = pickle.load(
                    open(dr() + "Activities/" + level + dic.replace(".bin", "").replace(".json", "") + ".bin", "rb"))
                yield ORG

        def Get(sch, sv):  # 5
            # print("scroll_x >>> ",sv.scroll_x)
            if sv.scroll_x > 1.:
                try:
                    vibrator.vibrate(1 / 20)
                except:
                    pass
                try:
                    DICT = next(self.JobTalent_Generator)
                    self.JobTalent_LG.cols = self.JobTalent_LG.cols + 1
                    self.JobTalent_LG.size = (self.JobTalent_LG.size[0] + (Window.width / 1.5),
                                              Window.size[1] / 6)  # Window.width / 1.3  size[0]+(Window.width / 1.5)
                    self.JobTalent_LG.add_widget(self.caro(DICT, schm=sch + "/" + DICT["sidd"]))
                except Exception as e:
                    dic = {"action": "next", "zone": self.ME["adress"], "idd": self.ME["idd"],
                           "recipients": [self.ME["idd"]], "schm": sch, "sidd": str(uuid.uuid4())[:3]}  # "Id":Id
                    send(dic)
                    print("END.")
                    return

        if dicti:
            """
            schm=dicti["schm"]+"/"+dicti["sidd"]     ?????????
            """
            self.JobTalent_LG.add_widget(self.caro(DI=dicti, schm=dicti["schm"] ),index=len(self.JobTalent_LG.children)) # + "/" + dicti["sidd"]
            self.JobTalent_LG.size = (self.JobTalent_LG.size[0] + (Window.width / 1.5), Window.size[1] / 6)
            return

        skat = Scatter(size_hint=(None, None), pos=pos)
        with skat.canvas.before:
            Color(1, 1, 1, 1)
            rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(Window.size[0] / 20, Window.size[0] / 30))
        self.JobTalent_srt = ScrollView(size_hint=(None, None), size=(Window.width, Window.size[1] / 6),
                                        pos_hint={'center_x': .2, 'center_y': .5}, do_scroll_x=True,  # 2
                                        do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10,
                                        bar_color=(1, 1, 0, 1),
                                        bar_margin=0)

        self.JobTalent_LG = GridLayout(cols=4, ids={"lv": schm}, spacing=5, size_hint=(None, None),
                                       col_default_width=Window.width / 1.5,  # 1 : ids schm
                                       col_force_default=True, size=((Window.width / 1.3) + 200, Window.size[1] / 6),
                                       pos_hint={'center_x': .5, 'center_y': .5})  # 3

        scren = RelativeLayout(size_hint=(1., 1.))
        self.JobTalent_Generator = generator(self.JobTalent_LG)

        for x in range(2):  # 3  few first elements
            try:
                DICT = next(self.JobTalent_Generator)
            except Exception as e:
                DICT = {}
                # return
                break
            self.JobTalent_LG.add_widget(self.caro(DICT, schm=schm + "/" + DICT["sidd"]))
        self.JobTalent_srt.add_widget(self.JobTalent_LG)

        self.JobTalent_srt.bind(on_scroll_stop=lambda w, x: Get(schm, self.JobTalent_srt))  # 4

        skat.add_widget(self.JobTalent_srt)

        skat.size = (Window.width, Window.size[1] / 6)
        self.JobTalent_srt.pos = (skat.size[0] / 20, 0)

        self.add_widget(skat)
        skat.bind(on_touch_up=self.TOUCH)

        # self.JobTalent_LG.remove_widget(self.JobTalent_LG.children[-1])

    def Lines_paidAdds(self, pos=None, dicti=None, schm=None, ):
        def generator(gr):  # 6
            level = gr.ids["lv"]
            for dic in self._files(dr() + "Activities/" + level):
                ORG = pickle.load(
                    open(dr() + "Activities/" + level + dic.replace(".bin", "").replace(".json", "") + ".bin", "rb"))
                yield ORG

        def Get(sch, sv):  # 5
            # print("scroll_x >>> ",sv.scroll_x)
            if sv.scroll_x > 1.:
                try:
                    vibrator.vibrate(1 / 20)
                except:
                    pass
                try:
                    DICT = next(self.paidAdds_Generator)
                    self.paidAdds_LG.cols = self.paidAdds_LG.cols + 1
                    self.paidAdds_LG.size = (self.paidAdds_LG.size[0] + (Window.width / 1.5),
                                             Window.size[1] / 6)  # Window.width / 1.3  size[0]+(Window.width / 1.5)
                    self.paidAdds_LG.add_widget(self.caro(DICT, schm=sch + "/" + DICT["sidd"]))
                except Exception as e:
                    dic = {"action": "next", "zone": self.ME["adress"], "idd": self.ME["idd"],
                           "recipients": [self.ME["idd"]], "schm": sch, "sidd": str(uuid.uuid4())[:3]}  # "Id":Id
                    send(dic)
                    print("END.")
                    return

        if dicti:
            """
            schm=dicti["schm"]+"/"+dicti["sidd"]     ?????????
            """
            self.paidAdds_LG.add_widget(self.caro(DI=dicti, schm=dicti["schm"] ),
                                        index=len(self.paidAdds_LG.children)) # + "/" + dicti["sidd"]
            self.paidAdds_LG.size = (self.paidAdds_LG.size[0] + (Window.width / 1.5), Window.size[1] / 6)
            return

        skat = Scatter(size_hint=(None, None), pos=pos)
        with skat.canvas.before:
            Color(1, 1, 1, 1)
            rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(Window.size[0] / 20, Window.size[0] / 30))
        self.paidAdds_srt = ScrollView(size_hint=(None, None), size=(Window.width, Window.size[1] / 6),
                                       pos_hint={'center_x': .2, 'center_y': .5}, do_scroll_x=True,  # 2
                                       do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10,
                                       bar_color=(1, 1, 0, 1),
                                       bar_margin=0)

        self.paidAdds_LG = GridLayout(cols=4, ids={"lv": schm}, spacing=5, size_hint=(None, None),
                                      col_default_width=Window.width / 1.5,  # 1 : ids schm
                                      col_force_default=True, size=((Window.width / 1.3) + 200, Window.size[1] / 6),
                                      pos_hint={'center_x': .5, 'center_y': .5})  # 3

        scren = RelativeLayout(size_hint=(1., 1.))
        self.paidAdds_Generator = generator(self.paidAdds_LG)

        for x in range(2):  # 3  few first elements
            try:
                DICT = next(self.paidAdds_Generator)
            except Exception as e:
                DICT = {}

                # return
                break
            self.paidAdds_LG.add_widget(self.caro(DICT, schm=schm + "/" + DICT["sidd"]))
        self.paidAdds_srt.add_widget(self.paidAdds_LG)

        self.paidAdds_srt.bind(on_scroll_stop=lambda w, x: Get(schm, self.paidAdds_srt))  # 4

        skat.add_widget(self.paidAdds_srt)

        skat.size = (Window.width, Window.size[1] / 6)
        self.paidAdds_srt.pos = (skat.size[0] / 20, 0)

        self.add_widget(skat)
        skat.bind(on_touch_up=self.TOUCH)

        # self.paidAdds_LG.remove_widget(self.paidAdds_LG.children[-1])

    def Lines(self, pos=None, dicti=None, schm=None, ):
        def generator(gr):                                                                                                  #  6
            level = gr.ids["lv"]
            for dic in self._files(dr() + "Activities/" + level):
                ORG = pickle.load(open(dr() + "Activities/" + level + dic.replace(".bin", "").replace(".json", "") + ".bin", "rb"))
                yield ORG
        def Get(sch,sv):                                                                                                    # 5
            # print("scroll_x >>> ",sv.scroll_x)
            if sv.scroll_x > 1. :
                try:
                    vibrator.vibrate(1/50)
                except:
                    pass
                try:
                    DICT = next(self.Generator)
                    self.LG.cols=self.LG.cols+1
                    self.LG.size=(self.LG.size[0]+(Window.width / 1.5), Window.size[1] / 6)#Window.width / 1.3  size[0]+(Window.width / 1.5)
                    self.LG.add_widget(self.caro(DICT, schm=sch + "/" + DICT["sidd"]))
                except Exception  as e :
                    print("END.")
                    return

        if dicti:
            """
            schm=dicti["schm"]+"/"+dicti["sidd"]     ?????????
            """
            self.LG.add_widget(self.caro(DI=dicti, schm=dicti["schm"]+"/"+dicti["sidd"]), index=len(self.LG.children))
            self.LG.size=(self.LG.size[0]+(Window.width / 1.5), Window.size[1] / 6)
            return

        skat = Scatter(size_hint=(None, None),pos=pos)
        with skat.canvas.before:
            Color(1, 1, 1, 1)
            rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(Window.size[0] / 20, Window.size[0] / 30))
        self.srt = ScrollView(size_hint=(None, None), size=(Window.width, Window.size[1] / 6),
                         pos_hint={'center_x': .2, 'center_y': .5}, do_scroll_x=True,  # 2
                         do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=10, bar_color=(1, 1, 0, 1),
                         bar_margin=0)

        self.LG = GridLayout(cols=4,ids={"lv":schm}, spacing=5, size_hint=(None, None), col_default_width=Window.width / 1.5,  #  1 : ids schm
                             col_force_default=True, size=((Window.width / 1.3)+200, Window.size[1] / 6),
                             pos_hint={'center_x': .5, 'center_y': .5})  # 3

        scren = RelativeLayout(size_hint=(1., 1.))
        self.Generator=generator(self.LG)                                                                                     #    2
        print("self.Generator: ",self.Generator)


        for x in range(2):                                                                                                    #  3  few first elements
            try:
                DICT=next(self.Generator)
            except Exception as e :
                DICT = {}

                # return
                break
            self.LG.add_widget(self.caro(DICT, schm=schm +"/"+ DICT["sidd"]))
        self.srt.add_widget(self.LG)

        self.srt.bind(on_scroll_stop=lambda w, x: Get(schm, self.srt))                                                     #  4

        skat.add_widget(self.srt)

        skat.size = (Window.width, Window.size[1] / 6)
        self.srt.pos = (skat.size[0] / 20, 0)

        self.add_widget(skat)
        skat.bind(on_touch_up=self.TOUCH)

        # self.LG.remove_widget(self.LG.children[-1])

    def caro(self,DI,schm=None,idd=None,clr=None):  # file=uuid    dir  kyeg
        def DELT(btn):
            pth=dr()+"Activities/"+btn.ids["schm"].replace(".bin","")
            fil=dr()+"Activities/"+btn.ids["schm"].replace(".bin","")+".bin"

            if os.path.isfile(fil):
                os.remove(fil)
            if os.path.isdir(pth):
                os.rmdir(pth)
            for pic in btn.ids["pics"]:
                if os.path.isfile(dr()+"Items/"+pic):
                    print("DELETE MEDIA TOO")
                else:
                    if os.path.isfile(pic):
                        print("DELETE MEDIA TOO")
            btn.parent.parent.remove_widget(btn.parent)

        def Afirm(btn):
            B=Button(size_hint=(1,1),background_color=(0,0,0,.8))
            self.add_widget(B)
            rel=RelativeLayout(size_hint=(.6,.15),pos_hint={"center_x":.5,"center_y":.5})
            lab=Label(text="Deleting this message will delete All it comments, media and likes :",pos_hint={"center_x":.5,"center_y":.5})
            lab.font_size=lab.font_size-3
            yes=MDRaisedButton(on_press=lambda BT: DELT(btn),rounded_button=5,text="Yes",pos_hint={"center_x":.8,"center_y":.01})
            No=MDRaisedButton(rounded_button=5,text="Non",pos_hint={"center_x":.4,"center_y":.01})
            rel.add_widget(lab)
            rel.add_widget(No)
            rel.add_widget(yes)

            B.bind(on_release=lambda _: self.remove_widget(rel))
            B.bind(on_release=lambda _: self.remove_widget(B))
            No.bind(on_release=lambda _: self.remove_widget(rel))
            No.bind(on_release=lambda _: self.remove_widget(B))
            yes.bind(on_release=lambda _: self.remove_widget(rel))
            yes.bind(on_release=lambda _: self.remove_widget(B))


            self.add_widget(rel)

        try:
            DI["pht"].remove("")
        except:
            pass

        sms=DI.get("msg","No Message")
        R, G, B, O = randint(0, 100) / 100, randint(30, 100) / 100, randint(30, 100) / 100, 1
        scren = RelativeLayout(size_hint=(1,1))
        with scren.canvas.before:#   DI  dict will have local images, already downloaded
            Color(R, G, B, O)
            rect = RoundedRectangle( pos=(0, 0), radius=[20], size=(Window.size[0] / 1.5, Window.size[1] / 6))  # DI  dict will have local images, already downloaded
        if len(DI.get("pht", [])) > 0:
            with scren.canvas.before:
                Color(G,B,R,O)  # Color(1,1,1,1)
                rect2 = RoundedRectangle( source=DI["pht"][0],pos=((Window.size[0] / 1.5)-Window.size[0] / 6, 0), radius=[70],size=(Window.size[0] / 7, Window.size[0] / 7))

        org=MDRaisedButton(text=DI["org"], icon="pencil",text_color=(0,0,1,1),md_bg_color=(1,1,1,1), rounded_button=20,size_hint=(.25,.1), pos_hint={'center_x': .2,'center_y': .8})

        pht=MDRaisedButton(text=str(len(DI["pht"]))+"phot..", text_color=(0,0,1,1),md_bg_color=(1,1,1,1), rounded_button=20,size_hint=(.1,.1), pos_hint={'center_x': .45,'center_y': .8})

        subject=MDRaisedButton(text=DI.get("subject","No subject"), text_color=(1,1,1,1),md_bg_color=(0,0,0,.6), rounded_button=10,size_hint=(.25,.1),
                               pos_hint={'center_x': .3,'center_y': .575})

        delete = MDIconButton(icon="photos/trash.png" ,ids={"schm":schm.replace(".bin",""),"pics":DI["pht"]},text_color=(1, 1, 1, 1),icon_size=Window.size[0]/15,md_bg_color=(0, 0, 0, 0), size_hint=(.25, .1),
                                 pos_hint={'center_x': .05, 'center_y': .45},on_release=Afirm)   # 575


        date=MDRaisedButton(text=DI.get("day",""), text_color=(1,1,1,1),md_bg_color=(0,0,1,.4), rounded_button=10,size_hint=(.25,.1),
                               pos_hint={'center_x': .75,'center_y': .8})


        msg=TextInput(text=sms[:100]+"...",background_color=(1,1,1,0),foreground_color=(0,0,0,.6),size_hint=(.8,.5), pos_hint={'center_x': .5, 'center_y': .11})

        back = MDRaisedButton(md_bg_color=(1, 1, 1, 0), x=3,ids={"schm":schm.replace(".bin",""),"idd":DI["idd"],"dt":DI,"COLOR":[R,G,B,O]},
                              rounded_button=10, size_hint=(.98, .98), pos_hint={'center_x': .5, 'center_y': .3},on_release=self.MSG)

        back.bind(on_press=lambda x: send({"action":"contact","idd":DI["idd"],"sidd":str(uuid.uuid4())[:4]}))

        scren.add_widget(org)
        scren.add_widget(pht)
        scren.add_widget(subject)
        scren.add_widget(back)
        scren.add_widget(msg)
        scren.add_widget(date)
        scren.add_widget(delete)
        # delete.elevation=0


        rect.size = (Window.size[0]/1.5, Window.size[1] / 6)
        msg.size=(Window.size[0]/3,Window.size[0]/13)
        msg.elevation=0
        date.elevation=0
        subject.elevation=0
        # if len(DI["pht"]) > 0 :
        back.elevation = 0

        return scren

    def PERM(self,bt):
        print(bt.ids)
        d=json.load(open("SD/conf/me.json","r"))
        g_new = GridLayout(cols=1, spacing=Window.size[0] / 180)  ##  ,col_default_width=Window.width/1.5,col_force_default=True,row_default_height=Window.height/9,row_force_default=True

        new_popup = Popup(title="Welcome Dear", title_size=Window.size[1] / 80, title_align="center",
                          separator_color=(1, 1, 1, 0), size_hint=(.4, .3), content=g_new, disabled=False)

        textes=["Job/Talent","Special Advert","Org/Leaders"]
        PER=[ "Activities/JobTalent/", "Activities/paidAdds/","Activities/org/"]
        for i in range(3):
            try:
                BT=MDRaisedButton(text=textes[i], md_bg_color=(0,1,0, .8),rounded_button=8,
                                            ids={"perm":d["perm"][i],"schm":PER[i],"data":bt.ids["data"],"files":bt.ids["pht"]},size_hint=(.1, None),size=(1,Window.size[1]/24),pos_hint={'center_y': .6},
                                                on_release=lambda w:self.SND(w))

            except:
                BT=MDRaisedButton(text=textes[i], md_bg_color=(1, 1, 1, .3), rounded_button=8,size_hint=(.1, None),
                                                size=(1, Window.size[1] / 24), pos_hint={'center_y': .6},
                                  on_release=lambda w:self.IP(x=w,pm="2"))    #  ids={"perm": d["perm"][i], "schm": PER[i]},on_release=lambda w: self.SND(snd)
            g_new.add_widget(BT)
            BT.bind(on_release=lambda b: new_popup.dismiss())

        bt.ids["pht"] = []
        new_popup.open()

    def Add_item(self):
        global compt
        def clean(btn):
            grio.clear_widgets()
            compt = 0
            grio.add_widget(TF())
        def newIT(w,v=None):
            global compt
            """SEND TO SERVER"""
            if "old" in locals() :
                if w.text == old :
                    print("RETURNED")
                    return
            if w.text == "" :
                return
            if not w.text in self.Items .keys():
                compt+=1
                # self.Items[w.text]={}
                self.to_server[w.text] = {"idd":str(uuid.uuid4())[:5].replace("-","").replace(" ","").replace("_",""), "lcl": ""}
                grio.size = (grio.size[0]+Window.size[0]/1.1,1)
                grio.cols = compt + 1
                grio.add_widget(TF())
                my_spin.scroll_x=.8
                print(self.to_server)


            else:
                w.helper_text="Already exist !"
                # self.Items[w.text] = {}
                self.to_server[w.text] = {"idd": str(uuid.uuid4())[:5].replace("-","").replace(" ","").replace("_",""), "lcl": ""}
                grio.size = (grio.size[0] + Window.size[0] / 1.1, 1)
                grio.cols = compt + 1
                grio.add_widget(TF())
                my_spin.scroll_x = .8
            old = w.text

        def TF():
            BOIT=GridLayout(cols=3, spacing=5, size_hint=(None,None),size=(Window.width /1.5, Window.height / 18) , pos_hint={'center_x': .5, 'center_y': .07})

            item = MDTextField(hint_text_color_normal=(1, .6, .3, .4),text_color_normal= (1, 1, 1, .3),text_color_focus= (1, 1, 1, 1),line_color_normal=(1, 1, 1, .8),
                               icon_right_color_normal=(1, .6, 1, .8), hint_text="Talent or Item "+str(compt+1),
                               foreground_color=(1, 1, 1, 1), pos_hint={'center_x': .5, 'center_y': .5},
                               background_color=(1, 1, 1, .8), multiline=False, allow_copy=True, size_hint=(.98,1),helper_text_mode="on_error")
            # item.bind(on_text_validate=newIT)
            item.bind(focus=newIT)

            # item.focus = False
            # if compt > 0 :
            #     item.focus=True
            BOIT.add_widget(item)
            notext=str(uuid.uuid4())[:5].replace("-","").replace(" ","").replace("_","")

            phot = MDRaisedButton(text="...", md_bg_color=(.5, .6, 1, .25), rounded_button=20,ids={"data": self.Items,"pht":[],"x":10}, size_hint=(.1, None),
                                 size=(1, Window.size[1] / 24), pos_hint={'center_y': .6},
                                  on_release=lambda x: self.PHT(txt=self.to_server[item.text]["idd"] if item.text != "" else notext,msg=item.text))
            file=MDIconButton(text="+", icon="photos/f1.png",md_bg_color=(.5, .6, 1, .3),rounded_button=10,ids={"x":10},
                           size_hint=(None, None),size=(Window.size[1]/24,Window.size[1]/24),pos_hint={'center_y': .6},on_release=lambda btn: self.LoadAny(snd))



            BOIT.add_widget(phot)
            BOIT.add_widget(file)
            return BOIT

        compt=0
        self.to_server={}

        self.All=GridLayout(cols=2, spacing=5, size_hint=(.92,.11),  pos_hint={'center_x': .5, 'center_y': .05})
        with self.All.canvas.before:
            Color(0,0,0, randint(0,100)/100)
            self.rideau = Rectangle(pos=(0,0), size=(Window.width, (Window.height/100)*13) )

        my_spin = ScrollView(size_hint=(.8,1), pos_hint={'center_x': .5, 'center_y': .5},
                             do_scroll_x=True, do_scroll_y=False, scroll_type=['bars', 'content'], bar_width=1,bar_color=(1, 1, 0, 1), bar_margin=0)

        grio = GridLayout(cols=1, spacing=50, size_hint=(None, 1), size=(Window.size[0]/1.37, 1),
                          pos_hint={'center_x': .5, 'center_y': .5})

        grio.add_widget(TF() )

        grio.size=((Window.size[0]/1.3)*len(grio.children),1)
        grio.cols=compt+1

        snd=MDIconButton(text="+", icon="photos/s1.png",md_bg_color=(.5, .6, 1, .3),rounded_button=10,
                           ids={"data":self.Items,"pht":[]},size_hint=(None, None),size=(Window.size[1]/24,Window.size[1]/24),pos_hint={'center_y': .6},on_release=self.PERM)
        snd.bind(on_release=clean)
        my_spin.add_widget(grio)
        self.All.add_widget(my_spin )
        self.All.add_widget(snd)
        return self.All

    def SND(self,snd):
        print(snd.ids)
        """{"perm":d["perm"][i],"schm":PER[i],"data":bt.ids["data"]}"""
        if self.to_server.get(None,0):
            del self.to_server[None]
        if len(self.to_server) == 1 :
            ky=list(self.to_server.keys())[0]
            iD =  os.path.basename(self.to_server[ky]["lcl"])[:-4]
            if len(iD) <=2:
                iD=str(uuid.uuid4())[:8]

            bsn = {"schm":snd.ids["schm"]+"/"+iD,"action": "B_U","org":self.ME["Name"][0],"msg":ky,"zone":self.ME["adress"],"day": time.strftime("%d/%m/%y %H:%M:%S"),
                   'subject':self.ME["busy"] ,"BUSY":[[ky,self.to_server[ky]["lcl"]]],"pht":[self.to_server[ky]["lcl"]]+snd.ids["files"],"sidd":iD, "idd": self.ME["idd"]}


            #    THE SERVER WILL DO THIS TOO, WE CAN NOT SEND BIG DICT.  LET THE SERVER COMBINE WITH PREVIOUS
            try:
                ALL=json.load(dr()+"contacts/"+self.ME["idd"]+"/"+self.ME["idd"]+".json")
                ALL["BUSY"].append([bsn["msg"],self.to_server[ky]["lcl"]])
                ALL["msg"]=bsn["msg"]
                json.dump(bsn, open(dr() +"contacts/"+self.ME["idd"]+"/"+ iD+".json", "w"))
            except:
                if not os.path.isdir(dr()+"contacts/"+self.ME["idd"]):
                    os.mkdir(dr()+"contacts/"+self.ME["idd"])

                if not os.path.isdir(dr()+"contacts/"+self.ME["idd"]+"/chats/"):
                    os.mkdir(dr()+"contacts/"+self.ME["idd"]+"/chats/")

                if not os.path.isfile(dr()+"contacts/"+self.ME["idd"]+"/"+self.ME["idd"]+".json"):
                    json.dump(bsn, open(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json", "w"))

                ALL = json.load(open(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json","r"))
                ALL["BUSY"].append([bsn["msg"], bsn["pht"][0]])
                json.dump(ALL, open(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json", "w"))

            send(bsn)
            self.RECEIVER(json.dumps(bsn).encode())
            pickle.dump(bsn,open(dr()+bsn["schm"]+".bin","wb"))
            self.to_server={}
        elif len(self.to_server) > 1 :   #   IT WILL NOT REACH TO PEOPLE TO SAVE THEIR MB, BUT SENT TO SERVER WITH YOU MB, IF ANY LOOKS FOR YOU, OKAY, FIND YOU
            msg=[]
            pht=snd.ids["files"]
            for ky in self.to_server.keys():
                msg.append(ky)
                pht.append(self.to_server[ky]["lcl"])
                iD = os.path.basename(self.to_server[ky]["lcl"])[:-4]
                if len(iD) <= 2:
                    iD = str(uuid.uuid4())[:8]

                bsn = {"schm":snd.ids["schm"]+"/"+iD,"action": "B_U", "org": self.ME["Name"][0], "msg": ",".join(msg), "prfl": self.ME["idd"] + ".png",
                       'subject': self.ME["busy"], "BUSY": [], "pht": pht, "sidd":iD, "idd": self.ME["idd"],"day": time.strftime("%d/%m/%y %H:%M:%S")}

                #    THE SERVER WILL DO THIS TOO, WE CAN NOT SEND BIG DICT.  LET THE SERVER COMBINE WITH PREVIOUS
                try:
                    ALL = json.load(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json")
                    ALL["BUSY"].append([bsn["msg"], self.to_server[ky]["lcl"]])
                    All["msg"] = bsn["msg"]
                    json.dump(bsn, open(dr() + "contacts/" + self.ME["idd"] + "/" + iD + ".json", "w"))
                except:
                    if not os.path.isdir(dr() + "contacts/" + self.ME["idd"]):
                        os.mkdir(dr() + "contacts/" + self.ME["idd"])
                    if not os.path.isfile(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json"):
                        json.dump(bsn, open(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json", "w"))

                    ALL = json.load(open(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json", "r"))
                    ALL["BUSY"].append([bsn["msg"], bsn["pht"][0]])
                    json.dump(ALL, open(dr() + "contacts/" + self.ME["idd"] + "/" + self.ME["idd"] + ".json", "w"))
                self.RECEIVER(json.dumps(bsn).encode())
                pickle.dump(bsn, open(dr()+bsn["schm"] + ".bin", "wb"))
            send(ALL)

            self.to_server={}

    def LoadAny(self,btn_ids):

        def on_selected(ob, val):
            global choosen, result_ready,Im,List
            """
            REMOVE THIS IF CONDITION TO SUPPORT ALL FILES.
            
            IN READER ON RECEIVER:
            
            TRY READ AS VIDEO
            TRY READ AS PHOTO
            TRY READ AS AUDIO
            TRY READ AS PDF
            """
            if val[0].endswith(("pdf","PDF","png", "PNG", "jpg", "JPG", "jpeg", "JPEG","mp4","MP4","avi","AVI","mkv","MKV","3gp","3GP")):            #   , ".bmp", ".BMP", ".gif", ".GIF"
                btn_ids.ids["pht"].append(val[0] )
                print(btn_ids.ids)


        from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
        R, G, B, O = randint(10, 20) / 100, randint(5, 20) / 100, randint(5, 20) / 100, 1
        pg = GridLayout(cols=1, size_hint=(None,None),ids={"x":Window.size[0]/2},size=(Window.size[0]/1.5,Window.size[1]/2))
        with pg.canvas.before:
            Color(R,G,B,O)
            rect = RoundedRectangle(pos=(0, 0), radius=[10], size=(pg.size[0]+pg.size[0]/5,pg.size[1]))

        ll = [FileChooserListView(path=os.path.dirname(os.path.dirname(os.path.dirname(dr())))),
              FileChooserIconView(path=os.path.dirname(os.path.dirname(os.path.dirname(dr()))))]

        ch = ll[randint(1, 2) - 1]
        ch.dirselect = False
        ch.bind(selection=on_selected)

        pg.add_widget(ch)
        self.moveer(pg,pos=(100,200))

    def capture_image(self, instance):
        self.camera_preview.capture()

    def PHT(self,txt=None,msg=None,out=None):

        def SELF(w,t):
            try:
                # self.phot.bind(on_press=lambda c: paper.export_to_png(dr() + "Items/" + txt + ".png"))
                # self.phot.bind(on_press=lambda wd: self.CAPT(x=dr() + "Items/" + txt + ".png"))
                rl.remove_widget(self.phot)
                rl.remove_widget(self.BF)
                self.add_widget(self.phot)
                self.add_widget(self.BF)

                ##  once moved, they lost their bindinds
                # self.phot.bind(on_press=lambda c: paper.export_to_png(dr() + "Items/" + txt + ".png"))
                # self.phot.bind(on_press=lambda wd: self.CAPT(x=dr() + "Items/" + txt + ".png"))
            except:
                pass
        def ESC (W,v):
            # self.phot.bind(on_press=lambda c: paper.export_to_png(dr() + "Items/" + txt + ".png"))
            # self.phot.bind(on_press=lambda wd: self.CAPT(x=dr() + "Items/" + txt + ".png"))
            self.remove_widget(self.phot)
            self.remove_widget(self.BF)
            rl.remove_widget(self.phot)
            rl.remove_widget(self.BF)
            rl.add_widget(self.phot)
            rl.add_widget(self.BF)
            rl.pos= skat.pos
            rl.pos=skat.pos
            print(skat.pos)

            ##  once moved, they lost their bindinds
            # self.phot.bind(on_press=lambda c: paper.export_to_png(dr() + "Items/" + txt + ".png"))
            # self.phot.bind(on_press=lambda wd: self.CAPT(x=dr() + "Items/" + txt + ".png"))

        def front(bf):
            if platform != "android" :
                return
            if bf.text=="B" :
                self.camera.index=1
                bf.text="F"
            else:
                self.camera.index = 0
                bf.text = "B"
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.camera import Camera

        bx = BoxLayout(size_hint=(.5, .5), pos_hint={'center_x': self.HIDE, 'center_y': .5})
        skat = Scatter(size=(200, 200))
        skat.bind(on_touch_up=ESC)

        rl=RelativeLayout(size_hint=(.8,.8),pos_hint={'center_x':.5,'center_y': .5})
        paper=GridLayout(cols=1,size_hint=(.8,.8),pos_hint={'center_x':.5,'center_y': .5})


        self.camera = Camera(play=True, index=0,resolution=(640, 480))
        self.camera.allow_stretch = True
        # self.camera.bind(on_texture=self.flipping)

        paper.add_widget(self.camera)

        # rl.add_widget(paper)

        self.phot = MDRaisedButton(text="#", md_bg_color=(.5, .6, 1, .35), rounded_button=20, size_hint=(None, None),
                              size=(Window.size[1] / 20, Window.size[1] / 20), pos_hint={'center_x':.75,'center_y': .25})

        self.BF = MDRaisedButton(ids={"B":0,"F":1},text="B", md_bg_color=(.9, .6, 1, .35), rounded_button=20, size_hint=(None, None),
                              size=(Window.size[1] / 20, Window.size[1] / 20),pos_hint={'center_x': .25, 'center_y': .25},on_release=front)

        self.phot.bind(on_press= lambda c:paper.export_to_png(dr()+"Items/"+txt+".png"))
        paper.size = (Window.size[0] / 1.5, Window.size[1] / 1.5)
        self.phot.bind(on_press=lambda wd:self.CAPT(name=msg,x=dr()+"Items/"+txt+".png",widg=wd))
        # if out:
        #     self.phot.bind(on_press=lambda wd: self.phot.ids={"pht":dr() + "Items/" + txt + ".png"} )

        skat.size = paper.size
        paper.center=skat.center
        skat.add_widget(paper)
        rl.add_widget(skat)

        rl.add_widget(self.phot)
        rl.add_widget(self.BF)
        skat.bind(on_touch_down=SELF)
        # skat.bind(on_keyboard=ESC)
        self.call_slid(wid=rl)
        self.add_widget(rl)
        self.SLD.append([rl, self])

    def Loader(self,x=None,name=None,up=None):
        try:
            ftp = ftplib.FTP()
            ftp.connect(self.ip, 2121)
            ftp.login("aime shabani", self.PWD)
            retour = None
        except:
            retour=True
        if x:
            if os.path.exists( dr()+"Items/"+os.path.basename(x)):   #  Path
                self.CAPT(x=dr()+"Items/"+os.path.basename(x),name=name,p="1")
            elif os.path.isfile(x):
                self.CAPT(x=x, name=name, p="1")
            else:
                Path = x[x.index("/ACCOUNTS") + 1:]
                self.CAPT(x=x, name=name, p="1")
                if retour :
                    return
                ftp.cwd(os.path.dirname(Path))

                fl = open(dr()+"Items/"+os.path.basename(Path), "wb")
                ftp.retrbinary("RETR " + os.path.basename(Path), fl.write)
                fl.close()
                del ftp
                del fl
                del Path
        if up:
            if retour:
                return
            ftp.cwd("ACCOUNTS/"+self.ME["idd"]+"/" )
            bin = open(up, "rb")
            ftp.storbinary("STOR " + self.ME["idd"] + ".png", bin)

            im='ftp://aime shabani:'+self.PWD+'@'+self.ip+":"+"2121"+'/'+ "ACCOUNTS/"+self.ME["idd"]+"/"+self.ME["idd"] + ".png"
            self.CAPT(x=im, name=name, p="1")
            del bin
            del ftp
            del im

    def CAPT(self,x,name=None,p=None,widg=None):
        print("x: ", x, "name: ",name)
        if widg :
            widg.ids={"pht":x}
        if "hist" in locals():
            if hist == x :
                print("Returned")
                return
        from kivy.uix.image import Image
        if p:
            bx=BoxLayout(size_hint=(None,None),size=(Window.size[0]/1.2,Window.size[1]/1.2),pos_hint={'center_x':self.HIDE,'center_y': .5})
            skat = Scatter(size=(200,200))  #scale=max(self.parent.width / self.width, self.parent.height / self.height),size_hint=(1., 1.),pos_hint={'center_x':self.HIDE,'center_y': .5},
                                #do_rotation=True, do_translation=True, do_scale=True
                                                                                                 #
            c_i= AsyncImage(source=x,size_hint=(None,None),size=(Window.size[0]/1.2,Window.size[1]/1.2),pos_hint={'center_x':.5,'center_y': .5} ,allow_stretch=True, nocache=False,keep_ratio=True)

            bx.center= skat.center       #  Good idea    BORDERS ARE RESPECTED
            skat.add_widget(c_i)

            self.call_slid(wid=bx)
            skat.size=c_i.size       #  Good idea    BORDERS ARE RESPECTED
            bx.add_widget(skat)
            self.add_widget(bx)
            self.SLD.append([bx, self])
            # self.c_i.reload()
        else:
            pst=x
            Clock.schedule_once(lambda z:self.CAPT(x=pst,p=1),1)

        hist=x
        self.to_server[name]={"idd":os.path.basename(x)[:-4],"lcl":x}  #  this deletes photo from server if web is empty,  the server will provid web key as link
        if not self.Items.get(name,0) :
            self.Items[name] ={}
        self.Items[name]["lcl"]= x            #= {"web": "", "lcl": x}

        # self.Items.update({name:{"web":"","lcl":x}})
        # if not self.Items.get(name,0):

    def _search_client(self, w, t=None):
        print("Searching....")
        if len(w.text) < 2:
            w.text = ""
            w.hint_text = "2 digits above please"
            return

        if "f" in locals():
            if w.text == f:
                print('returned')
                return

        self.SCV = ScrollView(size_hint=(.97, .8), pos_hint={'center_x': .5, 'center_y': .45},
                              do_scroll_x=False,do_scroll_y=True, scroll_type=['bars', 'content'], bar_width=10,
                              bar_color=(1, 1, 0, 1), bar_margin=0)

        self.GG = GridLayout(cols=2, spacing=12,size_hint=(1, None), size=(1, Window.size[1] / 12),
                             pos_hint={'center_x': .5, 'center_y': .57})

        try:
            self.SSR.clear_widgets()
        except:
            pass

        try:
            self.SSR.add_widget(self.btn)
            self.SSR.add_widget(self.seach)
        except:
            pass
        self.SCV.add_widget(self.GG)
        # GTC.add_widget(self.SCV)
        self.SSR.add_widget(self.SCV)

        # threading.Thread(target=self.dinamo).start()
        f = w.text
        d = {"action": "LK", "kw": w.text, "ad":self.ME["adress"],"idd": self.ME["idd"],"sidd":str(uuid.uuid4()).replace("-","").replace("_","")[:4],"recipients": [self.ME["idd"]],"schm":"."}
        send(d)

    def sf(self,btn):
        if "Activities" in btn.ids["dt"]["schm"]:
            if not os.path.exists(dr() + btn.ids["dt"]["schm"].replace(".bin", "").replace(".json", "")):
                os.makedirs(dr() + btn.ids["dt"]["schm"].replace(".bin", "").replace(".json", ""))
            pickle.dump(btn.ids["dt"], open(dr() + btn.ids["dt"]["schm"] + ".bin", "wb"))

        else:
            if not os.path.exists(dr() + "Activities/" + btn.ids["dt"]["schm"].replace(".bin", "").replace(".json", "")):
                os.makedirs(dr() + "Activities/" + btn.ids["dt"]["schm"].replace(".bin", "").replace(".json", ""))
            pickle.dump(btn.ids["dt"], open(dr() + "Activities/" + btn.ids["dt"]["schm"] + ".bin", "wb"))

        Clock.schedule_once(lambda x:self.MSG(btn))

    def _layers(self, s):
        print("Found...")
        "CHANGE HERE TO FETCH ONLY IDD AND NAMES FROM SERVER,  NOT ALL DATAS   "
        R, G, B, O = randint(0, 100) / 100, randint(30, 100) / 100, randint(30, 100) / 100, 1

        # web = 'ftp://' + srv + ':' + pwd + '@' + IP + ":" + str(port) + '/' + FTP + s["acc"] + ".png"
        rl = RelativeLayout(size_hint=(None, None), size=(Window.size[1] / 8, Window.size[1] / 8))

        rl.add_widget(AsyncImage(source=self.profile(s["idd"]), size_hint=(1, 1),
                                 pos_hint={"center_x": .5, "center_y": .5}))  # IMAGE  ,   NAME   , TRANSPARENT BUTTON

        rl.add_widget(MDRaisedButton(text=s["org"],text_color=(1,1,1,1),md_bg_color=(0,0,0,1), rounded_button=10,size_hint=(.25,.1),
                                     pos_hint={"center_x": .5, "center_y": .2}))

        rl.add_widget(Button(background_color=(0, 0, 0, 0),ids={"schm":s['schm'].replace(".bin",""),"idd":s["idd"],"dt":s,"COLOR":[R,G,B,O]}, size_hint=(1, .77),
                             pos_hint={"center_x": .5, "center_y": .5},on_press=lambda x: send({"action":"contact","idd":s["idd"],"sidd":str(uuid.uuid4())[:4]}),on_release=self.sf))

        self.GG.add_widget(rl)
        if len(self.GG.children) % self.GG.cols == 0:
            self.GG.size[1] += Window.size[1] / 12

    def resiz(self, w, t=None):

        self.seach.unbind(focus=self.resiz)
        if "xx" in dir(self):
            if self.xx >= (Window.size[1]/100)*78:
                # self.SSR.pos_hint = {'center_x': .67, 'center_y': .5}
                self.btn.background_color = (1, 1, 1, .75)
                Clock.schedule_interval(self.smal, 0)
            else:
                self.skat.pos = (Window.size[0] / 2.5, Window.size[1]/5)
                self.xx =(Window.size[1]/100)*9
                # self.SSR.pos_hint = {'center_x': .67, 'center_y': .5}
                self.btn.background_color = (1, 1, 1, .75)
                Clock.schedule_interval(self.big, 0)
        else:
            self.xx = (Window.size[1]/100)*9

            self.skat.pos = (Window.size[0] / 2.5, Window.size[1] / 5)
            # self.SSR.pos_hint = {'center_x': .67, 'center_y': .5}
            self.btn.background_color = (1, 1, 1, .75)
            Clock.schedule_interval(self.big, 0)

    def big(self, x):                          #Window.size[0]/2,(Window.size[1]/100)*9

        if self.xx >= (Window.size[1]/100)*80:
            Clock.unschedule(self.big)
            self.seach.pos_hint = {'center_x': .5, 'center_y': .95}
            try:
                self.skat.size=self.SSR.size
            except:
                pass
            # print(self.xx)
        else:
            self.SSR.size = (Window.size[0]/2, self.xx)
            self.xx += Window.size[1]/100

    def _big(self, x):

        if self.xx >= 0.87:
            Clock.unschedule(self.big)
            self.seach.pos_hint = {'center_x': .5, 'center_y': .95}
            # print(self.xx)
        else:
            self.SSR.size_hint = (.5, self.xx)
            self.xx += 0.08

    def smal(self, x):
        # print(self.xx)
        if self.xx <= (Window.size[1]/100)*9 :
            Clock.unschedule(self.smal)
            self.SSR.pos_hint={'center_x': .67, 'center_y': .88}
            self.seach.pos_hint={'center_x': .5, 'center_y': .5}
            self.btn.bind(on_release=self.resiz)
            try:
                self.skat.size=self.SSR.size
                self.skat.pos = (Window.size[0] / 2.5, Window.size[1] - (Window.size[1] / 10))
            except:
                pass
            # print(self.xx)
        else:
            self.SSR.size = (Window.size[0]/2, self.xx)
            self.xx -= Window.size[1]/100

    def _smal(self, x):
        # print(self.xx)
        if self.xx <= 0.05:
            Clock.unschedule(self.smal)
            self.SSR.pos_hint={'center_x': .67, 'center_y': .88}
            self.seach.pos_hint={'center_x': .5, 'center_y': .5}
            self.btn.bind(on_release=self.resiz)

        else:
            self.SSR.size_hint = (.5, self.xx)
            self.xx -= 0.08


class Help(MDApp):
    # Window.borderless="1"
    if platform != "android" :
        Window.size=(500,720)
    def build(self):

        sm = ScreenManager(transition=FadeTransition())
        # sm.add_widget(BS(name="business"))
        sm.add_widget(RM(name="reminder"))
        return sm

    def on_stop(self):
        # from plyer import gps
        # Environment = autoclass('android.os.Environment')
        # storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
        # file_path = os.path.join(storage_path, "data/test")  # Adjust the path as needed
        # def locator(**kwargs):
        #     open(file_path, "a").write('stop  lat: {lat}, lon: {lon}'.format(**kwargs))
        #
        # if platform == "android":
        #     gps.configure(on_location=locator)
        #     gps.start()
        #     return True
        # else:
        #     return True
        return True

    def on_pause(self):
        # from plyer import gps
        #
        # Environment = autoclass('android.os.Environment')
        # storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()
        # file_path = os.path.join(storage_path, "data/test")  # Adjust the path as needed
        # def locator(**kwargs):
        #     open(file_path,"a").write('pause  lat: {lat}, lon: {lon}'.format(**kwargs))
        #     notf.notify(title='GPS', message='lat: {lat}, lon: {lon}'.format(**kwargs) )
        #
        # if platform == "android":
        #     gps.configure(on_location=locator)
        #     gps.start()
        #     return True
        # else:
        return True
        # return False

    def on_close(self):
        # return False
        return True

if __name__ == '__main__':
    print('1')
    Help().run()
