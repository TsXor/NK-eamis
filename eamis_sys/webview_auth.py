import time, webview
from threading import Lock
from datetime import datetime, timedelta
from requests.cookies import RequestsCookieJar


CHECK_INTERVAL = 0.1
EAMIS_HOME = 'https://eamis.nankai.edu.cn/eams/home.action'
EAMIS_LOGOUT = 'https://eamis.nankai.edu.cn/eams/logout.action'


def is_login_over(window) -> bool:
    if window.get_current_url() != EAMIS_HOME: return False
    return window.get_current_url() == EAMIS_HOME \
        and window.evaluate_js("document.querySelector('#mainTable')") is not None


def webview_login(cookie_jar: RequestsCookieJar, clean: bool = False):
    '''
    使用Webview辅助用户登录eamis。
    目前的缺陷为大部分时候每次运行都需要重新登录。
    '''
    window_present = True

    def on_closing():
        nonlocal window_present
        window_present = False

    def wait_for_cookies(window):
        if clean:
            window.evaluate_js(f'window.location.replace("{EAMIS_LOGOUT}")')

        while True:
            if not window_present: return
            try:
                if is_login_over(window): break
            except: return
            time.sleep(CHECK_INTERVAL)
        
        # 获取7天后的时间
        later = datetime.now() + timedelta(days=7)
        later_str = later.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        for ck in window.get_cookies():
            for k, v in ck.items():
                # 出于一些神奇的原因，我们需要重设这些cookie的过期时间
                v['expires'] = later_str; cookie_jar[k] = v
        
        # 已完成，关闭窗口
        window.destroy()

    window = webview.create_window('eamis login', EAMIS_HOME)
    window.events.closing += on_closing # type: ignore
    webview.start(wait_for_cookies, window, private_mode=False)
