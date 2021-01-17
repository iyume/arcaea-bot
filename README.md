## Arcbot
本项目使用了 Nonebot2 + go-cqhttp 作机器人通信，连接方式为 WebSocket 反向代理

go-cqhttp 配置文件位于`go-cqhttp/config.hjson`

nonebot 插件位于`nonebot2/*`，使用前请在 nonebot 目录下创建对应插件文件夹

建议使用`virtualenv manager`来创建 arcbot

## 功能介绍
获取 best30 并绘制成图片返回

根据 QQ 号储存用户信息

*Commands*
`//a recent`
`//a b30`
`//a register [code]`
`//a removeuser [code]`
`//get_user_list`

## 现有 arcbot
3520438881

## requirements
`Arc-api`
`Image`
`pandas`
`nb-cli`
