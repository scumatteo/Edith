import unittest
from agent.CentralOrderAgent import CentralOrderAgent
from utils.Order import Order
from user.LeaderUser import LeaderUser
from agent.StatisticalAgent import StatisticalAgent
from agent.TemporalAgent import TemporalAgent
from agent.GUIAgent import GUIAgent
from agent.HighwayAgent import HighwayAgent
import time
from random import randint
from user.User import User
from utils.JIDEnum import JIDEnum

class TestCentralOrderMethods(unittest.TestCase):
    """
        Class that test if CentralOrder's method correctly work.
    """
       
    def setUp(self):
        """
            Setup.
        """
        self.central = CentralOrderAgent(JIDEnum.CENT.value, "edith")
        self.lu = LeaderUser("Big Boss", self.central)
      
    def test_insert_remove_clean_historycal_order(self):
        self.central.insert_order(Order(103, 2))
        self.central.insert_order(Order(10, 12))
        self.assertEqual(self.central.count_orders(), 2)
        self.central.clean_orders()
        self.assertEqual(self.central.count_orders(), 0)
        self.central.insert_order(Order(10, 12))
        self.assertEqual(self.central.count_orders(), 1)
        self.central.remove_order_at(0)
        self.assertEqual(self.central.count_orders(), 0)
        self.assertNotEqual(self.central.get_hystorical_orders(), 0)
         
    def test_LeaderUser_insert_remove_order(self):
        self.central.clean_orders()
        self.lu.add_random_order()
        self.assertEqual(self.central.count_orders(), 10)
         
    def tearDown(self):
        """
            Stop agent.
        """
        self.central.stop()

           
class TestStatisticalAgent(unittest.TestCase): 
    """
        Class that test if StatisticalAgent correctly work.
    """

    def setUp(self):
        """
            Setup.
        """
        self.s_jid = JIDEnum.STAT.value
        self.stat = StatisticalAgent(self.s_jid, "edith")  
        self.temp = TemporalAgent(JIDEnum.TEMP.value, "edith")
        self.temp.start()
        self.stat.start() 
        
    def test_initialization(self):  
        self.assertDictEqual(self.stat._statistics._ranking, {}) 
        self.assertDictEqual(self.stat._historical._archive, {})
        self.assertDictEqual(self.stat._time, {})
        self.assertEqual(self.stat._jid, self.s_jid)
        
    def test_time_receive(self):    
        time.sleep(2) 
        self.assertTrue(self.stat._time)       
       
    def tearDown(self):
        """
            Stop agent.
        """
        self.stat.stop()
        self.temp.stop()
     
           
class TestGUI(unittest.TestCase):    
    """
        Class that test if GUIAgent correctly work.
    """

    def setUp(self):
        """
            Setup.
        """
        self.jid = "guiagent0@616.pub"
        self.user = User("Luca", self.jid)
       
    def test_initialization(self):          
        time.sleep(5)
        self.assertEqual(self.user._gui._agent._jid, self.jid)  
       
    def test_thread(self):  
        self.assertTrue(self.user._gui.is_alive())
           
    def tearDown(self):
        self.user._gui._agent.stop()
           
   
class TestTemporalAgent(unittest.TestCase):

    def setUp(self):
        """
            Setup.
        """
        self.temp = TemporalAgent(JIDEnum.TEMP.value, "edith")
        self.temp.start()
           
    def test_initialization(self):
        self.assertEqual(self.temp._time, 0)
           
    def tearDown(self):
        """
            Stop agent.
        """
        self.temp.stop()

   
class TestCentralToHighToGUIAgent(unittest.TestCase): 
    """
        Class that test if communication from CentralOrderAgent to GUIAgent correctly work.
    """

    def setUp(self):
        """
            Setup.
        """
        self.cent = CentralOrderAgent(JIDEnum.CENT.value, "edith")  
        self.high = HighwayAgent(JIDEnum.HIGH.value, "edith")
        self.gui = GUIAgent("guiagent2@616.pub", "edith")
        self.cent.start()
        time.sleep(2) 
        self.high.start()
        time.sleep(2)
        self.gui.start() 
        time.sleep(2)
       
    def test_receive(self):  
        self.assertEqual(self.cent._orders, []) 
        self.assertEqual(self.cent._historyOrders, [])
        self.cent.insert_order(Order(12, 2))
        self.cent.insert_order(Order(12, 3))
        self.assertEqual(self.cent._orders.__len__(), 2)
        time.sleep(5) 
        self.assertNotEqual(self.cent._orders.__len__(), 2)
        self.assertNotEqual(self.high._orders.__len__(), 0)  
        time.sleep(5)
        self.assertTrue(self.gui._msg_received)
        self.assertEqual(self.high._orders.__len__(), 1) 
  
    def tearDown(self):
        """
            Stop agent.
        """
        self.cent.stop()
        self.high.stop()
        self.gui.stop()
 
          
class TestCentralSortedToHighToGUIAgent(unittest.TestCase): 
    """
        Class that test if CentralOrderAgen sort the orders and if HighwayAgent dispatcher correctly work.
    """

    def setUp(self):
        """
            Setup.
        """
        self.cent = CentralOrderAgent(JIDEnum.CENT.value, "edith")  
        self.high = HighwayAgent(JIDEnum.HIGH.value, "edith")
        self.gui = GUIAgent("guiagent1@616.pub", "edith")
        self.cent.start()
        time.sleep(2) 
        self.high.start()
        time.sleep(2)
        self.gui.start() 
        time.sleep(2)
      
    def test_receive(self):  
        self.assertEqual(self.cent._orders, []) 
        self.assertEqual(self.cent._historyOrders, [])
        for i in range(15):
            self.cent.insert_order(Order(randint(0, 99), i))
        self.assertEqual(self.cent.get_order_at(0)._priority, 0)
        self.assertEqual(self.cent._orders.__len__(), 14)
        time.sleep(2) 
        self.assertNotEqual(self.cent.get_order_at(0)._priority, 0)
        self.assertNotEqual(self.cent._orders.__len__(), 15)
        self.assertNotEqual(self.high._orders.__len__(), 0)  
        time.sleep(5)
        self.assertTrue(self.gui._msg_received)
        self.assertNotEqual(self.high._orders.__len__(), 0) 
 
    def tearDown(self):
        """
            Stop agent.
        """
        self.cent.stop()
        self.high.stop()
        self.gui.stop()

 
class TestTemporalToGUIAgent():    
    """
        Class that test if TemporalAgent and GUIAGent work correctly.
    """

    def setUp(self):
        """
            Setup.
        """
        self.jid = "guiagent0@616.pub"
        self.gui = GUIAgent(self.jid, "edith") 
        self.temp = TemporalAgent(JIDEnum.TEMP.value, "edith") 
        self.temp.start()
        self.gui.start()
      
    def test_working_time(self):  
        time.sleep(2)
        self.gui._is_working = True
        time.sleep(5)
        self.assertEqual(self.gui._time, 5)
          
    def tearDown(self):
        """
            Stop agent.
        """
        self.gui.stop()
        self.temp.stop()


if __name__ == '__main__':
    unittest.main()
    
    
