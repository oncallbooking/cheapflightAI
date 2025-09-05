import os
import aiohttp
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

EX_API = os.getenv("EXCHANGE_RATES_API_KEY", "")

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
async def get_rates():
    # Use a public free endpoint as fallback
    async with aiohttp.ClientSession() as s:
        if EX_API:
            url = f"https://openexchangerates.org/api/latest.json?app_id={EX_API}"
            async with s.get(url, timeout=10) as r:
                data = await r.json()
                return data.get("rates", {})
        else:
            # use exchangerate.host free endpoint
            url = "https://api.exchangerate.host/latest?base=USD"
            async with s.get(url, timeout=10) as r:
                data = await r.json()
                return data.get("rates", {})
