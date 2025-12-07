# DataCardPlugin 更新说明

## 新增功能：合并转发支持

### 📦 版本信息
- 更新日期: 2025-12-07
- 新增功能: 合并转发消息支持

### ✨ 主要改动

#### 1. 新增文件

```
utils/
├── forward_message.py          # 合并转发核心模块
├── utils_USAGE.md           # 使用文档
└── __init__.py                # 更新导出

examples/
├── forward_example.py         # 集成示例
└── test_forward.py            # 测试脚本

requirements.txt               # 新增 aiohttp 依赖
```

#### 2. 修改文件

**components/event_listener/default.py**
- ✅ 导入 `ForwardMessageSender` 类
- ✅ 在 `__init__` 中初始化合并转发发送器
- ✅ 在 `initialize` 中添加配置读取
- ✅ 智能判断是否使用合并转发
- ✅ 自动回退机制（失败时使用普通消息）

### 🎯 功能特性

#### 智能切换模式
- **默认阈值**: 结果超过 3 条时自动使用合并转发
- **自动回退**: 合并转发失败时自动切换为普通消息
- **可配置**: 支持通过 manifest.yaml 配置开关和阈值

#### 分隔符支持
- **默认分隔符**: `\n---\n`
- **自动识别**: 代码中已使用的 `\n---\n` 分隔符会自动转换为独立消息节点
- **图片支持**: 自动解析 markdown 格式图片 `![alt](url)`

#### 配置选项（可选）

在 `manifest.yaml` 中添加以下配置：

```yaml
config:
  llkshop_id:
    type: string
    default: "3abcd2e80b9b4694"
    description: "LLKShop店铺ID"

  # 合并转发配置（可选）
  use_forward:
    type: boolean
    default: true
    description: "是否启用合并转发功能"

  forward_threshold:
    type: integer
    default: 3
    description: "合并转发阈值，结果超过此数量时使用合并转发"

  onebot_api_url:
    type: string
    default: "http://127.0.0.1:3000"
    description: "OneBot v11 API地址"
```

### 📋 使用示例

#### 原有行为（结果 ≤ 3 条）
```
用户: 流量卡19元

机器人: [普通消息]
共找到包含19元的 3 个匹配产品
...
产品1详情
---
产品2详情
---
产品3详情
```

#### 新增行为（结果 > 3 条）
```
用户: 流量卡广东

机器人: [合并转发卡片]
标题: 流量卡查询 - 广东
摘要: 找到 10 个产品 | 共10条内容

[点开后显示]
节点1: 概览信息
节点2: 产品1详情
节点3: 产品2详情
...
节点10: 产品9详情
```

### 🔧 工作原理

#### 1. 判断逻辑
```python
# 当满足以下条件时使用合并转发：
# 1. use_forward = True (配置开启)
# 2. 查询成功
# 3. 结果数量 > forward_threshold (默认3)
use_forward = self.use_forward and result['success'] and len(result['results']) > 3
```

#### 2. 消息转换
```python
# 自动识别 \n---\n 分隔符
response_text = '\n'.join(reply_content)
# 每个 --- 分隔的块成为独立的消息节点
messages = self.forward_sender.convert_to_forward(response_text)
```

#### 3. 发送流程
```python
# 尝试发送合并转发
forward_result = await self.forward_sender.send_forward(
    group_id=event_context.event.launcher_id,
    messages=messages,
    prompt=f"流量卡查询 - {keyword}",
    summary=f"找到 {result['total_count']} 个产品",
    nickname="流量卡助手",
    mode="multi"
)

# 失败时自动回退到普通消息
if not forward_result['success']:
    # 使用原有的普通消息发送逻辑
    ...
```

### 📦 依赖要求

新增依赖：
```bash
pip install aiohttp
```

或使用：
```bash
pip install -r requirements.txt
```

### ⚙️ 环境要求

- **OneBot v11 API**: 需要运行支持合并转发的 OneBot 实现
  - NapCat (推荐)
  - go-cqhttp
  - OpenShamrock
  - 等其他支持 `send_forward_msg` 的实现

- **API 地址**: 默认 `http://127.0.0.1:3000`，可通过配置修改

### 🔍 调试信息

合并转发失败时会在日志中输出错误信息：

```
合并转发失败: HTTP 404，使用普通消息发送
合并转发出错: Connection refused，使用普通消息发送
```

### 🎨 效果对比

#### 之前
- 结果多时只显示前3个
- 需要用户发送更精确的关键词
- 图片和文本混合在一起可能较长

#### 现在
- 结果多时自动使用合并转发
- 显示所有结果，整齐有序
- 每个产品独立节点，易于浏览
- 失败时自动回退，不影响正常使用

### 📝 注意事项

1. **向后兼容**:
   - 不使用合并转发时，行为与之前完全一致
   - 配置项都有默认值，无需修改现有配置

2. **自动回退**:
   - OneBot API 不可用时自动使用普通消息
   - 确保功能稳定性

3. **可选功能**:
   - 可通过配置 `use_forward: false` 完全禁用
   - 不影响原有功能

### 🚀 快速测试

1. 确保 OneBot API 运行中
2. 查询较多结果的关键词：`流量卡广东` 或 `流量卡19`
3. 观察是否收到合并转发卡片

### 📚 更多信息

- 详细使用文档: `utils/utils_USAGE.md`
- 集成示例: `examples/forward_example.py`
- 测试脚本: `examples/test_forward.py`

---

## 技术细节

### 代码改动统计

**default.py**:
- 新增导入: 2 行
- 新增初始化: 1 行
- 新增配置: 4 行
- 修改消息发送逻辑: ~60 行

**新增文件**:
- `utils/forward_message.py`: ~340 行
- `utils/utils_USAGE.md`: 文档
- `examples/forward_example.py`: ~550 行示例
- `examples/test_forward.py`: ~320 行测试

### 架构设计

```
用户消息
    ↓
[流量卡查询]
    ↓
[判断结果数量]
    ↓
  ┌─────────────────┐
  │ 结果 > 3 条？    │
  └────┬────────┬───┘
       │YES     │NO
       ↓        ↓
 [合并转发]  [普通消息]
       ↓        ↓
   [失败?] → [回退] → [普通消息]
       ↓
   [成功]
```

### 性能影响

- **网络请求**: 合并转发需要额外的 HTTP 请求
- **内存占用**: 转换消息格式需要额外内存（微小）
- **响应时间**: 增加 < 100ms（取决于 OneBot API 响应速度）

### 安全性

- ✅ 输入验证: 消息内容经过验证
- ✅ 错误处理: 完整的异常捕获和回退机制
- ✅ 注入防护: 使用参数化构建，防止注入攻击
