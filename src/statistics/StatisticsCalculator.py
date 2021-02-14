class StatisticsCalculator(object):
    
    """
        Class that manage calculations of the statistics.
    """

    def __init__(self):
        """
            Simple constructor.
        """
        self._ranking = {}
        self._tot_time = {}
        self._tot_score = {}
        self._avg_time = {}
        self._errors = {}
    
    def __truncate(self, number, decimal):
        """
            Method that truncates a long float.
            
            
            Parameters:
            
            number: float
                The number that must be truncated.
            
            decimal: integer
                The number of decimal digit.
        """
        score_str = str(number).split(".")
        return float(score_str[0] + "." + score_str[1][:decimal])
    
    def calculate_avg_time(self, t, n, j):
        """
            Method that calculate the average time of execution.
            
            
            Parameters:
            
            t: integer
                The time of execution of the last order.
            
            n: integer
                The number of orders executed by this GUIAgent.
            
            j: string
                The JID of the GUIAgent that executed the order.
        """
        if(j not in self._tot_time):
            self._tot_time[j] = t
        else:
            self._tot_time[j] = self._tot_time[j] + t
        self._avg_time[j] = self.__truncate(self._tot_time[j] / n, 2)
        
    def calculate_tot_score(self, n, s):
        """
            Method that calculate the total score and, if any, errors.
            
            
            Parameters:
            
            n : string
                The JID of the GUIAgent that executed the order.
            
            s : Score
                The score calculated on the last order executed.
        """
        if(n not in self._errors):
            self._errors[n] = 0
        if(s._score < 0):
            self._errors[n] += 1    
        if(n not in self._tot_score):
            self._tot_score[n] = self.__truncate(s._score, 2)     
        else:
            self._tot_score[n] = self.__truncate(self._tot_score[n] + s._score, 2)     
        if self._tot_score[n] < 0:
            self._tot_score[n] = 0
            
    def calculate_ranking(self):
        """
            Method that computes the ranking of the GUIAgents.
        """
        self._ranking = {}
        i = 1
        sort = self._tot_score = {k: v for k, v in sorted(self._tot_score.items(), key=lambda item: item[1], reverse=True)}
        for k in sort:
            self._ranking[i] = k
            i += 1
            
    def get_tot_time_by_name(self, n):
        """
            Method that returns the total time of execution by name.
            
            
            Parameters:
            
            n : string
                The JID of the GUIAgent.
        """
        if(n in self._tot_time):
            return self._tot_time[n]
    
    def get_avg_time_by_name(self, n):
        """
            Method that returns the average time of execution by name.
            
            
            Parameters:
            
            n : string
                The JID of the GUIAgent.
        """
        if(n in self._avg_time):
            return self._avg_time[n] 
    
    def get_tot_score_by_name(self, n):
        """
            Method that returns the total score accumulated by name.
            
            
            Parameters:
            
            n : string
                The JID of the GUIAgent.
        """
        if(n in self._tot_score):
            return self._tot_score[n]
    
    def get_errors_by_name(self, n):
        """
            Method that returns the number of errors by name.
            
            
            Parameters:
            
            n : string
                The JID of the GUIAgent.
        """
        if(n in self._errors):
            return self._errors[n] 
        return 0
    
    def get_ranking_by_name(self, n):
        """
            Method that returns the ranking by name.
            
            
            Parameters:
            
            n : string
                The JID of the GUIAgent.
        """
        for key, value in self._ranking.items(): 
            if(n == value): 
                return key 
        
