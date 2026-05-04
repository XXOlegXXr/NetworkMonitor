from model.database import DatabaseModel
from model.network import NetworkModel

class MainController:
    def __intt__(self):
        self.db=DatabaseModel()
        self.network=NetworkModel()

    def setup_system(self):
        print("Налаштування бази даних...")
        self.db.init_db()

    def scan_and_save (self, target):
        print(f"Сканую: {target}...")
        is_alive, response_time = self.network.check_ping(target)
        status="Online" if is_alive else "offline"
        time_to_save = response_time if response_time is not None else 0.0
        self.db.save_log(target, status, time_to_save)