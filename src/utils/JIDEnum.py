import enum 


class JIDEnum(enum.Enum):
    """
        Enumeration that store the fixed JID of the system's agents.
    """
    
    __server = "@616.pub"
    
    TEMP = "temporalagent" + __server
    STAT = "statisticalagent" + __server
    HIGH = "highwayagent" + __server
    CENT = "centralorderagent" + __server
        
