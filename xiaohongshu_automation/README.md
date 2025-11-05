# 巨爆铺小红书自动化营销系统

自动生成并发布小红书营销内容的完整解决方案。

## 🎯 功能特点

- ✅ AI自动生成高质量文案
- ✅ 智能内容模板系统
- ✅ 自动话题标签匹配
- ✅ 定时发布调度
- ✅ 内容效果追踪
- ✅ 草稿审核机制

## 📁 项目结构

```
xiaohongshu_automation/
├── config/
│   ├── config.yaml          # 主配置文件
│   └── templates.json       # 内容模板
├── src/
│   ├── content_generator.py # AI内容生成器
│   ├── xhs_publisher.py     # 发布器
│   └── scheduler.py         # 定时调度器
├── assets/
│   ├── images/             # 图片资源
│   ├── videos/             # 视频资源
│   └── templates/          # 设计模板
├── logs/
│   ├── content_*.json      # 生成的内容
│   ├── draft_*.json        # 草稿
│   └── publish_log.json    # 发布日志
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install anthropic pyyaml schedule pillow
```

### 2. 配置API密钥

```bash
# Windows
set ANTHROPIC_API_KEY=your-api-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-api-key-here
```

### 3. 修改配置

编辑 `config/config.yaml`，根据你的需求调整：
- 产品信息
- 发布频率
- 内容策略
- AI参数

### 4. 测试内容生成

```bash
cd src
python content_generator.py --test
```

### 5. 查看生成的内容

生成的内容会保存在 `logs/content_*.json`

### 6. 发布内容

**方式A：手动发布（推荐）**
```bash
python xhs_publisher.py --manual
```

**方式B：指定文件发布**
```bash
python xhs_publisher.py --file ../logs/content_20250101_120000.json
```

### 7. 启动自动化调度器

```bash
python scheduler.py --start
```

## 📝 使用指南

### 生成单篇内容

```bash
python content_generator.py --test
```

### 批量生成内容

```bash
python content_generator.py --count 5
```

### 测试调度器

```bash
python scheduler.py --test
```

### 启动定时任务

```bash
python scheduler.py --start
```

## ⚙️ 配置说明

### config.yaml 主要配置项

```yaml
# 发布频率（每天2次）
content_strategy:
  post_frequency: 2
  post_times:
    - "09:00"
    - "20:00"

# 自动发布开关（建议先设为false，手动审核）
publish:
  auto_publish: false
  save_draft: true
```

### templates.json 模板配置

内置6种内容模板：
1. 工具合集-效率提升
2. 工具合集-新手友好
3. 对比测评型
4. 痛点共鸣型
5. 教程-快速上手
6. 教程-进阶技巧

## 🎨 内容定制

### 1. 添加新模板

在 `config/templates.json` 中添加：

```json
{
  "template_new": {
    "name": "新模板",
    "title_pattern": "{变量}模式的标题",
    "content_structure": ["段落1", "段落2"],
    "style": "风格描述",
    "emoji_density": "high"
  }
}
```

### 2. 修改话题标签

在 `config/config.yaml` 中修改 `hashtags` 部分：

```yaml
hashtags:
  primary:
    - "你的主要标签"
  secondary:
    - "次要标签1"
    - "次要标签2"
```

### 3. 调整AI参数

```yaml
ai:
  temperature: 0.8  # 创意度（0-1，越高越创意）
  max_tokens: 1500  # 最大字数
```

## 📊 效果监控

### 查看发布日志

```bash
cat logs/publish_log.json
```

### 日志格式

```json
{
  "timestamp": "2025-01-01T09:00:00",
  "title": "发布的标题",
  "content_type": "工具合集型",
  "result": {
    "status": "success",
    "likes": 120,
    "collections": 150
  }
}
```

## 🔧 高级功能

### 1. 图片生成

当前使用占位图片，实际使用时需要：

**方案A: 使用Canva**
1. 创建1242x1656px模板
2. 导出图片到 `assets/images/`

**方案B: 使用AI生成**
```python
# 在 content_generator.py 中集成
# Midjourney / Stable Diffusion
```

**方案C: 使用设计模板**
- 准备好图片模板
- 使用Python-PIL自动填充文字

### 2. 视频生成

集成剪映API或其他视频工具：
```python
# 示例代码
def generate_video(script):
    # 调用视频生成工具
    pass
```

### 3. A/B测试

在 `config/config.yaml` 中配置测试组：
```yaml
ab_testing:
  enabled: true
  variants:
    - title_style: "数字型"
    - title_style: "疑问型"
```

## 📱 在Claude Code中使用

在Claude Code环境中，可以直接调用小红书MCP进行发布：

```python
# xhs_publisher.py 中的实际发布代码
def publish_to_xiaohongshu_mcp(self, content, images):
    """使用MCP发布到小红书"""
    # 这段代码在Claude Code环境中运行
    result = mcp__xiaohongshu_mcp__publish_content(
        title=content['title'],
        content=content['content'],
        images=images
    )
    return result
```

## ⚠️ 注意事项

### 内容合规
- ❌ 避免使用"最好"、"第一"等绝对化用语
- ❌ 不要夸大宣传或虚假承诺
- ✅ 保持真实、诚恳的分享态度

### 发布频率
- 建议每天2篇（早晚高峰）
- 避免短时间内大量发布
- 注意内容质量优于数量

### 账号安全
- 定期发布非营销内容
- 积极回复评论互动
- 不要完全依赖自动化

## 🐛 故障排除

### 问题1: API密钥错误
```bash
# 检查环境变量
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY%  # Windows
```

### 问题2: 无法生成内容
- 检查网络连接
- 确认API余额充足
- 查看 `logs/` 中的错误信息

### 问题3: 调度器不执行
- 确认时间格式正确（HH:MM）
- 检查系统时间设置
- 使用 `--test` 参数测试

## 📚 学习资源

### 相关文档
- [小红书运营指南](../xiaohongshu_auto_marketing.md)
- [Claude API文档](https://docs.anthropic.com)
- [小红书MCP使用说明](https://github.com/your-mcp-repo)

### 示例内容
查看 `logs/` 目录中的生成示例

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请查看项目Issues或联系开发者。

---

**最后更新**: 2025-11-04
**版本**: v1.0.0
