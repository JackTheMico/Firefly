#!/usr/bin/env sh
set -e

# Firefly push: 先完整构建（失败即中止，不提交不推送）
pnpm build

# build 只可能改到这一个被跟踪的生成文件；有变化才提交。
# 用 pathspec 提交（git commit -- <path>），只提交该文件的工作区内容，
# 用户暂存区/工作区里的其他改动（如 WIP）原样保留，绝不用 git add -A。
if ! git diff --quiet HEAD -- src/constants/lqips.json; then
	git commit -m "chore: 重新生成 lqips.json" --no-verify -- src/constants/lqips.json
fi

# 内部真实推送：跳过 pre-push 的 build（本脚本已跑过），其余参数原样透传
FIREFLY_SKIP_PRE_PUSH_BUILD=1 git push "$@"
