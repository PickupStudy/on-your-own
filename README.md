# PKB Core Framework

这是一个独立于现有项目的个人知识库框架代码目录，遵循单一职责：

- `node/`: 命令入口、任务编排、同步服务
- `python/`: 笔记采集、总结、上下文样本构建
- `scripts/`: 本地启动与调度脚本

## 快速结构

```text
pkb-core/
  node/
  python/
  scripts/
```

## 目标能力（首版骨架）

1. `doctor`：检查环境与配置
2. `ingest`：扫描 Obsidian 笔记
3. `summarize`：执行结构化总结（当前为占位实现）
4. `bundle`：构建 context bundle
5. `sync`：执行 Git 同步
6. `pipeline`：串联 ingest -> summarize -> bundle -> sync

## 注意

- `.env` 中的密钥请本地配置，不要提交到仓库。
- `OBSIDIAN_VAULT_PATH` 必须指向真实 Vault 目录（包含 `.obsidian` 或笔记 `.md` 文件）。
- `MYSQL_DATABASE` 必须是 **MySQL 服务端已存在的库名**；若报 `Unknown database`，先在服务器执行 `CREATE DATABASE pkb ...` 或把变量改成已有库名。
- 同步在 **`pkb-core` 根目录** 初始化 Git（若尚无仓库会自动 `git init`），`origin` 已存在时会 `set-url` 而不是重复 `add`。

## 运行步骤（最小闭环）

1. 复制 `.env.example` 为 `.env` 并填入真实值
2. 安装依赖
   - Node: 在 `node/` 目录执行 `npm install`
   - Python: 在 `python/` 目录执行 `pip install -e .`
3. 运行健康检查（CMD 下双击或执行）  
   - `D:\Develop-project\agentLearning\scripts\doctor.bat`
4. 运行完整流程（CMD 下双击或执行）  
   - `D:\Develop-project\agentLearning\scripts\run_pipeline.bat`

## 定时任务安装（纯 CMD）

- 一键安装：在 CMD 中执行  
  `D:\Develop-project\agentLearning\scripts\install_tasks.bat`
- 会创建：
  - `PKB_Pipeline_Every2Hours`
  - `PKB_Pipeline_Nightly`
