from spade.agent import Agent
import json
from utils.Order import Order
from spade.behaviour import PeriodicBehaviour
from utils.MessageManager import MessageManager
from spade.message import Message
from utils.JIDEnum import JIDEnum
from spade.template import Template
from aioxmpp.structs import PresenceShow
from builtins import str
from utils.LogManager import LogManager


class HighwayAgent(Agent):
        
    """
        Class that represents an agent who dispatches order from CentralOrderAgent to GuiAgent.
    """
    
    def _first_available_in_ranking(self):
        """
            Method that returns the JID of the first available GUI Agent from all.
        """
        if(not self._ranking):
            return self._listAvaibleAgent.pop()
        
        else:
            for i in self._ranking:
                r = self._ranking[i]
                if r in self._listAvaibleAgent:
                    self._listAvaibleAgent.remove(r)
                    print(r)
                    return r
            
    class PresenceNotificationBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that updates the presence of the agent
                and subscribe the presence to other agents.
            """ 

            async def on_start(self):
                self.presence.set_available(show=PresenceShow.CHAT)
                self.presence.on_subscribe = self.on_subscribe
                self.presence.on_unsubscribe = self.on_unsubscribe
                self.presence.subscribe(JIDEnum.CENT.value)
                
            def on_subscribe(self, jid):
                self.presence.approve(jid) 
                self.presence.subscribe(jid)
            
            def on_unsubscribe(self, jid):
                self.presence.unsubscribe(jid)
            
            async def run(self):
                self.agent._listAvaibleAgent = []
                for c in self.presence.get_contacts():
                    if("guiagent" in str(c)):
                        if("subscription" in self.presence.get_contact(c)):
                            if(self.presence.get_contact(c)["subscription"] == "both"):
                                self.agent._listAvaibleAgent.append(str(c))
              
            async def on_end(self):
                await self.agent.stop()
    
    class ReceiveOrderBehav(PeriodicBehaviour):
        """
            Class that implements a behavior that receives messages from the CentralOrderAgent. 
        """

        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                LogManager.received(self.agent.name)
                tm = json.loads(msg.body)
                self.agent._orders.append(Order(tm["min_time"], tm["priority"]))
        
        async def on_end(self):
            await self.agent.stop()

    class ReceiveRankingBehav(PeriodicBehaviour):
        """
            Class that implements a behavior that receives messages from the StatisticalAgent. 
        """

        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                LogManager.received(self.agent.name)
                tm = json.loads(msg.body)
                self.agent._ranking = tm["ranking"]
              
        async def on_end(self):
            await self.agent.stop()
          
    class SwitchOrderBehav(PeriodicBehaviour):
        """
            Class that implements a behavior that switch the order trough the GUIAgent. 
        """

        async def run(self):
            if(self.agent._listAvaibleAgent):
                if(self.agent._orders):
                    order = self.agent._orders.pop()
                    b = MessageManager.get_order_message(order._min_execution_time, order._priority)

                    if self.agent._simpleSwitching:
                        jid = self.agent._listAvaibleAgent.pop()
                        msg = Message(to=jid, sender=self.agent._jid, body=b,
                                      metadata={"performative": "query"})
                        self.presence.unsubscribe(jid)
                    else :
                        jid = str(self.agent._first_available_in_ranking())
                        msg = Message(to=jid, sender=self.agent._jid, body=b,
                                      metadata={"performative": "query"})
            
                    await self.send(msg)
                    LogManager.sent(self.agent.name)
                    self.presence.unsubscribe(jid)
        
        async def on_end(self):
            await self.agent.stop()
            
    async def setup(self):
        LogManager.log(self.name, "HighwayAgent is starting...")
        high_presence_behav = self.PresenceNotificationBehav(1)  
        self.add_behaviour(high_presence_behav)
        t1 = Template(metadata={"performative" : "query"})
        receiveOrderBehav = self.ReceiveOrderBehav(1) 
        self.add_behaviour(receiveOrderBehav, t1) 
        t3 = Template(metadata={"performative" : "stat"})
        receiveRankingBehav = self.ReceiveRankingBehav(1)
        self.add_behaviour(receiveRankingBehav, t3)  
        simpleSwitchOrderBehav = self.SwitchOrderBehav(1)
        self.add_behaviour(simpleSwitchOrderBehav) 
    
    def __init__(self, *args, **kwargs):
        self._orders = []
        self._lastLenght = 0
        self._jid = args[0]
        self._simpleSwitching = False
        self._listAvaibleAgent = []
        self._ranking = {}
        super().__init__(*args, **kwargs)
        
