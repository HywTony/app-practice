#!/usr/bin/env python3
"""
小红书发布器
将生成的内容发布到小红书
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path


class XiaohongshuPublisher:
    def __init__(self, config_path="config/config.yaml"):
        """初始化发布器"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.log_path = self.config['publish']['log_path']

    def create_placeholder_images(self, count=3):
        """创建占位图片（实际使用时需要替换为真实图片）"""
        images = []
        image_dir = Path(self.config['image']['save_path'])
        image_dir.mkdir(parents=True, exist_ok=True)

        # 这里返回占位图片路径
        # 实际使用时需要：
        # 1. 使用设计工具生成图片
        # 2. 使用AI生成图片
        # 3. 使用预先准备的图片

        for i in range(count):
            # 占位符：实际使用时需要生成真实图片
            placeholder_path = image_dir / f"placeholder_{i+1}.png"
            images.append(str(placeholder_path))

        return images

    def validate_content(self, content):
        """验证内容格式"""
        required_fields = ['title', 'content', 'tags']

        for field in required_fields:
            if field not in content:
                raise ValueError(f"缺少必需字段: {field}")

        # 验证标题长度（小红书限制20个字）
        if len(content['title']) > 20:
            print(f"⚠️  警告: 标题过长 ({len(content['title'])}字)，小红书限制为20字")

        # 验证标签数量
        if len(content['tags']) > 10:
            print(f"⚠️  警告: 标签过多 ({len(content['tags'])}个)，建议6-8个")

        return True

    def format_content_for_publish(self, content):
        """格式化内容用于发布"""
        # 组合正文和标签
        full_content = content['content']

        # 添加标签
        if content['tags']:
            tags_line = ' '.join([f"#{tag.strip('#')}" for tag in content['tags']])
            full_content = f"{full_content}\n\n{tags_line}"

        return {
            "title": content['title'],
            "content": full_content,
            "images": self.create_placeholder_images(self.config['image']['count'])
        }

    def publish_to_xiaohongshu(self, content, images):
        """
        发布到小红书（使用MCP）

        注意：这需要在Claude Code环境中运行，
        因为需要使用xiaohongshu-mcp工具
        """
        print("\n" + "="*50)
        print("📤 准备发布到小红书...")
        print("="*50)

        print(f"\n标题: {content['title']}")
        print(f"\n正文:\n{content['content']}")
        print(f"\n图片数量: {len(images)}")

        # 在Claude Code环境中，可以使用MCP工具发布
        # 示例调用方式（需要在Claude Code中执行）：
        """
        from mcp_client import xiaohongshu_mcp

        result = xiaohongshu_mcp.publish_content(
            title=content['title'],
            content=content['content'],
            images=images,
            tags=content['tags']
        )
        """

        # 当前环境：保存为草稿
        if self.config['publish']['save_draft']:
            self.save_draft(content, images)

        return {
            "status": "draft_saved" if self.config['publish']['save_draft'] else "pending",
            "message": "内容已保存为草稿，请使用Claude Code发布到小红书"
        }

    def save_draft(self, content, images):
        """保存为草稿"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        draft_file = f"logs/draft_{timestamp}.json"

        draft = {
            "title": content['title'],
            "content": content['content'],
            "images": images,
            "saved_at": datetime.now().isoformat(),
            "status": "draft"
        }

        with open(draft_file, 'w', encoding='utf-8') as f:
            json.dump(draft, f, ensure_ascii=False, indent=2)

        print(f"\n💾 草稿已保存: {draft_file}")

    def log_publish(self, content, result):
        """记录发布日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "title": content['title'],
            "content_type": content.get('content_type', 'unknown'),
            "result": result
        }

        # 加载现有日志
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []

        # 添加新日志
        logs.append(log_entry)

        # 保存日志
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def publish(self, content_file_or_dict):
        """发布内容"""
        try:
            # 加载内容
            if isinstance(content_file_or_dict, str):
                with open(content_file_or_dict, 'r', encoding='utf-8') as f:
                    content = json.load(f)
            else:
                content = content_file_or_dict

            # 验证内容
            self.validate_content(content)

            # 格式化内容
            formatted = self.format_content_for_publish(content)

            # 发布（或保存草稿）
            result = self.publish_to_xiaohongshu(
                formatted,
                formatted['images']
            )

            # 记录日志
            self.log_publish(content, result)

            print(f"\n✅ 处理完成: {result['message']}")

            return result

        except Exception as e:
            print(f"\n❌ 发布失败: {str(e)}")
            return {"status": "error", "message": str(e)}


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='小红书发布器')
    parser.add_argument('--file', type=str, help='内容文件路径')
    parser.add_argument('--manual', action='store_true', help='手动模式（使用最新生成的内容）')
    args = parser.parse_args()

    publisher = XiaohongshuPublisher()

    if args.file:
        # 发布指定文件
        result = publisher.publish(args.file)
    elif args.manual:
        # 使用最新生成的内容
        logs_dir = Path("logs")
        content_files = sorted(logs_dir.glob("content_*.json"), reverse=True)

        if content_files:
            latest_file = content_files[0]
            print(f"📄 使用最新内容: {latest_file}")
            result = publisher.publish(str(latest_file))
        else:
            print("❌ 未找到生成的内容文件，请先运行 content_generator.py")
    else:
        print("请指定 --file 或 --manual 参数")


if __name__ == "__main__":
    main()
