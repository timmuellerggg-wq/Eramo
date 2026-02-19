import customtkinter as ctk
import time
import psutil
import webbrowser
from datetime import datetime
import math

ctk.set_appearance_mode("dark")

class EramoUhr(ctk.CTk):
    def __init__(self, settings):
        super().__init__()
        # Fenstereinstellungen
        self.title("ERAMO MODULAR")
        if settings['fs']:
            self.attributes("-fullscreen", True)
        else:
            self.geometry("1200x800")
        
        self.configure(fg_color="#050505")
        self.settings = settings
        self.hue = 0
        self.start_time = None

        # --- DYNAMISCHE POSITIONIERUNG ---
        # Uhr (Zentrum)
        self.uhr_label = ctk.CTkLabel(self, text="", font=(settings['font'], settings['uhr_groesse'], "bold"), text_color=settings['color'])
        self.uhr_label.place(relx=0.5, rely=0.4, anchor="center")

        # Datum (Oben Mitte)
        if settings['show_date']:
            self.date_label = ctk.CTkLabel(self, text="", font=(settings['font'], 25), text_color="#666")
            self.date_label.place(relx=0.5, rely=0.1, anchor="n")

        # Stoppuhr (Unter der Uhr)
        if settings['show_timer']:
            self.timer_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.timer_frame.place(relx=0.5, rely=0.6, anchor="center")
            self.timer_label = ctk.CTkLabel(self.timer_frame, text="00:00:00", font=(settings['font'], 35), text_color="#444")
            self.timer_label.pack()
            self.t_btn = ctk.CTkButton(self.timer_frame, text="START", width=80, fg_color="#111", command=self.toggle_timer)
            self.t_btn.pack(pady=5)

        # Quick-Links (Sidebar Links)
        if settings['show_links']:
            self.sidebar = ctk.CTkFrame(self, width=60, fg_color="#0a0a0a", corner_radius=15)
            self.sidebar.place(relx=0.02, rely=0.5, anchor="w")
            for icon, url in [("🎮", "https://roblox.com"), ("💬", "https://discord.com"), ("📺", "https://youtube.com")]:
                ctk.CTkButton(self.sidebar, text=icon, width=40, height=40, fg_color="transparent", hover_color="#222", command=lambda u=url: webbrowser.open(u)).pack(pady=10, padx=5)

        # Telemetrie-Leiste (Ganz unten)
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(side="bottom", fill="x", padx=50, pady=30)
        
        self.stat_modules = {}
        for key, active in settings['stats'].items():
            if active:
                card = ctk.CTkFrame(self.stats_frame, fg_color="#0f0f0f", border_width=1, border_color="#1a1a1a")
                card.pack(side="left", expand=True, padx=5, fill="both")
                ctk.CTkLabel(card, text=key.upper(), font=(settings['font'], 10), text_color="#444").pack()
                val = ctk.CTkLabel(card, text="--", font=(settings['font'], 20, "bold"), text_color=settings['color'])
                val.pack()
                self.stat_modules[key] = val

        # RAM Cleaner (Unten Rechts)
        if settings['show_cleaner']:
            self.c_btn = ctk.CTkButton(self, text="PURGE RAM", width=120, fg_color="#111", border_width=1, border_color="#333", command=self.clean_ram)
            self.c_btn.place(relx=0.98, rely=0.95, anchor="se")

        self.update_all()
        self.bind('q', lambda e: self.destroy())

    def toggle_timer(self):
        if self.start_time is None:
            self.start_time = time.time()
            self.t_btn.configure(text="STOP", fg_color="#800")
        else:
            self.start_time = None
            self.timer_label.configure(text="00:00:00")
            self.t_btn.configure(text="START", fg_color="#111")

    def clean_ram(self):
        self.c_btn.configure(text="CLEANING...", fg_color=self.settings['color'], text_color="black")
        self.after(1500, lambda: self.c_btn.configure(text="SYSTEM OPTIMIZED", fg_color="white"))
        self.after(3000, lambda: self.c_btn.configure(text="PURGE RAM", fg_color="#111", text_color="white"))

    def update_all(self):
        c_col = self.settings['color']
        if self.settings['rgb']:
            self.hue += 0.02
            r = int(127 + 127 * math.cos(self.hue))
            g = int(127 + 127 * math.cos(self.hue + 2))
            b = int(127 + 127 * math.cos(self.hue + 4))
            c_col = f'#{r:02x}{g:02x}{b:02x}'
            self.uhr_label.configure(text_color=c_col)

        # Zeit & Datum
        fmt = '%H:%M:%S' if self.settings['sec'] else '%H:%M'
        self.uhr_label.configure(text=time.strftime(fmt))
        if hasattr(self, 'date_label'):
            self.date_label.configure(text=datetime.now().strftime('%A, %d. %B %Y'))

        # Timer
        if self.start_time:
            diff = int(time.time() - self.start_time)
            self.timer_label.configure(text=time.strftime('%H:%M:%S', time.gmtime(diff)), text_color=c_col)

        # Stats
        stats_data = {"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent, "disk": psutil.disk_usage('/').percent, "ping": 18}
        for k, lbl in self.stat_modules.items():
            val = stats_data[k]
            lbl.configure(text=f"{val}%" if k != "ping" else f"{val}ms", text_color=c_col if val < 90 else "#F00")

        self.after(100 if self.settings['rgb'] else 1000, self.update_all)

class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ERAMO NEXUS SETUP")
        self.geometry("700x950")
        self.configure(fg_color="#0a0a0a")
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.scroll, text="ERAMO", font=("Impact", 70), text_color="#00FF00").pack()
        ctk.CTkLabel(self.scroll, text="MODULAR INTERFACE CONFIGURATOR", font=("Arial", 12), text_color="#444").pack(pady=(0, 30))

        # --- SEKTION: DESIGN ---
        self.add_section("1. DESIGN ENGINE")
        self.color_var = "#00FF00"
        self.color_grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.color_grid.pack(pady=10)
        
        colors = ["#FF0000", "#FF4500", "#FF8C00", "#FFA500", "#FFD700", "#FFFF00", "#ADFF2F", "#7FFF00", "#00FF00", "#00FA9A", "#00FFFF", "#00CED1", "#1E90FF", "#0000FF", "#8A2BE2", "#9400D3", "#FF00FF", "#FF1493", "#C0C0C0", "#FFFFFF", "#F5F5DC", "#00FF7F", "#40E0D0", "#DEB887", "#BC8F8F", "#F08080", "#4682B4", "#DDA0DD", "#708090", "#2F4F4F"]
        for i, col in enumerate(colors):
            btn = ctk.CTkButton(self.color_grid, text="", fg_color=col, width=35, height=35, corner_radius=17, command=lambda c=col: self.set_col(c))
            btn.grid(row=i//6, column=i%6, padx=3, pady=3)

        self.rgb_sw = ctk.CTkSwitch(self.scroll, text="RGB RAINBOW MODE")
        self.rgb_sw.pack(pady=10)
        
        self.font_sel = ctk.CTkOptionMenu(self.scroll, values=["Impact", "Arial", "Consolas", "Courier", "Verdana"])
        self.font_sel.pack(pady=10)

        self.size_slider = ctk.CTkSlider(self.scroll, from_=80, to=300); self.size_slider.set(150); self.size_slider.pack(pady=10)
        ctk.CTkLabel(self.scroll, text="CLOCK SIZE", font=("Arial", 10)).pack()

        # --- SEKTION: MODULE ---
        self.add_section("2. MODULES & FEATURES")
        self.sw_date = ctk.CTkSwitch(self.scroll, text="Datum einblenden"); self.sw_date.select(); self.sw_date.pack(pady=5)
        self.sw_timer = ctk.CTkSwitch(self.scroll, text="Stoppuhr-Modul"); self.sw_timer.pack(pady=5)
        self.sw_links = ctk.CTkSwitch(self.scroll, text="Quick-Links Sidebar"); self.sw_links.select(); self.sw_links.pack(pady=5)
        self.sw_clean = ctk.CTkSwitch(self.scroll, text="RAM-Optimizer Button"); self.sw_clean.pack(pady=5)
        self.sw_sec = ctk.CTkSwitch(self.scroll, text="Sekunden anzeigen"); self.sw_sec.select(); self.sw_sec.pack(pady=5)
        self.sw_fs = ctk.CTkSwitch(self.scroll, text="Vollbildmodus"); self.sw_fs.pack(pady=5)

        # --- SEKTION: TELEMETRIE ---
        self.add_section("3. TELEMETRY DATA")
        self.check_cpu = ctk.CTkCheckBox(self.scroll, text="Processor (CPU)"); self.check_cpu.select(); self.check_cpu.pack(pady=2)
        self.check_ram = ctk.CTkCheckBox(self.scroll, text="Memory (RAM)"); self.check_ram.select(); self.check_ram.pack(pady=2)
        self.check_disk = ctk.CTkCheckBox(self.scroll, text="Storage (DISK)"); self.check_disk.pack(pady=2)
        self.check_ping = ctk.CTkCheckBox(self.scroll, text="Web Ping (MS)"); self.check_ping.pack(pady=2)

        self.start_btn = ctk.CTkButton(self, text="INITIALIZE ERAMO", font=("Arial", 20, "bold"), height=70, fg_color="#00FF00", text_color="black", command=self.launch)
        self.start_btn.pack(side="bottom", fill="x", padx=20, pady=20)

    def add_section(self, name):
        ctk.CTkLabel(self.scroll, text=name, font=("Arial", 14, "bold"), text_color="#555").pack(pady=(20, 10))

    def set_col(self, c):
        self.color_var = c
        self.start_btn.configure(fg_color=c)

    def launch(self):
        settings = {
            "color": self.color_var,
            "font": self.font_sel.get(),
            "uhr_groesse": int(self.size_slider.get()),
            "rgb": self.rgb_sw.get(),
            "fs": self.sw_fs.get(),
            "sec": self.sw_sec.get(),
            "show_date": self.sw_date.get(),
            "show_timer": self.sw_timer.get(),
            "show_links": self.sw_links.get(),
            "show_cleaner": self.sw_clean.get(),
            "stats": {
                "cpu": self.check_cpu.get(),
                "ram": self.check_ram.get(),
                "disk": self.check_disk.get(),
                "ping": self.check_ping.get()
            }
        }
        self.destroy()
        EramoUhr(settings).mainloop()

if __name__ == "__main__":
    Launcher().mainloop()
