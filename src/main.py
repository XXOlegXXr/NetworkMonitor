import sys
import os
sys.path.append(os.path.dirname(__file__))
from controller.main_controller import MainController
from view.main_view import MainView

def main():
    print("Запуск Network Monitor")
    app_view = MainView()
    app = MainController(app_view)
    app.setup_system()
    app.scan_and_save("google.com")
    app.scan_and_save("8.8.8.8")
    app_view.mainloop()

if __name__ == "__main__":
    main()