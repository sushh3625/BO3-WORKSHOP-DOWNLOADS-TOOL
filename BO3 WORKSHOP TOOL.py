import tkinter as tk
from tkinter import filedialog, messagebox
import os, json, re, subprocess, threading, urllib.request, zipfile, webbrowser, shutil
import sys

# المعلومات والروابط
RIGHTS = "sushh3625"
GITHUB_URL = "https://github.com/sushh3625"
VERSION = "Beta Version 0.0"

class BO3FakhamaTool:
    def __init__(self, root):
        self.root = root
        self.root.title(f"BO3 Tool - {RIGHTS}")
        self.root.geometry("500x560")
        
        # ملف الإعدادات لحفظ المسارات تلقائياً
        self.config_dir = os.path.join(os.environ['LOCALAPPDATA'], 'BO3_Tool_sushh')
        if not os.path.exists(self.config_dir): os.makedirs(self.config_dir)
        self.config_file = os.path.join(self.config_dir, "paths_config.json")
        self.settings = self.load_settings()

        # --- تصميم الواجهة الفخم ---
        tk.Label(self.root, text="BO3 WORKSHOP TOOL", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(self.root, text=VERSION, font=("Arial", 10, "bold"), fg="gray").pack()
        
        lbl_rights = tk.Label(self.root, text=f"Created by {RIGHTS}", fg="blue", font=("Arial", 10, "underline", "italic"), cursor="hand2")
        lbl_rights.pack(pady=5)
        lbl_rights.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))

        # SteamCMD Section
        frame_s = tk.LabelFrame(self.root, text="SteamCMD Setup", padx=10, pady=10)
        frame_s.pack(pady=10, padx=20, fill="x")
        self.lbl_status = tk.Label(frame_s, text="Status: Checking...", fg="orange")
        self.lbl_status.pack()
        
        btn_f = tk.Frame(frame_s)
        btn_f.pack(pady=5)
        tk.Button(btn_f, text="Install to C:\\", width=15, command=self.auto_install_c).pack(side="left", padx=5)
        tk.Button(btn_f, text="Locate .exe", width=15, command=self.manual_locate_steam).pack(side="left", padx=5)

        # Game Path
        tk.Label(self.root, text="Step 1: Select Black Ops 3 Folder", font=("Arial", 10, "bold")).pack(pady=(15,0))
        f1 = tk.Frame(self.root)
        f1.pack(pady=5, padx=20, fill="x")
        self.entry_path = tk.Entry(f1)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=5)
        self.entry_path.insert(0, self.settings.get("game_path", ""))
        tk.Button(f1, text="Browse", command=self.browse_game).pack(side="right")

        # Workshop Link
        tk.Label(self.root, text="Step 2: Workshop Link", font=("Arial", 10, "bold")).pack(pady=(15,0))
        f2 = tk.Frame(self.root)
        f2.pack(pady=5, padx=20, fill="x")
        self.entry_url = tk.Entry(f2)
        self.entry_url.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(f2, text="Paste", command=self.paste_text).pack(side="left", padx=2)
        tk.Button(f2, text="Open Steam", command=lambda: webbrowser.open("https://steamcommunity.com/app/311210/workshop/")).pack(side="right")

        # Type Selection
        self.type_var = tk.StringVar(value="map")
        f3 = tk.Frame(self.root)
        f3.pack(pady=10)
        tk.Radiobutton(f3, text="Map (Usermaps)", variable=self.type_var, value="map").pack(side="left", padx=20)
        tk.Radiobutton(f3, text="Mod (Mods)", variable=self.type_var, value="mod").pack(side="left", padx=20)

        # Start Button
        self.btn_run = tk.Button(self.root, text="START DOWNLOAD", bg="#28a745", fg="white", 
                                 font=("Arial", 12, "bold"), height=2, width=25, command=self.start_logic)
        self.btn_run.pack(pady=20)

        self.update_status()

    # --- ميزة سحب الاسم الحقيقي ---
    def get_real_name(self, url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8')
                title = re.search(r'<div class="workshopItemTitle">(.*?)</div>', html).group(1)
                return re.sub(r'[\\/*?:"<>|]', '_', title).strip()
        except: return None

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f: return json.load(f)
            except: return {}
        return {}

    def save_settings(self):
        with open(self.config_file, "w") as f: json.dump(self.settings, f)

    def update_status(self):
        p = self.settings.get("steamcmd_path", "")
        if p and os.path.exists(p):
            self.lbl_status.config(text=f"READY: {p}", fg="green")
        else: self.lbl_status.config(text="SteamCMD NOT FOUND!", fg="red")

    def manual_locate_steam(self):
        p = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if p:
            self.settings["steamcmd_path"] = p
            self.save_settings()
            self.update_status()

    def auto_install_c(self):
        target = r"C:\steamcmd"
        if not os.path.exists(target): os.makedirs(target)
        def dl():
            try:
                url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
                zip_p = os.path.join(target, "temp.zip")
                urllib.request.request.urlretrieve(url, zip_p)
                with zipfile.ZipFile(zip_p, 'r') as z: z.extractall(target)
                os.remove(zip_p)
                self.settings["steamcmd_path"] = os.path.join(target, "steamcmd.exe")
                self.save_settings()
                self.root.after(0, self.update_status)
                messagebox.showinfo("Help", "Success!")
            except Exception as e: messagebox.showerror("Help", f"Error: {e}")
        threading.Thread(target=dl).start()

    def browse_game(self):
        p = filedialog.askdirectory()
        if p:
            self.entry_path.delete(0, tk.END); self.entry_path.insert(0, p)
            self.settings["game_path"] = p
            self.save_settings()

    def paste_text(self):
        try:
            self.entry_url.delete(0, tk.END)
            self.entry_url.insert(0, self.root.clipboard_get())
        except: pass

    def start_logic(self):
        url, path = self.entry_url.get(), self.entry_path.get()
        cmd = self.settings.get("steamcmd_path", "")
        if not url or not path or not os.path.exists(cmd):
            messagebox.showwarning("Help", "Check Path and URL!")
            return
        
        self.btn_run.config(state="disabled", text="Fetching Name...")
        def run():
            try:
                real_name = self.get_real_name(url)
                mid = re.search(r'id=(\d+)', url).group(1)
                folder_name = real_name if real_name else mid
                
                self.root.after(0, lambda: self.btn_run.config(text="Downloading..."))
                
                temp_dir = os.path.join(self.config_dir, "temp_dl")
                subprocess.run([cmd, "+login", "anonymous", "+force_install_dir", temp_dir, 
                                "+workshop_download_item", "311210", mid, "+quit"], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
                
                target_type = "usermaps" if self.type_var.get() == "map" else "mods"
                final_dest = os.path.join(path, target_type, folder_name)
                dl_content = os.path.join(temp_dir, "steamapps", "workshop", "content", "311210", mid)
                
                if os.path.exists(dl_content):
                    if os.path.exists(final_dest): shutil.rmtree(final_dest)
                    os.makedirs(os.path.dirname(final_dest), exist_ok=True)
                    shutil.move(dl_content, final_dest)
                    shutil.rmtree(temp_dir)
                    # نجاح: إظهار الرسالة ثم الإغلاق
                    messagebox.showinfo("Help", "ضبط ابشرك خلاص الله يعافيك لاتنسى تنشر الاداه يا وحش <_>")
                    self.root.quit()
                    sys.exit()
                else:
                    messagebox.showerror("Help", "Download failed. Program will stay open.")
            except Exception as e:
                messagebox.showerror("Help", f"Error: {e}\nProgram will stay open.")
            finally:
                self.btn_run.config(state="normal", text="START DOWNLOAD")
        
        threading.Thread(target=run).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BO3FakhamaTool(root)
    root.mainloop()
