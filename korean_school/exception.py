def check_requests(resp):
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
