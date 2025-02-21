你好，我是徐文浩。

有不少人在使用OpenAI提供的GPT系列模型的时候，都反馈效果并不好。这些反馈中有一大类问题，是回答不了一些简单的问题。比如当我们用中文问AI一些事实性的问题，AI很容易胡编乱造。而当你问它最近发生的新闻事件的时候，它就干脆告诉你它不知道21年之后的事情。

本来呢，我写到这里就可以了。不过到了3月24日，OpenAI推出了ChatGPT Plugins这个功能，可以让ChatGPT通过插件的形式链接外部的第三方应用。我自己也还在排队等waiting list，所以暂时也无法体验。不过，即使有了第三方应用，我们也不能确保自己想要知道的信息正好被其他人提供了。而且，有些信息和问题我们只想提供给自己公司的内部使用，并不想开放给所有人。这个时候，我们既希望能够利用OpenAI的大语言模型的能力，但是又需要这些能力仅仅在我们自己指定的数据上。那么这一讲，就是为了解决这个问题的。

## 大型语言模型的不足之处

我们先来尝试问ChatGPT一个人尽皆知的常识，“鲁迅先生去日本学习医学的老师是谁”，结果它给出的答案是鲁迅的好友，内山书店的老板内山完造，而不是大家都学习过的藤野先生。

![图片](https://static001.geekbang.org/resource/image/89/64/891fc431e1cd46b1d45f60fe79c2e964.png?wh=704x264)

之所以会出现这样的情况，和大模型的原理以及它使用训练的数据集是有关的。大语言模型的原理，就是利用训练样本里面出现的文本的前后关系，通过前面的文本对接下来出现的文本进行概率预测。如果类似的前后文本出现得越多，那么这个概率在训练过程里会收敛到少数正确答案上，回答就准确。如果这样的文本很少，那么训练过程里就会有一定的随机性，对应的答案就容易似是而非。而在GPT-3的模型里，虽然整体的训练语料很多，但是中文语料很少。只有不到1%的语料是中文的，所以如果问很多中文相关的知识性或者常识性问题，它的回答往往就很扯。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/ad/26/767527f6.jpg" width="30px"><span>Owen</span> 👍（7） 💬（0）<div>截止到目前，最新能运行的代码

&#39;&#39;&#39;
归纳总结文章内容
&#39;&#39;&#39;
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import SpacyTextSplitter
from llama_index.core import SummaryIndex, ServiceContext, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

documents = SimpleDirectoryReader(input_dir=&quot;data&quot;).load_data() # 只能填写文件夹，不能具体到文件

service_context = ServiceContext.from_defaults(
    llm=ChatOpenAI(temperature=0, model_name=&quot;gpt-3.5-turbo&quot;, max_tokens=1000, n=1),
    node_parser=SentenceSplitter(chunk_size=512, chunk_overlap=20),
)

index = SummaryIndex.from_documents(documents = documents, service_context = service_context)
query_engine = index.as_query_engine()
response = query_engine.query(&quot;用中文总结这个故事&quot;)

print(response)</div>2024-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/a5/56/b3cf71a9.jpg" width="30px"><span>Penguin Shi</span> 👍（7） 💬（0）<div>《藤野先生》输出摘要的代码，因为代码更新，有bug，参考https:&#47;&#47;gpt-index.readthedocs.io&#47;en&#47;latest&#47;guides&#47;primer&#47;usage_pattern.html更新代码如下：

from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import SpacyTextSplitter
from llama_index import ListIndex, LLMPredictor, ServiceContext
from llama_index import (
    VectorStoreIndex,
    get_response_synthesizer,
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.node_parser import SimpleNodeParser

# define LLM
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name=&quot;gpt-3.5-turbo&quot;, max_tokens=1024))

text_splitter = SpacyTextSplitter(pipeline=&quot;zh_core_web_sm&quot;, chunk_size = 2048)
parser = SimpleNodeParser(text_splitter=text_splitter)
documents = SimpleDirectoryReader(&#39;.&#47;data&#47;mr_fujino&#39;).load_data()

index = ListIndex.from_documents(documents)
retriever = index.as_retriever()

query_engine = RetrieverQueryEngine.from_args(retriever, response_mode=&#39;tree_summarize&#39;)
response = query_engine.query(&quot;下面鲁迅先生以第一人称‘我’写的内容，请你用中文总结一下:&quot;)

print(response)

另目前文档中，&quot;我把从网上找到的《藤野先生》这篇文章变成了一个 txt 文件，放在了 data&#47;mr_fujino 这个目录下。我们的代码也非常简单，一共没有几行。&quot;此文字下方代码的，第7行，index = GPTSimpleVectorIndex.from_documents(documents)中，“GPTSimpleVectorIndex”还未改成“GPTVectorStoreIndex” ；第9行，更改为index.storage_context.persist(&#39;index_mr_fujino&#39;)。
请更改，方便后续同学学习并运行代码。</div>2023-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqQOqqTaRhPyuHICBpPfMcnNgg7xXmkrNZwlsibyLekYzNsuHdwdk1JLTUicbm4Oq78Zx17TFib2EusQ/132" width="30px"><span>Wise</span> 👍（20） 💬（5）<div>在llama_index V0.6.1 版本中，没有GPTSimpleVectorIndex 类了
import openai, os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
os.environ[&quot;OPENAI_API_KEY&quot;] = &#39;&#39;
# 加载 documents
documents = SimpleDirectoryReader(&#39;.&#47;data&#47;mr_fujino&#39;).load_data()
index = GPTVectorStoreIndex.from_documents(documents)
index.storage_context.persist(&#39;index_mr_fujino&#39;)

# 从磁盘重新加载：
from llama_index import StorageContext, load_index_from_storage
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir=&quot;.&#47;index_mr_fujino&quot;)
# load index
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
response = query_engine.query(&quot;鲁迅先生在日本学习医学的老师是谁？&quot;)
print(response)

参考官方文档连接：https:&#47;&#47;gpt-index.readthedocs.io&#47;en&#47;latest&#47;getting_started&#47;starter_example.html</div>2023-05-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（15） 💬（4）<div>想请教下老师，我们喂的语料，会被其他人看到使用吗？</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/53/c93b8110.jpg" width="30px"><span>daz2yy</span> 👍（11） 💬（1）<div>老师，请问下一个问题，我把它用作 QA 系统的时候有个问题，原本 QA 就有标准的回答模版，里面包括有文档地址、操作步骤等；如果让 GPT 根据这个模版来回答问题，他会自由发挥，会漏掉一部分内容；想拥有 AI 自由对话的能力，又想有固定的回答模版这个怎么能较好的兼顾呢？</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/cb/08bbf097.jpg" width="30px"><span>Terry</span> 👍（8） 💬（1）<div>老师，请教一下langchain我理解也是一个LLM应用框架，它的功能和版本也更新很快。它和llama_index的区分是什么？在LLM应用开发上，我们一般怎么选择会比较好？</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/d2/74/7861f504.jpg" width="30px"><span>马听</span> 👍（8） 💬（3）<div>分享一个加载MySQL数据的例子：
from llama_index import GPTSimpleVectorIndex,download_loader

DatabaseReader = download_loader(&#39;DatabaseReader&#39;)

reader = DatabaseReader(
    scheme = &quot;mysql&quot;, # Database Scheme
    host = &quot;localhost&quot;, # Database Host
    port = &quot;3306&quot;, # Database Port
    user = &quot;martin&quot;, # Database User
    password = &quot;xxxxxx&quot;, # Database Password
    dbname = &quot;martin&quot;, # Database Name
)

query = f&quot;&quot;&quot;
select * from student_info
&quot;&quot;&quot;

documents = reader.load_data(query=query)
print(documents)</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/81/49/2451a946.jpg" width="30px"><span>Oxygen Au 昕</span> 👍（6） 💬（1）<div>
response = list_index.query(&quot;下面鲁迅先生以第一人称‘我’写的内容，请你用中文总结一下:&quot;, response_mode=&quot;tree_summarize&quot;)
print(response)


上面这段代码报错，AttributeError: &#39;GPTListIndex&#39; object has no attribute &#39;query&#39; ， 我用的是llama-index 0.6.1

下面是正确的代码
query_engine = list_index.as_query_engine(response_mode=&quot;tree_summarize&quot;)
response = query_engine.query(&quot;下面鲁迅先生以第一人称‘我’写的内容，请你用中文总结一下:&quot;)
print(response)

结果： 鲁迅先生在日本学习医学时遇到了藤野严九郎教授，他很有学问，对学生也很关心，甚至帮助鲁迅修改讲义。但鲁迅当时不够用功，有时也很任性。在学习中，他遇到了一些困难和不愉快的事情，最终决定离开医学去学习生物学。离开前，藤野先生送给他一张照片，并希望他能保持联系。鲁迅很久没有和任何人通信，但想起了这位热心的老师，他的照片挂在鲁迅的房间里，每当他疲倦时看到照片就会感到勇气和良心发现。</div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/ef/cbb8d881.jpg" width="30px"><span>黄智荣</span> 👍（2） 💬（1）<div>现在有很多应用，在你把文档上传之后，还会给你一系列的提示，告诉你可以向对应的书或者论文问什么问题。
------ 可以根据索引的文本，让chatgpt 设计几个提问的问题</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（2） 💬（3）<div>上面from llama_index import GPTSimpleVectorIndex会报错，因为现在已经改成了GPTVectorStoreIndex。
from llama_index import GPTVectorStoreIndex &#47;&#47;老师看到后可以更新下
</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a8/1c/d231cbfb.jpg" width="30px"><span>Viola</span> 👍（2） 💬（2）<div> 有同学遇到吗？
type object &#39;GPTSimpleVectorIndex&#39; has no attribute &#39;from_documents&#39;</div>2023-04-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL1ibGVhrcN2dn9g9ib0NRotH876fWRVdgMSiaW4bKtBZJjNUVblh8IYacaahYzAnUhcYZn8V0eXzgnw/132" width="30px"><span>hawk</span> 👍（2） 💬（3）<div>这些预选的问题，应该也是通过组合特定的提示语，和段落摘要，扔给GPT得到的吧？</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7e/ca/0689da8f.jpg" width="30px"><span>牛味浓龙魏流</span> 👍（1） 💬（2）<div>所以llama_index跟chatGPT没什么关系是吗。。还是说这个包本身也在跟openAI打交道，看代码看不出来</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/f5/afdf4a68.jpg" width="30px"><span>东临沧海</span> 👍（1） 💬（1）<div>建议老师安装的库文件标明一下版本号，遇到这样问题好几次了，每次都要浪费大量时间。
llama_index版本都到v0.6.5，更新太快了</div>2023-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/a1/49643e20.jpg" width="30px"><span>snow</span> 👍（1） 💬（2）<div>想请教下老师，为什么我在调用query 的时候，提示说BaseQueryEngine.query() got an unexpected keyword argument &#39;response_mode&#39; ？  发现当定义 list_index = GPTListIndex(nodes=nodes, service_context=service_context)， 没法直接调用list_index.query() ,而需要  list_index.as_query_engine().query() 这样子调用。 </div>2023-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/da/ed4803cb.jpg" width="30px"><span>CCC</span> 👍（1） 💬（3）<div>老师index创建的过程中会把文本内容传给openai进行embedding召回吗，这个地方不太理解索引创建是完全本地的还是需要openai的向量数据</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/a1/24/98e4985d.jpg" width="30px"><span>橘子🍊汽水</span> 👍（1） 💬（4）<div>重新输入了
!pip install -U llama-index
还是报错，老师可以帮忙看看吗？

ImportError: cannot import name &#39;GPTSimpleVectorIndex&#39; from &#39;llama_index&#39; (&#47;usr&#47;local&#47;lib&#47;python3.10&#47;dist-packages&#47;llama_index&#47;__init__.py)</div>2023-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/c1/92c540fe.jpg" width="30px"><span>joy  ོ</span> 👍（1） 💬（2）<div>针对开源模型，什么场景建议使用第二大脑？什么场景建议使用finetune?</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/17/57/ac61fff9.jpg" width="30px"><span>卯熙</span> 👍（1） 💬（1）<div>老师，为什么 用 GPTListIndex 消耗的 token 比 用  GPTSimpleVectorIndex 的要多， GPTSimpleVectorIndex 不是还有用到  Embedding 吗？</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/bc/c7514a30.jpg" width="30px"><span>Dev.lu</span> 👍（1） 💬（1）<div>谢谢老师分享，想问一下，
1. 语料的大小会不会影响回答问题的延时？
2. 如果需要对语料进行添加或者减少，每次都需要重跑代码？
3. 如果离线语料数据很大，index过后的语料数据有没有可能导致内存不够，或者OpenAI的API会限制request的大小吗？还是收费不同</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/99/5bf198e3.jpg" width="30px"><span>孟健</span> 👍（1） 💬（2）<div>如果是代码仓库，还适合用embedding这个方案吗？我看中科院开源的那个方案就可以总结源码，向源码提问什么的，不知道是怎么做的</div>2023-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/60/ad/03351e6e.jpg" width="30px"><span>xbc</span> 👍（1） 💬（1）<div>老师，带我们玩玩 modelscope.cn</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/19/e1/a7fbc963.jpg" width="30px"><span>Warren</span> 👍（1） 💬（1）<div>请问llama_index中的GPTSimpleVectorIndex就是调用openai的api做的embedding吗？</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（1）<div>请问老师，我换了一篇文章用 llama_index 做总结，一直报限速问题，好像是llama内部调用的报错，应该怎么改进代码呢？
Retrying langchain.chat_models.openai.ChatOpenAI.completion_with_retry.&lt;locals&gt;._completion_with_retry in 8.0 seconds as it raised RateLimitError: Rate limit reached for default-gpt-3.5-turbo in organization org-oEUgEoq9uZ4oju2xVxmZ7cUO on requests per min. Limit: 3 &#47; min. Please try again in 20s. Contact us through our help center at help.openai.com if you continue to have issues. Please add a payment method to your account to increase your rate limit. Visit https:&#47;&#47;platform.openai.com&#47;account&#47;billing to add a payment method..</div>2023-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/20/07/80337e76.jpg" width="30px"><span>江湖中人</span> 👍（0） 💬（1）<div>老师，请教一下，这个可以用来做机器人客服吗？看起来好像只要把自家的数据喂给它就可以了，如果用来做客服，有什么需要注意的呢</div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/00/cb00b423.jpg" width="30px"><span>郑雨瑛</span> 👍（0） 💬（1）<div>老师，我读取的自己的一个文件，然后运行的时候报错，请问这个错误是什么引起的？
执行语句：
------------
response = list_index.query(&quot;下面是一个项目的文件，请你用中文总结一下:&quot;, response_mode=&quot;tree_summarize&quot;)
print(response)
--------
File ~&#47;miniforge3&#47;envs&#47;geektime&#47;lib&#47;python3.10&#47;site-packages&#47;llama_index&#47;langchain_helpers&#47;text_splitter.py:157, in TokenTextSplitter.split_text_with_overlaps(self, text, extra_info_str)
    155 num_cur_tokens = max(len(self.tokenizer(cur_token)), 1)
    156 if num_cur_tokens &gt; effective_chunk_size:
--&gt; 157     raise ValueError(
    158         &quot;A single term is larger than the allowed chunk size.\n&quot;
    159         f&quot;Term size: {num_cur_tokens}\n&quot;
    160         f&quot;Chunk size: {self._chunk_size}&quot;
    161         f&quot;Effective chunk size: {effective_chunk_size}&quot;
    162     )
    163 # If adding token to current_doc would exceed the chunk size:
    164 # 1. First verify with tokenizer that current_doc
    165 # 1. Update the docs list
    166 if cur_total + num_cur_tokens &gt; effective_chunk_size:
    167     # NOTE: since we use a proxy for counting tokens, we want to
    168     # run tokenizer across all of current_doc first. If
    169     # the chunk is too big, then we will reduce text in pieces

ValueError: A single term is larger than the allowed chunk size.
Term size: 453
Chunk size: 356Effective chunk size: 356</div>2023-04-26</li><br/><li><img src="" width="30px"><span>Geek_a96962</span> 👍（0） 💬（1）<div>老师，既然是ai大模型之美，能不能介绍不用chatgpt的，比如用一些开源的大模型 来完成相同的业务</div>2023-04-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJEjHEWycVre5ZRtE6M8KaWyu1GKA0KOQsrrlm0ZdZf9EIljQ8P19uZdKS2uINwnzCibnv2iaRfmIPw/132" width="30px"><span>小黑</span> 👍（0） 💬（1）<div>INFO:llama_index.token_counter.token_counter:&gt; [query] Total LLM token usage: 4043 tokens
INFO:llama_index.token_counter.token_counter:&gt; [query] Total embedding token usage: 58 tokens

INFO:llama_index.token_counter.token_counter:&gt; [query] Total LLM token usage: 4160 tokens
INFO:llama_index.token_counter.token_counter:&gt; [query] Total embedding token usage: 45 tokens

为什么我总是提问消耗token多，回复可以用的token就不剩什么了？这个在哪里可以设置？</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/9d/1b/8f0f9f13.jpg" width="30px"><span>数据分析站站</span> 👍（0） 💬（1）<div>为什么执行index=GPTSimpleVectorIndex.from_documents(documents)
报错：AuthenticationError: Incorrect API key provided: &#39;&#39;. You can find your API key at https:&#47;&#47;platform.openai.com&#47;account&#47;api-keys.
执行之前课程的都是可以的</div>2023-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/72/43/a0898bb7.jpg" width="30px"><span>覃瑞星</span> 👍（0） 💬（1）<div>上传的是pdf的话，有办法定位到具体的引用位置吗。譬如查出来文字，给的gpt作参考，同时需要定位到文字是来自原文第一页第二段这样。</div>2023-04-17</li><br/>
</ul>