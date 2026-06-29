from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDTextButton, MDFlatButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from api.client import login_user

# =========================
# LOGIN SCREEN
# =========================
class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = AnchorLayout(
            anchor_x = "center",
            anchor_y = "center"
        )

        layout = BoxLayout(
            orientation = "vertical",
            spacing = 20,
            padding = [40, 80, 40, 80],
            size_hint= (None, None),
            width = 400,
            height = 350
        )

        title = MDLabel(
            text = "LOGIN",
            theme_text_color = "Custom",
            text_color = (0, 0 , 1, 1),
            font_size = "36sp",
            bold = True,
            halign = "center",
            size_hint_y = None,
            height = 60
        )

        self.email = MDTextField(
            hint_text = "Email",
            mode = "rectangle",
            size_hint = (1.5, None),
            height = 50,
            pos_hint = {"center_x": 0.5}
        )

        self.password = MDTextField(
            hint_text = "Password",
            password = True,
            mode = "rectangle",
            size_hint = (1.5, None),
            height = 50,
            pos_hint = {"center_x": 0.5}
        )

        login_button = MDRaisedButton(
            text = "Login",
            size_hint = (1.5, None),
            size = (200, 50),
            pos_hint = {"center_x": 0.5}
        )

        register_button = MDTextButton(
            text = "Create new account",
        )

        login_button.bind(on_press = self.login)

        register_button.bind(
            on_release = lambda x: setattr(self.manager, "current", "register")
        )
         
        layout.add_widget(title)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        
        root.add_widget(layout)
        self.add_widget(root)

    def login(self, instance):

        response = login_user(
                self.email.text,
                self.password.text 
        )

        if response.status_code == 200:

            self.email.text = ""
            self.password.text = ""

            token = response.json().get("access_token")
            MDApp.get_running_app().token = token

            self.manager.current = "tasks"
        else:
            print("Login failed", response.text)