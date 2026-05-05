import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Monitor")
        self.geometry("800x500")
        self.minsize(600, 400)
        self.center_window(800, 500)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.tab_monitor = ttk.Frame(self.notebook)
        self.tab_settings = ttk.Frame(self.notebook)
        #1
        self.texts = {
            "ua": {
                "scan_btn": "Сканувати",
                "clear_btn": "Очистити всю історію сканувань",
                "export_btn": "Експорт історії в CSV",
                "about_btn": "Про програму",
                "col_target": "Ціль",
                "col_status": "Статус",
                "col_time": "Відгук (мс)",
                "lang_label": "Мова інтерфейсу:",
                "tab_monitor": "Моніторинг",
                "tab_settings": "Налаштування",
                "frame_scan": "Управління скануванням",
                "lbl_target": "Ціль (IP/Домен):"
            },
            "en": {
                "scan_btn": "Scan",
                "clear_btn": "Clear all scan history",
                "export_btn": "Export history to CSV",
                "about_btn": "About",
                "col_target": "Target",
                "col_status": "Status",
                "col_time": "Response (ms)",
                "lang_label": "Language:",
                "tab_monitor": "Monitoring",
                "tab_settings": "Settings",
                "frame_scan": "Scan Management",
                "lbl_target": "Target (IP/Domain):"
            }
        }
        self.clear_db_btn = ttk.Button(
            self.tab_settings,
            text="Очистити всю історію сканувань", 
            width=30
        )
        self.clear_db_btn.pack(pady=20) 
        
        self.export_csv_btn = ttk.Button(self.tab_settings, text="Експорт історії в CSV", width=30)
        self.export_csv_btn.pack(pady=5)

#9
        self.about_btn = ttk.Button(self.tab_settings, text="Про програму", width=30)
        self.about_btn.pack(pady=20)

        self.notebook.add(self.tab_monitor, text="Моніторинг")
        self.notebook.add(self.tab_settings, text="Налаштування")

        self._build_monitor_tab()
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Видалити")

        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _build_monitor_tab(self):
        #5
        self.control_frame = ttk.LabelFrame(self.tab_monitor, text="Управління скануванням")
        self.control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.control_frame.grid_columnconfigure(1, weight=1)

        self.target_label = ttk.Label(self.control_frame, text="Ціль (IP/Домен):")
        self.target_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.target_entry = ttk.Entry(self.control_frame)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        #6
        ttk.Label(self.control_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.scan_type_combo = ttk.Combobox(self.control_frame, values=["Ping", "Port"], state="readonly", width=8)
        self.scan_type_combo.current(0)
        self.scan_type_combo.grid(row=0, column=3, padx=5, pady=5)

        self.scan_btn = ttk.Button(self.control_frame, text="Сканувати")
        self.scan_btn.grid(row=0, column=4, padx=5, pady=5)

        # 12
        table_frame = ttk.Frame(self.tab_monitor)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.tab_monitor.grid_rowconfigure(1, weight=1)
        self.tab_monitor.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # 1
        self.lang_label = ttk.Label(self.tab_settings, text=self.texts["ua"]["lang_label"])
        self.lang_label.pack(pady=(10, 2))
        
        self.lang_combo = ttk.Combobox(self.tab_settings, values=["Українська", "English"], state="readonly", width=27)
        self.lang_combo.current(0) 
        self.lang_combo.pack(pady=(0, 10))

        columns = ("id", "target", "status", "time")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("target", text="Ціль")
        self.tree.heading("status", text="Статус")
        self.tree.heading("time", text="Відгук (мс)")
        
        self.tree.tag_configure("online_tag", foreground="green")
        self.tree.tag_configure("offline_tag", foreground="red")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("target", width=300, anchor="w")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("time", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")


    def update_language(self, lang_code):
        t = self.texts[lang_code]
        
        self.scan_btn.config(text=t["scan_btn"])
        self.clear_db_btn.config(text=t["clear_btn"])
        self.export_csv_btn.config(text=t["export_btn"])
        self.about_btn.config(text=t["about_btn"])
        self.lang_label.config(text=t["lang_label"])
        
        self.tree.heading("#2", text=t["col_target"]) 
        self.tree.heading("#3", text=t["col_status"]) 
        self.tree.heading("#4", text=t["col_time"])   

        self.notebook.tab(0, text=t["tab_monitor"])
        self.notebook.tab(1, text=t["tab_settings"])

        self.control_frame.config(text=t["frame_scan"])
        self.target_label.config(text=t["lbl_target"])
    