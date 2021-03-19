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
from .request import Requests
from .school import School

from .exception import NotFound
from .model import Academy
from .request import check_requests


class Client:
    """토큰 값을 저장하고, 학교와 학원의 기본 정보를 불러오기 위하여 사용됩니다.
        Parameters
        ----------
        token : Optional[str]
            https://open.neis.go.kr/portal/guide/actKeyPage.do 에서 발급 받은 토큰값이 들어갑니다.

        Attributes
        ----------
        requests
            NEIS Open API를 주고받는 aiohttp 형식의 웹 클라이언트입니다.
        token : str
            token 값이 들어가게 되어 있습니다.
    """
    def __init__(self, token: str = None):
        self.requests = Requests(token)
        self.token = token

    async def school(self, name: str = None, kind: int = None, location: str = None, provincial_code: str = None):
        """학교 정보를 불러옵니다.
            Parameters
            ----------
            name : Optional[str]
                학교 명이 들어갑니다.
            kind : Optional[int]
                학교의 종류가 들어갑니다. (참조: :class:`SchoolType`)
            location : Optional[str]
                학교의 소재지가 들어가게 됩니다. (ex. 서울특별시)
            provincial_code : Optional[str]
                교육청 코드가 들어갑니다. (참조: :class:`Location`)

            Returns
            ----------
            list[:class:`School`]
                검색된 학교 목록이 들어가게 됩니다.
        """
        type_m = None
        if kind is not None and 0 <= kind <= 3:
            tp = ["초등학교", "중학교", "고등학교", "특수학교"]
            type_m = tp[kind]

        json1 = await self.requests.get(
            "GET", "/schoolInfo",
            SCHUL_NM=name, SCHUL_KND_SC_NM=type_m, LCTN_SC_NM=location, ATPT_OFCDC_SC_CODE=provincial_code)

        check_requests(json1)

        school_data = json1['schoolInfo'][1]["row"]

        if len(school_data) == 0:
            return NotFound

        return [School(x, self.token) for x in school_data]

    async def academy(self, provincial_code, name: str = None, state: str = None):
        """학원 정보를 불러옵니다.
            Parameters
            ----------
            provincial_code : str
                교육청 코드가 들어갑니다. (참조: :class:`Location`)
            name : Optional[str]
                학원 명이 들어갑니다.
            state : Optional[str]
                학원의 소재지가 들어가게 됩니다. (ex. 강남구)

            Returns
            ----------
            list[:class:`Academy`]
                검색된 학원 목록이 들어가게 됩니다.
        """
        json1 = await self.requests.get(
            "GET", "/acaInsTiInfo",
            ACA_NM=name, ATPT_OFCDC_SC_CODE=provincial_code, ADMST_ZONE_NM=state)

        check_requests(json1)

        academy_data = json1['acaInsTiInfo'][1]["row"]

        if len(academy_data) == 0:
            return NotFound

        return [Academy(x) for x in academy_data]
