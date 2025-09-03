import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import webbrowser
from datetime import datetime
import threading
import cv2
import time

# For downloading
try:
    import requests
except Exception:
    requests = None
    import urllib.request

# === Configuration ===
HTML_LOG_FILE = "logs.html"
USERNAME = "admin"
PASSWORD = "admin"
PROJECT_INFO_URL = "https://github.com/adithya984/supraja-intern/raw/main/project%20%20info.pdf"
PROJECT_INFO_LOCAL = "project info.pdf"

DISABLE_CAM_CMD = r'powershell.exe -Command "Get-PnpDevice -Class Camera | Disable-PnpDevice -Confirm:$false"'
ENABLE_CAM_CMD = r'powershell.exe -Command "Get-PnpDevice -Class Camera | Enable-PnpDevice -Confirm:$false"'
CHECK_STATUS_CMD = r'powershell.exe -Command "Get-PnpDevice -Class Camera | Select-Object -ExpandProperty Status"'

# === HTML log template ===
HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Webcam Activity Log</title>
    <style>
        body { font-family: Arial, sans-serif; background: #111; color: #e6e6e6; padding: 20px; }
        h2 { color: #03dac6; }
        ul { list-style: none; padding: 0; }
        li { margin: 10px 0; padding: 10px; border-radius: 8px; font-size: 15px; }
        .enabled { background-color: #2e7d32; color: white; }
        .disabled { background-color: #c62828; color: white; }
        .info { background-color: #37474f; color: white; }
    </style>
</head>
<body>
    <h2>📋 Webcam Activity Log</h2>
    <ul>
"""
HTML_FOOTER = """
    </ul>
</body>
</html>
"""

# === Initialize logs.html on startup ===
def init_html_log():
    if not os.path.exists(HTML_LOG_FILE):
        with open(HTML_LOG_FILE, "w", encoding="utf-8") as f:
            f.write(HTML_HEADER + HTML_FOOTER)

# Insert an entry right before the closing tags so file remains valid
def append_html_entry(entry_html):
    init_html_log()
    try:
        with open(HTML_LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        insert_at = content.rfind("</ul>")
        if insert_at == -1:
            content = content + entry_html + HTML_FOOTER
        else:
            content = content[:insert_at] + entry_html + content[insert_at:]
        with open(HTML_LOG_FILE, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print("Failed to append to HTML log:", e)

# === Logging ===
def log_to_html(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "Enabled" in action or "opened" in action or "Viewed" in action or "checked" in action:
        status_class = "enabled" if "Enabled" in action else "info"
        emoji = "✅" if "Enabled" in action else "ℹ️"
    else:
        status_class = "disabled"
        emoji = "❌"
    entry = f'        <li class="{status_class}">{emoji} <strong>{action}</strong> at {timestamp}</li>\n'
    append_html_entry(entry)

def log_to_gui(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, f"• {msg} at {timestamp}\n")
    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)
    log_to_html(msg)

# === Intruder Video Capture ===
def record_intruder_video():
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"intruder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        file_path = os.path.join(desktop_path, filename)

        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(file_path, fourcc, 20.0, (640, 480))

        start = time.time()
        while int(time.time() - start) < 10:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
        cap.release()
        out.release()

        log_to_gui(f"⚠️ Intruder video saved at: {file_path}")

    except Exception as e:
        log_to_gui(f"⚠️ Error recording intruder video: {e}")

# === Authentication ===
def authenticate(action_func):
    entered_pass = simpledialog.askstring("Password Required", "Enter password:", show="*")
    if entered_pass == PASSWORD:
        action_func()
    else:
        log_to_gui("❗ Wrong password attempt detected")
        threading.Thread(target=record_intruder_video, daemon=True).start()

# === Fast Command Execution ===
def fast_run(cmd):
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        log_to_gui(f"⚠️ Failed to run command: {e}")

# === Functional Buttons ===
def enable_camera():
    def task():
        fast_run(ENABLE_CAM_CMD)
        log_to_gui("✅ Camera Enabled")
    threading.Thread(target=task, daemon=True).start()

def disable_camera():
    def task():
        fast_run(DISABLE_CAM_CMD)
        log_to_gui("❌ Camera Disabled")
    threading.Thread(target=task, daemon=True).start()

def check_status():
    try:
        result = subprocess.check_output(CHECK_STATUS_CMD, shell=True, text=True)
        status = result.strip()
    except Exception:
        status = "Unknown"
    messagebox.showinfo("Status", f"Camera is currently: {status}")
    log_to_gui(f"ℹ️ Camera status checked: {status}")

def change_password():
    global USERNAME, PASSWORD
    new_user = simpledialog.askstring("Change Username", "Enter new username:")
    new_pass = simpledialog.askstring("Change Password", "Enter new password:", show="*")
    if new_user and new_pass:
        USERNAME = new_user
        PASSWORD = new_pass
        log_to_gui("🔐 Password changed")

def show_project_info():
    file_name = PROJECT_INFO_LOCAL
    local_path = os.path.abspath(file_name)

    if os.path.exists(local_path):
        try:
            open_file_with_default_app(local_path)
            log_to_gui("📄 Project Info opened (local)")
            return
        except Exception as e:
            log_to_gui(f"⚠️ Failed to open local Project Info: {e}")

    def download_and_open():
        try:
            log_to_gui("⬇️ Project Info download started")
            if requests:
                with requests.get(PROJECT_INFO_URL, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
            else:
                urllib.request.urlretrieve(PROJECT_INFO_URL, local_path)

            log_to_gui("⬇️ Project Info downloaded")
            try:
                open_file_with_default_app(local_path)
                log_to_gui("📄 Project Info opened (downloaded)")
            except Exception as e2:
                log_to_gui(f"⚠️ Downloaded but failed to open: {e2}")
                messagebox.showinfo("Downloaded", f"Project Info downloaded to:\n{local_path}")
        except Exception as e:
            log_to_gui(f"⚠️ Project Info download failed: {e}")
            messagebox.showerror("Download Failed", f"Could not download Project Info:\n{e}")

    threading.Thread(target=download_and_open, daemon=True).start()

def open_file_with_default_app(path):
    if os.name == 'nt':
        os.startfile(path)
    else:
        try:
            if os.uname().sysname == 'Darwin':
                subprocess.run(['open', path], check=False)
            else:
                subprocess.run(['xdg-open', path], check=False)
        except Exception:
            webbrowser.open('file://' + os.path.abspath(path))

def view_logs():
    if os.path.exists(HTML_LOG_FILE):
        log_to_gui("📂 Viewed logs")
        try:
            open_file_with_default_app(os.path.abspath(HTML_LOG_FILE))
        except Exception as e:
            log_to_gui(f"⚠️ Failed to open logs: {e}")
            webbrowser.open("file://" + os.path.abspath(HTML_LOG_FILE))
    else:
        messagebox.showinfo("Logs", "No logs available yet.")

def clear_logs():
    if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all logs?"):
        message_box.config(state=tk.NORMAL)
        message_box.delete("1.0", tk.END)
        message_box.insert(tk.END, "• Application started successfully\n")
        message_box.config(state=tk.DISABLED)
        with open(HTML_LOG_FILE, "w", encoding="utf-8") as f:
            f.write(HTML_HEADER + HTML_FOOTER)
        log_to_gui("🧹 Logs cleared")

# === Exit Confirmation ===
def exit_app():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        log_to_gui("👋 Application closed by user")
        root.destroy()

# === GUI Setup ===
init_html_log()

root = tk.Tk()
root.title("🔒 Webcam Spyware Security")
root.geometry("480x780")
root.configure(bg="black")

# Header
tk.Label(root, text="🔒 Webcam Spyware Security", font=("Helvetica", 18, "bold"),
         fg="#03dac6", bg="black").pack(pady=10)

# Image (optional top icon)
image_path = "images.png"
if os.path.exists(image_path):
    try:
        img = Image.open(image_path).resize((150, 150))
        photo = ImageTk.PhotoImage(img)
        tk.Label(root, image=photo, bg="black").pack(pady=5)
    except Exception:
        pass

# Styled button factory
def style_button(master, text, cmd):
    btn = tk.Button(master, text=text, command=cmd, font=("Arial", 11, "bold"),
                    bg="#03dac6", fg="black", width=22, pady=6, bd=0, relief=tk.RAISED)
    btn.pack(pady=6)
    def on_enter(e): btn['bg'] = '#29b2a6'
    def on_leave(e): btn['bg'] = '#03dac6'
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# Top controls
top_frame = tk.Frame(root, bg="black")
top_frame.pack(pady=6)
style_button(top_frame, "Project Info", show_project_info)

# === Logo below Project Info ===
logo_path = "logo.png"  # change to your logo file
if os.path.exists(logo_path):
    try:
        logo_img = Image.open(logo_path).resize((120, 120))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(root, image=logo_photo, bg="black")
        logo_label.image = logo_photo
        logo_label.pack(pady=5)
    except Exception as e:
        log_to_gui(f"⚠️ Failed to load logo: {e}")

frame1 = tk.Frame(root, bg="black")
frame1.pack(pady=6)
style_button(frame1, "View Logs", lambda: authenticate(view_logs))
style_button(frame1, "Check Status", check_status)
style_button(frame1, "Change Password", change_password)

frame2 = tk.Frame(root, bg="black")
frame2.pack(pady=6)
style_button(frame2, "Disable Camera", lambda: authenticate(disable_camera))
style_button(frame2, "Enable Camera", lambda: authenticate(enable_camera))

bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(pady=6)
style_button(bottom_frame, "Clear Logs", clear_logs)
style_button(bottom_frame, "Exit", exit_app)

# Activity log label
tk.Label(root, text="📋 Activity Log:", font=("Arial", 11, "bold"),
         fg="white", bg="black").pack(pady=(10, 0))

message_box = tk.Text(root, height=12, width=60, bg="#121212", fg="#00ffcc",
                      font=("Courier", 10), wrap=tk.WORD)
message_box.pack(padx=10, pady=5)
message_box.insert(tk.END, "• Application started successfully\n")
message_box.config(state=tk.DISABLED)

log_to_gui("🟢 Application started")

root.mainloop()
