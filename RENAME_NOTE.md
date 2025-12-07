# 文档更新说明

## 📝 文件重命名

### 变更内容

`utils/FORWARD_USAGE.md` 已重命名为 `utils/utils_USAGE.md`

### 变更原因

新的文档名称更能反映其内容范围：
- ✅ 整合了**音乐卡片**使用文档
- ✅ 整合了**合并转发**使用文档
- ✅ 提供了统一的 utils 模块使用指南

### 新文档结构

`utils/utils_USAGE.md` 现在包含两大部分：

#### 📀 音乐卡片功能
- `MusicCardSender` 类详细说明
- 发送自定义音乐卡片
- 发送平台音乐卡片（QQ音乐、网易云音乐等）
- 使用示例和最佳实践

#### 📨 合并转发功能
- `ForwardMessageSender` 类详细说明
- 消息转换和分隔符支持
- 单节点/多节点模式
- 使用示例和最佳实践

### 影响范围

以下文档中的引用已自动更新：
- ✅ `CHANGES.md`
- ✅ `PROJECT_STRUCTURE.md`
- ✅ `QUICKSTART_FORWARD.md`
- ✅ `README_FORWARD.md`
- ✅ `SUMMARY.txt`

### 使用建议

现在查看 utils 模块的使用方法，请阅读：
```
utils/utils_USAGE.md
```

这个文档包含了：
- 📀 音乐卡片的完整使用方法
- 📨 合并转发的完整使用方法
- 🔧 同时使用两个功能的示例
- 📚 快速参考和 API 对照表

### 快速导航

| 功能 | 文档位置 | 说明 |
|------|---------|------|
| 音乐卡片 + 合并转发 | `utils/utils_USAGE.md` | 完整使用文档 |
| 合并转发快速入门 | `QUICKSTART_FORWARD.md` | 5分钟上手 |
| 完整示例代码 | `examples/forward_example.py` | 集成示例 |
| 测试脚本 | `examples/test_forward.py` | 功能测试 |

---

**更新时间**: 2025-12-07
**版本**: 1.0.1
