import asyncio
import logging
from src.classes.driver import Driver
from config import CONFIG


logger = logging.getLogger(__name__)


async def main():
    logger.info("Beginning process")
    driver = Driver()
    await driver.run()
    logger.info("All finished!")

if __name__=='__main__':
    asyncio.run(main())
