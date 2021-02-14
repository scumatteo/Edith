from user.LeaderUser import LeaderUser
from utils.JIDEnum import JIDEnum
from agent.AgentFactory import AgentFactory
import time

if __name__ == '__main__':
    pwd = "edith"
    factory = AgentFactory()
    t = factory.create_temporal_agent(JIDEnum.TEMP.value, pwd)
    t.start()
    time.sleep(2)
    c = factory.create_central_order_agent(JIDEnum.CENT.value, pwd)
    l = LeaderUser("Jeff Bezos", c)
    c.start()
    time.sleep(2)
    h = factory.create_highway_agent(JIDEnum.HIGH.value, pwd)
    h.start()
    time.sleep(2)
    s = factory.create_statistical_agent(JIDEnum.STAT.value, pwd)
    s.start()
