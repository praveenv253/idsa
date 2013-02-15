from random import expovariate as expdistr

class Event(object):
    """
    Class to describe an event.
    
    Attributes include:
    - inter-arrival time
    - service time
    """
    
    def __init__(self, *args):
        if args[0] is False:
            # Externally set inter-arrival time and service time
            self.inter_arrival_time = args[1]
            self.service_time = args[2]
        else:
            # Internally set inter-arrival time and service time.
            # In this case, arguments are the respective parameters for the
            # two exponential distributions.
            self.inter_arrival_time = _inter_arrival_time(args[0])
            self.service_time = _service_time(args[1])
    
    def _inter_arrival_time(self, mar):
        # mar is the mean arrival time
        # Inter-arrival time is exponential, with parameter 1/mar
        return expdistr(1 / float(mar))
    
    def _service_time(self, ast):
        # ast is the average service time
        # Service times are also exponential, with parameter 1/ast
        return expdistr(1 / float(ast))
    
    def __repr__(self):
        return unicode((self.inter_arrival_time, self.service_time))
