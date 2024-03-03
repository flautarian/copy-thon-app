
import tkinter

class FloatingMessage(tkinter.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.withdraw()  # Hide the window initially
        self.attributes('-alpha', 0.8)  # Set transparency level
        self.overrideredirect(True)  # Remove window decorations
        self.config(bg='green')  # Set background color
        
        # Create and place the label with the message
        self.label = tkinter.Label(self, text=message, fg='white', bg='green', padx=10, pady=5)
        self.label.pack()
        
        # Calculate middle of the current screen and setting message box in middle top
        screen_width = self.winfo_screenwidth()
        x = screen_width // 2 - self.winfo_width() // 2
        self.geometry(f'+{x}+0')
        
        # Make the window stay on top
        self.attributes('-topmost', True)
        
    def show(self):
        # Show the floating message window
        self.deiconify()

    def hide(self):
        # Hide the floating message window
        self.withdraw()