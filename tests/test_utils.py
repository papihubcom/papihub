from papihub import utils


def test_parse_cookies_expire_time():
    print(utils.parse_cookies_expire_time('session_id=abcd1234; expires=Wed, 09-Jun-2021 10:18:14 GMT'))
