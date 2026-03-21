<div align="center">

# BanPass

_🚫 为 [astrbot](https://github.com/AstrBotDevs/AstrBot) 设计的简易黑名单插件 🚫_

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
<br>
[![AstrBot](https://img.shields.io/badge/AstrBot-yellow.svg)](https://github.com/AstrBotDevs/AstrBot)
</div>

## 介绍

BanPass 是一个为 [astrbot](https://github.com/AstrBotDevs/AstrBot) 设计的简易黑名单插件，允许bot管理员在**会话**或**全局
**范围较为灵活地禁用指定用户。
ReNeBan 允许为**禁用/解禁**设置**时限**和**理由**，并自动整理记录。

该插件重构于[NekoiMeiov/astrbot_plugin_reneban](https://github.com/NekoiMeiov/astrbot_plugin_reneban)

---

## 命令

| 命令          | 语法                                               | 说明                       | 示例                                      |
|-------------|--------------------------------------------------|--------------------------|-----------------------------------------|
| `/ban`      | /ban <@用户> [<@用户2>] [时间（默认无期限）] [理由（默认无理由）]      | 在**当前会话**范围内禁用**指定用户**   | /ban @AAA高价收游戏账号 inf 打广告                |
| `/pass`     | /pass <@用户> [<@用户2>] [时间（默认无期限）] [理由（默认无理由）]     | 在**当前会话**范围内解除禁用**指定用户** | /pass @yfseh218 0 None                  |
| `/ban-all`  | /ban-all <@用户> [<@用户2>] [时间（默认无期限）] [理由（默认无理由）]  | 在**全局**范围内禁用**指定用户**     | /ban-all @2110453981 1d30m 试图让bot输出敏感内容 |
| `/pass-all` | /pass-all <@用户> [<@用户2>] [时间（默认无期限）] [理由（默认无理由）] | 在**全局**范围内解除禁用**指定用户**   | /pass-all @我想不出来啥名了 0 误封                |
| `/banhelp`  | /banhelp                                         | 输出简易帮助信息                 | /banhelp                                |
| `/bancheck` | /bancheck <@用户> [<@用户2>]                         | 查询**指定用户**的封禁状态          | /banhelp@NekoiMeiov                     |

时间字段支持如下格式：

```text
- `1d` → 1 天
- `2h` → 2 小时
- `30m` → 30 分钟
- `10s`，`10` → 10 秒
- `0`/`inf` → 永久（默认，且不支持与以上单位复用）
```

输入时需按单位大小填写！不允许如`20m1h`的时间表达式！

## 安装

- 从插件市场安装

在 插件管理 - 插件市场 搜索 ReNeBan

- 从链接安装

在 插件管理 - 安装 - 从链接安装 输入以下链接

``` text
https://github.com/oculr/astrbot_plugin_banpass
```

- 从源码安装

在终端中输入以下命令（若为手动安装，请将 /AstrBot 修改为手动安装的路径）

```bash
# 克隆仓库到插件目录
cd /AstrBot/data/plugins
git clone https://github.com/oculr/astrbot_plugin_banpass.git

# 控制台重启AstrBot
```

## 贡献指南

- 提交 Issue 报告问题/提出建议
- 提交 Pull Request 改进