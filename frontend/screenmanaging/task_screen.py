from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog

from api.client import  get_tasks, create_task, edit_task, update_task, delete_task_api

# =========================
# TASK SCREEN
# =========================
class TaskScreen(Screen):

    def on_enter(self):
        self.load_task()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         
        layout = BoxLayout(
            orientation = "vertical",
            spacing = 20,
            padding = [40, 80, 40, 80],
        )

        # title input
        self.title_input = MDTextField(
            hint_text = "Title",
            mode = "rectangle",
            size_hint = (1, None),
            height = 50,
            pos_hint = {"center_x": 0.5}
        )

        # search input
        self.search_input = MDTextField(
            hint_text = "Search",
            mode = "rectangle",
            size_hint = (1, None),
            height = 50,
            pos_hint = {"center_x": 0.5}
        )
        self.search_input.bind(text = self.search_tasks)

        # button
        add_button = MDRaisedButton(
            text = "Add Task",
            size_hint = (None, None),
            size = (90, 50)
        )

        logout_button = Button(
            text = "Logout",
            size_hint = (1, None)
        )

        # task container
        self.task_box = BoxLayout(
            orientation = "vertical",
            size_hint_y = None,
            spacing = 10
        )
        self.task_box.bind(minimum_height=self.task_box.setter('height'))

        scroll = ScrollView(size_hint = (1, 1))
        scroll.add_widget(self.task_box)

        # top section
        top_box = BoxLayout(
            orientation = "horizontal",
            size_hint = (1, None),
            height = 70,
            spacing = 10,
            padding = 10
        )

        top_box.add_widget(self.title_input)
        top_box.add_widget(add_button)

        logout_button.bind(on_press = lambda x: self.logout())
        
        # layout order
        layout.add_widget(self.search_input)
        layout.add_widget(scroll)
        layout.add_widget(top_box)
        layout.add_widget(logout_button)

        add_button.bind(on_press=self.add_task)

        self.add_widget(layout)

    # LOADD TASKS
    def load_task(self):
        token = MDApp.get_running_app().token
        
        if not token:
            self.manager.current = "login"
            return
        
        response = get_tasks(token)
        
        if response.status_code != 200:
            self.manager.current = "login"
            return
        
        tasks = response.json()
        self.tasks = tasks

        self.task_box.clear_widgets()

        for task in tasks:
            self.add_task_ui(task)

    # SEARCH TASKS
    def search_tasks(self, instance, value):
        query = value.lower().strip()

        self.task_box.clear_widgets()

        for task in self.tasks:
            if query in task["title"].lower():
                self.add_task_ui(task)
            
    # ADD TASKS
    def add_task(self, instance):

        title = self.title_input.text
        if not title:
            return

        token = MDApp.get_running_app().token
            
        response = create_task(token, title,)

        if response.status_code == 200:
            self.title_input.text = ""
            self.load_task()
    
    # TASK UI
    def add_task_ui(self, task):
        
        task_id = task["id"]
        title = task["title"]
        status = task.get("status", "pending")

        task_layout = BoxLayout(
            orientation = "horizontal",
            size_hint_y = None,
            height = 50,
            spacing = 10,
        )

        task_label = MDLabel(
            text = title, 
            theme_text_color = "Custom",
            text_color = (0, 0 , 0, 1),
            size_hint = (0.7, 1),
            halign = "left",
            valign = "middle"
        )

        checkbox = CheckBox(
            active =(status == "done"),
            size_hint = (None, None),
            size = (40, 40)
        )

        edit_button = MDIconButton(
           icon = "pencil",
           pos_hint = {"center_y": 0.5}
        )

        delete_button = MDIconButton(
            icon = "delete",
            pos_hint = {"center_y": 0.5}
        )

        card = MDCard(
            orientation = "vertical",
            size_hint_y = None,
            height = 70,
            radius = [15],
            spacing = 10,
            padding = 10
        )
               
        task_layout.add_widget(checkbox)
        task_layout.add_widget(task_label)
        task_layout.add_widget(edit_button)
        task_layout.add_widget(delete_button)
        

        card.add_widget(task_layout)

        # self.task_box.add_widget(task_layout)
        self.task_box.add_widget(card)

        checkbox.bind(
            active = lambda x, value: self.update_task_status(task_id, task_label, value)
        )

        edit_button.bind(
            on_press = lambda x: self.show_edit_dialog(task_id, title)
        )

        delete_button.bind(
            on_press = lambda x: self.show_delete_dialog(task_id)
        )

    def show_edit_dialog(self, task_id, current_title):

        self.edit_field = MDTextField(
            text = current_title,
            hint_text = "Task Title"
        )

        self.dialog = MDDialog(
            text = "Edit Task",
            type = "custom",
            content_cls = self.edit_field,
            buttons = [
                MDFlatButton(
                    text = "Cancel",
                    on_release = lambda x: self.dialod.dismiss()
                ),
                MDFlatButton(
                    text = "Save",
                    on_release = lambda x: self.save_task(task_id)
                )
            ]
        )
        self.dialog.open()
    
    def save_task(self, task_id):
        title = self.edit_field.text.strip()

        if not title:
            return
        
        token = MDApp.get_running_app().token

        response = edit_task(token, task_id, title)

        if response.status_code == 200:
            self.dialog.dismiss()
            self.load_task()

    # DELETE TASK
    def show_delete_dialog(self, task_id):

        self.delete_dialog = MDDialog(
            title = "Delete Task",
            text = "Are you sure you want to delete this task?",
            buttons = [
                MDFlatButton(
                    text = "Cancel",
                    on_release = lambda x: self. delete_dialog.dismiss()
                ),
                MDFlatButton(
                    text = "Delete",
                    on_release = lambda x: self. confirm_delete(task_id)
                )
            ]
        )
        self. delete_dialog.open()

    def confirm_delete(self, task_id):
        self.delete_dialog.dismiss()

        token = MDApp.get_running_app().token

        response = delete_task_api(token,task_id)

        if response.status_code == 200:
            self.load_task()

    def delete_task(self, task_id):
       self.show_delete_dialog(task_id)

    # UPDATE STATUS
    def update_task_status(self, task_id, task_label, value):

        token = MDApp.get_running_app().token
        
        status = "completed" if value else "pending"

        response = update_task(token, task_id, status)
        
        if response.status_code == 200:
            
            if value:
                task_label.text = "[Done] " + task_label.text.replace("[Done] ", "")

            else:
                task_label.text = task_label.text.replace("[Done] ", "")
    
    # LOGOUT
    def logout(self):
        MDApp.get_running_app().token = None
        self.manager.current = "login"