from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screenmanaging.login_screen import LoginScreen
from screenmanaging.register_screen import RegisterScreen
from screenmanaging.task_screen import TaskScreen

# from api.client import register_user, login_user, get_tasks, create_task, edit_task, update_task, delete_task_api

Window.size = (360, 640) # Mobile size preview

# ==========================
# APP
# ==========================
class MyApp(MDApp):
    
    def build(self):
        self.token = None

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()

        sm.add_widget(LoginScreen(name = "login"))
        sm.add_widget(RegisterScreen(name = "register"))
        sm.add_widget(TaskScreen(name = "tasks"))
 
        return sm

# RUN APP
if __name__ == "__main__":
    MyApp().run()
    



