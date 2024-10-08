<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">

# nonebot_plugin_matcher_block

通用指令阻断

</div>

## 安装

    pip install nonebot_plugin_matcher_block
	
## 使用

    nonebot.load_plugin('nonebot_plugin_matcher_block')
    
## 功能

### 添加阻断

`添加阻断 指令 参数`


__参数列表：__

`屏蔽` `冷却` `共享冷却` `全局`

__指令解析：__

使用 `添加阻断 今日运势 屏蔽` 后，`今日运势` 在本群内被屏蔽

使用 `添加阻断 娶群友 冷却 120` 后，本群内成员各自的 `娶群友` 将会有120秒冷却

使用 `添加阻断 点歌 共享冷却 120` 后，本群内成员共享 `点歌` 的冷却时间

_注意:以上三个参数只生效1个。可以把某一指令设置多种阻断类型，也就是即屏蔽，又冷却，也共享冷却。~~但是这样做没有什么必要~~_

使用 `添加阻断 金币签到 冷却 120 全局` 后，在全局为 `金币签到` 设置120秒CD

在全局设置之后还可以回到某一群单独设置
比如 `添加阻断 金币签到 屏蔽 全局` 会导致全全局屏蔽掉此指令。但是回到某一群发送 `解除阻断 金币签到 群` 可以仅在此群使用该指令。

### 解除阻断

`解除阻断 指令`

在本群取消阻断该指令，如果此指令设置过多种阻断方式会全部解除。

`解除阻断 指令 全局`

在全局取消阻断该指令，如果此指令未设置过全局指令则会解除失败。

__注意:即使你在所有的群都阻断了某一指令，这个指令的阻断也不是全局阻断，无法用全局参数为所有的群解除阻断。__

### 查看阻断

`查看阻断`

查看本群被阻断的指令。

## 关于指令参数

### 可选配置和功能：

    block_prod: bool = False	# 设为 True 时管理员以上权限将不受指令阻断规则限制
    block_match_start: bool = True	# 自动剔除你设置的Bot指令前缀（COMMAND_START）

以上配置需要填写在nonebot的配置中
    
### 不同指令前缀视为不同指令：

例如使用指令 `添加阻断 透群友 群` 在本群屏蔽了 `透群友` 指令。

但如果指令还可以用 `\透群友` 触发，那么 `\透群友` 事件并不会被屏蔽。

该功能可以关闭：

例如你希望仅使用 `添加阻断 本群cp 屏蔽` 即可同时屏蔽 `\本群cp` `#本群cp` ...，请在你的.env中添加：

    block_match_start = True

[~~插件广告：娶群友~~](https://github.com/KarisAya/nonebot_plugin_groupmate_waifu)


### 使用正则匹配：

如果指令以"^"开头，那么通用指令阻断将会认为本指令是一条正则匹配。

例如使用指令 `添加阻断 ^来.*张.+$ 冷却 300` 为 `来张xx色图` 添加阻断，

那么本条配置将会阻断诸如 `来张色图` `来三张白丝` 等 可以用 ^来.*张.+$ 匹配到的字符串。

[~~插件广告：我要一张xx涩图~~](https://github.com/KarisAya/nonebot_plugin_setu_collection)


## 其他


如有建议，bug反馈，以及讨论新玩法，新机制（或者单纯没有明白怎么用）可以来加群哦~

![群号](https://github.com/KarisAya/nonebot_plugin_game_collection/blob/master/%E9%99%84%E4%BB%B6/qrcode_1665028285876.jpg)
