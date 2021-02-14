from utils.Order import Order
from random import seed
from random import randint
from user.User import User
from gui.LeaderUserGUI import LeaderUserGUI


class LeaderUser(object):
    """
        Class that implements the user, who can add order and manage the GUI Agent in the system.
    """

    def __init__(self, name, central):
        """
            Constructor with parameters.
            
            Parameters:
            
            name : string
                The name of leader user.
                
            central : CentralOrderAgent
                The reference of central order .
        """
        self._name = name
        self._countOrders = 0
        self._countUsers = 0
        self._cn = central
        self.users = []
        self._gui = LeaderUserGUI(self)
        
    def add_random_order(self):
        """
            Method that create ten random order and insert this in CentralOrdernAgent.
        """
        seed(1)
        for _ in range(10):
            self._countOrders += 1
            self._cn.insert_order(Order(randint(0, 99), randint(0, 20)))
        
    def add_specific_order(self, min_execution_time, priority):
        """
            Method that create a specific order.
            
            Parameters:
            
            min_execution_time : integer
                The minimum execution time of the order.
                
            priority : integer
                The priority of the order.
        """
        self._countOrders += 1
        self._cn.insert_order(Order(min_execution_time, priority))
    
    def create_user(self, name):
        """
            Method that create a new user.
            
            Parameters:
            
            name : string
                The name of the user.
        """
        self._countUsers += 1
        self.users.append(User(name, "guiagent" + str(self._countUsers) + "@616.pub"))
        
