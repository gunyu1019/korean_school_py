import datetime

allergy_lists = ["난류", "우유", "메밀", "땅콩", "대두", "밀", "고등어", "게", "새우", "돼지고기", "복숭아", "토마토", "아황산염", "호두",
                 "닭고기", "쇠고기", "오징어", "조개류(굴,전복,홍합 등)"]


class meal:
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


class timetable:
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


class series:
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")


class classInfo:
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.class_nm = response.get("CLASS_NM")
        self.major = response.get("DDDEP_NM")


class major:
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.class_nm = response.get("CLASS_NM")
        self.major = response.get("DDDEP_NM")


class academy:
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


class schedule:
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


class timetable_class:
    def __init__(self, response):
        self.data = response

        self.name = response.get("SCHUL_NM")
        self.room = response.get("CLRM_NM")
        self.major = response.get("DDDEP_NM")
        self.series = response.get("ORD_SC_NM")
        self.grade = response.get("GRADE")
        self.year = response.get("AY")
        self.semester = response.get("SEM")
