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
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
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
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")


class ClassInfo:
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.class_nm = response.get("CLASS_NM")
        self.major = response.get("DDDEP_NM")


class Major:
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.class_nm = response.get("CLASS_NM")
        self.major = response.get("DDDEP_NM")


class Academy:
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
        self.teaching = response.get("REALM_SC_NM")
        self.teaching_list = response.get("LE_CRSE_LIST_NM")
        self.teaching_course = response.get("LE_CRSE_NM")
        self.tuition = response.get("PSNBY_THCC_CNTNT")
        self.tuition_disclosure = response.get("THCC_OTHBC_YN")
        self.dormitory = response.get("BRHS_ACA_YN")
        self.post_address = response.get("FA_RDNZC")
        self.address1 = response.get("FA_RDNMA")
        self.address2 = response.get("FA_RDNDA")


class Schedule:
    def __init__(self, response):
        self.data = response

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
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.room = response.get("CLRM_NM")
        self.major = response.get("DDDEP_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.semester = response.get("SEM")
