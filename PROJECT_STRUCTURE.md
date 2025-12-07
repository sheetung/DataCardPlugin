# DataCardPlugin 项目结构

## 📁 目录结构

```
DataCardPlugin/
├── components/
│   └── event_listener/
│       ├── default.py              # 主事件处理器 [已修改 - 添加合并转发]
│       └── manifest.yaml
├── core/
│   └── datacard_search.py          # 流量卡搜索核心逻辑
├── utils/                          # [新增] 工具模块
│   ├── __init__.py                 # 模块导出
│   ├── forward_message.py          # [新增] 合并转发核心
│   ├── music_card.py               # 音乐卡片发送
│   ├── url_shortener.py            # URL 短链接
│   └── utils_USAGE.md            # [新增] 合并转发使用文档
├── examples/                       # [新增] 示例代码
│   ├── forward_example.py          # [新增] 合并转发集成示例
│   └── test_forward.py             # [新增] 功能测试脚本
├── main.py                         # 插件入口
├── manifest.yaml                   # 插件配置清单
├── requirements.txt                # 依赖列表 [已修改 - 添加 aiohttp]
├── CLAUDE.md                       # Claude Code 项目说明
├── CHANGES.md                      # [新增] 更新说明
├── QUICKSTART_FORWARD.md           # [新增] 快速入门指南
└── PROJECT_STRUCTURE.md            # [新增] 项目结构说明（本文件）
```

## 🔧 核心文件说明

### 主要模块

#### `components/event_listener/default.py`
**功能**: 监听群消息，处理流量卡查询命令
**修改**:
- ✅ 导入 `ForwardMessageSender`
- ✅ 初始化合并转发发送器
- ✅ 智能判断是否使用合并转发
- ✅ 自动回退到普通消息

**关键代码**:
```python
# 判断是否使用合并转发
use_forward = (
    self.use_forward and 
    result['success'] and 
    len(result['results']) > self.forward_threshold
)
```

#### `utils/forward_message.py` [新增]
**功能**: 合并转发核心实现
**主要类**:
- `ForwardMessageSender`: 合并转发发送器
  - `send_forward()`: 发送合并转发消息
  - `convert_to_forward()`: 转换消息格式
  - `update_config()`: 更新配置

**支持特性**:
- ✅ 自定义分隔符
- ✅ 图片自动解析
- ✅ 单节点/多节点模式
- ✅ 错误处理

#### `core/datacard_search.py`
**功能**: 爬取 LLKShop 流量卡信息
**未修改**: 保持原有逻辑不变

### 配置文件

#### `manifest.yaml`
**原有配置**:
```yaml
config:
  llkshop_id:
    type: string
    default: "3abcd2e80b9b4694"
```

**可选新增配置**:
```yaml
config:
  use_forward:
    type: boolean
    default: true
  forward_threshold:
    type: integer
    default: 3
  onebot_api_url:
    type: string
    default: "http://127.0.0.1:3000"
```

#### `requirements.txt`
**新增依赖**:
```
aiohttp  # 用于异步 HTTP 请求
```

## 📚 文档文件

### `QUICKSTART_FORWARD.md` [新增]
**内容**: 5分钟快速入门指南
**适合**: 快速了解和使用合并转发功能

### `utils/utils_USAGE.md` [新增]
**内容**: 详细使用文档和 API 说明
**适合**: 深入了解功能细节和高级用法

### `CHANGES.md` [新增]
**内容**: 完整的更新说明和技术细节
**适合**: 了解所有改动和架构设计

### `examples/forward_example.py` [新增]
**内容**: 4种不同的集成方式示例
**适合**: 参考如何在代码中使用合并转发

### `examples/test_forward.py` [新增]
**内容**: 6个测试用例
**适合**: 验证功能是否正常工作

## 🔄 消息流程

### 普通消息流程（原有）

```
用户发送消息
    ↓
匹配 "流量卡<关键词>"
    ↓
调用 datacard_search
    ↓
构建回复内容
    ↓
解析 markdown 图片
    ↓
构建 MessageChain
    ↓
发送到群聊
```

### 合并转发流程（新增）

```
用户发送消息
    ↓
匹配 "流量卡<关键词>"
    ↓
调用 datacard_search
    ↓
判断结果数量 > 3？
    ↓ YES
使用 \n---\n 分隔符构建内容
    ↓
convert_to_forward() 转换格式
    ↓
send_forward() 发送合并转发
    ↓
成功？→ 完成
    ↓ NO
回退到普通消息流程
```

## 🎯 关键特性

### 1. 自动分隔符识别
代码中已使用 `\n---\n` 分隔产品信息，无需修改原有逻辑：

```python
reply_content.append("\n---\n")  # 自动识别为消息分隔符
```

### 2. 智能切换
根据结果数量自动选择发送方式：
- **≤ 3 条**: 普通消息
- **> 3 条**: 合并转发

### 3. 无缝回退
合并转发失败时自动使用普通消息，确保功能稳定性。

### 4. 零配置启用
默认配置即可使用，无需额外设置。

## 🔌 依赖关系

```
main.py
  └── DefaultEventListener (default.py)
      ├── datacard_search (core/)
      └── ForwardMessageSender (utils/)
          └── aiohttp (HTTP 请求)
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 确认 OneBot API
```bash
curl http://127.0.0.1:3000/get_login_info
```

### 3. 测试功能
在群聊发送：`流量卡广东`

### 4. 查看效果
- 结果 > 3 条：收到合并转发卡片
- 结果 ≤ 3 条：收到普通消息

## 📊 代码统计

| 文件 | 类型 | 行数 | 说明 |
|------|------|------|------|
| `default.py` | 修改 | +60 | 添加合并转发逻辑 |
| `forward_message.py` | 新增 | 340 | 核心功能实现 |
| `forward_example.py` | 新增 | 550 | 集成示例 |
| `test_forward.py` | 新增 | 320 | 测试脚本 |
| 文档 | 新增 | - | 4个文档文件 |

## 🎓 学习路径

1. **快速上手**: `QUICKSTART_FORWARD.md`
2. **了解改动**: `CHANGES.md`
3. **查看示例**: `examples/forward_example.py`
4. **深入学习**: `utils/utils_USAGE.md`
5. **运行测试**: `examples/test_forward.py`

## 💡 最佳实践

### 开发建议

1. **修改分隔符**: 在 `convert_to_forward()` 中指定 `separator` 参数
2. **调整阈值**: 修改 `forward_threshold` 配置
3. **自定义昵称**: 修改 `send_forward()` 的 `nickname` 参数
4. **调试模式**: 查看控制台的错误输出

### 部署建议

1. 确保 OneBot API 稳定运行
2. 配置正确的 API 地址
3. 监控合并转发失败率
4. 根据实际情况调整阈值

## 🆘 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|----------|
| 合并转发不生效 | 结果数量 | 确认 > 3 条 |
| 发送失败 | OneBot API | 检查 API 状态 |
| 图片不显示 | 图片 URL | 验证 URL 可访问 |
| 导入错误 | aiohttp | 安装依赖 |

## 📞 支持

- **GitHub Issues**: https://github.com/sheetung/langbot-plugin-all
- **QQ 群**: 965312424
- **文档**: 查看 `utils/utils_USAGE.md`

---

**版本**: 1.0.0 (2025-12-07)
**作者**: sheetung
**协议**: 与原项目保持一致
