from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDTextButton, MDFlatButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen

from api.client import register_user

# =========================
# REGISTER SCREEN
# =========================
class RegisterScreen(Screen):

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
            text = "Create Account",
            theme_text_color = "Custom",
            text_color = (0, 0 , 1, 1),
            font_size = "36sp",
            bold = True,
            halign = "center",
            size_hint_y = None,
            height = 60
        )

        self.username = MDTextField(
            hint_text = "Username",
            mode = "rectangle",
            size_hint = (1.5, None),
            height = 50,
            pos_hint = {"center_x": 0.5}
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

        register_button = MDRaisedButton(
            text = "Register",
            size_hint = (1.5, None),
            size = (200, 50),
            pos_hint = {"center_x": 0.5}
        )

        login_button = MDTextButton(
            text = "Already have an account",
        )
        register_button.bind(on_press = self.register)

        login_button.bind(
            on_release = lambda x: setattr(self.manager, "current", "login")
        )

        layout.add_widget(title)
        layout.add_widget(self.username)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(register_button)
        layout.add_widget(login_button)
        
        root.add_widget(layout)
        self.add_widget(root)

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