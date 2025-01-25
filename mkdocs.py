import os
import shutil
from pathlib import Path

import yaml


def _main():
    dirs = [
        'AI-大数据',
        '产品-运营',
        '前端-移动',
        '后端-架构',
        '管理-成长',
        '计算机基础',
        '运维-测试',
    ]
    all = []
    docs_dir = Path(__file__).parent.joinpath('dist')
    for dir in dirs:
        navs = [f"{dir}/index.md"]
        index_text = ''
        for sub_dir in sorted(os.listdir(dir)):
            item_dir = os.path.join(dir, sub_dir)
            item_mkdocs = os.path.join(item_dir, 'mkdocs.yml')
            if os.path.isfile(item_mkdocs):
                items = []
                with open(item_mkdocs, 'r') as f:
                    data = yaml.safe_load(f)
                    for nav in data['nav']:
                        nav_path = os.path.join(item_dir, nav)
                        real_nav_path = os.path.join(docs_dir, nav_path)
                        src_nav_path = os.path.join(item_dir, "docs", nav)
                        os.makedirs(os.path.dirname(real_nav_path), exist_ok=True)
                        shutil.copyfile(src_nav_path, real_nav_path)
                        items.append(nav_path)
                    index_text += f'\n[{os.path.basename(item_dir)}]({os.path.basename(item_dir)}/{os.path.basename(item_dir)})\n'
                navs.append({sub_dir: items})

        tag_index = os.path.join(docs_dir, dir, 'index.md')
        with open(tag_index, 'w') as wr:
            wr.write(index_text)

        all.append({dir: navs})

    with open('mkdocs.yml', 'w', encoding='utf-8') as w:
        with open("mkdocs_template.yml", 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            data.update({'nav': all})
            w.write(yaml.safe_dump(data, allow_unicode=True))

    shutil.copyfile('README.md', os.path.join(docs_dir, 'index.md'))


if __name__ == '__main__':
    _main()
