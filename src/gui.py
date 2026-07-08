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

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from src.generator import build_character_pool, generate_password, check_strength


def main():
    # Create a Window
    root = tk.Tk()
    root.title("🔐 Personal Password Generator")
    root.geometry("700x600")
    # root.configure(bg='#f0f0f0')

    # Setting Styles
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 12), padding=5)
    # style.configure('TFrame', background='#f0f0f0')

    # Main Frame
    main_frame = ttk.Frame(root, padding='20')
    main_frame.pack(fill='both', expand=True)

    # Headline
    title = ttk.Label(main_frame, text="🔐 Personal Password Generator", font=('Arial', 18, 'bold'))
    title.pack(pady=(0, 15))

    # Create Variables
    length_var = tk.IntVar(value=16)
    use_letters = tk.BooleanVar(value=True)
    use_digits = tk.BooleanVar(value=True)
    use_symbols = tk.BooleanVar(value=True)
    password_var = tk.StringVar(value="")
    service_var = tk.StringVar(value="")
    login_var = tk.StringVar(value="")


    def on_generate():
        # Retrieving Values
        length = length_var.get()
        letters = use_letters.get()
        digits = use_digits.get()
        symbols = use_symbols.get()

        # Type Checking
        if not (letters or digits or symbols):
            return password_var.set("⚠️ Select at least one character type.")

        # Func Generated Password
        pool = build_character_pool(letters, digits, symbols)
        password = generate_password(length, pool)
        password_var.set(password)

        # Password Strength Indicator
        strength = check_strength(password)
        if strength == "Not Safe":
            strength_label.config(text="🔴 Not Safe!", fg='red')
        elif strength == 'Moderate':
            strength_label.config(text="🟡 Moderate", fg='orange')
        else:
            strength_label.config(text="🟢 Very Strong!", fg='green')


    def copy_password():
        # Copied Password
        password = password_var.get()
        if password:
            root.clipboard_clear()
            root.clipboard_append(password)
            password_var.set("✅ Copied!")
            root.after(2000, lambda: password_var.set(password))


    def save_password():
        # Save Password
        password = password_var.get()
        service = entry_service.get().strip()
        login = entry_email.get().strip()

        if not password:
            return password_var.set("⚠️ Generate a password!")

        if not service:
            return service_var.set("⚠️ Empty a service name!")

        if not login:
            return login_var.set("⚠️ Empty a login/email name!")


        # File Selection Dialog
        file_path = filedialog.asksaveasfilename(
            title="Save password file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="password.txt" # Default name for the file
        )

        # If the user clicked cancel - we exit
        if not file_path:
            return

        # Saving to the selected file
        with open(file_path, 'a', encoding="utf-8") as file:
            file.write(f"Service: {service} | Login/email: {login} | Password: {password}\n")

        password_var.set(f"✅ Saved to: {file_path}")
        service_var.set("")
        login_var.set("")
        root.after(2000, lambda: password_var.set(password))


    # ---- INTERFACE ELEMENTS ----

    # Length mark
    ttk.Label(main_frame, text="Length Password:").pack(anchor='center')

    # Slider
    scale = tk.Scale(main_frame, from_=16, to=64, orient="horizontal", variable=length_var, length=400, resolution=1)
    scale.pack(fill='x', pady=(0, 10))
    ttk.Label(main_frame, textvariable=length_var, font=('Arial', 12)).pack()

    # Checkboxes
    ttk.Checkbutton(main_frame, text="Use Letters", variable=use_letters).pack(anchor='w')
    ttk.Checkbutton(main_frame, text="Use Digits", variable=use_digits).pack(anchor='w')
    ttk.Checkbutton(main_frame, text="Use Symbols", variable=use_symbols).pack(anchor='w', pady=(0, 10))

    # Your service name
    ttk.Label(main_frame, text="Service name:").pack(anchor='w')
    entry_service = ttk.Entry(main_frame, textvariable=service_var, width=30, font=('Arial', 11))
    entry_service.pack(fill='x', pady=(0, 5))

    # Your login/email
    ttk.Label(main_frame, text="Login or email:").pack(anchor='w')
    entry_email = ttk.Entry(main_frame, textvariable=login_var, width=30, font=('Arial', 11))
    entry_email.pack(fill='x', pady=(0, 10))

    # Button
    generate_btn = ttk.Button(main_frame, text="🎲 Generate Password", command=on_generate)
    generate_btn.pack(pady=(10, 5))

    # Password field
    entry_password = ttk.Entry(main_frame, textvariable=password_var, width=40, font=('Arial', 12))
    entry_password.pack(fill='x', pady=(5, 5))

    # Password strength indicator
    strength_label = tk.Label(
        main_frame,
        text="",
        font=('Arial', 12, 'bold'),
        pady=5,
    )

    strength_label.pack()

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

    # Launch Window
    root.mainloop()


if __name__ == "__main__":
    main()
