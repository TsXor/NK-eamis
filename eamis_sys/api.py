from typing import cast
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from .call_js import js_eval_data_reload
from .webview_auth import webview_login
from .client import EamisClientBasics
from .dtypes import LessonData


class EamisJsDataError(Exception): pass


class EamisClient(EamisClientBasics):
    '''
    注意：连续调用API时需要在中间插入sleep，否则服务端只会回复“不要过快点击”。
    '''

    @classmethod
    def from_webview(cls):
        obj = cls()
        clean = False
        while True:
            webview_login(obj.cookies, clean)
            if not obj.cookies: raise ValueError('登录未成功')
            resp = obj.std_elect_course()
            if not resp.is_redirect: break
            clean = True
            obj.cookies.clear()
        return obj

    def std_elect_course(self):
        '''
        你需要首先调用这个函数来访问选课主界面，
        否则对任何选课界面的访问都会造成服务端错误。
        为什么呢？要问就问eamis开发人员吧。
        '''
        return self.document('/eams/stdElectCourse.action', allow_redirects=False)

    def default_page(self, profile_id: int):
        resp = self.document(
            '/eams/stdElectCourse!defaultPage.action',
            params={'electionProfile.id': str(profile_id)}
        )
        return resp.text

    @staticmethod
    def semester_id_from_default_page(page_text: str):
        soup = BeautifulSoup(page_text, features="lxml")
        qr_script_url: str = soup.find(id="qr_script")['src'] # type: ignore
        url_query = urlparse(qr_script_url).query
        return parse_qs(url_query)['semesterId'][0]

    def semester_id(self, profile_id: int):
        return self.semester_id_from_default_page(self.default_page(profile_id))

    def lesson_data(self, profile_id: int) -> list[LessonData]:
        resp = self.document(
            '/eams/stdElectCourse!data.action',
            params={'profileId': str(profile_id)}
        )
        try:
            dat = js_eval_data_reload(resp.text, 'lessonJSONs')
        except Exception:
            raise EamisJsDataError(resp.text)
        return cast(list[LessonData], dat)

    def elect_course(self, profile_id: int, course_id: int, semester_id: str):
        fetch_headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': f'https://{self.HOST}',
        }
        form_data = {
            'optype': 'true',
            'operator0': f'{course_id}:true:0',
            'lesson0': f'{course_id}',
            f'expLessonGroup_{course_id}': 'undefined',
            f'alternateElection_{course_id}': '1'
        }
        resp = self.xhr(
            'POST', '/eams/stdElectCourse!batchOperator.action',
            headers=fetch_headers,
            data=form_data,
            params={'profileId': str(profile_id)},
            cookies={'semester.id': str(semester_id)}
        )
        return resp.text
