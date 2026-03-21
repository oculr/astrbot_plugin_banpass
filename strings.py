# 文案啥的放这
MSG_NO_REASON = "无理由"
MSG_NO_TARGETS = "没有指定目标用户"
MSG_NO_BAN_RECORD = "没有封禁记录"
MSG_TIME_PARSE_ERROR = "解析时间格式失败"
MSG_HELP_TIME_FORMAT = """⏰ 时间格式说明：
- 数字+单位：1d(1天)/2h(2小时)/30m(30分钟)/10s(10秒)
- 默认永久限制"""

# command语法
commands = {
    "ban": "/ban <@用户> [时间（默认无期限）] [理由（默认无理由）]",
    "ban-all": "/ban-all <@用户> [时间（默认无期限）] [理由（默认无理由）]",
    "pass": "/pass <@用户> [时间（默认无期限）] [理由（默认无理由）]",
    "pass-all": "/pass-all <@用户> [时间（默认无期限）] [理由（默认无理由）]",
}
# 输出文案
messages = {
    "banned_user": "已在 {umo} 禁用以下用户 {user}，时限：{time}，理由：{reason}",
    "banned_user_global": "已全局禁用 {user}，时限：{time}，理由：{reason}",
    "passed_user": "已在 {umo} 解限 {user}，时限：{time}，理由：{reason}",
    "passed_user_global": "已在全局解限 {user}，时限：{time}，理由：{reason}",
}
