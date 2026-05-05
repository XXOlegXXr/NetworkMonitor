from model.database import DatabaseModel
from model.network import NetworkModel
import csv
from tkinter import filedialog, messagebox
import tkinter as tk 
from tkinter import ttk
class MainController:
    def __init__(self, view):
        self.view=view
        self.db=DatabaseModel()
        self.network=NetworkModel()
        self.load_history()
        self.view.scan_btn.config(command=self.handle_button_click)
        self.view.context_menu.entryconfig("Видалити", command=self.delete_selected_log)
        self.view.clear_db_btn.config(command=self.clear_database)
        self.view.export_csv_btn.config(command=self.export_to_csv)
        self.view.target_entry.bind("<Return>", lambda event: self.scan_and_save(self.view.target_entry.get()))
        self.view.about_btn.config(command=self.show_about_dialog) 
        # 1
        self.view.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

    def setup_system(self):
        print("Налаштування бази даних...")
        self.db.init_db()

    def scan_and_save(self, target):
        print(f"\n1. Починаємо сканування: {target}")
        
        scan_mode = self.view.scan_type_combo.get() 
        
        try:
            if scan_mode == "Port":
                if ":" in target:
                    ip_part, port_part = target.split(":")
                    
                    if not port_part.isdigit() or not (1 <= int(port_part) <= 65535):
                        print(f"Недійсний порт: {port_part}")
                        is_alive, response_time = False, 0.0  
                    else:
                        print(f"Режим Порт: перевіряємо {ip_part} на порту {port_part}")
                        is_alive, response_time = self.network.check_port(ip_part, port_part)
                else:
                    print(f"Режим Порт: порт не вказано, перевіряємо стандартний 80")
                    is_alive, response_time = self.network.check_port(target, 80)
            else:
                if ":" in target:
                    target = target.split(":")[0] 
                    
                print(f"Режим Пінг: перевіряємо {target}")
                is_alive, response_time = self.network.check_ping(target)
                
            print(f"2. Сканування завершено! is_alive: {is_alive}, час: {response_time}")
            
        except Exception as e:
            print(f"ПОМИЛКА СКАНУВАННЯ: {e}")
            is_alive, response_time = False, 0.0 
            
        status = "Online" if is_alive else "Offline"
        try:
            time_to_save = float(response_time) if response_time is not None else 0.0
        except (ValueError, TypeError):
            time_to_save = 0.0
        
        print("3. Пробуємо зберегти в базу...")
        new_id = self.db.save_log(target, status, time_to_save)
        print(f"4. Результат збереження, отриманий ID: {new_id}")
        
        if new_id:
            self.update_table(new_id, target, status, time_to_save)
            print("5. Успішно додано в таблицю інтерфейсу!")
        else:
            print("ПОМИЛКА: База даних повернула None. Рядок не буде намальовано.")

    def update_table(self, db_id, target, status, response_time):
        row_tag = "online_tag" if status == "Online" else "offline_tag"
        self.view.tree.insert("", "end", values=(db_id, target, status, f"{response_time} ms"), tags=(row_tag,))

    def handle_button_click(self):
        target_from_gui = self.view.target_entry.get().strip()
        if not target_from_gui:
            messagebox.showwarning("Помилка", "Будь ласка, введіть IP або домен!")
            return
        self.scan_and_save(target_from_gui)


    def load_history(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        records = self.db.get_all_logs()
        for row in records:
            if row[2] == "Online":
                row_tag = "online_tag"
            else:
                row_tag = "offline_tag"
            self.view.tree.insert("", "end", values=row, tags=(row_tag,))
        
    def delete_selected_log(self):
        #13
        selected_item = self.view.tree.selection()
        if not selected_item:
            return
        item_values = self.view.tree.item(selected_item, "values")
        log_id = item_values[0] 
        self.db.delete_log(log_id)
        self.view.tree.delete(selected_item)

    def clear_database(self):
        success = self.db.clear_all_logs()
        
        if success:
            for item in self.view.tree.get_children():
                self.view.tree.delete(item)
            print("Базу даних та таблицю повністю очищено!")
        else:
            print("Не вдалося очистити базу даних.")

    def export_to_csv(self):
        records = self.db.get_all_logs()
        
        if not records:
            messagebox.showwarning("Порожньо", "Немає даних для експорту!")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файли", "*.csv"), ("Всі файли", "*.*")],
            title="Зберегти історію як"
        )

        if filepath:
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Ціль", "Статус", "Відгук (мс)"])
                    writer.writerows(records)
                    
                messagebox.showinfo("Успіх", f"Дані успішно збережено у файл:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")


    def show_about_dialog(self): 
        about_window = tk.Toplevel(self.view)
        about_window.title("Про програму")
        about_window.geometry("300x150")
        about_window.resizable(False, False)
        about_window.transient(self.view)
        about_window.grab_set()

        title_label = ttk.Label(about_window, text="Network Monitor", font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(15, 5))

        desc_label = ttk.Label(about_window, text="Курсова робота \n Програма для мережевого моніторингу, провірка tcp портів та перевірка пінгу віддалених серверів", justify="center")
        desc_label.pack(pady=5)

        close_btn = ttk.Button(about_window, text="Закрити", command=about_window.destroy)
        close_btn.pack(pady=10)


    def change_language(self, event=None):
        selected_lang = self.view.lang_combo.get()
        if selected_lang == "English":
            self.view.update_language("en")
        else:
            self.view.update_language("ua")