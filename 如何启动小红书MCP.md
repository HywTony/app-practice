# 如何启动小红书 MCP

> 官方项目地址：https://github.com/xpzouying/xiaohongshu-mcp

## 快速开始

### 方式一：启动 MCP 服务（推荐）

#### 1. 启动 MCP 本地服务

直接运行可执行文件即可启动小红书 MCP 本地服务：

```bash
xiaohongshu-mcp-windos-amd64/xiaohongshu-mcp-windows-amd64.exe
```

服务启动后会在 `http://localhost:18060/mcp` 监听。

#### 2. 在 Claude Desktop 中配置 MCP

##### 查看当前 MCP 连接状态

```bash
claude mcp list
```

##### 添加小红书 MCP（首次使用）

如果还未添加小红书 MCP，使用以下命令：

```bash
claude mcp add --transport http xiaohongshu-mcp http://localhost:18060/mcp
```

**参数说明：**
- `--transport http`：使用 HTTP 传输协议
- `xiaohongshu-mcp`：MCP 服务名称（可自定义）
- `http://localhost:18060/mcp`：MCP 服务地址

#### 3. 验证连接

在 Claude 中可以使用小红书相关的 MCP 工具，例如：
- `mcp__xiaohongshu-mcp__check_login_status` - 检查登录状态
- `mcp__xiaohongshu-mcp__list_feeds` - 获取首页内容
- `mcp__xiaohongshu-mcp__publish_content` - 发布内容

### 方式二：启动测试界面（开发调试）

开发者提供了带图形界面的测试工具，用于测试小红书连接和发布功能：

```bash
xiaohongshu-mcp-windos-amd64/xiaohongshu-login-windows-amd64.exe
```

**适用场景：**
- 测试小红书账号登录
- 调试内容发布功能
- 验证 API 连接状态
- 开发功能测试

## 主要功能

### 登录管理
- 扫码登录小红书
- 检查登录状态
- Cookie 持久化存储

### 内容管理
- 浏览首页 Feeds
- 获取笔记详情
- 搜索笔记内容
- 查看用户主页

### 内容发布
- 发布图文笔记
- 发布视频内容
- 支持话题标签

### 互动功能
- 点赞/取消点赞
- 收藏/取消收藏
- 发表评论

## 使用流程

1. **启动服务**
   ```bash
   xiaohongshu-mcp-windows-amd64.exe
   ```

2. **配置 Claude**
   ```bash
   claude mcp add --transport http xiaohongshu-mcp http://localhost:18060/mcp
   ```

3. **登录账号**
   - 使用 `get_login_qrcode` 获取二维码
   - 使用小红书 App 扫码登录
   - 使用 `check_login_status` 验证登录状态

4. **开始使用**
   - 在 Claude 中直接调用小红书 MCP 工具
   - 所有工具都以 `mcp__xiaohongshu-mcp__` 前缀开头

## 注意事项

### 端口占用
- 默认端口：18060
- 检查端口占用：`netstat -ano | findstr 18060`
- 如需修改端口，请查看项目配置文档

### 登录状态
- 首次使用需要扫码登录
- 登录信息会保存在本地 Cookie 文件中
- 登录状态长期有效，除非手动删除 Cookie

### 安全建议
- Cookie 文件包含敏感信息，注意保护
- 不要在公共环境使用
- 定期检查登录设备

### MCP 服务
- MCP 服务需要保持运行才能在 Claude 中使用
- 服务崩溃后需要重新启动
- 建议在后台保持运行

## 常见问题

### 1. 服务无法启动

**可能原因：**
- 端口 18060 被占用
- 可执行文件权限不足
- 防火墙阻止

**解决方案：**
```bash
# 检查端口占用
netstat -ano | findstr 18060

# 以管理员权限运行
# 右键 -> 以管理员身份运行

# 检查防火墙设置
```

### 2. Claude 无法连接 MCP

**检查步骤：**
1. 确认 MCP 服务正在运行
2. 验证服务地址：`http://localhost:18060/mcp`
3. 检查 MCP 是否已添加：`claude mcp list`
4. 尝试重新添加 MCP
5. 重启 Claude Desktop

### 3. 登录失败或过期

**解决方案：**
1. 删除本地 Cookie 文件
2. 重新获取登录二维码
3. 使用小红书 App 重新扫码
4. 验证登录状态

### 4. 发布内容失败

**常见原因：**
- 未登录或登录过期
- 内容违反平台规则
- 图片/视频格式不支持
- 网络连接问题

**检查步骤：**
1. 先检查登录状态
2. 确认内容符合平台规范
3. 检查文件格式和大小
4. 查看详细错误信息

## 更多信息

- 项目地址：https://github.com/xpzouying/xiaohongshu-mcp
- 问题反馈：提交 GitHub Issue
- 更新日志：查看项目 Releases

## 版本信息

- 当前使用版本：windows-amd64
- 其他平台：查看项目 Releases 下载对应版本
