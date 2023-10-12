# import baostock as bs
from Common.CEnum import AUTYPE, DATA_FIELD, KL_TYPE
from Common.CTime import CTime
from Common.func_util import kltype_lt_day, str2float
from KLine.KLine_Unit import CKLine_Unit
from .CommonStockAPI import CCommonStockApi
# from Db.MySQLDb import MySQLDb
import pandas as pd


def create_item_dict(data, column_name):
    for i in range(len(data)):
        if i == 0:
            data[i] = parse_time_column(data[i])
        else:
            pass #data[i]
#         data[i] = parse_time_column(data[i]) if i == 0 else str2float(data[i])
    return dict(zip(column_name, data))


def parse_time_column(dinp):
    # 20230103100000
    # 20210902113000000
    # 20230103100000 14
    # 2021-09-13
    # 20230103100000
    # 20230103100000000000
    # 20210902113000000 # target

    # inp = dinp.strftime('%Y-%m-%d') 2023-09-01 09:30:00
    inp = dinp.replace(" ", "").replace("-", "").replace(":", "")

    if len(inp) == 10:
        year = int(inp[:4])
        month = int(inp[5:7])
        day = int(inp[8:10])
        hour = minute = 0
    elif len(inp) == 14:
        year = int(inp[:4])
        month = int(inp[4:6])
        day = int(inp[6:8])
        hour = int(inp[8:10])
        minute = int(inp[10:12])
    else:
        raise Exception(f"unknown time column from baostock:{inp}")
    # print('date', dinp, inp, year, month, day, hour, minute)
    return CTime(year, month, day, hour, minute)

class CsvData(CCommonStockApi):
    # mydb = MySQLDb()

    def __init__(
        self,
        code,
        k_type=KL_TYPE.K_DAY,
        begin_date=None,
        end_date=None,
        autype=AUTYPE.QFQ,
    ):
        super(CsvData, self).__init__(code, k_type, begin_date, end_date, autype)

    def get_kl_data(self):
        cols = ['time_key','open','high','low','close']
        dfr = pd.read_csv('iwm.csv',index_col=None).drop(columns=['Unnamed: 0'])
        for elem in dfr.values:
            d = create_item_dict(list(elem), cols)
            yield CKLine_Unit(d)

    @classmethod
    def do_init(cls):
        ...

    @classmethod
    def do_close(self):
        ...

    def is_day_plus(self):
        return (
            self.k_type == KL_TYPE.K_DAY
            or self.k_type == KL_TYPE.K_WEEK
            or self.k_type == KL_TYPE.K_MON
        )
