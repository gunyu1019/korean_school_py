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
import datetime

allergy_lists = ["난류", "우유", "메밀", "땅콩", "대두", "밀", "고등어", "게", "새우", "돼지고기", "복숭아", "토마토", "아황산염", "호두",
                 "닭고기", "쇠고기", "오징어", "조개류(굴,전복,홍합 등)"]


class Meal:
    """급식 정보를 포함합니다. 급식 정보에 대한 알레르기, 영양분 정보가 포함되어 있습니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        code : str
            식사코드가 리턴됩니다.
        type : str
            급식의 종류가 리턴됩니다. 대표적으로 조식(), 중식(점심), 석식(저녁)으로 구성되어 있습니다.
        date : datetime
            날짜 값이 datetime 형으로 리턴됩니다.
        date_data : str
            날짜 값의 원본 형태의 내용이 리턴됩니다.
        calorie : str
            급식의 칼로리 정보가 리턴됩니다.
        meal : list
            급식 정보가 포함되어 있습니다.
        allergy : list
            급식 정보에 대한 알르레기 정보가 포함되어 있습니다.
        origin : list
            급식에 대한 원산지 정보가 포함되어 있습니다.
        nutrition : list
            급식에 대한 영양분 정보가 포함되어 있습니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.code = response.get("MMEAL_SC_CODE")
        self.type = response.get("MMEAL_SC_NM")
        self.date = datetime.datetime.strptime(response.get("MLSV_YMD"), "%Y%m%d")
        self.date_data = response.get("MLSV_YMD")
        self.calorie = response.get("CAL_INFO")

        meal_data = response.get("DDISH_NM").split("<br/>")
        allergy = []
        for i in enumerate(meal_data):
            allergy_cache = []
            for j in range(18, 0, -1):
                if "{}.".format(j) in meal_data[i[0]]:
                    allergy_cache.append(allergy_lists[j-1])
                meal_data[i[0]] = meal_data[i[0]].replace("{}.".format(j), "")
            allergy.append(allergy_cache)

        origin = dict()
        origin_data = response.get("ORPLC_INFO").split("<br/>")
        for i in origin_data:
            key = i.split(":")[0].strip()
            value = i.split(":")[1].strip()
            origin[key] = value

        nutrition = dict()
        nutrition_data = response.get("NTR_INFO").split("<br/>")
        for i in nutrition_data:
            key = i.split(":")[0].strip()
            value = i.split(":")[1].strip()
            nutrition[key] = value

        self.meal = meal_data
        self.allergy = allergy
        self.origin = origin
        self.nutrition = nutrition


class Timetable:
    """시간표 정보가 포함됩니다. 시간표 정보는 n교시 마다 배열로 정보가 따로 있습니다. 따라서 그 날짜에 시간표를 불러온다면 시간표 정렬이 필요합니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        title : str
            과목명이 리턴됩니다.
        time : list
            과목에 따른 n시간이 리턴됩니다.
        semester : str
            학기 정보가 리턴됩니다.
        year : str
            학년도 정보가 리턴됩니다.
        date : datetime
            날짜 값이 datetime 형으로 리턴됩니다.
        date_data : str
            날짜 값의 원본 형태의 내용이 리턴됩니다.
        grade : str
            학년 정보가 리턴됩니다.
        class_nm : list
            반 정보가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.title = response.get("ITRT_CNTNT")
        self.semester = response.get("SEM")
        self.year = response.get("AY")
        self.date = datetime.datetime.strptime(response.get("ALL_TI_YMD"), "%Y%m%d")
        self.date_data = response.get("ALL_TI_YMD")
        self.grade = response.get("GRADE")
        self.class_nm = response.get("CLASS_NM")
        self.time = response.get("PERIO")


class Series:
    """학교 계열 정보가 포함됩니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        series : str
            학교 계열정보가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")


class ClassInfo:
    """학교 반 정보가 포함됩니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        series : str
            학교 계열정보가 리턴됩니다.
        year : str
            학년도 정보가 리턴됩니다.
        class_nm : str
            반 정보가 리턴됩니다.
        major : str
            반에 대한 학과 정보가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.class_nm = response.get("CLASS_NM")
        self.major = response.get("DDDEP_NM")


class Major:
    """학교 학과 정보가 포함됩니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        series : str
            학교 계열정보가 리턴됩니다.
        year : str
            학년도 정보가 리턴됩니다.
        major : str
            반에 대한 학과 정보가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.major = response.get("DDDEP_NM")


class Academy:
    """학원의 정보가 포함됩니다.

        Attributes
        ----------
        data : dict
            :class:`Client`에서 불러온 값이 저장됩니다.
        name : str
            학원 명칭이 들어가게 됩니다.
        state : str
            학원의 소재지가 들어가게 됩니다. (ex. 강남구)
        code : str
            학원의 번호가 리턴됩니다.
        provincial_code : str
            학원의 교육청 고유번호가 리턴됩니다.
        provincial : str
            학원의 소재지가 리턴됩니다.
        open : str
            학원의 개설날짜가 리턴됩니다.
        registration : str
            학원의 등재 날짜가 리턴됩니다.
        close_start : str
            학원의 휴업일이 리턴됩니다. 그중 휴원 시작일이 리턴되며, 정상적으로 운영시 None이 반환됩니다.
        close_end : str
            학원의 휴업일이 리턴됩니다. 그중 휴원 종료일이 리턴되며, 정상적으로 운영시 None이 반환됩니다.
        people : str
            학원의 정원 수이 리턴됩니다.
        people_temporary : str
            학원의 임시 정원 수가 리턴됩니다.
        branch : str
            학원의 분야가 리턴됩니다.
        teaching : str
            학원의 교습 계열명이 리턴됩니다.
        teaching_list : str
            학원의 교습 과정 목록이 리턴됩니다.
        teaching_course : str
            학원의 교습 과정 명이 리턴됩니다.
        tuition : str
            인당 수강료 정보가 리턴됩니다.
        tuition_disclosure : str
            수강료 공개 여부가 리턴됩니다.
        dormitory : str
            기숙사 여부가 리턴됩니다.
        post_address : str
            학원의 우편번호가 리턴됩니다.
        address1 : str
            학원의 주소가 리턴됩니다.
        address2 : str
            학원의 세부주소가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.name = response.get("ACA_NM")
        self.state = response.get("ADMST_ZONE_NM")
        self.code = response.get("ACA_ASNUM")
        self.provincial_code = response.get("ATPT_OFCDC_SC_CODE")
        self.provincial = response.get("ATPT_OFCDC_SC_NM")
        self.open = response.get("ESTBL_YMD")
        self.registration = response.get("REG_YMD")
        self.close_start = response.get("CAA_BEGIN_YMD")
        self.close_end = response.get("CAA_END_YMD")
        self.people = response.get("TOFOR_SMTOT")
        self.people_temporary = response.get("DTM_RCPTN_ABLTY_NMPR_SMTOT")
        self.branch = response.get("REALM_SC_NM")
        self.teaching = response.get("LE_ORD_NM")
        self.teaching_list = response.get("LE_CRSE_LIST_NM")
        self.teaching_course = response.get("LE_CRSE_NM")
        self.tuition = response.get("PSNBY_THCC_CNTNT")
        self.tuition_disclosure = response.get("THCC_OTHBC_YN")
        self.dormitory = response.get("BRHS_ACA_YN")
        self.post_address = response.get("FA_RDNZC")
        self.address1 = response.get("FA_RDNMA")
        self.address2 = response.get("FA_RDNDA")


class Schedule:
    """학교의 학사 일정이 포함되어 있습니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        type : str
            학교의 종류가 리턴됩니다.
        date : datetime
            날짜 값이 datetime 형으로 리턴됩니다.
        date_data : str
            날짜 값의 원본 형태의 내용이 리턴됩니다.
        year : str
            학년도 정보가 리턴됩니다.
        grade : list
            학년 별 해당 유/무가 리턴됩니다. (Y: True, F: False, *: 해당 안됨.)
        name : str
            행사명이 리턴됩니다.
        content : str
            행사내용이 리턴됩니다.
        deduction : str
            수업 공제일 명이 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.type = response.get("SCHUL_CRSE_SC_NM")
        self.date = datetime.datetime.strptime(response.get("AA_YMD"), "%Y%m%d")
        self.date_data = response.get("AA_YMD")
        self.deduction = response.get("SBTR_DD_SC_NM")
        self.year = response.get("AY")
        self.name = response.get("EVENT_NM")
        self.content = response.get("EVENT_CNTNT")
        self.grade = [
            response.get("ONE_GRADE_EVENT_YN"),
            response.get("TW_GRADE_EVENT_YN"),
            response.get("THREE_GRADE_EVENT_YN"),
            response.get("FR_GRADE_EVENT_YN"),
            response.get("FIV_GRADE_EVENT_YN"),
            response.get("SIX_GRADE_EVENT_YN")
        ]


class TimetableClass:
    """학교에 반 학과 정보가 포함됩니다.
        Attributes
        ----------
        data : dict
            이 모델의 원본 형태의 내용이 포함되어 있습니다.
        school : str
            학교 이름이 리턴됩니다.
        room : str
            강의실 정보가 리턴됩니다.
        series : str
            학교 계열정보가 리턴됩니다.
        grade : str
            학년 정보가 리턴됩니다.
        year : str
            학년도 정보가 리턴됩니다.
        major : str
            반에 대한 학과 정보가 리턴됩니다.
        semester : str
            학기 정보가 리턴됩니다.
    """
    def __init__(self, response):
        self.data = response

        self.school = response.get("SCHUL_NM")
        self.room = response.get("CLRM_NM")
        self.major = response.get("DDDEP_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.semester = response.get("SEM")
