
import tkinter

class FloatingMessage(tkinter.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.withdraw()  # Hide the window initially
        self.attributes('-alpha', 0.8)  # Set transparency level
        self.overrideredirect(True)  # Remove window decorations
        self.config(bg='black')  # Set background color
        
        # Create and place the label with the message
        self.label = tkinter.Label(self, text=message, fg='white', bg='black', padx=10, pady=5)
        self.label.pack()
        
        # Update position on mouse movement
        self.bind('<Motion>', self.update_position)
        
        # Make the window stay on top
        self.attributes('-topmost', True)

    def update_position(self, event):
        # Update the window position based on mouse coordinates
        x, y = event.x_root, event.y_root
        self.geometry(f'+{x}+{y}')
        
    def show(self):
        # Show the floating message window
        self.deiconify()

    def hide(self):
        # Hide the floating message window
        self.withdraw()