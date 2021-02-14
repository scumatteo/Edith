from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from statistics.Historical import HistoricalArchive
from statistics.Score import Score
import json
from statistics.StatisticsCalculator import StatisticsCalculator
from utils.MessageManager import MessageManager
from utils.JIDEnum import JIDEnum
from spade.message import Message
from spade.template import Template
from utils.LogManager import LogManager
from aioxmpp.structs import PresenceShow, JID


class StatisticalAgent(Agent):
        """
            Class that represents an agent who processes statistics.
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
                self.presence.subscribe(JIDEnum.TEMP.value)
                self.presence.subscribe(JIDEnum.HIGH.value)
            
            def on_subscribe(self, jid):
                self.presence.approve(jid) 
                self.presence.subscribe(jid)
                if("guiagent" in jid):
                    self.agent._gui.append(jid)
                self.agent._executed_orders[jid] = 0
            
            def on_unsubscribe(self, jid):
                self.presence.unsubscribe(jid)
                 
            async def run(self):
                return
            
            async def on_end(self):
                await self.agent.stop()
    
        class TimeReceiverBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that receives messages from the TemporalAgent. 
            """

            async def run(self):
                msg = await self.receive(timeout=2)
                if msg:
                    self.agent._time = json.loads(msg.body)                 
                                
            async def on_end(self):
                await self.agent.stop()
    
        class StatisticalBehav(PeriodicBehaviour):
            """
                Class that implements a behavior that receives messages from a GUIAgent and updates the global
                statistics.
                Then notifies the subscripted agents of the changes.
            """

            async def __notify_gui(self):
                """
                    Method that sends statistics to all the subscripted GUIAgents.
                """
                for jid in self.agent._gui:
                    b = MessageManager.get_statistic_to_GUI_message(self.agent._statistics.get_ranking_by_name(jid),
                                                            self.agent._statistics.get_tot_score_by_name(jid),
                                                            self.agent._statistics.get_avg_time_by_name(jid),
                                                            self.agent._executed_orders[jid],
                                                            self.agent._statistics.get_errors_by_name(jid))
                    msg = Message(to=jid, sender=self.agent._jid,
                                  body=b, metadata={"performative" : "inform"})
                    await self.send(msg)
                    LogManager.sent(self.agent.name)
            
            async def __notify_highway(self):
                """
                    Method that sends statistics to the subscripted HighwayAgent.
                """
                b = MessageManager.get_statistic_to_highway_message(self.agent._statistics._ranking)   
                msg = Message(to=JIDEnum.HIGH.value, sender=self.agent._jid,
                                  body=b, metadata={"performative" : "stat"})
                await self.send(msg)
                LogManager.sent(self.agent.name)
  
            async def run(self): 
                msg = await self.receive()
                if msg:
                    gm = json.loads(msg.body) 
                    gui_jid = str(msg.sender)       
                    if(gui_jid not in self.agent._executed_orders):
                        self.agent._executed_orders[gui_jid] = 0
                    self.agent._executed_orders[gui_jid] += 1                 
                    score = Score(int(gm["real_time"]), int(gm["min_time"]), int(gm["priority"]))  
                    self.agent._statistics.calculate_avg_time(int(gm["real_time"]),
                                                self.agent._executed_orders[gui_jid],
                                                gui_jid)   
                    self.agent._statistics.calculate_tot_score(gui_jid, score)     
                    self.agent._statistics.calculate_ranking()
                    if(self.presence.get_contact(JID.fromstr(gui_jid))["subscription"] == "both"):
                        await self.__notify_gui()
                    
                    if(self.presence.get_contact(JID.fromstr(JIDEnum.HIGH.value))["subscription"] == "both"):    
                        await self.__notify_highway()
                
                if(self.agent._time):
                    if(self.agent._time["time"] % 60 == 0):  # aggiorna lo storico ogni 60 secondi
                        self.agent._historical.set_archive(self.agent._time["time_stamp"], self.agent._statistics._ranking)
            
            async def on_end(self):
                await self.agent.stop()
            
        async def setup(self):
            LogManager.log(self.name, "StatisticalAgent starting...") 
            t1 = Template(metadata={"performative" : "temp"})
            t2 = Template(metadata={"performative" : "query"})
            stat_presence_behav = self.PresenceNotificationBehav(1)
            time_rec_behav = self.TimeReceiverBehav(1)
            statistic_behav = self.StatisticalBehav(1)
            self.add_behaviour(stat_presence_behav)
            self.add_behaviour(time_rec_behav, t1)
            self.add_behaviour(statistic_behav, t2)   
        
        def __init__(self, *args, **kwargs):
            self._historical = HistoricalArchive()
            self._statistics = StatisticsCalculator()
            self._jid = args[0]
            self._time = {}
            self._executed_orders = {}
            self._gui = []
            super().__init__(*args, **kwargs)
            
