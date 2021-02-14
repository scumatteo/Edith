class HistoricalArchive(object):
    """
        Class that models the ranking's historical archive of the GUIs agents.
    """

    def __init__(self):
        """
            Basic constructor.
        """
        self._archive = {}
    
    def set_archive(self, key, value):
        """
            Setter method used to update the archive.
            
            Parameters:
            
            key : time
                The time stamp of the global system.
            value : dictionary
                The actual ranking of the Users.
        """
        self._archive[key] = value
            
