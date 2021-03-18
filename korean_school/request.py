import json
import aiohttp


class requests:
    def __init__(self, token: str = None):
        self.base = "https://open.neis.go.kr/hub"
        self.token = token

    async def get(self, method: str, url: str, **kwargs):
        header = {
            'Type': 'json',
        }
        if self.token is not None:
            header['KEY'] = f'{self.token}'

        for i in kwargs.keys():
            if kwargs.get(i) is None:
                continue
            header.update({
                i: kwargs.get(i)
            })

        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.base}{url}", params=header) as resp:
                if resp.content_type.startswith("application/json"):
                    f_data = await resp.json()
                else:
                    data = await resp.text()
                    f_data = json.loads(data)
        return f_data
