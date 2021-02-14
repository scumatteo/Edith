from gui.UserGUI import UserGUI


class User(object):
    """
    Class that implement a user. 
    """

    def __init__(self, name, jid):
        """
            Constructor.
            
            Parameters:
                
                name: string
                    Name of User.
                
                jid: string
                    The JID of User.
        """
        self._name = name
        self._jid = jid
        self._gui = UserGUI(self._name, self._jid)
        
