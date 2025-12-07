# 合并转发功能快速入门

## 🚀 5分钟快速上手

### 1️⃣ 安装依赖

```bash
cd /home/sheetung/langbot-plugin-all/DataCardPlugin
pip install aiohttp
```

或使用：
```bash
pip install -r requirements.txt
```

### 2️⃣ 确认 OneBot API 运行

确保你的 OneBot v11 API（如 NapCat）正在运行：

```bash
# 检查 API 是否可访问
curl http://127.0.0.1:3000/get_login_info
```

如果返回 JSON 数据，说明 API 正常运行。

### 3️⃣ 功能已自动启用

**无需任何配置！** 合并转发功能已经集成到 `default.py` 中，默认启用。

### 4️⃣ 测试功能

在群聊中发送：

```
流量卡广东
```

或

```
流量卡19元
```

- **结果 ≤ 3 条**: 普通消息发送
- **结果 > 3 条**: 自动使用合并转发卡片

## 📋 工作原理

### 自动判断逻辑

```python
# 当满足以下条件时自动使用合并转发：
1. 配置启用 (默认: True)
2. 查询成功
3. 结果数量 > 3 条
```

### 消息分隔符

代码中已经使用的 `\n---\n` 分隔符会自动识别：

```python
reply_content.append("第一条消息")
reply_content.append("\n---\n")  # 这个分隔符会将消息分成独立节点
reply_content.append("第二条消息")
reply_content.append("\n---\n")
reply_content.append("第三条消息")
```

每个 `---` 分隔的块都会成为合并转发中的独立消息节点。

### 自动回退

如果合并转发失败（如 OneBot API 不可用），会自动回退到普通消息：

```
合并转发失败: Connection refused，使用普通消息发送
```

## ⚙️ 可选配置

如果你想自定义配置，在 `manifest.yaml` 中添加：

```yaml
config:
  # 已有配置...
  llkshop_id:
    type: string
    default: "3abcd2e80b9b4694"

  # 合并转发配置（可选）
  use_forward:
    type: boolean
    default: true
    description: "是否启用合并转发"

  forward_threshold:
    type: integer
    default: 3
    description: "结果超过几条时使用合并转发"

  onebot_api_url:
    type: string
    default: "http://127.0.0.1:3000"
    description: "OneBot v11 API地址"
```

### 配置说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `use_forward` | boolean | `true` | 是否启用合并转发 |
| `forward_threshold` | integer | `3` | 结果超过此数量时使用合并转发 |
| `onebot_api_url` | string | `http://127.0.0.1:3000` | OneBot API 地址 |

## 🎯 使用示例

### 示例 1: 少量结果（普通消息）

```
用户: 流量卡29元特惠

机器人: [普通消息]
共找到包含29元特惠的 2 个匹配产品
...
产品详情1
---
产品详情2
```

### 示例 2: 大量结果（合并转发）

```
用户: 流量卡广东

机器人: [合并转发卡片]
┌─────────────────────┐
│ 流量卡查询 - 广东    │
│ 找到 10 个产品      │
│ 共10条内容          │
└─────────────────────┘

点击打开后显示：
├─ 概览信息
├─ 产品1
├─ 产品2
├─ ...
└─ 产品10
```

## 🔧 故障排查

### 问题 1: 合并转发不生效

**检查项**:
1. 结果是否超过 3 条？
2. OneBot API 是否运行？
3. 查看日志是否有错误信息

**解决方法**:
```bash
# 检查 API
curl http://127.0.0.1:3000/get_status

# 查看插件日志
# （具体位置取决于你的 LangBot 配置）
```

### 问题 2: 显示"合并转发失败"

**可能原因**:
- OneBot API 不支持 `send_forward_msg` 接口
- API 地址配置错误
- 网络连接问题

**解决方法**:
1. 确认使用的是 NapCat 或其他支持合并转发的实现
2. 检查 `onebot_api_url` 配置
3. 查看 OneBot 日志

### 问题 3: 想要禁用合并转发

在 `manifest.yaml` 中添加：

```yaml
config:
  use_forward:
    type: boolean
    default: false
```

或者直接修改 `default.py:33`：

```python
self.use_forward = False  # 强制禁用
```

## 📊 效果对比

| 特性 | 之前 | 现在 |
|------|------|------|
| 结果显示 | 最多3条 | 全部显示 |
| 消息长度 | 可能很长 | 整洁的卡片 |
| 浏览体验 | 需要滚动 | 独立节点，易于浏览 |
| 失败处理 | - | 自动回退到普通消息 |

## 🎨 自定义分隔符

默认使用 `\n---\n` 作为分隔符。如果你想修改代码使用其他分隔符：

```python
# 在 default.py 中修改
messages = self.forward_sender.convert_to_forward(
    response_text,
    separator="|||"  # 使用自定义分隔符
)
```

## 📚 更多资源

- **详细文档**: `utils/utils_USAGE.md`
- **集成示例**: `examples/forward_example.py`
- **测试脚本**: `examples/test_forward.py`
- **更新说明**: `CHANGES.md`

## ✅ 检查清单

- [x] 已安装 `aiohttp` 依赖
- [x] OneBot API 正在运行
- [x] 已测试流量卡查询功能
- [x] 合并转发正常工作
- [ ] （可选）已添加自定义配置

## 💡 提示

1. **首次使用**: 建议先测试一个会返回多个结果的查询，如 "流量卡广东"
2. **调试模式**: 查看控制台输出，了解是否使用了合并转发
3. **回退机制**: 即使 OneBot API 不可用，插件也能正常工作（回退到普通消息）

## 🆘 需要帮助？

如果遇到问题：

1. 查看 `utils/utils_USAGE.md` 详细文档
2. 运行测试脚本: `python3 examples/test_forward.py`
3. 检查 OneBot API 日志
4. 加入 QQ 群: 965312424

---

**现在就试试吧！在群里发送 "流量卡广东" 看看效果！** 🎉
