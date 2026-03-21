import astrbot.api.message_components as message_components
from astrbot.api import logger, AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, StarTools

import time

from . import time_utils, strings, banpass_manager


def extract_args(event: AstrMessageEvent):
    """
    返回 用户列表user_ids[str], 封禁时间time, 封禁原因reason
    """
    at_users = []
    _time = float('inf')
    _reason = strings.MSG_NO_REASON

    args = ""
    msgs = event.get_messages()
    at_component_pos = 0
    for i in range(len(msgs)):
        if isinstance(msgs[i], message_components.At) and getattr(msgs[i], "qq") != event.get_self_id():
            at_users.append(str(msgs[i].qq))
            at_component_pos = i

    if at_component_pos+1 >= len(msgs):
        return at_users, _time, _reason

    # /ban [At:] [At:] [At:] 1d 原因xxx
    for i in range(at_component_pos+1, len(msgs)):
        if isinstance(msgs[i], message_components.Plain) and getattr(msgs[i], "text"):
            args += getattr(msgs[i], "text")

    split = args.split()
    if len(split) >= 1:
        _time = time_utils.time_str_to_float(split[0])
    if len(split) >= 2:
        _reason = split[1]
    return at_users, _time, _reason

class ReNeBan(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        # 初始化数据文件管理器
        super().__init__(context, config)
        self.manager = banpass_manager.BanPassManager(
            StarTools.get_data_dir()
        )

    @filter.command("banhelp")
    async def ban_help(self, event: AstrMessageEvent):
        """
        显示reneban帮助信息
        """
        yield event.plain_result("\n".join([cmd for k, cmd in strings.commands.items()]))

    def update_user(
            self,
            umo: str,
            tgt_users: list[str],
            is_ban: bool,
            _time: float,
            _reason: str,
            is_global=False,
    ):
        expire_reason = banpass_manager.build_expire_reason(_time, _reason)

        # 这里如果是ban的话，重置pass记录
        bp = banpass_manager.BanPass(ban_=expire_reason, pass_=banpass_manager.ExpireReason()) if is_ban else banpass_manager.BanPass(pass_=expire_reason)
        for user in tgt_users:
            self.manager.update(umo, user, bp, is_global)

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ban")
    async def ban_user(
            self,
            event: AstrMessageEvent,
    ):
        """
        在会话中禁用指定用户的使用权限。
        格式：/ban <@用户|UID（QQ号）> [时间（默认无期限）] [理由（默认无理由）] [UMO]
        时间格式：数字+单位（d=天，h=小时，m=分钟，s=秒），如 1d 表示1天，12h 表示12个小时，不带单位默认秒，0表示无期限
        示例：/ban @张三 7d
        注意：单次仅能禁用一个会话的一个用户
        """
        umo = event.unified_msg_origin
        try:
            tgt_users, _time, _reason = extract_args(event)
        except ValueError as err:
            logger.error(err)
            yield event.plain_result(str(err) + "\n" + strings.MSG_HELP_TIME_FORMAT)
            return
        if not tgt_users:
            yield event.plain_result(strings.MSG_NO_TARGETS)
            return
        if _time is None:
            _time = float("inf")
        self.update_user(umo, tgt_users, True, _time, _reason)

        yield event.plain_result(
            strings.messages["banned_user"].format(
                umo=umo, user=str(tgt_users), time=time_utils.time_remaining_format(_time), reason=_reason
            )
        )

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ban-all")
    async def ban_all(
            self,
            event: AstrMessageEvent,
    ):
        """
        在全局禁用指定用户的使用权限。
        格式：/ban-all <@用户|UID（QQ号）> [时间（默认无期限）] [理由（默认无理由）]
        时间格式：数字+单位（d=天，h=小时，m=分钟，s=秒），如 1d 表示1天，12h 表示12个小时，不带单位默认秒，0表示无期限
        示例：/ban-all @张三 7d
        注意：单次仅能禁用一个用户
        """
        umo = event.unified_msg_origin
        try:
            tgt_users, _time, _reason = extract_args(event)
        except ValueError as err:
            logger.error(err)
            yield event.plain_result(str(err) + "\n" + strings.MSG_HELP_TIME_FORMAT)
            return
        if not tgt_users:
            yield event.plain_result(strings.MSG_NO_TARGETS)
            return
        self.update_user(umo, tgt_users, True, _time, _reason, True)

        yield event.plain_result(
            strings.messages["banned_user_global"].format(
                user=str(tgt_users), time=time_utils.time_remaining_format(_time), reason=_reason
            )
        )

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("pass")
    async def pass_user(
            self,
            event: AstrMessageEvent,
    ):
        """
        在会话中解限指定用户。
        格式：/pass <@用户|UID（QQ号）> [时间（默认无期限）] [理由（默认无理由）] [UMO]
        时间格式：数字+单位（d=天，h=小时，m=分钟，s=秒），如 1d 表示1天，12h 表示12个小时，不带单位默认秒，0表示无期限
        示例：/pass @张三 7d
        注意：单次仅能解限一个会话的一个用户
        """
        umo = event.unified_msg_origin
        try:
            tgt_users, _time, _reason = extract_args(event)
        except ValueError as err:
            logger.error(err)
            yield event.plain_result(str(err) + "\n" + strings.MSG_HELP_TIME_FORMAT)
            return
        if not tgt_users:
            yield event.plain_result(strings.MSG_NO_TARGETS)
            return
        self.update_user(umo, tgt_users, False, _time, _reason, False)

        yield event.plain_result(
            strings.messages["passed_user"].format(
                umo=umo, user=str(tgt_users), time=time_utils.time_remaining_format(_time), reason=_reason
            )
        )

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("pass-all")
    async def pass_all(
            self,
            event: AstrMessageEvent,
    ):
        """
        在全局中解限指定用户。
        格式：/pass-all <@用户|UID（QQ号）> [时间（默认无期限）] [理由（默认无理由）]
        时间格式：数字+单位（d=天，h=小时，m=分钟，s=秒），如 1d 表示1天，12h 表示12个小时，不带单位默认秒，0表示无期限
        示例：/pass-all @张三 7d
        注意：单次仅能解限一个用户
        """
        umo = event.unified_msg_origin
        try:
            tgt_users, _time, _reason = extract_args(event)
        except ValueError as err:
            logger.error(err)
            yield event.plain_result(str(err) + "\n" + strings.MSG_HELP_TIME_FORMAT)
            return
        if not tgt_users:
            yield event.plain_result(strings.MSG_NO_TARGETS)
            return
        self.update_user(umo, tgt_users, False, _time, _reason, True)

        yield event.plain_result(
            strings.messages["passed_user_global"].format(
                user=str(tgt_users), time=time_utils.time_remaining_format(_time), reason=_reason
            )
        )

    @filter.command("bancheck")
    async def ban_check(self, event: AstrMessageEvent):
        umo = event.unified_msg_origin
        tgt_users, _, _ = extract_args(event)
        if not tgt_users:
            tgt_users.append(event.get_sender_id())

        result_str = []
        now = time.time()
        for user in tgt_users:
            bp = self.manager.get(umo, user)
            if bp:
                if bp.is_baned():
                    result_str.append(
                        strings.messages["banned_user"].format(umo=umo, user=user, time=time_utils.time_remaining_format(
                            bp.ban_.get_expire_at() - now), reason=bp.ban_.get_reason())
                    )
                else:
                    result_str.append(
                        strings.messages["passed_user"].format(umo=umo, user=user, time=time_utils.time_remaining_format(
                            bp.pass_.get_expire_at() - now), reason=bp.pass_.get_reason())
                    )
        if result_str:
            yield event.plain_result("\n".join(result_str))
        else:
            yield event.plain_result(strings.MSG_NO_BAN_RECORD)

    # 设置优先级，可在其他未设置优先级（priority=0）的命令/监听器/钩子前过滤
    @filter.event_message_type(filter.EventMessageType.ALL, priority=10000)
    async def filter_banned_users(self, event: AstrMessageEvent):
        """
        全局事件过滤器：
        如果禁用功能启用且发送者被禁用，则停止事件传播，机器人不再响应该用户的消息。
        """
        if "bancheck" in event.message_str.strip():
            return
        if self.manager.is_baned(event.unified_msg_origin, event.get_sender_id()):
            logger.info(f"用户{event.get_sender_id()}已从{event.unified_msg_origin}被禁用")
            event.stop_event()

    async def terminate(self):
        """可选择实现 terminate 函数，当插件被卸载/停用时会调用。"""
