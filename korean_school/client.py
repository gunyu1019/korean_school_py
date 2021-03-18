from .request import requests
from .school import school
from .exception import check_requests, NotFound
from .model import academy


class client:
    def __init__(self, token: str = None):
        self.requests = requests(token)
        self.token = token

    async def school(self, name: str = None, kind: int = None, location: str = None, provincial_code: str = None):
        type_m = None
        if kind is not None and 0 <= kind <= 3:
            tp = ["초등학교", "중학교", "고등학교", "특수학교"]
            type_m = tp[kind]

        json1 = await self.requests.get(
            "GET", "/schoolInfo",
            SCHUL_NM=name, SCHUL_KND_SC_NM=type_m, LCTN_SC_NM=location, ATPT_OFCDC_SC_CODE=provincial_code)
        print(1)

        check_requests(json1)

        school_data = json1['schoolInfo'][1]["row"]

        if len(school_data) == 0:
            return NotFound

        return [school(x, self.token) for x in school_data]

    async def academy(self, provincial_code, name: str = None, state: str = None):
        json1 = await self.requests.get(
            "GET", "/acaInsTiInfo",
            ACA_NM=name, ATPT_OFCDC_SC_CODE=provincial_code, ADMST_ZONE_NM=state)

        check_requests(json1)

        academy_data = json1['acaInsTiInfo'][1]["row"]

        if len(academy_data) == 0:
            return NotFound

        return [academy(x) for x in academy_data]
