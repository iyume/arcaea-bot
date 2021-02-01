from nonebot import on_command, on_keyword
from nonebot.matcher import Matcher, matchers
from nonebot.rule import to_me, command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

import os
import httpx
import asyncio
import base64

from .adduser import *
from .arcapi import genimg, getrecent, getbest30, getuserinfo


command_list = on_command('help', aliases={'command'})

@command_list.handle()
async def _command_list(bot: Bot, event: Event, state: T_State, matcher: Matcher):
    li = ['prefix: / //\n',
        '//a recent', '//a b30', '//a register [code]', '//a removeuser [code]\n',
        '//get_user_list', '//setu {other keywords}', '//python {python3}']
    await bot.send(message='\n'.join(li), event=event)
    await command_list.finish()



arcbot = on_command('a', aliases={'arc'}, priority=2)

@arcbot.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    # await bot.send(message=event.get_session_id(), event=event)
    arg = str(event.get_message()).strip()
    if arg:
        state["arg"] = arg

@arcbot.got('arg', prompt='参数见 help')
async def handle_best30(bot: Bot, event: Event, state: T_State):

    userlst = str(showuser())

    if state['arg'] == 'userinfo':
        if str(event.get_session_id()) in userlst:
            try:
                code = qqnum2code(int(event.get_session_id()))
                userinfo = await getuserinfo(code)
                await bot.send(message=str(userinfo), event=event)
            except:
                await bot.send(message='失败了~', event=event)
        else:
            await bot.send(message='未注册', event=event)
        await arcbot.finish()


    if state['arg'] == 'recent':
        if str(event.get_session_id()) in userlst:

            try:
                code = qqnum2code(int(event.get_session_id()))
                recent = await getrecent(code)
                await bot.send(message=str(recent), event=event)
            except:
                await bot.send(message='失败了~', event=event)

        else:
            await bot.send(message='未注册', event=event)
        await arcbot.finish()


    if state['arg'] == 'b30':
        # await bot.send(message="[CQ:image,file=file:///root/service/notebook_workdir/img.jpg]b30", event=event)
        # await bot.send(message=[{"type":"image","data":{"file":"file:///root/service/notebook_workdir/img.jpg"}}], event=event)
        # cq_img = await get_best30(int(event.get_session_id()))
        # await bot.send(message=event.get_event_name(), event=event)
#        if 'private' in event.get_event_name():
#            await get_best30(int(event.get_session_id()), False)
#        else:
#            await get_best30(int(event.get_session_id()), True)
        # await bot.send(message=event.get_user_id(), event=event)
        if str(event.get_session_id()) in str(showuser()):
            try:
                await bot.send(message= 'ID: ' + str(event.get_session_id()) + '\n努力生成中`(*>﹏<*)\n注意：初次查分会耗时 1min 左右', event=event)
                code = qqnum2code(int(event.get_session_id()))
                # path = await genimg(code)
                path = await getbest30(code)
                await bot.send(message=[{"type":"image","data":{"file":f"file://{path}"}}], event=event)
            except:
                await bot.send(message='异常警报！请联系 Master', event=event)
        else:
            await bot.send(message='未注册哼哼 啊啊啊啊啊啊 啊啊啊啊啊啊啊啊啊啊啊ヾο(=ω＜=)ρ', event=event)

        await arcbot.finish()


    if state['arg'].split(' ')[0] == 'register' or 'bind':
        code = state['arg'].split(' ')[-1] or ''
        if len(code) == 9:
            if event.get_session_id() not in userlst:
                adduser(int(code), int(event.get_session_id()))
                await bot.send(message='Success', event=event)
            else:
                await bot.send(message='已注册', event=event)
        else:
            await bot.send(message='Code invalid', event=event)


    if state['arg'].split(' ')[0] == 'removeuser':
        code = state['arg'].split(' ')[1] or None
        if code != None and str(code) in str(showuser()):
            _ = deluser(int(code))
            await bot.send(message=f'Delete {code} Success', event=event)
        else:
            await bot.send(message='Code invalid',event=event)
        await arcbot.finish()


    await arcbot.finish()



get_users = on_command('get_user_list', command('get_user_list'))

@get_users.handle()
async def _get_users(bot: Bot, event: Event, state: T_State):
    await bot.send(message=str(showuser()), event=event)
    await get_users.finish()



setu = on_command('setu', command('setu'))
setu_t = on_keyword(['哭', '枯', '难受', 'wsl'])

proxy_url = 'api.ineko.cc/pixiv'

async def fetch(target, client):
    return await client.get(target)

@setu.handle()
@setu_t.handle()
async def _setu(bot: Bot, event: Event, state: T_State):

    try:
        async with httpx.AsyncClient() as client:
            r = await asyncio.gather(fetch('https://api.lolicon.app/setu/?apikey=986214496009b5f04da0c8&size1200=true&proxy=' + proxy_url, client))
    except:
        await bot.send(message='超时了qwq', event=event)
        await setu.finish()

    content = r[0].json()

    if content['code'] == 429:
        await bot.send(message='setu 看太多了啦，api 都不够用了', event=event)
        await setu.finish()

    try:

        pix_url = content['data'][0]['url']
        img_url = pix_url
        pid = content['data'][0]['pid']
        quota = content['quota']

        async with httpx.AsyncClient() as client:
            img = await asyncio.gather(fetch(img_url, client))

        img_encoded = base64.b64encode(img[0].content)

        # await bot.send(message=[{"type":"image","data":{"file":send_url}}], event=event)
        await bot.send(message=[{"type":"text","data":{"text":f"PID: {pid}\n"}}, {"type":"text","data":{"text":f"剩余次数: {quota}"}}, {"type":"image","data":{"file":"base64://"+img_encoded.decode()}}], event=event)
        #await bot.send(message=f"PID: {pid}", event=event)

    except:

        await bot.send(message='超时了qwq', event=event)

    await setu.finish()
