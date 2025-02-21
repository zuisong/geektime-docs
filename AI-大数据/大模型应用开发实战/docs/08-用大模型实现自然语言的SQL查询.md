你好，我是黄佳。今天我们继续利用大模型的能力来构建简单又实用的工具。

今天我将带着你学习如何利用 Claude 大模型生成从简单到复杂的 SQL 查询语句。我们的目标是展示如何将自然语言问题转化为精确的 SQL 命令，以便有效地从数据库中提取所需信息。这样，我们就能充分地利用 Claude 的自然语言处理能力，简化和自动化 SQL 查询的生成过程，使得数据分析工作更加高效和直观。

这里，我们选用一个强大的模型——Claude-3 Opus。

下面就开始第一个实战：生成简单的SQL查询语句。

## 生成 SQL 查询语句

利用Claude这样一个大语言模型来生成SQL查询的关键步骤如下：

1. 设置好要使用的大语言模型。
2. 创建一个测试数据库，并插入示例数据。
3. 获取数据库的Schema信息，并将其格式化为字符串。
4. 定义一个函数，将自然语言问题和数据库Schema发送给Claude，并获取生成的SQL查询。
5. 执行生成的SQL查询，并打印结果。

下面一步步来完成它。

### 步骤 1：设置模型

这一步是准备工作，创建大模型的客户端。

```plain
from dotenv import load_dotenv
load_dotenv()

# 导入Anthropic库
from anthropic import Anthropic

# 设置Anthropic API客户端
client = Anthropic()
MODEL_NAME = "claude-3-opus-20240229"
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/96/da84604a.jpg" width="30px"><span>回到原点</span> 👍（1） 💬（2）<div>用gpt-4-turbo弄了一些，每次出来的结果都不一样，感觉有点不太行啊，但是换了gpt-4o每次出来结果就一样了</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/55/b6c9c0f4.jpg" width="30px"><span>liyinda0000</span> 👍（0） 💬（1）<div>老师，感觉您的示例还是比较简单，如果正式环境写sql会很复杂，有什么好方法可以保障自然语言能够转化成正确的sql吗？</div>2024-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rURvBicplInVqwb9rX21a4IkcKkITIGIo7GE1Tcp3WWU49QtwV53qY8qCKAIpS6x68UmH4STfEcFDJddffGC7lw/132" width="30px"><span>onemao</span> 👍（0） 💬（1）<div>跟langchian课里是不是类似啊，那里用的gpt，这里换成了Claude</div>2024-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/60/8b9572ac.jpg" width="30px"><span>小风</span> 👍（0） 💬（0）<div>这个怎么使用本地的模型呢。https:&#47;&#47;modelscope.cn&#47;models&#47;senjia&#47;llama-3-8B-Instruct-text2sql
就就像这个模型</div>2024-07-03</li><br/><li><img src="" width="30px"><span>谢江涛</span> 👍（0） 💬（0）<div>老师，您好。这两个表之间的关系：employees e ON d.name = e.department，是大模型自动识别的吗？我们使用千问搭建的大模型环境不能正确识别两个表之间的关系，请问该如何处理？谢谢！</div>2024-06-17</li><br/>
</ul>