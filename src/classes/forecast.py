import logging
import asyncio
from typing import List
from src.classes.models import ModelA, ModelB, ModelC, Model
from config import CONFIG


logger = logging.getLogger(__name__)


class Forecast:
    
    def __init__(self, name: str, model_a: ModelA, model_b: ModelB, model_c: ModelC):
        self.name = name
        
        self.model_a = model_a
        self.model_b = model_b
        self.model_c = model_c
        
        # Add a reference to the forecast object in each of the models
        # This allows the models to signal to this object that they have finished
        self.models: List[Model] = [self.model_a, self.model_b, self.model_c]
        for model in self.models:
            model.add_forecast(forecast=self)
            
        logger.info(f"Forecast {self.name} received:")
        for model in self.models:
            logger.info(f"{type(model)}: {model.name}, {model.modeling_time}")
        
        self.result = 0
        self.models_done = asyncio.Event()
        self.done = False
        
    def model_finished_callback(self, task: asyncio.Task):
        """A method that can be called from the models attached to this class
        to signal that they have completed their modeling activities.
        """
        logger.info(f"Forecast {self.name}: received notice of finished model")
        if all([model.done for model in self.models]):
            logger.info(f"Forecast {self.name}: all done")
            # Set the event to release the main thread and initiate modeling 
            self.models_done.set()
            
    async def run(self) -> float:
        """
        """
        logger.info(f"Forecast {self.name}: start")
        await self.models_done.wait()
        self.result = sum([model.result for model in self.models])
        logger.info(f"Forecast {self.name}: final result is {self.result} seconds")
        self.done = True
        return self.result
        