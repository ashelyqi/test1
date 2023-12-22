import logging

# def log_format():
#     #设置日志显示
#     logging.basicConfig(
#         filename='log.txt',
#         level=logging.INFO,
#         filemode='a',
#         encoding='utf-8',
#         format='%(asctime)s %(levelname)-8s %(name)s [%(funcName)s(%(module)s:%(lineno)s)] %(message)s'
#     )

import logging
import logging.config
import logging.handlers
import json
import yaml

def log_format():
    # print("执行了logformate...")
    config={
        "version":1,
        "formatters":{
            "formatter":{
                "format":"%(asctime)s %(levelname)-8s %(name)s [%(funcName)s(%(module)s:%(lineno)s)] %(message)s"
            }
        
        },
        "handlers":{
            # "tcp_handler":{
            #     "level":"DEBUG",
            #     "class":"logging.handlers.SocketHandler",
            #     "host":"127.0.0.1",
            #     "port":"9020"
            # },
            "console_handler":{
                "class":"logging.StreamHandler",
                "formatter":"formatter",
                "level":"INFO"

            },
            "file_handler":{
                "class":"logging.FileHandler",
                "encoding":"utf-8",
                "filename":"log.txt",
                "mode":"a",
                "formatter":"formatter",
                "level":"INFO"

            }
        },
        "loggers":{
            "":{
                "level":"DEBUG",
                "handlers":["file_handler","console_handler"]
            }
        }
    }

    with open("config.yaml",'w') as f:
        yaml.safe_dump(config,f)

    with open("config.yaml") as f:
        logging.config.dictConfig(yaml.safe_load(f))

    # logger=logging.getLogger("mainApp")
    # logger_code=logging.getLogger("mainApp.code")
    # logger_test=logging.getLogger("mainApp.test")

    # def add(a,b):
    #     logger_code.info(f'收到的参数，a={a},b={b}')

    #     c=a+b
    #     logger_code.error(f'输出结果c={c}')

    # if __name__=="__main__":
    #     add(1,2)