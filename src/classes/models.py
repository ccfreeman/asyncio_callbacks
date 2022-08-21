import logging
import random
import asyncio
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class Model(ABC):
    
    def __init__(self, name: str):
        self.name = f"{self.name}{name}"
        self.modeling_time = (self.max_time - self.min_time) * random.random() + self.min_time
        self.done = False
        self.result = None
        self.forecasts = []
    
    @property
    @abstractmethod
    def min_time(self) -> int:
        ...
    
    @property
    @abstractmethod
    def max_time(self) -> int:
        ...
    
    @property
    @abstractmethod
    def name(self) -> str:
        ...
        
    def add_forecast(self, forecast):
        self.forecasts.append(forecast)
        
    def notify_forecasts(self, task):
        logger.info(f"Model {self.name}: notifying {len(self.forecasts)} forecasts")
        for forecast in self.forecasts:
            forecast.model_finished_callback(task)
        
    async def predict(self) -> float:
        logger.info(f"Model {self.name}: predicting for {self.modeling_time} seconds")
        await asyncio.sleep(self.modeling_time)
        logger.info(f"Model {self.name}: finished")
        self.result = self.modeling_time
        self.done = True
        return self.result
    
    
class ModelA(Model):
    min_time = 1
    max_time = 2
    name = 'A'
    
    
class ModelB(Model):
    min_time = 3
    max_time = 7
    name = 'B'
    
    
class ModelC(Model):
    min_time = 5
    max_time = 10
    name = 'C'
    
    