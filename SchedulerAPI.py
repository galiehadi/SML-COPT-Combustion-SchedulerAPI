import time, requests, db_config, inspect, threading
from urllib.parse import quote_plus as urlparse

_UNIT_CODE_ = db_config._UNIT_CODE_
_UNIT_NAME_ = db_config._UNIT_NAME_
_USER_ = db_config._USER_
_PASS_ = urlparse(db_config._PASS_)
_IP_ = db_config._IP_
_DB_NAME_ = db_config._DB_NAME_
_LOCAL_IP_ = db_config._LOCAL_IP_

Timer = {
    'safeguard_check': {
        'last_running': 0,
        'scheduler': 1
    },
    'ml_run': {
        'last_running': 0,
        'scheduler': 3
    },
}

def now():
    ms = str(time.time() % 1)[2:5]
    return time.strftime(f'%Y-%m-%d %X.{ms}\t')

def safeguard_check():
    func_name = inspect.currentframe().f_code.co_name
    if (time.time() - Timer[func_name]['last_running']) > Timer[func_name]['scheduler']:
        Timer[func_name]['last_running'] = time.time()

        # Run code here
        # print(now(), f'running {func_name}')
        safeguard_url = f'http://{_LOCAL_IP_}:8083/service/copt/bat/combustion/background/safeguardcheck'
        try:
            requests.get(safeguard_url)
        except Exception as E:
            print(now(), f'Failed to call "{safeguard_url}"')
        

def ml_run():
    func_name = inspect.currentframe().f_code.co_name
    if (time.time() - Timer[func_name]['last_running']) > Timer[func_name]['scheduler']:
        Timer[func_name]['last_running'] = time.time()

        # Run code here
        print(now(), f'running {func_name}')
        ## update ml_run timer

        try: 
            requests.get(f'http://{_LOCAL_IP_}:8083/service/copt/bat/combustion/background/runner')
            data = requests.get(f'http://{_LOCAL_IP_}:8083/service/copt/bat/combustion/background/get_recom_exec_interval')
            Timer[func_name]['scheduler'] = 60 * (float(data.json()['object']))
            print(now(), f"Updated timer to {Timer[func_name]['scheduler']} sec.")
        except Exception as e:
            print(now(), f'Error calling "{e}"')

def main():
    t1 = threading.Thread(target=safeguard_check)
    t2 = threading.Thread(target=ml_run)
    t1.start()
    t2.start()
    

while True:
    main()
    time.sleep(1)
