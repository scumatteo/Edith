import tkinter as tk
from tkinter import Button
from tkinter.constants import  DISABLED, ACTIVE
from threading import Thread
import time
from gui.MessageDialog import MessageDialog
from agent.AgentFactory import AgentFactory


class UserGUI(Thread):    
    """
        A simple GUI for a User.
    """

    def __init__(self, name, jid):
        self._factory = AgentFactory()
        self._username = name
        self._agent = self._factory.create_gui_agent(jid, "edith")
        self._agent.start()
        time.sleep(3)
        self._active = True
        Thread.__init__(self)
        self.start()

    def __callback(self):
        """
            Callback that establishes a policy of closure.
        """
        self.root.quit()
 
    def run(self):  
        self.root = tk.Tk()
        self.root.winfo_toplevel().title(f"GUI di {self._username}")
        self.root.protocol("WM_DELETE_WINDOW", self.__callback)
        self.__build_gui() 
        while(self._active):
            self.root.update()
            self.__update_gui()
            time.sleep(0.02)
              
    def __update_gui(self): 
        """
            Method that update the GUI state, according to the corresponding GUIAgent.
        """
        if(self._agent._msg_received):
            mydialog = MessageDialog(self.root, self._username)
            self.root.wait_window(mydialog.top)            
            self._agent._notify_msg_processed() 
            self._agent._start_working()
                 
        if(self._agent._is_working):
            self.__cronosLabel.config(text="Hai iniziato ad eseguire un ordine!")
            self.__secondsLabel.config(text="Secondi impiegati: {}".format(self._agent._time))
            if(self._agent._time > 0):
                self.__button.config(state=ACTIVE)
                          
        else:
            self.__secondsLabel.config(text="")
            self.__cronosLabel.config(text="Non stai eseguendo nessun ordine.")
            self.__button.config(state=DISABLED) 
        
        self.__rankValue.config(text=self._agent._ranking)
        self.__avgtimeValue.config(text=self._agent._avg_time)
        self.__scoreValue.config(text=self._agent._tot_score)
        self.__nordValue.config(text=self._agent._tot_orders)
        self.__errorsValue.config(text=self._agent._errors)
    
    def __build_gui(self):
        """
            Method that contains all the elements of the GUI. It's used to build the GUI when the class is created.
        """
        self.__frame = tk.Frame(self.root, width=600, height=400)
        self.__frame.pack()
        self.root.resizable(False, False)
        self.__nameLable = tk.Label(self.__frame, font=(50), text="Postazione di {}".format(self._username))
        self.__nameLable.place(x=300, y=20, anchor="center")
        self.__cronosLabel = tk.Label(self.__frame, font=(20), text="Non stai eseguendo nessun ordine.")
        self.__cronosLabel.place(x=300, y=60, anchor="center")
        self.__secondsLabel = tk.Label(self.__frame, font=(20), text="")
        self.__secondsLabel.place(x=300, y=100, anchor="center")
        self.__button = Button(self.root, text="Ordine completato", command=self._agent._stop_working, state=DISABLED)
        self.__button.place(x=300, y=140, anchor="center")
        self.__statLabels = tk.Label(self.__frame, font=(10), text="Le tue statistiche")
        self.__statLabels.place(x=300, y=200, anchor="center")
        self.__rank = tk.Label(self.__frame, text="Il tuo ranking: ")
        self.__rank.place(x=260, y=230, anchor="center")
        self.__rankValue = tk.Label(self.__frame, text="0")
        self.__rankValue.place(x=320, y=230, anchor="center")
        self.__avgtime = tk.Label(self.__frame, text="Tempo medio di esecuzione(s): ")
        self.__avgtime.place(x=215, y=260, anchor="center")
        self.__avgtimeValue = tk.Label(self.__frame, text="0")
        self.__avgtimeValue.place(x=320, y=260, anchor="center")
        self.__score = tk.Label(self.__frame, text="Score totale: ")
        self.__score.place(x=265, y=290, anchor="center")
        self.__scoreValue = tk.Label(self.__frame, text="0")
        self.__scoreValue.place(x=320, y=290, anchor="center")
        self.__nord = tk.Label(self.__frame, text="Numero di ordini eseguiti: ")
        self.__nord.place(x=229, y=320, anchor="center")
        self.__nordValue = tk.Label(self.__frame, text="0")
        self.__nordValue.place(x=320, y=320, anchor="center")
        self._errors = tk.Label(self.__frame, text="Numero di errori: ")
        self._errors.place(x=254, y=350, anchor="center")
        self.__errorsValue = tk.Label(self.__frame, text="0")
        self.__errorsValue.place(x=320, y=350, anchor="center")
