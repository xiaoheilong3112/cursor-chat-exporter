import os
import argparse
from cursor_chat_exporter.cursor_chat_util import CursorChatUtil

def main():
    parser = argparse.ArgumentParser(description='导出Cursor/Windsurf聊天记录')
    parser.add_argument('--app', choices=['cursor', 'windsurf'], default='cursor',
                      help='选择要导出的应用类型 (cursor 或 windsurf)')
    parser.add_argument('--output', '-o', default='chat_exports',
                      help='导出文件的输出目录')
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output, exist_ok=True)
    
    # 初始化工具类并导出聊天记录
    chat_util = CursorChatUtil()
    chat_util.export_all_chats(app_type=args.app)
    chat_util.export_to_markdown(args.output)

if __name__ == "__main__":
    main()
