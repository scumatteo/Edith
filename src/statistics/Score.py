class Score(object):
    """
        Class that models the concept of score.
    """

    def __init__(self, r, m, p):
        """
            Constructor of the class.
            
            Parameters:
            
            r : integer
                The real time of execution of the order.
            m : integer
                The minimum time for the execution of the order
            p : integer
                The priority of the execution, that corresponds to a score.
            
            The score is negative if the real time of execution is less than the minimum time. It raise an error.     
        """
        if(r > 0):
            self._score = m * p / r
        else:
            self._score = m * p
        if(r < m):
            self._score = -self._score
