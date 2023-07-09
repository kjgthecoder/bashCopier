class EventHandler: 
    def __init__(self):
        self.methods = {}

    def subscribe(self, event, method):
        """
        Adds class function to an array associated with Key Event. 
        """
        if event not in self.methods:
            self.methods[event] = []
        self.methods[event].append(method)

    def publish(self, event, data=None):
        """
        Every time an event is published, we go through and invoke each class function 
        that we associated with that key_event. 
        """
        if event in self.methods:
            for class_function in self.methods[event]:
                class_function(event, data)

