# 08-运行时与原型

> 本目录存放 Omega 系统的**实际可运行代码、脚本、原型和配置**——不是方法论描述，而是能真正执行的工程产物。

## 子目录规划

```
08-运行时与原型/
├── README.md                   ← 你在这里
├── scripts/                    ← 自动化脚本
│   ├── task-contract-generator ← 任务契约生成器原型
│   ├── tool-router             ← 工具/Agent 选择器原型
│   └── radar-scanner           ← AI 工具生态雷达扫描脚本
├── mcp-configs/                ← MCP Server 配置草案
├── docker/                     ← Docker 沙箱配置
├── playwright-scripts/         ← 浏览器自动化示例
└── prototypes/                 ← 实验性原型
```

## 用途

- Claude Code 后续真正使用的脚本和 CLI 工具
- 任务契约生成器、工具路由器原型
- MCP 配置草案
- Playwright / Computer Use 自动化示例
- Docker 沙箱和安全配置文件

## 与其他目录的关系

- 方法论在 `01-方法论/`（定义"要做什么"）
- 实现在 `08-运行时与原型/`（定义"怎么做"）
- 测试在 `09-功能基准任务花园/`（验证"做对了吗"）
