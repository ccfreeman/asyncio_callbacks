import logging
import random
import asyncio
from src.classes.forecast import Forecast
from src.classes.models import ModelA, ModelB, ModelC
from config import CONFIG


logger = logging.getLogger(__name__)


class Driver:
    
    def __init__(self):
        # Generate the model wrappers, and make a class member that contains a list of them we can operate on
        model_a1 = ModelA(1)
        model_a2 = ModelA(2)
        model_b1 = ModelB(1)
        model_b2 = ModelB(2)
        model_c1 = ModelC(1)
        model_c2 = ModelC(2)
        
        self.models = [model_a1, model_a2, model_b1, model_b2, model_c1, model_c2]
        
        self.forecasts = [
            Forecast(
                name=f"F{i}", 
                model_a = random.choice([model_a1, model_a2]),
                model_b = random.choice([model_b1, model_b2]),
                model_c = random.choice([model_c1, model_c2])
            ) for i in range(CONFIG.NUM_FORECASTS)
        ]
        
        self.forecasts_done = asyncio.Event()
        self.sleep_time = 0
        
    def forecast_finished_callback(self, task: asyncio.Task):
        """
        """
        logger.info(f"Driver: received notice of finished forecast")
        if all([forecast.done for forecast in self.forecasts]):
            logger.info(f"Driver: forecasts all done")
            self.forecasts_done.set()
            
    async def run(self):
        logger.info(f"Driver: Starting process")
        
        # Initiate forecast tasks before models, so that completions will be registered
        # in running forecasts
        self.forecast_tasks = set()
        for forecast in self.forecasts:
            forecast_task = asyncio.create_task(forecast.run())
            self.forecast_tasks.add(forecast_task)
            forecast_task.add_done_callback(self.forecast_finished_callback)
            forecast_task.add_done_callback(self.forecast_tasks.discard)
        
        # Initiate model tasks
        self.model_tasks = set()
        for model in self.models:
            modeling_task = asyncio.create_task(model.predict())
            self.model_tasks.add(modeling_task)
            modeling_task.add_done_callback(model.notify_forecasts)
            modeling_task.add_done_callback(self.model_tasks.discard)
        logger.info("Driver: awaiting all forecasts to complete")
        await self.forecasts_done.wait()
        logger.info(f"Driver: all forecasts complete")
        self.result = [{forecast.name: forecast.result} for forecast in self.forecasts]
        logger.info(f"Driver: the answer is {self.result}")
        logger.info("Driver: done")
        return self.result
        