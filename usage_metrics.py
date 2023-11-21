from datetime import datetime

class Usage_Metrics:
   metered_value: float
   metered_peak_demand: float
   timestamp: datetime
   
   def __init__(self, timestamp, value, power):
      self.timestamp = timestamp
      self.metered_value = value
      self.metered_peak_demand = power