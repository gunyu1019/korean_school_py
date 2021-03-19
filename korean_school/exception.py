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


class Schoolexception(Exception):
    """Korean-School의 메인 예외 클래스 입니다."""
    pass


class RequestsExcetion(Schoolexception):
    """Korean-School의 requests 예외 클래스입니다."""
    def __init__(self, response):
        self.response = response

        msg = self.response.get('MESSAGE')
        code = self.response.get('CODE')
        super().__init__(f"{msg} (반환 값: {code})")


class NotFound(RequestsExcetion):
    """해당하는 데이터가 없습니다."""
    pass


class Forbidden(RequestsExcetion):
    """인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오."""
    pass


class TooManyRequests(RequestsExcetion):
    """일별 트래픽 제한을 넘은 호출입니다. 오늘은 더이상 호출할 수 없습니다."""
    pass


class NotImplemented(RequestsExcetion):
    """요청위치 값의 타입이 유효하지 않습니다.요청위치 값은 정수를 입력하세요."""
    pass


class InternalServerError(RequestsExcetion):
    """서버 오류입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다."""
    pass
