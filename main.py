import EventHandler
import Root 
import InputFrame
import OutputFrame

def main(): 
    # Setting event handler 
    event_handler = EventHandler.EventHandler()
    # Configuring the main app to have the event handler 
    main_window = Root.Root(event_handler)
    # Configuring the input frame. 
    input_frame = InputFrame.InputFrame(main_window.root, event_handler)
    input_frame.pack(side="left", fill="y", expand=True) #, padx=5, pady=5)
    # # Configuring the output frame. 
    output_frame = OutputFrame.OutputFrame(main_window.root, event_handler)
    output_frame.pack(side="left", fill="y", expand=True) #, padx=5, pady=5)
    # Running window 
    main_window.root.mainloop()
    

if __name__ == "__main__": 
    main()

# TODO: Try to make better formatting algo? 
#       Make the entire app responsive? Probably not 