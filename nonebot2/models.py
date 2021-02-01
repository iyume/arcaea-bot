from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import GroupMessageEvent

def validate_status() -> Rule:

    async def _validate_status(bot: "Bot", event: "Event") -> bool:
        if isinstance(event, GroupMessageEvent):
            if event.group_id not in bot.config.GroupList.values():
                return False
            elif event.get_type() == 'private':
                return True
            elif event.group_id in bot.config.GroupList.values():
                return False
        else:
          return False

    return Rule(_validate_status)