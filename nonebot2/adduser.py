import pandas as pd


def showuser():
    return pd.read_pickle('/root/service/nonebot/nonebot/plugins/arcbot/db.pkl')

def adduser(code, qqnum) -> str:
    df = pd.read_pickle('/root/service/nonebot/nonebot/plugins/arcbot/db.pkl')
    df.loc[df.index.size] = [int(code), int(qqnum)]
    df.to_pickle('/root/service/nonebot/nonebot/plugins/arcbot/db.pkl')
    return 'success'

def deluser(code) -> str:
    df = pd.read_pickle('/root/service/nonebot/nonebot/plugins/arcbot/db.pkl')
    df.drop(df[df['code'] == int(code)].index, inplace=True)
    df.reset_index(drop=True)
    df.to_pickle('/root/service/nonebot/nonebot/plugins/arcbot/db.pkl')
    return 'success'

def qqnum2code(qqnum) -> int:
    df = pd.read_pickle('/root/service/nonebot/nonebot/plugins/arcbot/db.pkl')
    return df[df['qqnum'] == int(qqnum)]['code'].values[0]
