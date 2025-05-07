import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Toggle Button Example")

# Initial state tracker
toggled = False

# Create a label with initial text

# Function to toggle text and button color
def toggle():
    global toggled
    if toggled:
        button.config(bg="SystemButtonFace", fg="black", text="Click Me")
    else:
        button.config(bg="green", fg="white", text="Clicked!")
    toggled = not toggled

# Create the button
button = tk.Button(root, text="Click Me", command=toggle, font=("Arial", 12))
button.pack(pady=10)

# Run the application
root.mainloop()
