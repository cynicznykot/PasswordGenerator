import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from generator import build_character_pool, generate_password, check_strength


def main():
    # Create a window
    root = tk.Tk()
    root.title("Your Personal Password Generator")
    root.geometry("700x600")

    # Create variables
    length_var = tk.IntVar(value=16)
    use_letters = tk.BooleanVar(value=True)
    use_digits = tk.BooleanVar(value=True)
    use_symbols = tk.BooleanVar(value=True)
    password_var = tk.StringVar(value="")


    def on_generate():
        # Retrieving values
        length = length_var.get()
        letters = use_letters.get()
        digits = use_digits.get()
        symbols = use_symbols.get()

        # Type checking
        if not (letters or digits or symbols):
            password_var.set("⚠️ Select at least one character type.")
            return

        # Func generated password
        pool = build_character_pool(letters, digits, symbols)
        password = generate_password(length, pool)
        # Final result
        password_var.set(password)

        # Password strength indicator
        strength = check_strength(password)
        if strength == "Not Safe":
            strength_label.config(text="🔴 Not Safe!", fg="red")
        elif strength == "Moderate":
            strength_label.config(text="🟡 Moderate", fg="orange")
        else:
            strength_label.config(text="🟢 Very Strong!", fg="green")


    def copy_password():
        password = password_var.get()
        if password:
            root.clipboard_clear()
            root.clipboard_append(password)
            password_var.set("✅ Copied!")
            root.after(2000, lambda: password_var.set(password))


    def save_password():
        password = password_var.get()
        service = entry_service.get().strip()

        if not password:
            password_var.set("⚠️ Generate a password first!")
            return

        if not service:
            password_var.set("⚠️ Enter a service name!")

        # File selection dialog
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
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"Service: {service} | Password: {password}\n")

        password_var.set(f"✅ Saved to: {file_path}")
        entry_service.delete(0, tk.END)
        root.after(2000, lambda: password_var.set(password))


    # ---- INTERFACE ELEMENTS ----

    # Length mark
    Label_length = tk.Label(root, text="Length Password:", font=("Arial", 15))
    Label_length.pack(pady=5)

    # Slider
    scale = tk.Scale(root, from_=15, to=64, orient="horizontal", variable=length_var, length=500)
    scale.pack(pady=5)

    # Checkboxes
    check_letters = tk.Checkbutton(root, text="Use Letters", variable=use_letters, font=("Arial", 13))
    check_letters.pack(pady=5)

    check_digits = tk.Checkbutton(root, text="Use Digits", variable=use_digits, font=("Arial", 13))
    check_digits.pack(pady=5)

    check_symbols = tk.Checkbutton(root, text="Use Symbols", variable=use_symbols, font=("Arial", 13))
    check_symbols.pack(pady=5)

    # Your service name

    label_service = tk.Label(root, text="Your Service name:", font=("Arial", 15))
    label_service.pack(pady=5)

    entry_service = tk.Entry(root, width=40, font=("Arial", 15))
    entry_service.pack(pady=5)

    # Button
    button = tk.Button(root, text="Generate Password", command=on_generate, font=("Arial", 17))
    button.pack(pady=5)

    # Password field
    entry = tk.Entry(root, textvariable=password_var, width=70, font=("Arial", 12), justify="center")
    entry.pack(pady=15)
    entry.pack(pady=15)
    entry.pack()

    # Password strength indicator
    strength_label = tk.Label(
        root,
        text="",
        font=("Arial", 12, "bold"),
        pady=5,
    )

    strength_label.pack()

    copy_button = tk.Button(
        root,
        text="📋 Copy to clipboard",
        command=copy_password,
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        padx=15,
        pady=5,
    )
    copy_button.pack(pady=5)

    save_button = tk.Button(
        root,
        text="💾 Save the password to file",
        command=save_password,
        font=("Arial", 12),
        bg="#FF9800",
        fg="white",
        padx=15,
        pady=5,
    )

    save_button.pack(pady=5)

    # Launch window
    root.mainloop()


if __name__ == "__main__":
    main()