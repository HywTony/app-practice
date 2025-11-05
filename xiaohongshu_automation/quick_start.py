#!/usr/bin/env python3
"""
快速启动脚本
一键测试整个系统
"""

import os
import sys
from pathlib import Path


def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...\n")

    # 检查API密钥
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ 未设置 ANTHROPIC_API_KEY 环境变量")
        print("\n请设置你的Claude API密钥：")
        print("  Windows: set ANTHROPIC_API_KEY=your-key")
        print("  Linux/Mac: export ANTHROPIC_API_KEY=your-key\n")
        return False

    print("✅ API密钥已设置")

    # 检查必要文件
    required_files = [
        "config/config.yaml",
        "config/templates.json",
        "src/content_generator.py",
        "src/xhs_publisher.py",
        "src/scheduler.py"
    ]

    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少文件: {file}")
            return False

    print("✅ 所有必要文件存在\n")
    return True


def check_dependencies():
    """检查依赖包"""
    print("🔍 检查依赖包...\n")

    required_packages = [
        ('anthropic', 'anthropic'),
        ('yaml', 'pyyaml'),
        ('schedule', 'schedule'),
        ('PIL', 'pillow')
    ]

    missing = []
    for package, pip_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name} 未安装")
            missing.append(pip_name)

    if missing:
        print(f"\n请安装缺失的依赖：")
        print(f"  pip install {' '.join(missing)}\n")
        return False

    print()
    return True


def show_menu():
    """显示菜单"""
    print("\n" + "="*60)
    print("  巨爆铺 - 小红书自动化营销系统")
    print("="*60)
    print("\n请选择操作：\n")
    print("  1. 生成一篇测试内容")
    print("  2. 批量生成内容（5篇）")
    print("  3. 查看最新生成的内容")
    print("  4. 发布最新内容（保存为草稿）")
    print("  5. 测试定时任务")
    print("  6. 启动定时调度器")
    print("  7. 查看配置信息")
    print("  0. 退出")
    print("\n" + "="*60)


def generate_content(count=1):
    """生成内容"""
    os.chdir("src")
    os.system(f"python content_generator.py --test --count {count}")
    os.chdir("..")


def view_latest_content():
    """查看最新内容"""
    import json
    from datetime import datetime

    logs_dir = Path("logs")
    content_files = sorted(logs_dir.glob("content_*.json"), reverse=True)

    if not content_files:
        print("\n❌ 没有找到生成的内容")
        return

    latest_file = content_files[0]

    with open(latest_file, 'r', encoding='utf-8') as f:
        content = json.load(f)

    print("\n" + "="*60)
    print("📄 最新生成的内容")
    print("="*60)
    print(f"\n文件: {latest_file.name}")
    print(f"生成时间: {content.get('generated_at', 'unknown')}")
    print(f"内容类型: {content.get('content_type', 'unknown')}")
    print(f"\n标题: {content['title']}\n")
    print("正文:")
    print(content['content'])
    print(f"\n话题标签: {' '.join(content['tags'])}")
    print("\n" + "="*60)


def publish_latest():
    """发布最新内容"""
    os.chdir("src")
    os.system("python xhs_publisher.py --manual")
    os.chdir("..")


def test_scheduler():
    """测试定时任务"""
    os.chdir("src")
    os.system("python scheduler.py --test")
    os.chdir("..")


def start_scheduler():
    """启动定时调度器"""
    print("\n⚠️  即将启动定时调度器")
    print("按 Ctrl+C 可以随时停止\n")
    input("按 Enter 继续...")

    os.chdir("src")
    os.system("python scheduler.py --start")
    os.chdir("..")


def show_config():
    """显示配置信息"""
    import yaml

    with open("config/config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    print("\n" + "="*60)
    print("⚙️  当前配置")
    print("="*60)
    print(f"\n产品名称: {config['product']['name']}")
    print(f"产品网址: {config['product']['url']}")
    print(f"\n发布频率: 每天 {config['content_strategy']['post_frequency']} 次")
    print(f"发布时间: {', '.join(config['content_strategy']['post_times'])}")
    print(f"\nAI模型: {config['ai']['model']}")
    print(f"自动发布: {'开启' if config['publish']['auto_publish'] else '关闭'}")
    print(f"保存草稿: {'开启' if config['publish']['save_draft'] else '关闭'}")
    print("\n" + "="*60)


def main():
    """主函数"""
    # 检查环境
    if not check_environment():
        sys.exit(1)

    if not check_dependencies():
        sys.exit(1)

    print("✅ 环境检查通过！\n")
    input("按 Enter 继续...")

    while True:
        show_menu()

        choice = input("\n请输入选项 (0-7): ").strip()

        if choice == "1":
            generate_content(1)
        elif choice == "2":
            generate_content(5)
        elif choice == "3":
            view_latest_content()
        elif choice == "4":
            publish_latest()
        elif choice == "5":
            test_scheduler()
        elif choice == "6":
            start_scheduler()
        elif choice == "7":
            show_config()
        elif choice == "0":
            print("\n👋 再见！")
            break
        else:
            print("\n❌ 无效选项，请重新选择")

        input("\n按 Enter 继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1)
