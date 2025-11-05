#!/usr/bin/env python3
"""
定时任务调度器
自动生成和发布小红书内容
"""

import schedule
import time
import yaml
from datetime import datetime
from content_generator import ContentGenerator
from xhs_publisher import XiaohongshuPublisher


class ContentScheduler:
    def __init__(self, config_path="config/config.yaml"):
        """初始化调度器"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.generator = ContentGenerator()
        self.publisher = XiaohongshuPublisher()

        # 发布时间配置
        self.post_times = self.config['content_strategy']['post_times']
        self.auto_publish = self.config['publish']['auto_publish']

    def job_generate_and_publish(self):
        """生成并发布内容的任务"""
        print("\n" + "="*60)
        print(f"⏰ 定时任务触发: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        try:
            # 生成内容
            content = self.generator.generate_content()

            if content:
                # 保存内容
                filepath = self.generator.save_content(content)

                if self.auto_publish:
                    # 自动发布
                    print("\n🚀 开始自动发布...")
                    result = self.publisher.publish(content)

                    if result['status'] == 'success':
                        print("✅ 自动发布成功！")
                    else:
                        print(f"⚠️  发布状态: {result['status']}")
                else:
                    # 仅保存草稿
                    print("\n💾 内容已生成并保存为草稿")
                    print("📌 请手动审核后发布")

                print("\n" + "="*60)

        except Exception as e:
            print(f"❌ 任务执行失败: {str(e)}")

    def setup_schedule(self):
        """设置定时任务"""
        print("\n⏱️  设置定时任务...")

        for post_time in self.post_times:
            schedule.every().day.at(post_time).do(self.job_generate_and_publish)
            print(f"   ✓ 每天 {post_time} 自动生成内容")

        print(f"\n📋 任务配置:")
        print(f"   • 发布频率: 每天 {len(self.post_times)} 次")
        print(f"   • 发布时间: {', '.join(self.post_times)}")
        print(f"   • 自动发布: {'开启' if self.auto_publish else '关闭（仅生成草稿）'}")

    def run(self):
        """运行调度器"""
        self.setup_schedule()

        print("\n" + "="*60)
        print("🎯 调度器已启动，等待任务执行...")
        print("="*60)
        print("\n💡 提示:")
        print("   • 按 Ctrl+C 停止调度器")
        print("   • 查看 logs/ 目录获取生成的内容")
        print("   • 查看 logs/publish_log.json 获取发布记录")
        print("\n")

        # 显示下次执行时间
        next_run = schedule.next_run()
        if next_run:
            print(f"⏰ 下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次

        except KeyboardInterrupt:
            print("\n\n👋 调度器已停止")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='小红书自动化调度器')
    parser.add_argument('--start', action='store_true', help='启动调度器')
    parser.add_argument('--test', action='store_true', help='立即执行一次测试')
    args = parser.parse_args()

    scheduler = ContentScheduler()

    if args.test:
        print("🧪 测试模式: 立即执行一次任务\n")
        scheduler.job_generate_and_publish()

    elif args.start:
        scheduler.run()

    else:
        print("使用方法:")
        print("  python scheduler.py --start    # 启动调度器")
        print("  python scheduler.py --test     # 测试执行一次")


if __name__ == "__main__":
    main()
