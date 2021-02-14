from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from datetime import datetime
from utils.MessageManager import MessageManager
from spade.message import Message
from utils.LogManager import LogManager
from aioxmpp.structs import PresenceShow


class TemporalAgent(Agent):
        """
            Class that represents an agent that maintains the global time of the system.
        """
        
        class PresenceNotificationBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that updates the presence of the agent
                and subscribe the presence to other agents.
            """ 

            async def on_start(self):
                self.presence.set_available(show=PresenceShow.CHAT)
                self.presence.on_subscribe = self.on_subscribe
                self.presence.on_unsubscribe = self.on_unsubscribe
                
            def on_subscribe(self, jid):
                self.presence.approve(jid) 
                self.presence.subscribe(jid)
            
            def on_unsubscribe(self, jid):
                self.presence.unsubscribe(jid)
            
            async def run(self):
                return
                
            async def on_end(self):
                await self.agent.stop()                    
                              
        class TemporalBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that sends messages to the subscripted agents, to notify the time.
            """   

            async def run(self):
                self.agent._time_stamp = str(datetime.now())
                for c in self.presence.get_contacts():
                    if("subscription" in self.presence.get_contact(c)):
                        if(self.presence.get_contact(c)["subscription"] == "both"):
                            msg = Message(to=str(c), sender=self.agent._jid,
                                          body=MessageManager.get_temporal_message(self.agent._time, self.agent._time_stamp),
                                            metadata={"performative" : "temp"})
                            await self.send(msg)
           
                self.agent._time += 1
            
            async def on_end(self):
                await self.agent.stop()
        
        async def setup(self):
            LogManager.log(self.name, "TemporalAgent starting...")   
            temp_presence_behav = self.PresenceNotificationBehav(1)  
            temporal_behav = self.TemporalBehav(1)
            self.add_behaviour(temp_presence_behav)
            self.add_behaviour(temporal_behav)
        
        def __init__(self, *args, **kwargs):
            self._time = 0
            self._time_stamp = None
            self._jid = args[0]
            super().__init__(*args, **kwargs)
            
