import tkinter as tk
from tkinter import messagebox, ttk

# Functions
def add_bartender():
    bartender_frame = tk.Frame(bartenders_container, bg="#f7f7f7", padx=5, pady=5)
    bartender_frame.pack(fill="x", pady=2)
    
    name_entry = tk.Entry(bartender_frame, width=20, font=("Arial", 12), bd=2, relief="groove", justify="right")
    name_entry.pack(side="right", padx=5, pady=5)
    
    hours_entry = tk.Entry(bartender_frame, width=10, font=("Arial", 12), bd=2, relief="groove", justify="right")
    hours_entry.pack(side="right", padx=5, pady=5)
    
    remove_button = tk.Button(bartender_frame, text="X", command=lambda: bartender_frame.destroy(), bg="#ff4444", fg="white", font=("Arial", 10), bd=0)
    remove_button.pack(side="left", padx=5, pady=5)
    
    bartenders_entries.append((name_entry, hours_entry))

def add_waiter():
    waiter_frame = tk.Frame(waiters_container, bg="#f7f7f7", padx=5, pady=5)
    waiter_frame.pack(fill="x", pady=2)
    
    name_entry = tk.Entry(waiter_frame, width=20, font=("Arial", 12), bd=2, relief="groove", justify="right")
    name_entry.pack(side="right", padx=5, pady=5)
    
    hours_entry = tk.Entry(waiter_frame, width=10, font=("Arial", 12), bd=2, relief="groove", justify="right")
    hours_entry.pack(side="right", padx=5, pady=5)
    
    remove_button = tk.Button(waiter_frame, text="X", command=lambda: waiter_frame.destroy(), bg="#ff4444", fg="white", font=("Arial", 10), bd=0)
    remove_button.pack(side="left", padx=5, pady=5)
    
    waiters_entries.append((name_entry, hours_entry))

def calculate_tips():
    try:
        total_tips = float(tip_entry.get())
        is_weekend = weekend_var.get()

        # Get bartenders' data
        bartender_hours = {}
        for name_entry, hours_entry in bartenders_entries:
            name = name_entry.get().strip()
            hours = hours_entry.get().strip()
            if name and hours:
                bartender_hours[name] = float(hours)

        # Get waiters' data
        waiter_hours = {}
        for name_entry, hours_entry in waiters_entries:
            name = name_entry.get().strip()
            hours = hours_entry.get().strip()
            if name and hours:
                waiter_hours[name] = float(hours)

        # Calculate bartenders' share
        bartender_ratio = 0.15 if is_weekend else 0.12
        bartender_total = total_tips * bartender_ratio
        total_bartender_hours = sum(bartender_hours.values())
        bartender_share = {name: (hours / total_bartender_hours) * bartender_total for name, hours in bartender_hours.items()}

        # Calculate restaurant's share
        remaining_tips = total_tips - bartender_total
        total_waiter_hours = sum(waiter_hours.values())
        waiter_rate = remaining_tips / total_waiter_hours if total_waiter_hours > 0 else 0
        restaurant_ratio = 0.17 if waiter_rate > 90 else 0.15
        restaurant_share = remaining_tips * restaurant_ratio

        # Calculate waiters' share
        waiters_total = remaining_tips - restaurant_share
        waiter_share = {name: (hours / total_waiter_hours) * waiters_total for name, hours in waiter_hours.items()}

        # Display results
        result_text = f"הפרשה לברמנים: {bartender_total:.2f} ש\"ח ({bartender_ratio * 100:.0f}%)\n"
        result_text += f"הפרשה למסעדה: {restaurant_share:.2f} ש\"ח ({restaurant_ratio * 100:.0f}%)\n"
        result_text += f"טיפ שקיבלו המלצרים (בסך הכל): {waiters_total:.2f} ש\"ח\n"
        result_text += f"כמה כסף יצא לשעה: {waiter_rate:.2f} ש\"ח\n"
        result_text += "\nכמה קיבל כל מלצר:\n"
        for name, share in waiter_share.items():
            result_text += f"{name}: {share:.2f} ש\"ח\n"
        result_text += "\nכמה קיבל כל ברמן:\n"
        for name, share in bartender_share.items():
            result_text += f"{name}: {share:.2f} ש\"ח\n"

        result_label.config(text=result_text, bg="#ffffff", fg="#333333", justify="right", font=("Arial", 12))
    except ValueError as e:
        messagebox.showerror("שגיאה", "נא למלא את כל השדות בצורה נכונה.")

# Main window
root = tk.Tk()
root.title("מחשבון טיפים משודרג")
root.geometry("500x700")
root.configure(bg="#f0f0f0")

# Tip amount
tip_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
tip_frame.pack(fill="x")

tk.Label(tip_frame, text="סכום הטיפ:", bg="#f0f0f0", font=("Arial", 12), anchor="e").pack(side="right")
tip_entry = tk.Entry(tip_frame, width=20, font=("Arial", 12), bd=2, relief="groove", justify="right")
tip_entry.pack(side="right", padx=10)

# Weekend checkbox
weekend_var = tk.BooleanVar()
tk.Checkbutton(root, text="סוף שבוע", variable=weekend_var, bg="#f0f0f0", font=("Arial", 12), anchor="e").pack(pady=5)

# Bartenders section
bartenders_frame = tk.LabelFrame(root, text="ברמנים", bg="#f0f0f0", font=("Arial", 12), padx=10, pady=10)
bartenders_frame.pack(fill="x", padx=10, pady=10)

bartenders_entries = []
bartenders_container = tk.Frame(bartenders_frame, bg="#f0f0f0")
bartenders_container.pack(fill="x", padx=5, pady=5)

tk.Button(bartenders_frame, text="הוסף ברמן", command=add_bartender, bg="#4CAF50", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

# Waiters section
waiters_frame = tk.LabelFrame(root, text="מלצרים", bg="#f0f0f0", font=("Arial", 12), padx=10, pady=10)
waiters_frame.pack(fill="x", padx=10, pady=10)

waiters_entries = []
waiters_container = tk.Frame(waiters_frame, bg="#f0f0f0")
waiters_container.pack(fill="x", padx=5, pady=5)

tk.Button(waiters_frame, text="הוסף מלצר", command=add_waiter, bg="#4CAF50", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

# Calculate button
tk.Button(root, text="חשב", command=calculate_tips, bg="#2196F3", fg="white", font=("Arial", 14), bd=0, padx=20, pady=10).pack(pady=10)

# Results
result_label = tk.Label(root, text="", bg="#ffffff", fg="#333333", justify="right", font=("Arial", 12), bd=2, relief="groove", padx=10, pady=10)
result_label.pack(fill="x", padx=10, pady=10)

# Start the main loop
root.mainloop()