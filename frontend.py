import tkinter as tk
from tkinter import messagebox, ttk
from delete import delete_user
from input_user import insert_user
from utils import fetch_comparison_results, fetch_highest_total, fetch_lifter_stats

def add_user():
    try:
        username = username_entry.get()
        password = password_entry.get()
        sex = sex_combobox.get()
        competition_type = competition_combobox.get()
        federation = federation_entry.get()

        # Validate and convert numeric fields
        body_weight = float(body_weight_entry.get())
        deadlift = float(deadlift_entry.get())
        bench = float(bench_entry.get())
        squat = float(squat_entry.get())
        weight_class = weight_class_entry.get()

        # Pass validated inputs to the `insert_user` function
        cid, username = insert_user(username, password, sex, competition_type, body_weight, deadlift, bench, squat, weight_class, federation)

        # Use the custom message dialog
        show_custom_message(
            "Success", 
            f"User {username} added successfully!\nCompetitor ID: {cid}"
        )
    except ValueError as ve:
        messagebox.showerror("Input Error", f"Invalid numeric value entered: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



def delete_existing_user():
    try:
        c_id = delete_user_entry.get()
        delete_user(c_id)
        messagebox.showinfo("Success", f"User with C_ID {c_id} deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def format_results(results):
    """
    Formats the results into a readable string.

    Args:
        results (list): List of tuples containing the query results.

    Returns:
        str: Formatted string of results.
    """
    formatted_rows = []
    for row in results:
        # Replace 'nan' with 'N/A' for better readability
        row = [value if value is not None and str(value) != 'nan' else 'N/A' for value in row]
        
        formatted_row = (
            f"C_ID: {row[0]}, Rank: {row[1]}, Equipped: {row[2]}, Date: {row[3]}, "
            f"Deadlift: {row[4]}, Bench: {row[5]}, Squat: {row[6]}, "
            f"Weight Class: {row[7]}, Total: {row[8]}, GLP: {row[9]}, Federation: {row[10]}"
        )
        formatted_rows.append(formatted_row)
    return "\n\n".join(formatted_rows)

def fetch_comparison():
    try:
        user_id = comparison_user_entry.get()
        results = fetch_comparison_results(user_id)
        if results:
            # Format results for readability
            formatted_results = format_results(results)
            show_custom_message("Comparison Results", formatted_results)
        else:
            messagebox.showinfo("Comparison Results", "No data found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def show_custom_message(title, message):
    """
    Displays a custom dialog with a larger text area for longer messages.

    Args:
        title (str): The title of the dialog.
        message (str): The message to display in the dialog.
    """
    dialog = tk.Toplevel()
    dialog.title(title)

    # Make the dialog resizable
    dialog.geometry("500x400")

    # Add a text widget for the message
    text_area = tk.Text(dialog, wrap="word", padx=10, pady=10)
    text_area.insert("1.0", message)
    text_area.config(state="disabled")  # Make the text read-only
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    # Add an OK button to close the dialog
    ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
    ok_button.pack(pady=10)

    # Center the dialog
    dialog.transient(root)  # Tie dialog to the main window
    dialog.grab_set()  # Make dialog modal


def fetch_highest_total_gui():
    try:
        results = fetch_highest_total()
        if results:
            # If results is a list, extract the first tuple
            if isinstance(results, list) and results:
                results = results[0]  # Get the first tuple

            # Unpack the tuple
            c_id, name, total = results
            # Format the output message
            formatted_message = f"Highest total is {name} (C_ID {c_id}) with a {total:.1f} total."
            # Use custom dialog for the message
            show_custom_message("Highest Total", formatted_message)
        else:
            show_custom_message("Highest Total", "No data found.")
    except Exception as e:
        show_custom_message("Error", f"An error occurred: {e}")



def fetch_lifter_stats_gui():
    try:
        user_id = stats_user_entry.get()
        results = fetch_lifter_stats(user_id)
        if results:
            # Unpack the tuple from the results
            for row in results:
                bench, deadlift, squat = row
                formatted_results = (
                    f"Bench: {bench} kilos\n"
                    f"Deadlift: {deadlift} kilos\n"
                    f"Squat: {squat} kilos"
                )
                # Show the formatted message
                messagebox.showinfo("Lifter Stats", formatted_results)
        else:
            messagebox.showinfo("Lifter Stats", "No data found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Tkinter GUI setup

root = tk.Tk()
root.title("LiftMaster Management System")

# Make the window wider
root.geometry("800x600")  # Adjust width and height

# Add User Section (Left Column)
add_user_frame = tk.Frame(root, padx=10, pady=10)
add_user_frame.grid(row=0, column=0, sticky="n")

tk.Label(add_user_frame, text="Add User").grid(row=0, column=0, columnspan=2, pady=(10, 5))

tk.Label(add_user_frame, text="Username").grid(row=1, column=0, sticky="e", padx=(10, 5))
username_entry = tk.Entry(add_user_frame)
username_entry.grid(row=1, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Password").grid(row=2, column=0, sticky="e", padx=(10, 5))
password_entry = tk.Entry(add_user_frame, show="*")
password_entry.grid(row=2, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Sex").grid(row=3, column=0, sticky="e", padx=(10, 5))
sex_combobox = ttk.Combobox(add_user_frame, values=["M", "F"])
sex_combobox.grid(row=3, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Competition Type").grid(row=4, column=0, sticky="e", padx=(10, 5))
competition_combobox = ttk.Combobox(add_user_frame, values=[
    "classic_powerlifting", "equipped_powerlifting", "classic_bench_press", "equipped_bench_press"
])
competition_combobox.grid(row=4, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Federation").grid(row=5, column=0, sticky="e", padx=(10, 5))
federation_entry = tk.Entry(add_user_frame)
federation_entry.grid(row=5, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Body Weight").grid(row=6, column=0, sticky="e", padx=(10, 5))
body_weight_entry = tk.Entry(add_user_frame)
body_weight_entry.grid(row=6, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Deadlift").grid(row=7, column=0, sticky="e", padx=(10, 5))
deadlift_entry = tk.Entry(add_user_frame)
deadlift_entry.grid(row=7, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Bench").grid(row=8, column=0, sticky="e", padx=(10, 5))
bench_entry = tk.Entry(add_user_frame)
bench_entry.grid(row=8, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Squat").grid(row=9, column=0, sticky="e", padx=(10, 5))
squat_entry = tk.Entry(add_user_frame)
squat_entry.grid(row=9, column=1, padx=(5, 10))

tk.Label(add_user_frame, text="Weight Class").grid(row=10, column=0, sticky="e", padx=(10, 5))
weight_class_entry = tk.Entry(add_user_frame)
weight_class_entry.grid(row=10, column=1, padx=(5, 10))

tk.Button(add_user_frame, text="Add User", command=add_user, height=1, width=15).grid(row=11, column=0, columnspan=2, pady=10)

# Other Functionality Section (Right Column)
other_functions_frame = tk.Frame(root, padx=10, pady=10)
other_functions_frame.grid(row=0, column=1, sticky="n")

# Delete User Section
tk.Label(other_functions_frame, text="Delete User").grid(row=0, column=0, columnspan=2, pady=(10, 5))

tk.Label(other_functions_frame, text="C_ID").grid(row=1, column=0, sticky="e", padx=(10, 5))
delete_user_entry = tk.Entry(other_functions_frame)
delete_user_entry.grid(row=1, column=1, padx=(5, 10))

tk.Button(other_functions_frame, text="Delete User", command=delete_existing_user, height=1, width=15).grid(row=2, column=0, columnspan=2, pady=10)

# Fetch Comparison Results Section
tk.Label(other_functions_frame, text="Fetch Comparison Results").grid(row=3, column=0, columnspan=2, pady=(20, 5))

tk.Label(other_functions_frame, text="User ID").grid(row=4, column=0, sticky="e", padx=(10, 5))
comparison_user_entry = tk.Entry(other_functions_frame)
comparison_user_entry.grid(row=4, column=1, padx=(5, 10))

tk.Button(other_functions_frame, text="Fetch Comparison", command=fetch_comparison, height=1, width=15).grid(row=5, column=0, columnspan=2, pady=10)

# Fetch Highest Total Section
tk.Label(other_functions_frame, text="Fetch Highest Total").grid(row=6, column=0, columnspan=2, pady=(20, 5))
tk.Button(other_functions_frame, text="Fetch Highest Total", command=fetch_highest_total_gui, height=1, width=15).grid(row=7, column=0, columnspan=2, pady=10)

# Fetch Lifter Stats Section
tk.Label(other_functions_frame, text="Fetch Lifter Stats").grid(row=8, column=0, columnspan=2, pady=(20, 5))

tk.Label(other_functions_frame, text="User ID").grid(row=9, column=0, sticky="e", padx=(10, 5))
stats_user_entry = tk.Entry(other_functions_frame)
stats_user_entry.grid(row=9, column=1, padx=(5, 10))

tk.Button(other_functions_frame, text="Fetch Stats", command=fetch_lifter_stats_gui, height=1, width=15).grid(row=10, column=0, columnspan=2, pady=10)

root.mainloop()

