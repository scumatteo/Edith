import json
from builtins import staticmethod


class MessageManager(object):
    """
        Utility class used to compose the messages to exchange between the agents.
    """

    @staticmethod
    def get_GUI_to_statistic_message(m_t, r_t, p):   
        """
            Static method that returns a JSON. Used to send messages from GUIAgent to StatisticalAgent.
            
            Parameters:
            
            m_t : integer
                Minimum time for the execution of the order.
            
            r_t : integer
                Real time of execution.
            
            p : integer
                Priority of the order. Represents a score.
            
        """
        msg = {"min_time" : m_t, "real_time" : r_t, "priority" : p}
        return json.dumps(msg)
    
    @staticmethod
    def get_statistic_to_GUI_message(r, t_s, a_t, t_o, e):   
        """
            Static method that returns a JSON. Used to send messages from StatisticalAgent to GUIAgent.
            
            Parameters:
            
            r : integer
                Position in the ranking of the GUIAgent's User.
            
            t_s : integer
                Total score accumulated by the GUIAgent's User.
            
            a_t : integer
                Average time of orders' execution of the GUIAgent's User.
            
            t_o : integer
                Total number of orders executed by the GUIAgent's User.
            
        """
        msg = {"ranking": r, "tot_score" : t_s, "avg_time" : a_t, "tot_orders" : t_o, "errors" : e}
        return json.dumps(msg)
    
    @staticmethod
    def get_temporal_message(t, t_s):
        """
            Static method that returns a JSON. Used by TemporalAgent to notify other agent about the 
            system's global time.
            
            Parameters:
            
            t : integer
                Global time calculate in seconds.
            
            t_s : time
                Global time stamp.
            
        """  
        msg = {"time" : t, "time_stamp" : t_s}
        return json.dumps(msg)
    
    @staticmethod
    def get_statistic_to_highway_message(r):  
        """
            Static method that returns a JSON. Used by StatisticalAgent to send messages to HighwayAgent.
            
            Parameters:
            
            r : dictionary
                Ranking of the Users.
            
        """   
        msg = {"ranking": r}
        return json.dumps(msg)
    
    @staticmethod
    def get_order_message(m_t, p):   
        """
            Static method that returns a JSON. Used by HighwayAgent to send messages to GUIAgents and 
            by CentralOrderAgent to send messages to HighwayAgent.
            
            Parameters:
            
            m_t : integer
                Minimum time for the execution of the order.
            
            p : integer
                Priority of the order. Represents a score.
            
        """  
        msg = {"min_time" : m_t, "priority" : p}
        return json.dumps(msg)
