from nonebot import on_command
from nonebot.rule import to_me, command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

import os
import httpx

from .adduser import *
from .arcapi import genimg, getrecent


command_list = on_command('command', command('command'))

@command_list.handle()
async def _command_list(bot: Bot, event: Event, state: T_State):
    li = ['//a recent', '//a b30', '//a register [code]', '//a removeuser [code]', '//get_user_list']
    await bot.send(message='\n'.join(li), event=event)
    await command_list.finish()



arcbot = on_command('a', command('a'))

@arcbot.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    # await bot.send(message=event.get_session_id(), event=event)
    arg = str(event.get_message()).strip()
    if arg:
        state["arg"] = arg

@arcbot.got('arg', prompt='出错啦，请艾特 Master')
async def handle_best30(bot: Bot, event: Event, state: T_State):

    if state['arg'] == 'recent' and str(event.get_session_id()) in str(showuser()):
        try:
            code = qqnum2code(int(event.get_session_id()))
            recent = await getrecent(code)
            await bot.send(message=recent, event=event)
        except:
            await bot.send(message='查询失败了~', event=event)

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
                await bot.send(message= 'ID: ' + str(event.get_session_id()) + '\n努力生成中`(*>﹏<*)', event=event)
                code = qqnum2code(int(event.get_session_id()))
                path = await genimg(code)
                await bot.send(message=[{"type":"image","data":{"file":f"file://{path}"}}], event=event)
            except:
                await bot.send(message='查询失败，可能是歌曲未打满 30 首', event=event)
        else:
            await bot.send(message='未注册哼哼 啊啊啊啊啊啊 啊啊啊啊啊啊啊啊啊啊啊ヾο(=ω＜=)ρ', event=event)

        await arcbot.finish()


    if state['arg'].split(' ')[0] == 'register':
        code = state['arg'].split(' ')[1] or ''
        if len(code) == 9:
            adduser(int(code), int(event.get_session_id()))
            await bot.send(message='Success', event=event)
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
