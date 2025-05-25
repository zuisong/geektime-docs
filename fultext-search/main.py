import os
import hashlib
import meilisearch
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量获取配置，如果不存在则使用默认值
MEILISEARCH_URL = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
MEILISEARCH_MASTER_KEY = os.getenv(
    "MEILISEARCH_MASTER_KEY", "geektime-search-master-key"
)
INDEX_NAME = os.getenv("MEILISEARCH_INDEX_NAME", "geektime-docs")

# 定义所有需要导入的中文目录
CHINESE_DIRS = [
    "产品-运营",
    "前端-移动",
    "后端-架构",
    "运维-测试",
    "计算机基础",
    "管理-成长",
    "AI-大数据",
]


def get_file_hash(file_path):
    """生成文件路径的哈希值"""
    return hashlib.md5(file_path.encode()).hexdigest()


def import_docs_to_meilisearch(docs_dir):
    client = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_MASTER_KEY)

    try:
        index = client.create_index(INDEX_NAME)
        print(f"创建索引 {INDEX_NAME}")
    except:
        print(f"索引 {INDEX_NAME} 已存在，继续使用")

    index = client.index(INDEX_NAME)
    # 优化索引设置
    index.update_settings(
        {
            "searchableAttributes": ["title", "content"],
            "displayedAttributes": ["title", "content", "path", "tags", "id"],
            "filterableAttributes": ["path", "tags"],
            "sortableAttributes": ["title"],
            "typoTolerance": {
                "enabled": True,
                "minWordSizeForTypos": {"oneTypo": 4, "twoTypos": 8},
            },
            "pagination": {"maxTotalHits": 20},
        }
    )

    for root, _, files in os.walk(docs_dir):
        docs = []
        for file in files:
            if file.endswith(".md") and file != "index.md":
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, docs_dir)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                doc = {
                    "id": get_file_hash(relative_path),
                    "title": os.path.splitext(file)[0],
                    "content": content,
                    "path": relative_path,
                    "tags": [docs_dir.replace("../", ""), relative_path.split("/")[0]],
                }
                docs.append(doc)
        if docs:
            index.add_documents(docs)
            print(f"成功导入 {len(docs)} 个文档到 Meilisearch")
    else:
        print("没有找到需要导入的文档")


if __name__ == "__main__":
    total_docs = 0
    for dir_name in CHINESE_DIRS:
        docs_dir = f"../{dir_name}"
        if not os.path.exists(docs_dir):
            print(f"警告：目录 {docs_dir} 不存在，跳过")
            continue
        print(f"\n开始导入 {dir_name} 目录的文档...")
        import_docs_to_meilisearch(docs_dir)
        total_docs += 1

    print(f"\n导入完成！共处理了 {total_docs} 个目录")
