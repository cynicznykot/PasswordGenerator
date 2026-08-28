"""
Graphical user interface for the Password Generator application.

This module provides a tkinter-based GUI that allows users to:
- Generate cryptographically secure passwords
- Adjust password length and character types
- Evaluate password strength in real-time
- Copy password to clipboard
- Save passwords to a file with service name and login/email

The GUI interacts with the generator module for all core logic.
"""

import json
import os
import urllib.request
import tkinter as tk
import webbrowser
import datetime
import tempfile
import shutil
from datetime import datetime, timedelta
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from src.generator import build_character_pool, generate_password, check_strength, load_passwords, save_passwords
from src.generator import SETTINGS_FILE
from src.config import APP_VERSION, GITHUB_API_URL


def safe_read_settings():
    """
    Safely read settings from settings.json.

    Return an empty dict if the file doesn't exist or cannot be read.
    This prevents crashes on Windows when the file is locked by another process.
    """
    try:
        if os.path.exists("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def safe_write_settings():
    """
    Safely write settings to settings.json using a temporary file.

    Uses an atomic move operation to prevent file corruption on Windows.
    """
    try:
        # Create a temporary file in the current directory
        fd, temp_path = tempfile.mkstemp(suffix=".json", prefix="settings_", dir=os.path.dirname("."))
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        shutil.move(temp_path, "settings.json")
    except Exception:
        pass


def check_for_updates():
    """
    Check for new versions on GitHub.

    - Reads the last dismissed timestamp from settings.json
    - If less than 24 hours have passed, skip the check
    - Otherwise, fetches the latest release from GitHub API
    - Shows a notification if a new version is available
    """
    data = safe_read_settings()

    # Check if the user has dismissed the notification within the last 24 hours
    if data.get("app_version") != APP_VERSION:
        safe_write_settings()
        return

    last_dismissed = data.get("last_dismissed")
    if last_dismissed:
        saved_time = datetime.strptime(last_dismissed, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - saved_time < timedelta(hours=24):
            return  # Skip the update check

    # Fetch the latest release from GitHub
    try:
        url = GITHUB_API_URL
        response = urllib.request.urlopen(url)
        data = response.read()
        text = data.decode('utf-8')
        json_data = json.loads(text)
        latest_version = json_data['tag_name']

        if latest_version != APP_VERSION:
            result = messagebox.askyesnocancel(
                "Update available!",
                f"Version {latest_version} is already available.\nDo you want to open "
                f"the download page?"
            )
            if result:
                import webbrowser
                webbrowser.open("https://github.com/cynicznykot/PasswordGenerator/releases/latest")
            elif result is False:
                # Save the dismissal timestamp
                safe_write_settings({
                    "last_dismissed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "app_version": APP_VERSION
                })
    except Exception:
        pass


def save_dismiss_time():
    """Save the current time app version to settings.json."""
    now_time = datetime.now()
    save_time = now_time.strftime("%Y-%m-%d %H:%M:%S")

    data = {"last_dismissed": save_time, "app_version": APP_VERSION}

    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def show_passwords(root):
    """
    Open a new window displaying all saved passwords.

    - Prompts the user to select a file (if not remembered)
    - Displays passwords in a table with search and delete functionality
    """
    win = tk.Toplevel(root)
    win.title("Your Passwords")
    win.geometry("750x600")

    # Try to load the previously used file path
    file_path = load_password_file_path()

    # If the file no longer exists, ask the user to select a new one
    if file_path and not os.path.exists(file_path):
        file_path = None

    if not file_path:
        file_path = filedialog.askopenfilename(
            title="Select passwords file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

    if not file_path:
        return  # User cancelled

    # Save the selected path for future use
    save_password_file_path(file_path)

    # Load passwords from the selected file
    all_passwords = load_passwords(file_path)

    if not all_passwords:
        tk.Label(win, text="No passwords found.", font=('Arial', 14)).pack(pady=20)
        return

    # --- Search bar ---
    search_frame = ttk.Frame(win)
    search_frame.pack(fill='x', padx=10, pady=10)

    ttk.Label(search_frame, text="Search by service:").pack(side='left', padx=5)

    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side='left', padx=5)

    # --- Password table ---
    tree = ttk.Treeview(win, columns=("Service", "Login", "Password"), show="headings")
    tree.heading("Service", text="Service")
    tree.heading("Login", text="Login / Email")
    tree.heading("Password", text="Password")

    for p in all_passwords:
        tree.insert("", "end", values=(p["service"], p["login"], p["password"]))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Action buttons ---
    btn_frame = ttk.Frame(win)
    btn_frame.pack(fill='x', padx=10, pady=10)

    delete_btn = ttk.Button(btn_frame, text="🗑️ Delete Selected",
                            command=lambda: delete_selected_password(tree, file_path, win))
    delete_btn.pack(side='left', padx=5)

    export_btn = ttk.Button(
        btn_frame,
        text="📤 Export",
        command=lambda: export_passwords(tree, file_path)
    )
    export_btn.pack(side='left', padx=5)


def export_passwords(tree, file_path):
    """Export the current table data to a file."""
    passwords = []
    for row in tree.get_children():
        values = tree.item(row, 'values')
        if values:
            passwords.append({
                "service": values[0],
                "login": values[1],
                "passwords": values[2]
            })

    if not passwords:
        messagebox.showinfo("Export", "No data to export.")
        return

    export_path = filedialog.askopenfilename(
        title="Export passwords",
        defaultextension=".csv",
        filetypes=[
            ("CSV files", "*.csv"),
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("Word files", "*.docx")
        ]
    )

    if not export_path:
        return

    save_passwords(export_path, passwords)

    messagebox.showinfo("Export", f"✅ Exported to: {export_path}")
    

def delete_selected_password(tree, file_path, parent_window):
    """
    Delete the currently selected password from the table and the file.

    - Prompts the user for confirmation before deletion
    - Reloads the file, filters out the selected entry and saves the updated list
    - Removes the row from the table
    """
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a password to delete.", parent=parent_window)
        return

    values = tree.item(selected[0], 'values')
    if not values:
        return

    service, login, password = values

    # Ask for confirmation
    if not messagebox.askyesno("Delete", f"Delete password for '{service}'?", parent=parent_window):
        return

    # Reload passwords, filter out the selected one and save
    all_passwords = load_passwords(file_path)
    new_passwords = [
        p for p in all_passwords
        if not (p['service'] == service and p['login'] == login and p['password'] == password)
    ]
    save_passwords(file_path, new_passwords)

    # Remove the row from the table
    tree.delete(selected[0])


def save_password_file_path(path):
    """
    Save the path to the password file in settings.json.
    """
    data = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            data = {}

        data["passwords_file"] = path

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def load_password_file_path():
    """
    Load the saved password file path from settings.json.
    Returns None if the file doesn't exist or is invalid.
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if content:
                        data = json.loads(content)
                        return data.get("passwords_file")
        except (json.JSONDecodeError, ValueError):
            return None
    return None


def main():
    """Initialize the main application window and run the Tkinter event loop."""
    root = tk.Tk()
    root.title("🔐 Personal Password Generator")
    root.geometry("700x700")
    root.after(1000, check_for_updates)
    root.focus_set()

    # --- Styles ---
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 12), padding=5)

    # --- Main frame ---
    main_frame = ttk.Frame(root, padding='20', borderwidth=0, relief='flat')
    main_frame.pack(fill='both', expand=True)

    # --- View passwords button ---
    view_btn = tk.Button(
        main_frame,
        text="🔍 View Passwords",
        command=lambda: show_passwords(root),
        font=('Arial', 12),
        bg='#9C27B0',
        fg='white',
        padx=15,
        pady=5
    )
    view_btn.pack(pady=5)

    # --- Title ---
    title = ttk.Label(main_frame, text="🔐 Personal Password Generator", font=('Arial', 18, 'bold'))
    title.pack(pady=(0, 15))

    # --- Variables ---
    length_var = tk.IntVar(value=16)
    use_letters = tk.BooleanVar(value=True)
    use_digits = tk.BooleanVar(value=True)
    use_symbols = tk.BooleanVar(value=True)
    password_var = tk.StringVar(value="")
    service_var = tk.StringVar(value="")
    login_var = tk.StringVar(value="")
    theme_var = tk.StringVar(value='light')  # Current theme

    # --- Mouse wheel handler ---
    def on_mouse_wheel(event):
        """Adjust password length using the mouse wheel."""
        if event.widget in (entry_service, entry_email, entry_password):
            return

        current = length_var.get()

        if hasattr(event, 'delta') and event.delta:
            delta = event.delta
            new_value = current + (1 if delta > 0 else -1)
        else:
            if event.num == 4:
                new_value = current + 1
            elif event.num == 5:
                new_value = current - 1
            else:
                return

        if 16 <= new_value <= 64:
            length_var.set(new_value)

    # --- Password generation ---
    def on_generate():
        """Generate a password based on user settings."""
        length = length_var.get()
        letters = use_letters.get()
        digits = use_digits.get()
        symbols = use_symbols.get()

        if not (letters or digits or symbols):
            return password_var.set("⚠️ Select at least one character type.")

        pool = build_character_pool(letters, digits, symbols)
        password = generate_password(length, pool)
        password_var.set(password)

        # Update strength indicator
        strength = check_strength(password)
        if strength == "Not Safe":
            strength_label.config(text="🔴 Not Safe!", fg='red')
        elif strength == 'Moderate':
            strength_label.config(text="🟡 Moderate", fg='orange')
        else:
            strength_label.config(text="🟢 Very Strong!", fg='green')

    # --- Copy password to clipboard ---
    def copy_password():
        """Copy the generated password to clipboard."""
        password = password_var.get()
        if password:
            root.clipboard_clear()
            root.clipboard_append(password)
            password_var.set("✅ Copied!")
            root.after(2000, lambda: password_var.set(password))

    # --- Theme management ---
    def apply_theme(theme):
        """Apply light or dark theme to the entire interface."""
        if theme == 'light':
            top_frame.config(bg='#f0f0f0')
            root.configure(bg='#f0f0f0')
            style.configure('TFrame', background='#f0f0f0')
            style.configure('TLabel', background='#f0f0f0', foreground='black')
            style.configure('TEntry', fieldbackground='#f0f0f0')
            style.configure('TCheckbutton', background='#f0f0f0', foreground='black')
            style.configure('TButton', background='#f0f0f0', foreground='black')
            length_label.config(background='#f0f0f0', foreground='black')

            # Scale
            scale.config(background='#f0f0f0', foreground='black', troughcolor='lightgray')

            # Checkboxes
            style.map('TCheckbutton', background=[('active', '#f0f0f0'), ('selected', '#f0f0f0')])

            # Manual widgets
            strength_label.config(background='#f0f0f0', foreground='black')
            copy_button.config(background='#2196F3', foreground='white')
            save_button.config(background='#FF9800', foreground='white')

            main_frame.configure(style="TFrame")

        if theme == 'dark':
            top_frame.config(bg='#1e1e1e')
            root.configure(background='#1e1e1e')
            style.configure('TFrame', background='#1e1e1e', borderwidth=0, relief='flat')
            style.configure('TCheckbutton', background='#1e1e1e', foreground='white')
            style.configure('TLabel', background='#1e1e1e', foreground='white')
            length_label.config(background='#1e1e1e', foreground='white')
            style.configure('TEntry', fieldbackground='#2d2d2d', foreground='white', insertcolor='white')

            # Scale
            scale.config(background='#1e1e1e', foreground='white', troughcolor='#2b2b2b')

            # Checkboxes
            style.map('TCheckbutton', background=[('active', '#1e1e1e'), ('selected', '#1e1e1e')])

            # Manual widgets
            generate_btn.config(background='#4CAF50', foreground='white')
            strength_label.config(background='#1e1e1e', foreground='white')
            copy_button.config(background='#0d47a1', foreground='white')
            save_button.config(background='#e65100', foreground='white')

            main_frame.configure(style="TFrame")


    def toggle_theme():
        """Switch between light and dark themes."""
        theme_var.get()
        if theme_var.get() == "light":
            theme_var.set('dark')
            apply_theme('dark')
            theme_toggle.config(text="☀️ Light Theme")
        else:
            theme_var.set('light')
            apply_theme('light')
            theme_toggle.config(text="🌙 Dark Theme")


    # --- Save password to file ---
    def save_password():
        """Save the generated password to a file selected by the user."""
        password = password_var.get()
        service = entry_service.get().strip()
        login = entry_email.get().strip()

        if not password:
            return password_var.set("⚠️ Generate a password!")
        if not service:
            return service_var.set("⚠️ Empty a service name!")
        if not login:
            return login_var.set("⚠️ Empty a login/email name!")

        file_path = filedialog.asksaveasfilename(
            title="Save password file",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("Word files", "*.docx")
            ]
        )
        if not file_path:
            return

        save_password_file_path(file_path)

        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(f"Service: {service} | Login/email: {login} | Password: {password}\n")

        password_var.set(f"✅ Saved to: {file_path}")
        service_var.set("")
        login_var.set("")
        root.after(2000, lambda: password_var.set(password))


    # ============================ INTERFACE ELEMENTS ===================================

    # Length mark
    ttk.Label(main_frame, text="Length Password:").pack(anchor='center')

    # Slider
    scale = tk.Scale(
        main_frame,
        from_=16,
        to=64,
        orient="horizontal",
        variable=length_var,
        length=400,
        resolution=1,
        highlightthickness=0,
        troughcolor='lightgray',
    )
    scale.pack(pady=(0, 10))

    # Mouse wheel control linked to the main window
    root.bind("<MouseWheel>", on_mouse_wheel)
    root.bind("<Button-4>", on_mouse_wheel)
    root.bind("<Button-5>", on_mouse_wheel)

    length_label = tk.Label(
        main_frame,
        textvariable=length_var,
        font=("Arial", 12),
        bg='lightgray',
        fg='black',
        highlightthickness=0
    )

    # Checkboxes
    ttk.Checkbutton(main_frame, text="Use Letters", variable=use_letters).pack(anchor='w')
    ttk.Checkbutton(main_frame, text="Use Digits", variable=use_digits).pack(anchor='w')
    ttk.Checkbutton(main_frame, text="Use Symbols", variable=use_symbols).pack(anchor='w', pady=(0, 10))

    # Your service name
    ttk.Label(main_frame, text="Service name:").pack(anchor='w')
    entry_service = tk.Entry(
        main_frame,
        textvariable=service_var,
        width=40,
        font=('Arial', 12),
        bg='white',
        fg='black',
        insertbackground='white',
    )
    entry_service.pack(fill='x', pady=(0, 5))

    # Your login/email
    ttk.Label(main_frame, text="Login or email:").pack(anchor='w')
    entry_email = tk.Entry(
        main_frame,
        textvariable=login_var,
        width=40,
        font=('Arial', 12),
        bg='white',
        fg='black',
        insertbackground='white',
    )
    entry_email.pack(fill='x', pady=(0, 10))

    # Button
    generate_btn = tk.Button(
        main_frame,
        text="🎲 Generate Password",
        command=on_generate,
        font=('Arial', 12),
        bg='#4CAF50',
        fg='white',
        padx=20,
        pady=8
    )
    generate_btn.pack(pady=(10, 5))

    # Password field
    entry_password = tk.Entry(
        main_frame,
        textvariable=password_var,
        width=40,
        font=('Arial', 12),
        bg='white',
        fg='black',
        insertbackground='white',
    )
    entry_password.pack(fill='x', pady=(5, 5))

    # Password strength indicator
    strength_label = tk.Label(
        main_frame,
        text="",
        font=('Arial', 12, 'bold'),
        pady=5,
    )
    strength_label.pack()

    # Copy Button
    copy_button = tk.Button(
        main_frame,
        text="📋 Copy to clipboard",
        command=copy_password,
        font=('Arial', 12),
        bg='#2196F3',
        fg='white',
        padx=15,
        pady=5,
    )
    copy_button.pack(pady=5)

    # Save Button
    save_button = tk.Button(
        main_frame,
        text="💾 Save the password to file",
        command=save_password,
        font=('Arial', 12),
        bg='#FF9800',
        fg='white',
        padx=15,
        pady=5,
    )
    save_button.pack(pady=5)

    # Button Change Theme
    top_frame = tk.Frame(main_frame, borderwidth=0, highlightthickness=0, bg='lightgray')
    top_frame.pack(pady=(0, 15))

    theme_toggle = tk.Button(
        top_frame,
        text="🌙 Dark Theme",
        command=toggle_theme,
        font=('Arial', 12),
        bg='#2196F3',
        fg='white',
        padx=10,
        pady=5,
    )
    theme_toggle.pack(side='right')

    # Launch Window
    apply_theme('light')
    root.mainloop()


if __name__ == "__main__":
    main()
