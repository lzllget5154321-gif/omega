# Omega

Omega 是一套面向 AI Agent 工作流的早期生态系统设计。本仓库保存了它在 Obsidian 中形成的设计蓝图、构建包、可执行脚本、配置、Schema、测试与直接相关的演化记录。

## 目录

- [`omega-vault/omega生态系统项目/`](omega-vault/omega生态系统项目/)：按原 Obsidian 项目目录保留的设计资料，包含总览、方法论、架构、能力矩阵、运行时原型、基准任务、外部 AI 注册表和创意可视化。
- [`omega-vault/omega生态系统项目/99-交付给Codex的构建包/`](omega-vault/omega生态系统项目/99-交付给Codex的构建包/)：交付给 Codex 的构建包，包含 PowerShell/Python/Shell 脚本、YAML 配置、JSON Schema、Docker/MCP 模板、测试夹具和验收测试。
- [`related-context/`](related-context/)：解释 Omega 前史、Ω-Loop 演化和项目暂停背景的直接相关笔记。
- [`provenance/`](provenance/)：来源路径、文件分类、大小和 SHA-256 校验记录。

## 设计入口

建议按以下顺序阅读：

1. [`omega-vault/omega生态系统项目/00-总览/omega生态系统项目-总说明.md`](omega-vault/omega生态系统项目/00-总览/omega生态系统项目-总说明.md)
2. [`omega-vault/omega生态系统项目/00-总览/Omega 构建指导书 — 给 Codex 的系统构造规范.md`](omega-vault/omega生态系统项目/00-总览/Omega%20构建指导书%20—%20给%20Codex%20的%20系统构造规范.md)
3. [`omega-vault/omega生态系统项目/01-方法论/Omega 最终完整方法论.md`](omega-vault/omega生态系统项目/01-方法论/Omega%20最终完整方法论.md)
4. [`omega-vault/omega生态系统项目/02-架构/Tool-Agent Router：最佳工具与最佳执行者选择器.md`](omega-vault/omega生态系统项目/02-架构/Tool-Agent%20Router：最佳工具与最佳执行者选择器.md)
5. [`omega-vault/omega生态系统项目/08-运行时与原型/Omega Runtime Architecture.md`](omega-vault/omega生态系统项目/08-运行时与原型/Omega%20Runtime%20Architecture.md)
6. [`omega-vault/omega生态系统项目/99-交付给Codex的构建包/README.md`](omega-vault/omega生态系统项目/99-交付给Codex的构建包/README.md) 与 [`MANIFEST.yaml`](omega-vault/omega生态系统项目/99-交付给Codex的构建包/MANIFEST.yaml)

## 当前实现边界

这份快照保存的是 Omega 的设计与冷启动构建材料。原项目中没有已经完成的 Omega 应用主程序或可安装 Python package；当前可执行部分主要是 `omega-vault/omega生态系统项目/99-交付给Codex的构建包/scripts/` 中的策略验证、端点策略、打包门禁、环境初始化和沙箱网络脚本，以及同目录 `tests/` 中的 Python/PowerShell 测试。构建清单里规划的 `omega` CLI、路由器、规划器、执行器和数据库服务仍属于待构建目标，不能把设计规范误读为已经交付的运行时。

## 来源与保真度

源目录为 `D:\obsidian\lzl的个人知识库\omega生态系统项目`。仓库保留原始文件名和目录语义；仅排除了 Python `__pycache__` 生成物，并在原本为空的三个目录中加入 `.gitkeep` 以便 Git 保留目录结构。原始 Windows 快捷方式 `01-方法论.lnk` 也保留在快照中，但 GitHub 网页端不会解析其本机路径。

所有复制文件的原始相对路径、分类、大小和 SHA-256 记录在 [`provenance/SOURCE_MANIFEST.json`](provenance/SOURCE_MANIFEST.json) 中。

## 历史状态

项目在 Obsidian 中被标记为早期/暂停方向；相关的 Ω-Loop、v12.0 和 v13.0 记录放在 `related-context/`，用于理解它为何产生、哪些理念后来被吸收，以及哪些部分没有进入可运行实现。仓库不把暂停项目包装成已完成产品。
