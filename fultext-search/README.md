# 极客时间文档全文搜索系统

这是一个基于 Meilisearch 的文档全文搜索系统，专为极客时间文档设计。系统包含文档导入工具和搜索前端界面，支持快速检索和标签筛选功能。

## 环境要求

- Docker
- Python 3.12

## 安装指南

### 1. 配置环境变量

项目使用环境变量进行配置，提高了安全性和灵活性。您可以通过以下两种方式设置环境变量：

#### a. 创建 `.env` 文件

创建 `.env` 文件（与 `main.py` 同目录）:

```
# Meilisearch 配置
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_MASTER_KEY=geektime-search-master-key
MEILISEARCH_INDEX_NAME=geektime-docs

# Docker 配置
MEILISEARCH_PORT=7700
MEILI_ENV=development
MEILI_MASTER_KEY=geektime-search-master-key
WEB_PORT=8000
```

### 2. 启动 Docker compose

环境变量将自动应用于 Docker 容器：

```sh
docker-compose up -d
```

这将启动两个服务：

- **Meilisearch**: 搜索引擎，默认在端口 7700
- **Web 服务器**: 提供前端界面，默认在端口 8000

## 使用方法

### 1. 导入文档

注意，文档只需要导入一次，不需要重复导入

将 Markdown 文档放置在对应的目录下（参考 `main.py` 中的 `CHINESE_DIRS` 列表），然后运行:

```bash
python main.py
```

导入工具会自动从环境变量读取 Meilisearch 配置。

### 2. 访问搜索界面

Docker Compose 已经为您启动了一个 Web 服务器，可以直接在浏览器中访问:

```
http://localhost:8000
```

如果您修改了 `WEB_PORT` 环境变量，请使用对应的端口。

## 搜索界面使用说明

1. **基本搜索**：在搜索框中输入关键词，搜索结果会实时显示
2. **标签筛选**：点击界面上方的标签可以筛选特定类别的文档
   - 标签为互斥选择，每次只能选择一个标签
   - 点击已选中的标签可以取消筛选
3. **查看详情**：搜索结果显示文档标题、路径和内容预览
4. **分页浏览**：使用底部分页控件浏览更多结果

## 系统架构

- **后端**: Meilisearch 搜索引擎
- **导入工具**: Python 脚本 (`main.py`)
- **前端界面**: HTML + CSS + JavaScript (`index.html`)
- **部署**: Docker Compose

## 环境变量说明

| 变量名 | 用途 | 默认值 |
|-------|------|--------|
| MEILISEARCH_URL | Meilisearch 服务地址 | <http://localhost:7700> |
| MEILISEARCH_MASTER_KEY | Meilisearch 访问密钥 | geektime-search-master-key |
| MEILISEARCH_INDEX_NAME | 索引名称 | geektime-docs |
| MEILISEARCH_PORT | Docker容器暴露的端口 | 7700 |
| MEILI_ENV | Meilisearch环境模式 | development |
| MEILI_MASTER_KEY | Meilisearch容器内密钥 | geektime-search-master-key |
| WEB_PORT | Web服务器端口 | 8000 |

## 自定义设置

### 修改索引设置

可以在 `main.py` 中修改 Meilisearch 的索引设置:

```python
index.update_settings({
    "searchableAttributes": ["title", "content"],
    "displayedAttributes": ["title", "content", "path", "tags", "id"],
    "filterableAttributes": ["path", "tags"],
    # 其他设置...
})
```

### 修改前端界面

可以编辑 `index.html` 文件修改界面样式和行为。

## 故障排除

1. **无法连接到 Meilisearch**
   - 确保 Docker 容器正在运行: `docker-compose ps`
   - 检查环境变量配置是否正确
   - 验证端口映射: `docker-compose logs meilisearch`

2. **搜索结果为空**
   - 确保已成功导入文档（查看 `main.py` 的输出日志）
   - 检查索引名称是否匹配（在环境变量和前端代码中）
   - 验证文档内容: `curl http://localhost:7700/indexes/geektime-docs/documents?limit=1`

3. **标签筛选不生效**
   - 确保文档中包含正确的标签
   - 检查 `filterableAttributes` 设置中是否包含 "tags"

## 贡献指南

欢迎提交 Pull Request 或 Issue 来改进这个系统。

## 许可证

[MIT License](LICENSE)
