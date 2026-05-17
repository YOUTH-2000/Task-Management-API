import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen


class MyApp(App):
    
    def build(self):
        
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(TaskScreen(name="tasks"))

        return sm
    
class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation = "vertical",
            spacing = 10,
            padding = 20
        )

        self.email = TextInput(
            hint_text="Email",
            size_hint = (1, None),
            height = 50
        )

        self.password = TextInput(
            hint_text="Password",
            password=True,
            size_hint = (1, None),
            height = 50
        )

        button = Button(
            text = "Login",
            size_hint = (1, None),
            height = 50      
        )
        button.bind(on_press = self.login_user)

        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(button)

        self.add_widget(layout)

    def login_user(self, instance):
        response = requests.post(
            "http://127.0.0.1:8000/auth/login",
            json = {
                "email" : self.email.text,
                "password" : self.password.text
            }  
        )

        token = response.json().get("access_token")

        if token:
            App.get_running_app().token = token
            self.manager.current = "tasks"

class TaskScreen(Screen):

    def on_enter(self):
        self.load_task()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         
        layout = BoxLayout(
                orientation="vertical",
                spacing = 10,
                padding = 20
            )

        # title input
        self.title_input = TextInput(
            hint_text = "Title",
            size_hint = (0.8, None),
            height = 50
        )

        # Description input
        # self.description_input = TextInput(
        #     hint_text = "Description",
        #     size_hint = (0.8, None),
        #     height = 50
        # )

        # button
        self.button = Button(
            text="Add Task",
            size_hint = (0.2, None),
            height = 50
        )

        # task container
        self.task_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
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
        # top_box.add_widget(self.description_input)
        top_box.add_widget(self.button)
        
        # layout order
        layout.add_widget(scroll)
        layout.add_widget(top_box)

        self.button.bind(on_press=self.change_text)

        self.add_widget(layout)

    def load_task(self):
        token = App.get_running_app().token

        headers = {
            "Authorization" : f"Bearer {token}"
        }
        
        response =requests.get(
            "http://127.0.0.1:8000/tasks",
            headers=headers
        )

        tasks = response.json()

        self.task_box.clear_widgets()

        for task in tasks:
            self.add_task_ui(task)

    def change_text(self, instance):
        task = self.title_input.text
      
        if not task:
            return

        token = App.get_running_app().token

        headers = {"Authorization" : f"Bearer {token}"}
            
        response =requests.post(
            "http://127.0.0.1:8000/tasks",
            json={
                "title": task,
                "description": "",
                "status": "pending",
                "priority": "low"
            },
            headers=headers
        )
        print(response.json())

        if response.status_code == 200:
            self.title_input.text = ""
            # self.description_input.text = ""
            self.load_task()
    
    def add_task_ui(self, task):
        
        task_id = task["id"]
        title = task["title"]
        # description = task["description"]
        status = task.get("status", "pending")

        task_layout = BoxLayout(
            orientation = "horizontal",
            size_hint_y = None,
            height = 50,
            spacing = 10,
            padding = 5
        )

        task_label = Label(text = title)

        checkbox = CheckBox(
            active =(status == "done"),
            size_hint = (0.15, 1)
        )

        delete_button = Button(
            text = "Delete",
            size_hint = (0.25, 1)
        )
               
        task_layout.add_widget(checkbox)
        task_layout.add_widget(task_label)
        task_layout.add_widget(delete_button)

        self.task_box.add_widget(task_layout)

        delete_button.bind(
            on_press = lambda x: self.delete_task(task_layout)
        )
        checkbox.bind(
            active = lambda x, value: self.update_task_status(task_id, task_label, value)
        )

    def delete_task(self, task_layout):
        self.task_box.remove_widget(task_layout)

    def update_task_status(self, task_id, task_label, value):

        token = App.get_running_app().token

        headers = {"Authorization" : f"Bearer {token}"}
        
        status = "done" if value else "pending"

        response =requests.put(
            f"http://127.0.0.1:8000/tasks/{task_id}",
            json = {"status" : status},
            headers=headers
        )
        
        if response.status_code == 200:
            if value:
                task_label.text = "[Done] " + task_label.text.replace("[Done] ", "")

            else:
                task_label.text = task_label.text.replace("[Done] ", "")
    

if __name__ == "__main__":
    MyApp().run()
    



