import tkinter as tk


class MessageDialog(object):
    """
        A class used to represents a message dialog.
    
    """

    def __init__(self, parent, name):
        """
            Constructor that builds the dialog.
            
            Parameters:
            
            parent : TKinter
                The root of the GUI.
                
            name : string
                The name of the GUI's User.
        
        """

        top = self.top = tk.Toplevel(parent)
        self.top.resizable(False, False)
        self.top.winfo_toplevel().title(f"Messaggio per {name}")
        tk.Label(top, text="NUOVO ORDINE", font=(20)).pack()
        tk.Label(top, text="{} hai ricevuto un nuovo ordine da eseguire. ".format(name) + 
                                      "Clicca ok per iniziare a eseguire l'ordine.", padx=10).pack()
        
        b = tk.Button(top, text="OK", command=self.__ok, width=20)
        b.pack(pady=5)
        self.top.protocol("WM_DELETE_WINDOW", self.__callback)
        
    def __callback(self):
        """
            Callback that establishes a policy of closure.
        """
        self.top.quit()

    def __ok(self):
        """
            Callback called when the OK button is pressed.
        
        """
        self.top.destroy()
        
