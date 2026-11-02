# Fork 维护说明（hj01857655/zcode-token-usage-statusbar）

本 fork = 上游 `ByteRax/zcode-token-usage-statusbar` main + 本机定制。单向依赖：
上游是兼容性知识的权威源（渲染桥指纹表、引擎白名单、收尾链），本 fork 只做增量。

## 与上游的差异（全部在此清单内，合并冲突时以此为准）

1. **magpie 本地中转额度适配**（`quota-client.cjs`）：
   - `relayQuotaUrls` 增加 `/v1/magpie/quotas` 端点
   - `normalizeMagpie()`：按上游 provider 分组聚合（data[] 混多上游账号），
     取 Σlimit 最大组；周期窗按 amount/limit 加权，模型池并入 plan 槽；
     产出 `plan.productName/validEnd` + `windows{fiveHour,weekly,daily,monthly,plan}`
   - custom 适配器探测顺序：sub2api → magpie → legacy
2. **自更新器关闭**（本机 `config.json` 的 `plugin_auto_update: false`）：
   官方 release 会用官方包覆盖 runtime，冲掉上述适配器。更新一律走本文件流程。

## 升级流程（上游有新提交时）

```bash
git fetch upstream
git merge upstream/main          # 冲突点大概率在 quota-client.cjs 的上述三处
python tools/runtime-sync.py     # 同步 runtime（不动 config.json）
# 重启 ZCode 生效；额度 chip 应显示订阅名 + 三窗口
```

合并冲突时重移植三处拼接（锚点：relayQuotaUrls 返回行 / `/* --- OpenCode Go` 前 /
custom fetchOne 的 `normalizeSub2api` 之后），参考 `feat/magpie-quotas` 分支的历史提交。

## 回滚

- 整目录：`~/.zcode/zcode-token-usage-statusbar.bak-before-fork-upgrade/`
- 官方自更新：config.json 的 `plugin_auto_update` 改回 `true`
