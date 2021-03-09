import datetime
import json
import smtplib

import requests

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.spinner import MDSpinner

Window.size = (385, 580)

headers = {"Content-Type": "application/json"}


class HomeScreen(Screen):
    def build(self):
        self.theme_cls.primary_palette = "Green"

    def add_service_request(self):
        # self.theme_cls.primary_palette = "Green"
        print('add service request')


class AddServiceScreen(Screen):
    dialog = None

    # with self.root.canvas:
    #     Color(rgba=(.5, .5, .5))
    # return self.root

    def create_service(self):
        services = ["Laundry", "Dry Cleaning", "Ironing"]
        menu_items = [{"text": str(i)} for i in services]
        self.menu = MDDropdownMenu(
            caller=self.ids['client_services'],
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()
        self.menu.bind(on_release=self.set_item)

    def set_item(self, instance_menu, instance_menu_item):
        print('inside menu callback')
        # self.ids['client_services'].hint_text = ''
        self.ids['client_services'].text = instance_menu_item.text
        instance_menu.dismiss()

    def select_date(self):
        print('inside select date')
        # date_dialog = MDDatePicker(
        #     callback=self.on_save,
        #     min_date=datetime.date(2021, 2, 1),
        #     max_date=datetime.date(2022, 12, 31),
        # )
        # To make the MDDatePicker work and the MDDropDown work install the
        #  pip3 install https://github.com/kivymd/KivyMD/archive/master.zip

        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.ids['client_date'].text = str(value)

    def on_cancel(self, instance, value):
        instance.dismiss()

    def set_slot_item(self, instance_menu, instance_menu_item):
        self.ids['client_slot'].text = instance_menu_item.text
        instance_menu.dismiss()

    def available_slots(self):
        print('available slots are')
        time_slots = ["9 AM - 10 AM", "10:30 - 11:30", "12 PM - 2 PM", " 3 PM - 5 PM"]
        menu_items = [{"text": str(i)} for i in time_slots]
        self.menu = MDDropdownMenu(
            caller=self.ids['client_slot'],
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()
        self.menu.bind(on_release=self.set_slot_item)

    def select_time(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.set_time)
        time_dialog.open()

    def set_time(self, instance, time):
        self.ids['client_time'].text = str(time)
        return time

    def add_service(self):
        print('add service')
        client_name = self.ids['client_name'].text
        client_phone = self.ids['client_phone'].text
        service_type = self.ids['client_services'].text
        service_dt = self.ids['client_date'].text
        service_time = self.ids['client_slot'].text
        desc = self.ids['client_desc'].text
        print(client_name, client_phone, service_type, service_dt, service_time, desc)

        try:

            receiver_email_id = "alfservices9@gmail.com"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("alfservices9@gmail.com", "Arun@alf")
            # print(data)
            data = "Client Name : " + client_name + "\n" + "Client Phone: " + client_phone + "\n"
            data = data + "Service Type: " + service_type + "\n" + "Client Address: " + desc + "\n"
            data = data + "Service Date: " + service_dt + "\n" + "Service Time: " + service_time
            print(data)
            message = 'Subject: {}\n\n{}'.format("New Service Request", data)
            print('preparing to send email')
            s.sendmail("alfservices9@gmail.com", receiver_email_id, message)
            s.quit()
            print('Mail Sent.................')

            self.clear_data()
            self.show_dialog()
        except:
            print('error connecting email')

    def spin(self):
        btn = self.ids['submit']
        btn.add_widget(
            MDSpinner(
                active=True,
                pos_hint="'center_x': .5, 'center_y': .5",
            )
        )

    def show_dialog(self):

        self.dialog = MDDialog(
            title="Success!",
            text="Service request placed Successfully!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    on_release=self.close_dialog,
                ),
            ],
        )
        self.dialog.open()

        # If registration successful return to login screen
        self.manager.current = 'login_screen'

    def close_dialog(self, inst):
        self.dialog.dismiss()

    def clear_data(self):
        self.ids['client_name'].text = ""
        self.ids['client_phone'].text = ""
        self.ids['client_services'].text = "Select Service Type *"
        self.ids['client_desc'].text = ""

    def show_datetime_picker(self):
        # min_date = datetime.strptime("2020:02:15", '%Y:%m:%d').date()
        # max_date = datetime.strptime("2020:05:30", '%Y:%m:%d').date()

        date_dialog = MDDatePicker(
            callback=self.got_date,
            min_date=datetime.date(2020, 2, 15),
            max_date=datetime.date(2022, 3, 27),
        )
        # date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        print(instance, time)
        self.ids['service_time'].text = str(time)
        return time

    def got_date(self, the_date):
        print(the_date)
        self.ids['service_dt'].text = str(the_date)

    def go_home(self):
        self.manager.current = 'home_screen'


class MainApp(MDApp):

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
        print('current screen is set to : ', screen_manager.current)
    # def build(self):
    #     return Builder.load_string(KV)


if __name__ == '__main__':
    app = MainApp()
    app.run()
