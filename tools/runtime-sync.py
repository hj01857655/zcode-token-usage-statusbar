#!/usr/bin/env python3
"""把仓库当前代码同步到本地 runtime 目录（~/.zcode/zcode-token-usage-statusbar）。

fork 维护专用：upstream/main 合并后跑一次本脚本，再重启 ZCode 生效。
只覆盖 RUNTIME_FILES 白名单内的文件，config.json 与其它本地状态一律不动。
用法：python tools/runtime-sync.py [--runtime <dir>] [--dry-run]
"""
import argparse, os, shutil, sys

RUNTIME_FILES = [
    "inject-main.cjs", "plugin-updater.cjs", "plugin-release.cjs", "plugin-storage.cjs",
    "quota-client.cjs", "model-puller.cjs", "engine-patch.cjs", "release_unpack.py",
    "runtime_lock.py", "usage_stats.py", "turn-stats.js", "overlay.js", "zusage.py",
    "usage_mcp.py", "token_rate.py", "renderer_bridge.py",
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runtime", default=os.path.join(os.path.expanduser("~"), ".zcode", "zcode-token-usage-statusbar"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(a.runtime):
        print("runtime 目录不存在：", a.runtime); return 1
    n = 0
    for f in RUNTIME_FILES:
        src = os.path.join(here, f)
        dst = os.path.join(a.runtime, f)
        if not os.path.isfile(src):
            print("  跳过（仓库无此文件）：", f); continue
        same = os.path.isfile(dst) and open(src, "rb").read() == open(dst, "rb").read()
        if same:
            print("  一致：", f); continue
        print(("  [dry-run] 将复制：" if a.dry_run else "  已复制："), f)
        if not a.dry_run:
            shutil.copy2(src, dst); n += 1
    print(("  [dry-run] " if a.dry_run else "") + f"完成，更新 {n} 个文件。主进程改动需重启 ZCode 生效。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
