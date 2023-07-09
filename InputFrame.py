import dark_mode_theme as col
import EventHandler 
import tkinter as tk 
import pyperclip 

class InputFrame(tk.Frame):
    def __init__(self, parent, event_handler): 
        super().__init__(parent, bg="#FFE194", width=400, height=400) # Yellow
        self.event_handler = event_handler 
        self.input_text = ""

        # Input Box Wrapper 
        self.input_box_wrapper = tk.Frame(self, 
                                          width=400, 
                                          height=360, 
                                          bg="#A3CFA7") # Green "#A3CFA7"
        self.input_box_wrapper.grid(row=0, column=0, sticky="nsew")
        self.input_box_wrapper.grid_propagate(False) # Textbox frame will not take up a crazy amount of space
        self.grid_rowconfigure(0, weight=1, minsize=360) # input_box_wrapper will stretch if needed
        # Configure grid options for text box
        self.input_box_wrapper.columnconfigure(0, weight=1)
        self.input_box_wrapper.rowconfigure(0, weight=1)

        # Text Box 
        self.input_box = tk.Text(self.input_box_wrapper, #padx=5, pady=5
                                 bg=col.dark_bg, 
                                 fg=col.dark_fg, 
                                 insertbackground=col.dark_fg, 
                                 selectbackground=col.dark_highlight)
        self.input_box.grid(row=0, column=0)
        self.input_box.bind("<Configure>", self.on_configure)

        # Button Wrapper 
        self.button_wrapper = tk.Frame(self, 
                                       width=400, 
                                       height=40, 
                                       bg=col.dark_highlight, padx=5) # pady=5
        self.button_wrapper.grid(row=1, column=0, sticky="nsew")
        self.button_wrapper.columnconfigure(0, weight=1, minsize=200)
        self.button_wrapper.columnconfigure(1, weight=1, minsize=200)
        self.button_wrapper.rowconfigure(0, weight=1, minsize=40)

        # Paste & Clear Buttons 
        self.paste_button = tk.Button(self.button_wrapper, 
                                      text="Paste", 
                                      font=("Consolas", 10), 
                                      height=1, 
                                      bg=col.dark_bg, 
                                      fg=col.dark_fg, 
                                      relief=tk.RIDGE, 
                                      command=self.begin_paste_event) # Publishes "PASTE_EVENT"
        self.paste_button.grid(row=0, column=0)

        self.clear_button = tk.Button(self.button_wrapper, 
                                      text="Clear", 
                                      font=("Consolas", 10), 
                                      height=1, 
                                      bg=col.dark_bg, 
                                      fg=col.dark_fg, 
                                      relief=tk.RIDGE, 
                                      command=self.begin_clear_event)
        self.clear_button.grid(row=0, column=1)

        # Subscribing to events 
        self.event_handler.subscribe("WINDOW_CHANGE_EVENT", self.grow_textbox_size) # When receiving this signal, textbox size will change
        self.event_handler.subscribe("WINDOW_CLEAR_EVENT", self.shrink_textbox_size)

    # Functions 
    def begin_paste_event(self): 
        """
        Clears text box & inputs contents from clipboard onto the text box. 
        Publishes PASTE_EVENT which then begins sequence of events that take place 
        after the "Paste" button is clicked. 
        """
        self.input_box.delete("1.0", tk.END)
        content = pyperclip.paste() 
        self.input_text = content 
        self.input_box.insert(tk.END, content)
        print("\nInputFrame: PASTE_EVENT - published")
        # Publish event 
        self.event_handler.publish('PASTE_EVENT',data=self.input_text)

    def begin_clear_event(self): 
        """
        Starts the chain of events that takes place when the clear 
        button is pressed. 
        """
        self.input_box.delete("1.0", tk.END)
        print("\nInputFrame: CLEAR_EVENT - published")
        self.event_handler.publish('CLEAR_EVENT')

    def on_configure(self, event): 
        width = event.width 
        max_width = 200  # Maximum width for the text box
         # Adjust the width and height if they exceed the maximum values
        if width > max_width:
            self.input_box.configure(width=max_width)

    def grow_textbox_size(self, event, data): 
        """
        Grows the textbox when the contents of the output frame requires the window to grow.
        Just eyecandy. 
        """
        new_window_height = data
        new_textbox_height = new_window_height - self.button_wrapper.winfo_reqheight() 
        if (new_textbox_height > 360): 
            self.input_box.configure(height=new_textbox_height)

    def shrink_textbox_size(self, event, data): 
        """
        Grows the textbox when the contents of the output frame requires the window to grow.
        Just eyecandy. 
        """
        print("I am here now")
        print("INPUTFRAME: shrink_textbox_size")
        if (self.input_box.winfo_reqheight() > 360): 
            self.input_box.configure(height=360)