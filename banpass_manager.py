import time
from dataclasses import dataclass
from pathlib import Path
from diskcache import Index

GLOBAL = "GLOBAL"



"""
优先级 pass > ban > pass-all > ban-all
{
    "user_id":
    {
    "umo_str/UMO_ALL":
        {
        "ban_":
            {
                "expire_at": 1774018450
                "reason": "理由文本"
            }
        "pass_":
            {
                "expire_at": 1774018450
                "reason": "理由文本"
            }
        }
    }
}
"""


@dataclass
class ExpireReason:
    EXPIRE_AT = "expire_at"

    REASON = "reason"

    _data: dict

    def __init__(self, data: dict = None):
        self._data = {} if data is None else data

    def get_expire_at(self) -> float:
        return self._data.get(ExpireReason.EXPIRE_AT, 0)

    def get_reason(self) -> str:
        return self._data.get(ExpireReason.REASON, )

    def update(self, expire_at: float, reason: str):
        self._data[ExpireReason.EXPIRE_AT] = expire_at
        self._data[ExpireReason.REASON] = reason


@dataclass
class BanPass:
    ban_: ExpireReason = None
    pass_: ExpireReason = None

    def is_baned(self) -> bool:
        current_time = time.time()
        if self.pass_.get_expire_at() > current_time:
            return False
        if self.ban_.get_expire_at() > current_time:
            return True
        return False

    def is_pass(self) -> bool:
        return not self.is_baned()

    def update(self, ban_: ExpireReason, pass_: ExpireReason):
        if ban_ is not None:
            self.ban_ = ban_
        if pass_ is not None:
            self.pass_ = pass_

        return self


def _update(umo: str, user_record: dict, to_update: BanPass):
    bp = user_record.get(umo, user_record.get(GLOBAL))
    bp = BanPass(ExpireReason(), ExpireReason()) if bp is None else BanPass(bp.ban_, bp.pass_)
    bp.update(to_update.ban_, to_update.pass_)
    user_record[umo] = bp
    return user_record


def build_expire_reason(_time: float, _reason: str = None, ) -> ExpireReason:
    expire_at = time.time() + _time
    return ExpireReason({
        ExpireReason.EXPIRE_AT: expire_at,
        ExpireReason.REASON: _reason
    })


class BanPassManager:

    def __init__(self, data_path: Path):
        self.ban_pass_db = Index(str(data_path))

    def is_baned(self, umo: str, user_id: str) -> bool:
        user_record = self.ban_pass_db.get(user_id)
        if user_record is None:
            return False
        bp = user_record.get(umo, user_record.get(GLOBAL))
        if bp is None:
            return False
        return bp.is_baned()

    def get(self, umo: str, user_id: str) -> BanPass:
        user_record = self.ban_pass_db.get(user_id, {})
        bp = user_record.get(umo, user_record.get(GLOBAL))
        return bp

    def update(self, umo: str, user_id: str, to_update: BanPass, is_global=False):
        user_record = self.ban_pass_db.get(user_id, {})
        _update(umo, user_record, to_update)
        if is_global:
            _update(GLOBAL, user_record, to_update)
            for _umo in user_record.keys():
                _update(_umo, user_record, to_update)

        self.ban_pass_db[user_id] = user_record
