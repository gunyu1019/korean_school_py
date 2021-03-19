"""
MIT License

Copyright (c) 2021 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import aiohttp

from .exception import *


class Requests:
    """학교의 값이 저장되고, 이 클래스를 통하여 급식, 시간표, 학사 일정 등을 불러올 수 있습니다.
        Parameters
        ----------
        token : Optional[str]
            https://open.neis.go.kr/portal/guide/actKeyPage.do 에서 발급 받은 토큰값이 들어갑니다.

        Attributes
        ----------
        base : str
            Neis OpenAPI 주소의 Base URL 정보가 들어가 있습니다.
        token : str
            token 값이 들어가게 되어 있습니다.
    """
    def __init__(self, token: str = None):
        self.base = "https://open.neis.go.kr/hub"
        self.token = token

    async def get(self, method: str, url: str, **kwargs):
        """해당 함수를 통하여 NEIS openAPI와 연결됩니다.
            Parameters
            ----------
            method : str
                GET, POST 등의 HTTP method가 들어갑니다.
            url : str
                base를 기반으로 NEIS OpenAPI와 연결될 주소에 대한 값이 들어옵니다.

            Returns
            ----------
            dict
                NEIS OpenAPI에서 리턴된 값이 dict 형태로 변환되어 리턴됩니다.
        """
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


def check_requests(resp):
    """해당 함수를 통하여 NEIS openAPI와 연결됩니다.
        Parameters
        ----------
        resp : dict
            반환된 json 값이 포함됩니다.

        Raises
        ----------
        .exception.Notfound
            해당하는 데이터가 없습니다.
        .exception.Forbidden
            관리자에 의해 인증키 사용이 제한되거나, 인증키가 유효하지 않습니다.
        .exception.NotImplemented
            필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.
        .exception.TooManyRequests
            데이터요청은 한번에 최대 1,000건을 넘거나, 일별 트래픽 제한을 넘은 호출입니다. 일별 트래픽 제한을 초과하면 오늘은 더이상 호출할 수 없습니다.
        .exception.TooManyRequests
            서버 오류입니다. 지속적으로 발생시 OpenAPI 홈페이지로 문의(Q&A) 바랍니다.
    """
    if 'RESULT' in resp.keys():
        if 'CODE' in resp['RESULT'].keys():
            ercode = resp['RESULT']['CODE']
            if ercode == 'INFO-200':
                raise NotFound(resp['RESULT'])
            elif ercode == 'INFO-300' or ercode == 'ERROR-290':
                raise Forbidden(resp['RESULT'])
            elif ercode == 'ERROR-300' or ercode == 'ERROR-333':
                raise NotImplemented(resp['RESULT'])
            elif ercode == 'ERROR-336' or ercode == 'ERROR-337':
                raise TooManyRequests(resp['RESULT'])
            elif ercode == 'ERROR-500' or ercode == 'ERROR-600' or ercode == 'ERROR-601':
                raise InternalServerError(resp['RESULT'])
    return
