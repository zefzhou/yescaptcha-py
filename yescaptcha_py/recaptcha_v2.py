from loguru import logger
import requests
import asyncio
import aiohttp


class RecaptchaV2:

    def __init__(
        self,
        client_key,
        site_url,
        site_key,
        wait_seconds_per_try: int = 3,
        max_wait_tries: int = 40,
        domain: str = 'https://api.yescaptcha.com',
        task_id: str = None,
        task_type: str = 'NoCaptchaTaskProxyless',
        # HCaptchaTaskProxyless -- h_captcha
    ):
        if not client_key:
            raise ValueError('yescaptcha client_key is nil')
        self.client_key = client_key
        self.site_url = site_url
        self.site_key = site_key
        self.wait_seconds_per_try = wait_seconds_per_try
        self.max_wait_tries = max_wait_tries
        self.domain = domain
        self.task_type = task_type
        self.task_id = task_id

    async def solve(self):
        await self.create_task()
        if self.task_id is None:
            return None
        return await self.get_code()

    async def create_task(self):
        url = f'{self.domain}/createTask'
        data = {
            'clientKey': self.client_key,
            'task': {
                'websiteURL': self.site_url,
                'websiteKey': self.site_key,
                'type': self.task_type
            }
        }

        try:
            async with aiohttp.client.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    result = await response.json()
                    task_id = result.get('taskId')
                    if task_id is not None:
                        logger.info(f'reCAPTCHA 解码任务创建成功，ID = {task_id}')
                        self.task_id = task_id
                        return
                    logger.error(f'reCAPTCHA 解码任务创建失败')
        except Exception as e:
            logger.error(f'reCAPTCHA 解码任务创建失败, {e}')

    async def get_code(self):
        wait_tries = 0
        while wait_tries < self.max_wait_tries:
            try:
                url = f'{self.domain}/getTaskResult'
                data = {'clientKey': self.client_key, 'taskId': self.task_id}
                async with aiohttp.client.ClientSession() as session:
                    async with session.post(url, json=data) as response:
                        result = await response.json()
                        solution = result.get('solution', {})
                        if solution:
                            response = solution.get('gRecaptchaResponse')
                            if response:
                                # logger.info(f'reCAPTCHA 解码成功, code = {response}')
                                logger.info(f'reCAPTCHA 解码成功')
                                return response
            except Exception as e:
                logger.error(e)
            wait_tries += 1
            await asyncio.sleep(self.wait_seconds_per_try)
        return None


async def test_recaptcha_v2():
    client_key = ''
    site_key = ''
    site_url = ''
    re = RecaptchaV2(
        client_key=client_key,
        site_url=site_url,
        site_key=site_key,
    )
    code = await re.solve()
    print(f'code = {code}')


if __name__ == '__main__':
    asyncio.run(test_recaptcha_v2())
