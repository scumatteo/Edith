from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from utils.JIDEnum import JIDEnum
import json
from spade.message import Message
from utils.MessageManager import MessageManager
from spade.template import Template
from utils.LogManager import LogManager
from aioxmpp.structs import PresenceShow, JID


class GUIAgent(Agent):            
        """
            Class that represents an agent that manage a GUI.
        """
    
        def _stop_working(self):
            """
                Method called when the button to notify the job's finish is pressed.
            """
            self._is_working = False 
        
        def _start_working(self):
            """
                Method called when the button to start the job is pressed.
            """
            self._is_working = True   
        
        def _notify_msg_processed(self):      
            """
                Method that confirms that the GUI has shown the dialog when a message from the HighwayAgent is received.
            """
            self._msg_received = False            
    
        class PresenceNotificationBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that updates the presence of the agent
                and subscribe the presence to other agents.
            """ 

            async def on_start(self):
                self.presence.set_available(show=PresenceShow.CHAT)
                self.presence.on_subscribe = self.on_subscribe
                self.presence.on_unsubscribe = self.on_unsubscribe
                self.presence.subscribe(JIDEnum.HIGH.value)  
                self.presence.subscribe(JIDEnum.STAT.value)
                self.work = False
            
            def on_subscribe(self, jid):
                self.presence.approve(jid) 
                self.presence.subscribe(jid)
            
            def on_unsubscribe(self, jid):
                self.presence.unsubscribe(jid)
            
            async def run(self):    
                
                if(self.agent._is_working):
                    if(not self.work):
                        self.presence.subscribe(JIDEnum.TEMP.value)
                        self.work = True
                else:
                    if(self.work):
                        self.presence.unsubscribe(JIDEnum.TEMP.value)
                        self.presence.subscribe(JIDEnum.HIGH.value)
                        self.work = False
            
            async def on_end(self):
                await self.agent.stop()
                   
        class TemporalWorkingBehav(CyclicBehaviour):
            """
                Class that implements a behavior that receive message from TemporalAgent and
                update an internal time.
            """ 

            async def run(self):
                msg = await self.receive(timeout=60)
                if(msg):
                    LogManager.received(self.agent.name)
                    if(self.agent._is_working):
                        self.agent._time += 1  
            
            async def on_end(self):
                await self.agent.stop()
                 
        class GUIStatisticsBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that receive messages from StatisticalAgent 
                and save the statistics to display them on the user interface.
            """
            
            async def run(self):
                msg = await self.receive(timeout=5)
                if(msg):
                    LogManager.received(self.agent.name)
                    stat = json.loads(msg.body)
                    self.agent._ranking = stat["ranking"]
                    self.agent._tot_score = stat["tot_score"]
                    self.agent._avg_time = stat["avg_time"]  
                    self.agent._tot_orders = stat["tot_orders"]    
                    self.agent._errors = stat["errors"]  
            
            async def on_end(self):
                await self.agent.stop()
    
        class GUIWorkingBehav(PeriodicBehaviour):
                
            async def __notify_statistics(self): 
                """
                    Method that informs the subscripted StatisticalAgent about the job just done by this GUIAgent.
                """
                b = MessageManager.get_GUI_to_statistic_message(self._high_message["min_time"],
                                                                  self.agent._time,
                                                                  self._high_message["priority"])
                msg = Message(to=JIDEnum.STAT.value, sender=self.agent._jid, body=b,
                                   metadata={"performative" : "query"})            
                await self.send(msg)
                LogManager.sent(self.agent.name)
                                            
            async def run(self):                  
                msg = await self.receive(timeout=1)
                
                if(msg and not self.agent._is_working): 
                    self._high_message = json.loads(msg.body) 
                    self.agent._msg_received = True
                elif(self.agent._time != 0 and not self.agent._is_working):
                    if(JID.fromstr(JIDEnum.STAT.value) in self.presence.get_contacts()):
                        if("subscription" in self.presence.get_contact(JID.fromstr(JIDEnum.STAT.value))):
                            if(self.presence.get_contact(JID.fromstr(JIDEnum.STAT.value))["subscription"] == "both"):  
                                await self.__notify_statistics()
                    self.agent._time = 0
                    
            async def on_start(self):
                self._high_message = {}  
            
            async def on_end(self):
                await self.agent.stop()               
    
        async def setup(self):
            LogManager.log(self.name, "GUIAgent is starting...")  
            t1 = Template(metadata={"performative" : "inform"})
            t2 = Template(metadata={"performative" : "query"})
            t3 = Template(metadata={"performative" : "temp"})
            gui_presence_behav = self.PresenceNotificationBehav(1)
            gui_stat_behav = self.GUIStatisticsBehav(1)
            gui_work_behav = self.GUIWorkingBehav(1)
            gui_temp_behav = self.TemporalWorkingBehav()
            self.add_behaviour(gui_presence_behav)
            self.add_behaviour(gui_stat_behav, t1)
            self.add_behaviour(gui_work_behav, t2)
            self.add_behaviour(gui_temp_behav, t3)
            
        def __init__(self, *args, **kwargs):
            self._time = 0 
            self._ranking = None
            self._avg_time = None
            self._errors = 0
            self._tot_score = 0
            self._tot_orders = 0
            self._is_working = False
            self._msg_received = False
            self._jid = args[0]
            super().__init__(*args, **kwargs)
            
