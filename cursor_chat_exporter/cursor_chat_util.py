import os
import sqlite3
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from dateutil import parser

class CursorChatUtil:
    def __init__(self):
        self.chat_data = []
        self.app_data_paths = {
            'cursor': [
                os.path.expanduser('~/AppData/Roaming/Cursor/User/workspaceStorage'),
                os.path.expanduser('~/.config/Cursor/User/workspaceStorage'),
            ],
            'windsurf': [
                os.path.expanduser('~/AppData/Roaming/Windsurf/User/workspaceStorage'),
                os.path.expanduser('~/.config/Windsurf/User/workspaceStorage'),
            ]
        }

    def scan_workspace_storage(self, app_type='cursor'):
        """扫描工作区存储目录"""
        paths = self.app_data_paths.get(app_type, [])
        found_any = False
        
        for base_path in paths:
            if os.path.exists(base_path):
                found_any = True
                print(f"扫描目录: {base_path}")
                for workspace_dir in os.listdir(base_path):
                    workspace_path = os.path.join(base_path, workspace_dir)
                    if os.path.isdir(workspace_path):
                        # 搜索state.vscdb文件
                        state_db = os.path.join(workspace_path, 'state.vscdb')
                        if os.path.exists(state_db):
                            print(f"发现数据库: {state_db}")
                            self.extract_chat_from_db(state_db)
        
        if not found_any:
            print(f"未找到{app_type}的工作区存储目录")

    def extract_chat_from_db(self, db_path):
        """从数据库中提取聊天数据"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT key, value FROM ItemTable WHERE key = 'workbench.panel.aichat.view.aichat.chatdata'")
            row = cursor.fetchone()
            
            if row:
                key, value = row
                try:
                    if isinstance(value, bytes):
                        value_str = value.decode('utf-8')
                    elif isinstance(value, str):
                        value_str = value
                    else:
                        return
                    
                    data = json.loads(value_str)
                    
                    if 'tabs' in data:
                        for tab in data['tabs']:
                            if 'bubbles' in tab:
                                messages = []
                                for bubble in tab['bubbles']:
                                    # 尝试从不同位置提取消息内容
                                    content = None
                                    
                                    # 检查bubble的data字段
                                    if 'data' in bubble and isinstance(bubble['data'], dict):
                                        data = bubble['data']
                                        if 'parts' in data and isinstance(data['parts'], list):
                                            # 合并所有文本部分
                                            content = '\n'.join(str(part) for part in data['parts'] if part)
                                        elif 'text' in data:
                                            content = data['text']
                                    # 如果data中没有找到，检查bubble本身
                                    elif 'parts' in bubble and isinstance(bubble['parts'], list):
                                        content = '\n'.join(str(part) for part in bubble['parts'] if part)
                                    elif 'text' in bubble:
                                        content = bubble['text']
                                    elif 'message' in bubble:
                                        content = bubble['message']
                                    
                                    # 保存消息
                                    if content:
                                        messages.append({
                                            'timestamp': bubble.get('timestamp', 'Unknown time'),
                                            'type': bubble.get('type', 'Unknown type'),
                                            'message': content
                                        })
                                
                                if messages:  # 只保存有内容的聊天
                                    self.chat_data.append({
                                        'title': tab.get('chatTitle', 'Untitled'),
                                        'id': tab.get('tabId', 'Unknown'),
                                        'messages': messages
                                    })
                    
                except json.JSONDecodeError:
                    pass
                except Exception:
                    pass
            
            cursor.close()
            conn.close()
            
        except sqlite3.Error:
            pass
        except Exception:
            pass
    
    def process_chat_data(self, chat_data, workspace_id):
        """处理聊天数据并格式化"""
        messages = chat_data.get('messages', [])
        for msg in messages:
            try:
                timestamp = parser.parse(msg.get('timestamp', ''))
                formatted_msg = {
                    'workspace_id': workspace_id,
                    'timestamp': timestamp,
                    'role': msg.get('role', ''),
                    'content': msg.get('content', ''),
                    'id': msg.get('id', '')
                }
                self.chat_data.append(formatted_msg)
            except Exception as e:
                print(f"处理消息时出错: {str(e)}")
    
    def export_to_markdown(self, output_dir):
        """将聊天数据导出为Markdown文件"""
        if not self.chat_data:
            print("没有找到任何聊天数据")
            return
            
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            for chat in self.chat_data:
                try:
                    # 创建安全的文件名
                    title = chat.get('title', 'Untitled')
                    chat_id = chat.get('id', 'unknown')[:8]
                    
                    # 移除不安全的字符
                    safe_title = "".join(x for x in title if x.isalnum() or x in (' ', '-', '_')).strip()
                    if not safe_title:  # 如果标题为空，使用默认值
                        safe_title = "untitled_chat"
                        
                    filename = f"{safe_title}_{chat_id}.md"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        # 写入标题
                        f.write(f"# {title}\n\n")
                        
                        # 写入消息
                        for msg in chat.get('messages', []):
                            if msg.get('message'):  # 只写入有内容的消息
                                msg_type = msg.get('type', 'Unknown')
                                content = msg.get('message', '').strip()
                                if content:
                                    f.write(f"## {msg_type}\n\n")
                                    f.write(f"{content}\n\n")
                                    f.write("---\n\n")
                                    
                    print(f"已导出: {filename}")
                    
                except Exception as e:
                    print(f"导出单个聊天记录时出错: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"导出过程中出错: {str(e)}")
    
    def export_all_chats(self, app_type='cursor'):
        """导出所有工作区的聊天数据"""
        print("开始导出Cursor聊天数据...")
        self.scan_workspace_storage(app_type)
    
    def check_cursor_paths(self):
        """检查所有可能的Cursor数据存储位置"""
        paths = [
            self.app_data_paths['cursor'][0],
            self.app_data_paths['cursor'][1],
            self.app_data_paths['windsurf'][0],
            self.app_data_paths['windsurf'][1],
        ]
        
        for path in paths:
            if os.path.exists(path):
                print(f"\n发现Cursor数据路径: {path}")
                if os.path.isfile(path):
                    if path.endswith('.json'):
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                print(f"JSON文件内容预览: {str(data)[:200]}...")
                        except Exception as e:
                            print(f"读取JSON文件时出错: {str(e)}")
                else:
                    try:
                        files = os.listdir(path)
                        print(f"目录内容: {', '.join(files[:10])}...")
                    except Exception as e:
                        print(f"读取目录时出错: {str(e)}")
            else:
                print(f"\n路径不存在: {path}")
