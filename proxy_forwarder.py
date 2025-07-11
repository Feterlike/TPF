import requests
import time
import logging
from telegram import Bot
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
TELEGRAM_BOT_TOKEN = "?????????????????????????"
TELEGRAM_CHAT_ID = "????????"
PROXY_URL = "????????????????????????????"
CHECK_INTERVAL = 300  # seconds

# Set to store already sent proxies
sent_proxies = set()

async def send_proxy_to_telegram(bot, proxy):
    """Send a proxy to the Telegram channel."""
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"New Proxy: {proxy}"
        )
        logger.info(f"Successfully sent proxy: {proxy}")
    except Exception as e:
        logger.error(f"Error sending proxy to Telegram: {e}")

async def fetch_and_process_proxies():
    """Fetch proxies from the URL and send new ones to Telegram."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    while True:
        try:
            # Fetch proxies
            async with aiohttp.ClientSession() as session:
                async with session.get(PROXY_URL) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Process content directly without base64 decoding
                        proxies = content.strip().split('\n')
                        
                        # Process each proxy
                        for proxy in proxies:
                            proxy = proxy.strip()
                            if proxy and proxy not in sent_proxies:
                                await send_proxy_to_telegram(bot, proxy)
                                sent_proxies.add(proxy)
                    else:
                        logger.error(f"Failed to fetch proxies. Status code: {response.status}")
            
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        
        # Wait for the next check
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    """Main function to run the proxy forwarder."""
    logger.info("Starting proxy forwarder...")
    try:
        await fetch_and_process_proxies()
    except KeyboardInterrupt:
        logger.info("Script stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
