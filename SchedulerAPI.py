import asyncio, time, requests
import aioschedule as schedule

_IP_ = '192.168.2.11:8083'
_MLIP_ = '192.168.2.11:5002'

RECOM_EXEC_INTERVAL = 5

def strftime():
    f = str(round(time.time() % 1,5)).replace('0.','')
    return time.strftime(f'[%Y-%m-%d %H:%M:%S.{f}]')

def prints(*args):
    print(strftime(), end=' ')
    print(args)

def init_get_recom_exec_interval():
    try:
        data = requests.get(f'http://{_IP_}/service/copt/bat/combustion/background/get_recom_exec_interval').json()
        interval = data['object']
    except Exception as e:
        prints('Initial get recom exec interval error:', e)
    return interval

async def get_recom_exec_interval():
    global RECOM_EXEC_INTERVAL
    try:
        data = requests.get(f'http://{_IP_}/service/copt/bat/combustion/background/get_recom_exec_interval').json()
        interval = data['object']
        RECOM_EXEC_INTERVAL = interval
    except Exception as e:
        prints('Get recom exec interval error:', e)
    return interval

async def safeguard_check():
    try:
        data = requests.get(f'http://{_IP_}/service/copt/bat/combustion/background/safeguardcheck')
        await asyncio.sleep(1)
    except Exception as e:
        prints('Safeguard check error:', e)

async def machine_learning_predict():
    try:
        data = requests.get(f'http://{_IP_}/service/copt/bat/combustion/background/update_machine_learning_recommendation')
    except Exception as e:
        prints('Machine learning prediction error:', e)
    

try: RECOM_EXEC_INTERVAL = init_get_recom_exec_interval()
except: pass

schedule.every().seconds.do(safeguard_check)
schedule.every(RECOM_EXEC_INTERVAL).minutes.do(machine_learning_predict)


loop = asyncio.get_event_loop()
while True:
   loop.run_until_complete(schedule.run_pending())
   time.sleep(0.1)

