from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

def tick(): # 定义作业，打印当前时间
    print("Tick time is:s%",datetime.now())

if __name__=="__main__": # 定义主函数入口
    schduler = BlockingScheduler() # 实例化BlockingScheduler类，不带参默认储存器-内存
    schduler.add_job(tick,'interval',seconds=5)
    print("Press ctrl+{0} to exit".format('break') if os.name == 'nt' else 'c') #  打印退出方法信息，触发器date，cron,interval
    try:
        schduler.start() # 启动调度器
    except {KeyboardInterrupt,SystemExit}:
        pass