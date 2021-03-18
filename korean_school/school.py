from .request import requests
from .exception import check_requests, NotFound
from .model import *
from datetime import datetime

t_id = {"초등학교": "els", "중학교": "mis", "고등학교": "his", "특수학교": "sps"}


class school:
    def __init__(self, data=None, token=None, sc_code: str = None, sd_code: str = None, kind: int = None):
        if data is None:
            data = dict()

        self.data = data
        self.requests = requests(token)

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

        return [meal(x) for x in json2.get('mealServiceDietInfo')[1].get('row')]

    async def timetable(self, grade, class_nm,
                        date: datetime = datetime.now(), from_date: datetime = None, to_date: datetime = None,
                        semester=None, year=None):
        if isinstance(grade, int):
            grade = str(grade)
        if isinstance(class_nm, int):
            class_nm = str(class_nm)

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
        return [timetable(x) for x in json2.get(f'{t_id[type_nm]}Timetable')[1].get('row')]

    async def series(self):
        json2 = await self.requests.get(
            "GET", "/schulAflcoinfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code)

        check_requests(json2)

        if len(json2.get('schulAflcoinfo')[1].get('row')) == 0:
            raise NotFound

        return [series(x) for x in json2.get('schulAflcoinfo')[1].get('row')]

    async def classInfo(self, grade=None, year=None):
        if isinstance(grade, int):
            grade = str(grade)

        json2 = await self.requests.get(
            "GET", "/classInfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
            AY=year, GRADE=grade)

        check_requests(json2)

        if len(json2.get('classInfo')[1].get('row')) == 0:
            raise NotFound

        return [classInfo(x) for x in json2.get('classInfo')[1].get('row')]

    async def major(self, grade=None, year=None):
        if isinstance(grade, int):
            grade = str(grade)

        json2 = await self.requests.get(
            "GET", "/schoolMajorinfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
            AY=year, GRADE=grade)

        check_requests(json2)

        if len(json2.get('schoolMajorinfo')[1].get('row')) == 0:
            raise NotFound

        return [major(x) for x in json2.get('schoolMajorinfo')[1].get('row')]

    async def schedule(self, date: datetime = datetime.now(), from_date: datetime = None, to_date: datetime = None):
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

        return [schedule(x) for x in json2.get('SchoolSchedule')[1].get('row')]

    async def timetable_room(self, grade=None, semester=None, year=None):
        json2 = await self.requests.get(
            "GET", "/tiClrminfo",
            ATPT_OFCDC_SC_CODE=self.sc_code, SD_SCHUL_CODE=self.sd_code,
            GRADE=grade, AY=year, SEM=semester)

        check_requests(json2)

        if len(json2.get('tiClrminfo')[1].get('row')) == 0:
            raise NotFound

        return [timetable_class(x) for x in json2.get('tiClrminfo')[1].get('row')]