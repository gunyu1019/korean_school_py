# korean_school_py
A python wrapper for [NEIS OpenAPI](https://open.neis.go.kr/portal/mainPage.do) <br/>
이 파이썬 래퍼는 [NEIS OpenAPI](https://open.neis.go.kr/portal/mainPage.do) 를 위하여 제작된 라이브러리 입니다.

### 설치(Installation)
```python3
# Windows
py -3 -m pip install korean_school

# Linux / MacOS
python3 -m pip install korean_school
```

### 예제(Samples)
* Sample
  * [급식 정보 불러오기](#급식-정보-불러오기)
  * [시간표 정보 불러오기](#시간표-정보-불러오기)
  * [학원 정보 불러오기](#학원-정보-불러오기)
    
#### 급식 정보 불러오기

```python
import korean_school
import asyncio


async def main():
  client = korean_school.Client()
  school = await client.school(name="<학교명>")
  meal = await school[0].meal()

  print(meal[0].Meal)
  print(meal[0].allergy)
  print(meal[0].type)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# > ['칼슘수수밥k', '감자수제비국s', '메추리알곤약조림k', '애느타리깨소스무침k', '수제코다리살강정', '배추겉절이(입찰)k', '키위']
# > [[], ['아황산염', '밀', '대두'], ['아황산염', '밀', '대두', '난류'], ['아황산염', '밀', '대두'], ['아황산염', '토마토', '밀', '대두', '난류'], ['아황산염', '새우'], []]
# > 중식
# 본 정보는 가락고등학교의 2021년 3월 19일 기준 중식 자료 입니다.
```

#### 시간표 정보 불러오기
```python
import korean_school
import asyncio


async def main():
    client = korean_school.Client()
    school = await client.school(name="<학교명>")
    # 학년과 반은 int형이나, str으로 작성해도 문제 없음.
    timetable = await school[0].timetable(grade="학년", class_nm="반")
    
    print("{}시간: {}".format(timetable[0].time, timetable[0].title))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# > 1시간: 자율활동
# 본 정보는 가락고등학교 2학년 1반의 2021년 3월 2일 기준 자료 입니다.
```

#### 학원 정보 불러오기
```python
import korean_school
import asyncio


async def main():
    client = korean_school.Client()
    # 학원 정보를 불러 올때에는 무조건 시/도 지역을 지정해주셔야합니다.
    academy = await client.academy(provincial_code=korean_school.Location.Seoul, name="<학원명>")
    print(academy[0].name)
    print(academy[0].address1)
    print(academy[0].address2)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```