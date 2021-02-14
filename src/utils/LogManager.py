class LogManager(object):
    """
        Utility class used to print on console.
    """
    
    @staticmethod
    def log(name, msg):
        """
            Static method that prints on console.
            
            Parameters:
            
            name : string
                The agent's name.
            msg : string
                The message to print.
        """
        print(f"{name} - {msg}")   
    
    @staticmethod
    def received(name):
        """
            Static method that prints on console.
            
            Parameters:
            
            name : string
                The agent's name.            
        """
        print(f"{name} - Message received!")
    
    @staticmethod
    def sent(name):
        """
            Static method that prints on console.
            
            Parameters:
            
            name : string
                The agent's name.            
        """
        print(f"{name} - Message sent!")
