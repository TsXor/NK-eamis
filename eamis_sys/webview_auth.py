import time, webview
from threading import Lock
from datetime import datetime, timedelta
from requests.cookies import RequestsCookieJar


CHECK_INTERVAL = 0.1
EAMIS_HOME = 'https://eamis.nankai.edu.cn/eams/home.action'


def cookies_to_jar(window, cookie_jar: RequestsCookieJar):
    # 获取7天后的时间
    later = datetime.now() + timedelta(days=7)
    later_str = later.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    for ck in window.get_cookies():
        for k, v in ck.items():
            # 出于一些神奇的原因，我们需要重设这些cookie的过期时间
            v['expires'] = later_str; cookie_jar[k] = v


def is_login_over(window) -> bool:
    if window.get_current_url() != EAMIS_HOME: return False
    return window.get_current_url() == EAMIS_HOME \
        and window.evaluate_js("document.querySelector('#mainTable')") is not None


def webview_login(cookie_jar: RequestsCookieJar):
    '''
    使用Webview辅助用户登录eamis。
    '''
    window_present = True

    def on_closing():
        nonlocal window_present
        window_present = False

    def wait_for_cookies(window):
        while True:
            if not window_present: return
            try:
                if is_login_over(window): break
            except: return
            time.sleep(CHECK_INTERVAL)

        window.evaluate_js('window.location.reload()')
        
        cookies_to_jar(window, cookie_jar)
        
        # 已完成，关闭窗口
        window.destroy()

    window = webview.create_window('eamis login', EAMIS_HOME)
    window.events.closing += on_closing # type: ignore
    webview.start(wait_for_cookies, window, private_mode=False)
