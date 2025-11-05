#!/usr/bin/env python3
"""
小红书内容生成器
使用Claude AI生成小红书笔记内容
"""

import os
import json
import random
import yaml
from anthropic import Anthropic
from datetime import datetime


class ContentGenerator:
    def __init__(self, config_path="config/config.yaml", templates_path="config/templates.json"):
        """初始化内容生成器"""
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # 加载模板
        with open(templates_path, 'r', encoding='utf-8') as f:
            self.templates = json.load(f)

        # 初始化Claude客户端
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("请设置环境变量 ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key)

        # 产品信息
        self.product = self.config['product']

    def select_content_type(self):
        """根据权重随机选择内容类型"""
        content_types = self.config['content_strategy']['content_types']
        weights = [ct['weight'] for ct in content_types]
        selected = random.choices(content_types, weights=weights)[0]
        return selected

    def select_template(self, content_type):
        """选择模板"""
        template_ids = content_type['templates']
        template_id = random.choice(template_ids)
        return self.templates['templates'][template_id]

    def generate_hashtags(self, count=6):
        """生成话题标签"""
        primary = self.config['hashtags']['primary']
        secondary = self.config['hashtags']['secondary']
        optional = self.config['hashtags']['optional']

        # 选择标签
        selected = []
        # 1个主要标签
        selected.append(random.choice(primary))
        # 2-3个次要标签
        selected.extend(random.sample(secondary, min(3, len(secondary))))
        # 1-2个可选标签
        selected.extend(random.sample(optional, min(2, len(optional))))

        # 去重并限制数量
        selected = list(set(selected))[:count]

        # 格式化
        return [f"#{tag}" for tag in selected]

    def build_prompt(self, template, content_type):
        """构建AI提示词"""
        # 替换模板变量
        title_pattern = template['title_pattern']
        for var_name, var_values in self.templates['variables'].items():
            placeholder = f"{{{var_name}}}"
            if placeholder in title_pattern:
                title_pattern = title_pattern.replace(placeholder, random.choice(var_values))

        prompt = f"""你是一个专业的小红书营销文案专家，擅长创作高互动量的内容。

【产品信息】
名称：{self.product['name']}
网址：{self.product['url']}
简介：{self.product['description']}
功能：{', '.join(self.product['features'])}
目标用户：{', '.join(self.product['target_users'])}
核心痛点：{', '.join(self.product['pain_points'])}

【内容类型】{content_type['name']}

【模板信息】
标题参考：{title_pattern}
内容结构：{', '.join(template['content_structure'])}
写作风格：{template['style']}
表情符号密度：{template['emoji_density']}

【要求】
1. 标题：12-20字，吸引眼球，可以使用数字或疑问句
2. 正文：200-350字，分段清晰，多用emoji（根据密度要求）
3. 风格：口语化、接地气、有共鸣感、真诚
4. 避免：绝对化用语（最好、第一）、夸大宣传、虚假承诺
5. 重点：突出产品价值，解决用户痛点，提供实用信息

【参考优秀案例风格】
"做了半年Temu，终于找到宝藏工具了！🎉

之前每天光是上架产品就要花3个小时😭
- 手动复制粘贴商品信息
- 一个个核对价格
- 库存变动要手动更新

直到我发现了这个神器！⚡️

现在效率提升10倍，每天多出2小时去优化策略💪"

请生成一篇完整的小红书笔记内容，包括：
1. 标题（不要加"标题："前缀）
2. 正文内容
3. 不需要包含话题标签（我会单独添加）

注意：
- 不要使用markdown格式
- 直接输出纯文本
- 标题和正文之间用空行分隔
- 保持真实感，像真人在分享经验
"""
        return prompt

    def generate_content(self, test_mode=False):
        """生成内容"""
        try:
            # 选择内容类型和模板
            content_type = self.select_content_type()
            template = self.select_template(content_type)

            print(f"📝 正在生成内容...")
            print(f"内容类型: {content_type['name']}")
            print(f"模板: {template['name']}")

            # 构建提示词
            prompt = self.build_prompt(template, content_type)

            # 调用Claude API
            ai_config = self.config['ai']
            message = self.client.messages.create(
                model=ai_config['model'],
                max_tokens=ai_config['max_tokens'],
                temperature=ai_config['temperature'],
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # 解析响应
            content = message.content[0].text.strip()

            # 分离标题和正文
            lines = content.split('\n', 1)
            if len(lines) == 2:
                title = lines[0].strip()
                body = lines[1].strip()
            else:
                # 如果没有正确分离，尝试其他方式
                paragraphs = content.split('\n\n')
                title = paragraphs[0].strip()
                body = '\n\n'.join(paragraphs[1:]).strip()

            # 生成话题标签
            hashtags = self.generate_hashtags()

            # 组装完整内容
            result = {
                "title": title,
                "content": body,
                "tags": hashtags,
                "content_type": content_type['name'],
                "template": template['name'],
                "generated_at": datetime.now().isoformat(),
                "test_mode": test_mode
            }

            print(f"\n✅ 内容生成成功！\n")
            print(f"标题: {title}")
            print(f"\n正文预览:\n{body[:100]}...\n")
            print(f"话题标签: {' '.join(hashtags)}")

            return result

        except Exception as e:
            print(f"❌ 生成失败: {str(e)}")
            return None

    def save_content(self, content, filename=None):
        """保存生成的内容"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_{timestamp}.json"

        filepath = os.path.join("logs", filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

        print(f"💾 内容已保存到: {filepath}")
        return filepath


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='小红书内容生成器')
    parser.add_argument('--test', action='store_true', help='测试模式')
    parser.add_argument('--count', type=int, default=1, help='生成数量')
    args = parser.parse_args()

    generator = ContentGenerator()

    for i in range(args.count):
        if args.count > 1:
            print(f"\n{'='*50}")
            print(f"生成第 {i+1}/{args.count} 篇")
            print(f"{'='*50}\n")

        content = generator.generate_content(test_mode=args.test)

        if content:
            generator.save_content(content)

            if args.test:
                print("\n" + "="*50)
                print("完整内容预览:")
                print("="*50)
                print(f"\n标题: {content['title']}\n")
                print(content['content'])
                print(f"\n{' '.join(content['tags'])}")
                print("\n" + "="*50)


if __name__ == "__main__":
    main()
