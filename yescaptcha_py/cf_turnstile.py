import requests
import time
from loguru import logger
import asyncio
import aiohttp


class CfTurnstile:

    def __init__(
        self,
        client_key,
        site_url,
        site_key,
        domain: str = 'https://api.yescaptcha.com',
        proxy=None,
        task_type: str = 'TurnstileTaskProxyless',
        wait_seconds_per_try: int = 3,
        max_wait_tries: int = 30,
    ):
        if not client_key:
            raise ValueError('yescaptcha client_key is nil')

        self.client_key = client_key
        self.site_url = site_url
        self.site_key = site_key
        self.domain = domain
        self.proxy = proxy
        self.task_type = task_type
        self.wait_seconds_per_try = wait_seconds_per_try
        self.max_wait_tries = max_wait_tries

    async def create_task(self):
        data = {
            "clientKey": self.client_key,
            "task": {
                "type": self.task_type,
                "websiteURL": self.site_url,
                "websiteKey": self.site_key,
                "proxy": self.proxy,
            }
        }
        api_url = f"{self.domain}/createTask"
        try:
            async with aiohttp.client.ClientSession() as session:
                async with session.post(api_url, json=data) as response:
                    result = await response.json()
                    return result
        except Exception as e:
            logger.error(f'create cf_turnstile task failed : {e}')
            return None

    async def get_task(self, task_id):
        api_url = f"{self.domain}/getTaskResult"
        data = {"clientKey": self.client_key, "taskId": task_id}
        try:
            async with aiohttp.client.ClientSession() as session:
                async with session.post(api_url, json=data) as response:
                    result = await response.json()
                    return result
        except Exception as e:
            logger.error(f'get cf_turnstile task failed : {e}')
            return None

    async def resolve(self):
        task_response = await self.create_task()
        if not task_response or not task_response.get('taskId'):
            return task_response

        for _ in range(self.max_wait_tries):
            await asyncio.sleep(self.wait_seconds_per_try)
            result = await self.get_task(task_response.get('taskId'))
            if result.get('status') == 'processing':
                continue
            elif result.get('status') == 'ready':
                return result
            else:
                return {"status": "unknown"}
        return {"status": "timeout"}


async def test_cf_turnstile():
    yes_captcha_key = ''
    website_url = ''
    website_key = ''

    result = await CfTurnstile(
        client_key=yes_captcha_key,
        site_url=website_url,
        site_key=website_key,
    ).resolve()
    print(result)


if __name__ == '__main__':
    asyncio.run(test_cf_turnstile())
