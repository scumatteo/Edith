class Order(object):
    """
        Class that implement an order object.
    """

    def __init__(self, min_execution_time, priority):
        """
            Constructor.
            
            
            Parameters:
            
            min_execution_time : integer
                The minimum execution time of the order.
                
            priority : integer
                The priority of the order.
        """
        self._min_execution_time = min_execution_time
        self._priority = priority
