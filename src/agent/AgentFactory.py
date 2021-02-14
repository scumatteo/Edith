from agent.CentralOrderAgent import CentralOrderAgent
from agent.HighwayAgent import HighwayAgent
from agent.TemporalAgent import TemporalAgent
from agent.StatisticalAgent import StatisticalAgent
from agent.GUIAgent import GUIAgent


class AgentFactory(object):
    """
        Class that implements the design pattern Factory and represents a factory for the agents.
    """

    def create_central_order_agent(self, jid, password):
        """
            Method that returns a CentralOrderAgent.
            
            Parameters:
                
                jid : string
                    The JID of the agent.
                password : string
                    The password of the agent.
        """
        return CentralOrderAgent(jid, password)
    
    def create_highway_agent(self, jid, password):
        """
            Method that returns a HighwayAgent.
            
            Parameters:
                
                jid : string
                    The JID of the agent.
                password : string
                    The password of the agent.
        """
        return HighwayAgent(jid, password)
    
    def create_temporal_agent(self, jid, password):
        """
            Method that returns a TemporalAgent.
            
            Parameters:
                
                jid : string
                    The JID of the agent.
                password : string
                    The password of the agent.
        """
        return TemporalAgent(jid, password)
    
    def create_statistical_agent(self, jid, password):
        """
            Method that returns a StatisticalAgent.
            
            Parameters:
                
                jid : string
                    The JID of the agent.
                password : string
                    The password of the agent.
        """
        return StatisticalAgent(jid, password)
    
    def create_gui_agent(self, jid, password):
        """
            Method that returns a GUIAgent.
            
            Parameters:
                
                jid : string
                    The JID of the agent.
                password : string
                    The password of the agent.
        """
        return GUIAgent(jid, password)
        
