from nonebot.plugin.on import on_message, on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Message, GROUP_ADMIN, GROUP_OWNER
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER

from pathlib import Path

import time
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json

# 加载阻断配置
path = Path() / "data" / "block"
if not path.exists():
    os.makedirs(path)

time_config_file = path / "time_config.json"

if time_config_file.exists():
    with open(time_config_file, "r", encoding="utf8") as f:
        time_config = json.load(f)
else:
    time_config = {}
    with open(time_config_file, "w", encoding="utf8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)


group_config_file = path / "group_config.json"

if group_config_file.exists():
    with open(group_config_file, "r", encoding="utf8") as f:
        group_config = json.load(f)
else:
    group_config = {}
    with open(group_config_file, "w", encoding="utf8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

cache = {}

block = on_message(priority = 1, block = False)

@block.handle()
async def _(matcher: Matcher, event:GroupMessageEvent):
    arg = str(event.message)
    for command in set(group_config.keys()):
        if arg.startswith(command):
            group_id = event.group_id
            if group_id in group_config[command]:
                matcher.stop_propagation()
                return
            break

    for command in set(time_config.keys()):
        if arg.startswith(command):
            group_id = event.group_id
            user_id = event.user_id
            cache.setdefault(group_id,{})
            cd = time.time() - cache[group_id].get(user_id,0)
            if cd > time_config[command]:
                cache[group_id][user_id] = time.time()
                return
            else:
                matcher.stop_propagation()
                await block.send(f"你的【{command}】冷却还有{int(time_config[command] - cd) + 1}秒",at_sender = True)
                return


add_block = on_command("添加阻断", permission = SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority = 5, block = True)

@add_block.handle()
async def _(matcher: Matcher, event:GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if msg and len(msg) >= 2:
        command = msg[0]
        if command in ["添加阻断","解除阻断"]:
            await add_block.finish("不可以这么做")
        block_type = msg[1]
        if (block_type == "时间" or block_type == "冷却") and len(msg) == 3:
            try:
                cd = int(msg[2])
            except:
                await add_block.finish(f"添加阻断接受了错误的时间参数：{msg[2]}")
            time_config[command] = cd
            with open(time_config_file, "w", encoding="utf8") as f:
                json.dump(time_config, f, ensure_ascii=False, indent=4)
            await add_block.finish(f"指令【{command}】已设置冷却：{cd}s")
        elif block_type == "群":
            group_config.setdefault(command,[])
            group_config[command].append(event.group_id)
            group_config[command] = list(set(group_config[command]))
            with open(group_config_file, "w", encoding="utf8") as f:
                json.dump(group_config, f, ensure_ascii=False, indent=4)
            await add_block.finish(f"指令【{command}】已在本群屏蔽。")

    await add_block.finish("添加阻断指令格式错误。")


del_block = on_command("解除阻断", permission = SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority = 5, block = True)

@del_block.handle()
async def _(matcher: Matcher, event:GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if msg and len(msg) == 2:
        command = msg[0]
        block_type = msg[1]
        if block_type == "时间" or block_type == "冷却":
            if command in time_config.keys():
                del time_config[command]
                with open(time_config_file, "w", encoding="utf8") as f:
                    json.dump(time_config, f, ensure_ascii=False, indent=4)
                await del_block.finish(f"指令【{command}】已解除冷却限制。")
            else:
                await del_block.finish(f"指令【{command}】没有设置冷却。")
        elif block_type == "群":
            group_id = event.group_id
            if command in group_config.keys():
                if group_id in group_config[command]:
                    group_config[command].remove(group_id)
                    with open(group_config_file, "w", encoding="utf8") as f:
                        json.dump(group_config, f, ensure_ascii=False, indent=4)
                    await del_block.finish(f"指令【{command}】已解除屏蔽。")

            await del_block.finish(f"指令【{command}】未屏蔽。")

    await del_block.finish("解除阻断指令格式错误。")