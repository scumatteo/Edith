import tkinter as tk
from tkinter import Button
from threading import Thread
from builtins import str
import time


class LeaderUserGUI(Thread):
    
    """
        Class that implement the LeaderUser GUI.
    """

    def __init__(self, leader):
        """
            Constructor of this class.
            
            Parameters:
            
            leader: LeaderUser
                The LeaderUser that manage this GUI.
            
        """
        self._leader = leader
        Thread.__init__(self)
        self.start()
        self._active = True
    
    def run(self):
        """
            Method that execute action during the run of the thread.
        """
        self.root = tk.Tk()
        self.root.winfo_toplevel().title("Amministratore " + self._leader._name)
        self.root.protocol("WM_DELETE_WINDOW", self.__callback)
        self.__build_gui()
        while(self._active):
            self.root.update()
            self.__update_gui()
            time.sleep(0.02)
            
    def __update_gui(self): 
        """
            Method that update data in  GUI.
        """
        self.__orders.config(text="Numero di ordini inseriti: " + str(self._leader._countOrders))
        self.__users.config(text="Numero di user al lavoro: " + str(self._leader._countUsers))
    
    def __callback(self):
        """
            Method that are called for quit of the GUI.
        """
        self._active = False
        self.root.quit()
    
    def __is_not_blank (self, myString):
        """
            Method that returns if a string in not blank.
        """
        return bool(myString and myString.strip())
    
    def __add_order(self):
        """
            Method that add order to a system, when the order's button are pressed.
        """
        minTime = self.__timeEntry.get()
        priority = self.__priorityEntry.get()
        if minTime and priority:
            self._leader.add_specific_order(minTime, priority)
    
    def __add_user(self):
        """
            Method that add user to a system, when the user's button are pressed.
        """
        username = self.__userEntry.get()
        if username:
            self._leader.create_user(str(username))
        
    def __build_gui(self):
        """
            Method that build the GUI through the TKinter library.
        """
        self.__frame = tk.Frame(self.root, width=600, height=500)
        self.__frame.pack()
        self.root.resizable(False, False)
        self.__nameLable = tk.Label(self.__frame, font=(50), text="Centro di Controllo di {}".format(self._leader._name))
        self.__nameLable.place(x=300, y=20, anchor="center")
        self.__orderLabel = tk.Label(self.__frame, font=(20), text="Ordine")
        self.__orderLabel.place(x=300, y=60, anchor="center")
        self.__timeLabel = tk.Label(self.__frame, text="Tempo minimo d'esecuzione")
        self.__timeLabel.place(x=100, y=110, anchor="w")
        self.__timeEntry = tk.Entry(self.__frame, font=(20))
        self.__timeEntry.place(x=500, y=110, anchor="e")
        self.__priorityLabel = tk.Label(self.__frame, text="Priorita' dell'ordine")
        self.__priorityLabel.place(x=100, y=140, anchor="w")
        self.__priorityEntry = tk.Entry(self.__frame, font=(20))
        self.__priorityEntry.place(x=500, y=140, anchor="e")
        self.__button = Button(self.__frame, text="Inserimento Ordine", command=self.__add_order)
        self.__button.place(x=300, y=190, anchor="center")
        """
            Implementation of user's insertion.
        """
        self.__userLabel = tk.Label(self.__frame, font=(20), text="Utente")
        self.__userLabel.place(x=300, y=260, anchor="center")
        self.__userEntry = tk.Entry(self.__frame, font=(20))
        self.__userEntry.place(x=100, y=300, anchor="w")
        self.__userButton = Button(self.root, text="Inserimento Utente", command=self.__add_user)
        self.__userButton.place(x=500, y=300, anchor="e")
        """
            Implementation of the system's status.
        """
        self.__statusLabels = tk.Label(self.__frame, font=(10), text="Stato attuale del sistema")
        self.__statusLabels.place(x=300, y=370, anchor="center")
        self.__orders = tk.Label(self.__frame, text="Numero di ordini inseriti: " + str(self._leader._countOrders))
        self.__orders.place(x=250, y=410, anchor="center")
        self.__users = tk.Label(self.__frame, text="Numero di user al lavoro: " + str(self._leader._countUsers))
        self.__users.place(x=250, y=450, anchor="center")
    
