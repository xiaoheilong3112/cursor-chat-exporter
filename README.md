# Cursor Chat Exporter

一个用于导出 Cursor 和 Windsurf IDE 聊天记录的工具。

## 功能特点

- 支持导出 Cursor 和 Windsurf 的 AI 聊天记录
- 自动扫描工作区存储目录
- 将聊天记录导出为 Markdown 格式
- 支持 Windows 和 Linux 系统
- 提供详细的错误处理和状态反馈

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/cursor-chat-exporter.git
cd cursor-chat-exporter
```

2. 使用 Poetry 安装依赖：
```bash
poetry install
```

或者使用 pip 安装：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

1. 导出 Cursor 的聊天记录：
```bash
python -m cursor_chat_exporter.export_chats --app cursor --output cursor_chats
```

2. 导出 Windsurf 的聊天记录：
```bash
python -m cursor_chat_exporter.export_chats --app windsurf --output windsurf_chats
```

### 命令行参数

- `--app`: 选择要导出的应用类型
  - `cursor`: 导出 Cursor IDE 的聊天记录
  - `windsurf`: 导出 Windsurf IDE 的聊天记录
- `--output` 或 `-o`: 指定输出目录（默认为 'chat_exports'）

### 输出格式

聊天记录将以 Markdown 格式导出，每个聊天会话生成一个单独的文件。文件名格式为：`{聊天标题}_{会话ID}.md`

每个 Markdown 文件包含：
- 聊天标题
- 所有消息内容
- 消息类型标记
- 分隔线

## 数据存储位置

### Windows
- Cursor: `%APPDATA%\Cursor\User\workspaceStorage`
- Windsurf: `%APPDATA%\Windsurf\User\workspaceStorage`

### Linux
- Cursor: `~/.config/Cursor/User/workspaceStorage`
- Windsurf: `~/.config/Windsurf/User/workspaceStorage`

## 故障排除

1. 如果没有找到聊天记录：
   - 确认 IDE 是否已经创建过聊天记录
   - 检查数据存储路径是否正确
   - 确认是否有权限访问存储目录

2. 如果导出过程中出错：
   - 检查输出目录的写入权限
   - 确保有足够的磁盘空间
   - 查看错误信息以获取详细信息

## 开发说明

项目使用 Poetry 进行依赖管理。主要文件：

- `cursor_chat_util.py`: 核心工具类，处理数据提取和导出
- `export_chats.py`: 命令行入口脚本

### 开发环境设置

1. 安装 Poetry：
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. 安装依赖：
```bash
poetry install
```

3. 激活虚拟环境：
```bash
poetry shell
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持 Cursor 和 Windsurf 聊天记录导出
- Markdown 格式输出
- 命令行界面
