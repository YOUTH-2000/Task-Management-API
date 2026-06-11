from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen

from api.client import register_user, login_user, get_tasks, create_task, update_task, delete_task_api

# =========================
# APP
# =========================
class MyApp(App):
    
    def build(self):
        self.token = None

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(TaskScreen(name="tasks"))
 
        return sm

# =========================
# LOGIN SCREEN
# =========================
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

        register_button = Button(
            text = "Create Account",
            size_hint = (1,None),
            height = 50
        )

        login_button = Button(
            text = "Login",
            size_hint = (1, None),
            height = 50      
        )

        register_button.bind(
            on_press = lambda x: setattr(self.manager, "current", "register")
        )

        login_button.bind(on_press = self.login)

        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(register_button)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def login(self, instance):

        response = login_user(
                self.email.text,
                self.password.text 
        )

        if response.status_code ==200:

            self.email.text =""
            self.password.text =""

            token = response.json().get("access_token")
            App.get_running_app().token = token

            self.manager.current = "tasks"
        else:
            print("Login failed", response.text)

# =========================
# REGISTER SCREEN
# =========================
class RegisterScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation = "vertical",
            spacing = 10,
            padding = 20
        )

        self.username = TextInput(
            hint_text = "Username",
            size_hint = (1,None),
            height = 50
        )

        self.email = TextInput(
            hint_text = "Email",
            size_hint = (1,None),
            height = 50
        )

        self.password = TextInput(
            hint_text = "Password",
            size_hint = (1,None),
            height = 50
        )

        register_button = Button(
            text = "Register",
            size_hint = (1,None),
            height = 50
        )

        login_button = Button(
            text = "Back to Login",
            size_hint = (1,None),
            height = 50
        )
        register_button.bind(on_press = self.register)

        login_button.bind(
            on_press = lambda x: setattr(self.manager, "current", "login")
        )

        layout.add_widget(self.username)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(register_button)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def register(self, instance):

        response = register_user(
            self.username.text,
            self.email.text,
            self.password.text
        )

        if response.status_code == 200:
            self.username.text = ""
            self.email.text = ""
            self.password.text = ""
            self.manager.current = "login"

        else:
            print("Register failed", response.text)

# =========================
# TASK SCREEN
# =========================
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

        # button
        add_button = Button(
            text="Add Task",
            size_hint = (0.2, None),
            height = 50
        )

        logout_button = Button(text = "Logout")

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
        top_box.add_widget(add_button)
        
        # Logout button
        logout_button.bind(on_press = lambda x: self.logout())
        top_box.add_widget(logout_button)

        # layout order
        layout.add_widget(scroll)
        layout.add_widget(top_box)

        add_button.bind(on_press=self.add_task)

        self.add_widget(layout)

    # LOADD TASKS
    def load_task(self):
        token = App.get_running_app().token
        
        if not token:
            self.manager.current = "login"
            return
        
        response =get_tasks(token)
        
        if response.status_code != 200:
            self.manager.current = "login"
            return
        
        tasks = response.json()

        self.task_box.clear_widgets()

        for task in tasks:
            self.add_task_ui(task)

    # ADDD TASKS
    def add_task(self, instance):

        title = self.title_input.text
        if not title:
            return

        token = App.get_running_app().token
            
        response = create_task(token, title)

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
            padding = 5
        )

        task_label = Label(
            text = title, 
            size_hint = (0.6, 1)
        )

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
            on_press = lambda x: self.delete_task(task_id)
        )
        checkbox.bind(
            active = lambda x, value: self.update_task_status(task_id, task_label, value)
        )

    # DELETE TASK
    def delete_task(self, task_id):
        token = App.get_running_app().token

        response = delete_task_api(token,task_id)

        if response.status_code == 200:
            self.load_task()

    # UPDATE STATUS
    def update_task_status(self, task_id, task_label, value):

        token = App.get_running_app().token
        
        status = "done" if value else "pending"

        response = update_task(token, task_id, status)
        
        if response.status_code == 200:
            
            if value:
                task_label.text = "[Done] " + task_label.text.replace("[Done] ", "")

            else:
                task_label.text = task_label.text.replace("[Done] ", "")
    
    # LOGOUT
    def logout(self):
        App.get_running_app().token = None
        self.manager.current = "login"

# RUN APP
if __name__ == "__main__":
    MyApp().run()
    



