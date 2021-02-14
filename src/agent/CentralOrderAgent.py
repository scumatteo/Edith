from spade.agent import Agent
from utils.JIDEnum import JIDEnum
from spade.behaviour import PeriodicBehaviour
from utils.MessageManager import MessageManager
from spade.message import Message
from aioxmpp import PresenceShow
from utils.LogManager import LogManager


class CentralOrderAgent(Agent):
    """
            Class that represents an agent who receives orders from the leader and sort these.
    """
    
    def get_orders(self):
        
        """
            Method that returns a list of actual orders. 
            
        """  
        return self._orders.copy()
    
    def get_hystorical_orders(self):
        
        """
            Method that returns a list of whole orders that system has computed. 
            
        """  
        return self._historyOrders.copy()
        
    def get_order_at(self, index):
        """
            Method that returns a list of actual order. 
            
            Parameters:
            
            index : integer
                Index of the order in list.
        """
        return self._orders.pop(index)
    
    def count_orders(self):
        """
            Method that returns the number of actual order. 
            
        """
        return self._orders.__len__()
    
    def remove_order_at(self, index):
        """
            Method for removes order from system. 
            
            Parameters:
            
            index : integer
                Index of order to remove.
        """
        return self._orders.remove(self._orders.__getitem__(index))
    
    def insert_order(self, order):
        """
            Method for insert order in the system. 
            
            Parameters:
            
            order : Order
                Order to add.
        """
        self._orders.append(order)
        self._historyOrders.append(order)
        
    def clean_orders(self):
        """
            Method for remove all orders. 
            
        """
        self._orders.clear()
        
    class PresenceNotificationBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that control the availability of HighwayAgent through 
                the SPADE's Presence Notification.
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
                for c in self.presence.get_contacts():
                    if(str(c) == JIDEnum.HIGH.value):
                        if("subscription" in self.presence.get_contact(c)):
                            if(self.presence.get_contact(c)["subscription"] == "both"):
                                self.agent._highwayAvailable = True
                            else:
                                self.agent._highwayAvailable = False
                    
            async def on_end(self):
                await self.agent.stop()

    class SortBehav(PeriodicBehaviour):
        """
                Class that implements a behavior that sorts order in the list when a new order was added.
                Orders are sort using priority as key. 
        """
             
        async def on_start(self):
            self.agent._lastLength = self.agent._orders.__len__()

        async def run(self):
            
            def myFunc(e):
                return e._priority 
            
            length = self.agent._orders.__len__()
            if length >= self.agent._lastLength and length > 2 :
                self.agent._orders.sort(key=myFunc, reverse=True)
                self.agent._lastLength = length 
            else:
                self.agent._lastLength = length
        
        async def on_end(self):
            await self.agent.stop()

    class SendOrderBehav(PeriodicBehaviour):
        """
            Class that implements a behavior that sends messages from a HighwayAgent.
        """

        async def run(self):
            if self.agent._highwayAvailable:
                if self.agent._orders.__len__() > 0:
                    o = self.agent.get_order_at(0)
                    b = MessageManager.get_order_message(o._min_execution_time,
                                                              o._priority)
                    msg = Message(to=JIDEnum.HIGH.value, sender=self.agent._jid, body=b,
                                  metadata={"performative" : "query"})
                    await self.send(msg)
                    LogManager.sent(self.agent.name)
        
        async def on_end(self):
            await self.agent.stop()
        
    async def setup(self):
        self._orders = []
        self._historyOrders = []
        self._lastLenght = 0
        self._highwayAvailable = False
        self._jid = JIDEnum.CENT.value
        LogManager.log(self.name, "CentralOrderAgent is starting...")
        cent_presence_behav = self.PresenceNotificationBehav(1)  
        self.add_behaviour(cent_presence_behav)
        
        sort_behav = self.SortBehav(1)
        self.add_behaviour(sort_behav)
        send_behav = self.SendOrderBehav(1)
        self.add_behaviour(send_behav)
    
    def __init__(self, *args, **kwargs):
        self._orders = []
        self._historyOrders = []
        self._lastLenght = 0
        self._highwayAvailable = False
        self._jid = args[0]
        super().__init__(*args, **kwargs)
        
