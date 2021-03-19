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
from .request import Requests, check_requests
from .exception import NotFound
from .model import *
from datetime import datetime

t_id = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}


class School:
    """학교의 값이 저장되고, 이 클래스를 통하여 급식, 시간표, 학사 일정 등을 불러올 수 있습니다.

        Parameters
        ----------
        token : Optional[str]
            https://open.neis.go.kr/portal/guide/actKeyPage.do 에서 발급 받은 토큰값이 들어갑니다.
        data : Optional[dict]
            :class:`Client`의 값이 이어저 들어가게 구성되어 있습니다. 만약에 직접 사용하신 다면 이 매게변수에 아무런 값도 넣어주지 마세요.
        sc_code : Optional[str]
            교육청 코드가 들어가게 됩니다. 직접 사용하신 다면 이 값은 필수로 필요합니다. (참조: :class:`Location`)
        sd_code : Optional[str]
            해당 학교 고유번호가 들어가게 됩니다. 직접 사용하신 다면 이 값은 필수로 필요합니다.
        kind : Optional[int]
            학교의 종류가 들어갑니다. :def:`timetable`를 사용하기 위해서는 값을 넣으셔야합니다. (참조: :class:`SchoolType`)

        Attributes
        ----------
        data : dict
            :class:`Client`에서 불러온 값이 저장됩니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        requests
            NEIS Open API를 주고받는 aiohttp 형식의 웹 클라이언트입니다.
        sc_code : str
            교육청 코드가 들어가게 됩니다.
        sd_code : str
            학교 고유번호가 들어가게 됩니다.
        ofcdc : str
            학교가 소속된 관리 시/도 교육청 명칭이 들어가게 됩니다. 만약 직접 사용하신 다면 None이 리턴됩니다. (ex. 서울특별시교육청)
        name : str
            학교 명칭이 들어가게 됩니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        name_ENG : str
            학교 영문 명칭이 들어가게 됩니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        type : str
            학교의 종류가 들어갑니다.
        provincial : str
            학교의 소재지가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다. (ex. 서울특별시)
        location : str
            학교가 소속된 교육청의 값이 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다. (ex. 서울특별시교육청)
        post_address : str
            학교의 우편번호가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        address1 : str
            학교의 주소가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        address2 : str
            학교의 세부주소가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        phone : str
            학교의 전화번호가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        site : str
            학교의 사이트 주소가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        fax : str
            학교의 팩스 번호가 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        opening : str
            학교의 개교일이 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
        anniversary : str
            학교의 개교기념일이 들어갑니다. 만약 직접 사용하신 다면 None이 리턴됩니다.
    """
    def __init__(self, data=None, token=None, sc_code: str = None, sd_code: str = None, kind: int = None):
        if data is None:
            data = dict()

        self.data = data
        self.requests = Requests(token)

        self.sc_code = data.get('ATPT_OFCDC_SC_CODE')
        self.sd_code = data.get('SD_SCHUL_CODE')

        self.ofcdc = data.get('ATPT_OFCDC_SC_NM')
        self.name = data.get('SCHUL_NM')
        self.name_ENG = data.get('ENG_SCHUL_NM')
        self.type = data.get('SCHUL_KND_SC_NM')
        self.provincial = data.get('LCTN_SC_NM')
        self.location = data.get('JU_ORG_NM')
        self.post_address = data.get('ORG_RDNZC')
        self.address1 = data.get('ORG_RDNMA')
        self.address2 = data.get('ORG_RDNDA')
        self.phone = data.get('ORG_TELNO')
        self.site = data.get('HMPG_ADRES')
        self.fax = data.get('ORG_FAXNO')
        self.opening = data.get('FOND_YMD')
        self.anniversary = data.get('FOND_YMD')

        if data is None:
            self.sc_code = sc_code
            self.sd_code = sd_code
            if sc_code is None or sd_code is None:
                raise IndexError("Please enter sc_code and sd_code as required.")
            if kind is not None and 0 <= kind <= 3:
                tp = ["초등학교", "중학교", "고등학교", "특수학교"]
                self.type = tp[kind]

    async def meal(self, date: datetime = datetime.now(), from_date: datetime = None, to_date: datetime = None):
        """급식 정보를 불러옵니다.
            Parameters
            ----------
            date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다.
            from_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            to_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.

            Returns
            ----------
            list[:class:`Meal`]
                조회된 급식 목록이 들어가게 됩니다.
        """
        if from_date is not None and to_date is not None:
            json2 = await self.requests.get(
                "GET", "/mealServiceDietInfo",
                ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
                MLSV_FROM_YMD=from_date.strftime("%Y%m%d"),
                MLSV_TO_YMD=to_date.strftime("%Y%m%d"))
        else:
            json2 = await self.requests.get(
                "GET", "/mealServiceDietInfo",
                ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
                MLSV_YMD=date.strftime("%Y%m%d"))

        check_requests(json2)

        if len(json2.get('mealServiceDietInfo')[1].get('row')) == 0:
            raise NotFound

        return [Meal(x) for x in json2.get('mealServiceDietInfo')[1].get('row')]

    async def timetable(self, grade, class_nm,
                        date: datetime = datetime.now(), from_date: datetime = None, to_date: datetime = None,
                        semester=None, year=None):
        """시간표 정보를 불러옵니다.
            Parameters
            ----------
            grade : int or str
                학년이 들어갑니다.
            class_nm : int or str
                반 정보가 들어갑니다.
            date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다.
            from_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            to_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            semester : Optional[int or str]
                학기 정보가 들어갑니다.
            year : Optional[int or str]
                학년 정보가 정보가 들어갑니다.

            Returns
            ----------
            list[:class:`Timetable`]
                조회된 시간표 목록이 들어가게 됩니다.
        """
        if isinstance(grade, int):
            grade = str(grade)
        if isinstance(class_nm, int):
            class_nm = str(class_nm)

        if isinstance(year, int):
            year = str(year)
        if isinstance(semester, int):
            semester = str(semester)

        class_nm = class_nm.zfill(2)

        type_nm = self.type
        if type_nm is None:
            raise TypeError("To get a timetable, you need to fill out the kind of school.")
        if type_nm not in t_id:
            raise TypeError("This school is not a searchable type.")

        if from_date is not None and to_date is not None:
            json2 = await self.requests.get(
                "GET", f"/{t_id[type_nm]}Timetable",
                ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
                GRADE=grade, CLASS_NM=class_nm,
                AY=year, SEM=semester,
                TI_FROM_YMD=from_date.strftime("%Y%m%d"),
                TI_TO_YMD=to_date.strftime("%Y%m%d"))
        else:
            json2 = await self.requests.get(
                "GET", f"/{t_id[type_nm]}Timetable",
                ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
                GRADE=grade, CLASS_NM=class_nm,
                AY=year, SEM=semester,
                ALL_TI_YMD=date.strftime("%Y%m%d"))

        check_requests(json2)
        return [Timetable(x) for x in json2.get(f'{t_id[type_nm]}Timetable')[1].get('row')]

    async def series(self):
        """학교 계열정보 정보를 불러옵니다.

            Returns
            ----------
            list[:class:`Series`]
                조회된 학교 계열 정보 목록이 들어가게 됩니다.
        """
        json2 = await self.requests.get(
            "GET", "/schulAflcoinfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code)

        check_requests(json2)

        if len(json2.get('schulAflcoinfo')[1].get('row')) == 0:
            raise NotFound

        return [Series(x) for x in json2.get('schulAflcoinfo')[1].get('row')]

    async def class_info(self, grade=None, year=None):
        """학교 반 정보를 불러옵니다.
            Parameters
            ----------
            grade : Optional[int or str]
                학년이 들어갑니다.
            year : Optional[int or str]
                학년 정보가 정보가 들어갑니다.

            Returns
            ----------
            list[:class:`ClassInfo`]
                조회된 반 정보 목록이 들어가게 됩니다.
        """
        if isinstance(grade, int):
            grade = str(grade)

        if isinstance(year, int):
            year = str(year)

        json2 = await self.requests.get(
            "GET", "/classInfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
            AY=year, GRADE=grade)

        check_requests(json2)

        if len(json2.get('classInfo')[1].get('row')) == 0:
            raise NotFound

        return [ClassInfo(x) for x in json2.get('classInfo')[1].get('row')]

    async def major(self, grade=None, year=None):
        """학교 학과 정보를 불러옵니다.
            Parameters
            ----------
            grade : Optional[int or str]
                학년이 들어갑니다.
            year : Optional[int or str]
                학년 정보가 정보가 들어갑니다.

            Returns
            ----------
            list[:class:`Major`]
                조회된 학교의 전공 계열 목록이 들어가게 됩니다.
        """
        if isinstance(grade, int):
            grade = str(grade)

        if isinstance(year, str):
            year = str(year)

        json2 = await self.requests.get(
            "GET", "/schoolMajorinfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
            AY=year, GRADE=grade)

        check_requests(json2)

        if len(json2.get('schoolMajorinfo')[1].get('row')) == 0:
            raise NotFound

        return [Major(x) for x in json2.get('schoolMajorinfo')[1].get('row')]

    async def schedule(self, date: datetime = datetime.now(), from_date: datetime = None, to_date: datetime = None):
        """학사 일정 정보를 불러옵니다.
            Parameters
            ----------
            date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다.
            from_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.
            to_date : Optional[datetime]
                조회하시는 급식 날짜가 들어갑니다. 만약에 특정 기간을 조회하고 싶으시면 본 매게변수를 이용해주세요.

            Returns
            ----------
            list[:class:`Schedule`]
                조회된 학사 일정 정보에 대한 목록이 들어가게 됩니다.
        """
        if from_date is not None and to_date is not None:
            json2 = await self.requests.get(
                "GET", "/SchoolSchedule",
                ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
                TI_FROM_YMD=from_date.strftime("%Y%m%d"),
                TI_TO_YMD=to_date.strftime("%Y%m%d"))
        else:
            json2 = await self.requests.get(
                "GET", "/SchoolSchedule",
                ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
                ALL_TI_YMD=date.strftime("%Y%m%d"))

        check_requests(json2)

        if len(json2.get('SchoolSchedule')[1].get('row')) == 0:
            raise NotFound

        return [Schedule(x) for x in json2.get('SchoolSchedule')[1].get('row')]

    async def timetable_room(self, grade=None, semester=None, year=None):
        """시간표에 따른 강의실 정보를 불러옵니다.
            Parameters
            ----------
            grade : Optional[int or str]
                학년이 들어갑니다.
            semester: Optional[int or str]
                검색하시는 학기 정보가 들어갑니다.
            year : Optional[int or str]
                학년 정보가 정보가 들어갑니다.

            Returns
            ----------
            list[:class:`TimetableClass`]
                조회된 시간표에 따른 강의실 정보가 목록으로 들어가게 됩니다.
        """
        if isinstance(grade, int):
            grade = str(grade)

        if isinstance(year, str):
            year = str(year)
        if isinstance(semester, str):
            semester = str(semester)

        json2 = await self.requests.get(
            "GET", "/tiClrminfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
            GRADE=grade, AY=year, SEM=semester)

        check_requests(json2)

        if len(json2.get('tiClrminfo')[1].get('row')) == 0:
            raise NotFound

        return [TimetableClass(x) for x in json2.get('tiClrminfo')[1].get('row')]
