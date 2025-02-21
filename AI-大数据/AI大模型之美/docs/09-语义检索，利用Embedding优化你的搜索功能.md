你好，我是徐文浩。

在过去的8讲里面，相信你已经对Embedding和Completion接口非常熟悉了。Embedding向量适合作为一个中间结果，用于传统的机器学习场景，比如分类、聚类。而Completion接口，一方面可以直接拿来作为一个聊天机器人，另一方面，你只要善用提示词，就能完成合理的文案撰写、文本摘要、机器翻译等一系列的工作。

不过，很多同学可能会说，这个和我的日常工作又没有什么关系。的确，日常我们的需求里面，最常使用自然语言处理（NLP）技术的，是搜索、广告、推荐这样的业务。那么，今天我们就来看看，怎么利用OpenAI提供的接口来为这些需求提供些帮助。

## 让AI生成实验数据

在实际演示代码之前，我们需要一些可以拿来实验的数据。之前，我们都是在网上找一些数据集，或者直接使用一些机器学习软件包里面自带的数据集。但是，并不是所有时候我们都能很快找到合适的数据集。这个时候，我们也可以利用AI，我们直接让AI帮我们生成一些数据不就好了吗？

```python
import openai, os

openai.api_key = os.environ.get("OPENAI_API_KEY")
COMPLETION_MODEL = "text-davinci-003"

def generate_data_by_prompt(prompt):
    response = openai.Completion.create(
        engine=COMPLETION_MODEL,
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
    )
    return response.choices[0].text

prompt = """请你生成50条淘宝网里的商品的标题，每条在30个字左右，品类是3C数码产品，标题里往往也会有一些促销类的信息，每行一条。"""
data = generate_data_by_prompt(prompt)
```
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/92/aa/360eefd3.jpg" width="30px"><span>廉烨</span> 👍（14） 💬（1）<div>老师，请问是否有开源的embedding组件，能够达到或接近openai embedding能力的？能够用于中文问答搜索</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ca/58/6fe1854c.jpg" width="30px"><span>金</span> 👍（6） 💬（1）<div>这门课程主要讲nlp吗？</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/ef/cbb8d881.jpg" width="30px"><span>黄智荣</span> 👍（4） 💬（1）<div>这个挺有意思的。不过这种性能应该会降低很多，就算有这种通过faiss计算。原来通过倒排索引，用很低的资源就可以实现，用这faiss 数据量一大，估计都要用显卡才可以，量大对显存要求也很高</div>2023-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/65/22a37a8e.jpg" width="30px"><span>Yezhiwei</span> 👍（4） 💬（3）<div>请问老师可以把关系型数据库的结构化数据embedding 到向量数据库吗？比如财务报表的数据，然后通过自然语言的方式查询数据，谢谢</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/a0/8b9d5aca.jpg" width="30px"><span>eagle</span> 👍（4） 💬（1）<div>过几天openAI的模型版本升级了，这些保存的embedding会失效吗？</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/aa/33/5e063968.jpg" width="30px"><span>Jelly</span> 👍（3） 💬（1）<div>当使用Llama Index导入一篇产品介绍的时候，问：本产品的特征是什么，向量匹配不准确。使用XXX的特征就没问题。当导入年报的时候问：2022年营收是多少？向量匹配也不准确，直接问：营收是多少就可以。请问怎么让用户问的问题更智能？</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（1） 💬（1）<div>embedding的实现是否也需要基础模型的知识沉淀呢？比如文字上虽然不相同，但是含义相近的句子生成的向量是相似的，这个是依靠模型之前学习的知识是吗？那这样自然就是越大的模型embedding的效果越好？可以这样理解吗？</div>2023-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/2f/c5e5b809.jpg" width="30px"><span>渔樵耕读</span> 👍（1） 💬（2）<div>请问有遇到安装faiss时提示：PackagesNotFoundError的没？改为pip install faiss 报错：
ERROR: Could not find a version that satisfies the requirement faiss (from versions: none)
ERROR: No matching distribution found for faiss</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/60/ad/03351e6e.jpg" width="30px"><span>xbc</span> 👍（1） 💬（1）<div>cosine_similarity 也可以传入多个embeddings. 

scores = cosine_similarity(list[list[float]], list[float])
indices = np.argsort(scores)[::-1]</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/f2/db90fa96.jpg" width="30px"><span>Oli张帆</span> 👍（1） 💬（3）<div>考虑到我的服务器硬件资源有限（300MB的软限制，500MB的硬限制，现在已经占到了450MB），而且我已经在进行其他任务时使用了很多资源，当我在OpenAI之上构建AI机器人时，我考虑使用这个策略。请老师看看是否能行得通。

每当用户发送请求时，我首先检测他的意图。我可以使用小的embeddings来帮助意图检测。甚至可以有其他方式，如缓存和预先一些意图让用户来点击，来加速意图检测。

在我检测到用户意图后，我可以调用不同的embeddings库。例如，我的客服embeddings库将仅有50个项目，这对于余弦相似性来说非常快速和高效。我还可以将新闻embeddings库限制为最新的100篇文章，以便它可以轻松地通过余弦相似性处理。

尽管这种方法可能不像搜索单个大型嵌入数据库那样准确，但如果我为用户提供足够的指导，您认为它能产生足够好的用户体验吗？例如，在我的界面中，我可以向用户显示他们当前正在讨论“最新的AI发展”或“客户服务”。然后，也可以允许用户快速地改变当前的话题。

请老师看看，这个办法能不能跑通。还没有什么我没有想到的地方？</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/a7/83bf4578.jpg" width="30px"><span>Devon</span> 👍（0） 💬（1）<div>老师，对于几十万个精准的中文公司名称或者单位地址进行向量化之后，预存进DataFrame作为之后的搜索源，使用时根据较为“脏”的公司名称或者单位地址进行匹配，在这样的操作中对于中文公司名称或者单位地址的向量化预处理，有什么推荐的方式或者模型吗？用OpenAI embedding的话，费用和时间会不会不太经济？</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（2）<div>老师 在最后一个例子中

def search_index(index, df, query, k=5):

这里面的 query 不用先进行向量化吗? 那么这个时候不是要调用到Openai?
</div>2023-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（3）<div>老师,这样的搜索效果的效率如何? 如果我是一个话术类搜索的,1万多个标题直接用内容来进行搜索的话可以?</div>2023-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/cf/43f201f2.jpg" width="30px"><span>幼儿编程教学</span> 👍（0） 💬（2）<div>请教老师， get_embedding函数会请求openai。那么cosine_similarity函数是否会请求openai接口？</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>原来商品搜索、推荐系统都已经使用上了 AI，确实强大</div>2023-04-18</li><br/><li><img src="" width="30px"><span>Geek_78a551</span> 👍（0） 💬（0）<div>taobao_product_title.parquet 你把所有相关中间文件放一个代码库里分享吧</div>2024-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/39/ca/4a07bfd8.jpg" width="30px"><span>Jahng</span> 👍（0） 💬（0）<div>很好奇我们提示语要淘宝数据，gpt是怎么拿到这个数据的，是因为训练集里面有数据，还是联网拿的实时数据？不管是哪种，我后面都有非常多的疑问🤔️</div>2024-03-07</li><br/><li><img src="" width="30px"><span>Geek_f0daf6</span> 👍（0） 💬（0）<div>可以用羊驼2大模型吗</div>2023-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>taobao_product_title.parquet  老师这个文件可否发下呢？</div>2023-07-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/9wNL7qwjpZ1NQ6VIVNsZDyJrtkhUW5e7rpqMgR1qTsouamibLZC1oOv445jVUg1BOIJib4cHiaPGKBwrskyXn8xWw/132" width="30px"><span>没角蜗牛</span> 👍（0） 💬（1）<div>老师您好，我想问几个问题：
1： 文本的Embedding跟算法有关系，跟具体某个大模型没有关系吧？如果有关系，是什么关系
2： 如果问题一跟大模型没关系，那我们只要知道Embedding算法就可以处理所有分本分类相关的工作，都不需要大模型了
3： 如果Embedding跟大模型没关系，为啥不同的大模型处理文本分类的效果差距很大？

利用 Embedding 之间的余弦相似度作为语义上的相似度，优化搜索。通过 Embedding 的相似度，我们不要求搜索词和查询的内容之间有完全相同的关键字，而只要它们的语义信息接近就好</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/65/0f/7b9f27f2.jpg" width="30px"><span>猿鸽君</span> 👍（0） 💬（1）<div>老师好，请问下，数据量较大的情况下，为什么用向量数据库而不是faiss，像milvus不也是in-memory计算？而且为什么milvus对search返回的topk限制在了16348？faiss好像没看到有这种限制</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（0） 💬（1）<div>老师我们想用视频的字幕做检索 用什么技术比较好呀</div>2023-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3f/8d/a89be8f9.jpg" width="30px"><span>寻路人</span> 👍（0） 💬（1）<div>报错如下：Traceback (most recent call last):
  File &quot;C:&#47;Users&#47;liuzq&#47;Desktop&#47;Source&#47;others&#47;pythonProject&#47;lzq&#47;aigc&#47;opt_search.py&quot;, line 82, in &lt;module&gt;
    results = search_product(df, &quot;自然淡雅背包&quot;, n=3)
  File &quot;C:&#47;Users&#47;liuzq&#47;Desktop&#47;Source&#47;others&#47;pythonProject&#47;lzq&#47;aigc&#47;opt_search.py&quot;, line 69, in search_product
    df123[&quot;similarity&quot;] = df123.embedding.apply(lambda x: cosine_similarity(x, product_embedding))
  File &quot;E:\Anaconda3\lib\site-packages\pandas\core\series.py&quot;, line 4630, in apply
    return SeriesApply(self, func, convert_dtype, args, kwargs).apply()
  File &quot;E:\Anaconda3\lib\site-packages\pandas\core\apply.py&quot;, line 1025, in apply
    return self.apply_standard()
  File &quot;E:\Anaconda3\lib\site-packages\pandas\core\apply.py&quot;, line 1076, in apply_standard
    mapped = lib.map_infer(
  File &quot;pandas\_libs\lib.pyx&quot;, line 2834, in pandas._libs.lib.map_infer
  File &quot;C:&#47;Users&#47;liuzq&#47;Desktop&#47;Source&#47;others&#47;pythonProject&#47;lzq&#47;aigc&#47;opt_search.py&quot;, line 69, in &lt;lambda&gt;
    df123[&quot;similarity&quot;] = df123.embedding.apply(lambda x: cosine_similarity(x, product_embedding))
  File &quot;E:\Anaconda3\lib\site-packages\openai\embeddings_utils.py&quot;, line 66, in cosine_similarity
    return np.dot(a, b) &#47; (np.linalg.norm(a) * np.linalg.norm(b))
  File &quot;&lt;__array_function__ internals&gt;&quot;, line 180, in dot
ValueError: shapes (1536,) and (6,1536) not aligned: 1536 (dim 0) != 6 (dim 0)</div>2023-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d0/e676ac19.jpg" width="30px"><span>梦典</span> 👍（0） 💬（0）<div>基于AGI的向量实现语义搜索，真的震撼到我了。能否介绍一些这方面的论文？</div>2023-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（0） 💬（0）<div>老师，请问下，利用 Embedding 进行语义搜索是不是仅限于上下文与提问的关键字存在相关性，比如文中的例子。如果问题是一个需要进行聚合计算之类的问题，比如提问：&quot;一共有多少个气质背包?&quot;。这种问题还能利用向量相似性来给出答案吗？</div>2023-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/49/4a488f4c.jpg" width="30px"><span>农民园丁</span> 👍（0） 💬（0）<div>运行## 通过Embedding进行语义搜索代码出现如下错误：
InvalidRequestError: Too many inputs. The max number of inputs is 1.  We hope to increase the number of inputs per request soon. Please contact us through an Azure support request at: https:&#47;&#47;go.microsoft.com&#47;fwlink&#47;?linkid=2213926 for further questions

------
用的是azure openapi，请问可能是什么原因？</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/49/4a488f4c.jpg" width="30px"><span>农民园丁</span> 👍（0） 💬（0）<div>运行## 通过Embedding进行语义搜索代码出现如下错误：
InvalidRequestError: Too many inputs. The max number of inputs is 1.  We hope to increase the number of inputs per request soon. Please contact us through an Azure support request at: https:&#47;&#47;go.microsoft.com&#47;fwlink&#47;?linkid=2213926 for further questions

------
用的是azure openapi，请问可能是什么原因？</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/b4/295338e7.jpg" width="30px"><span>Allan</span> 👍（0） 💬（0）<div>授人以鱼不如授人以渔</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（0）<div>打卡学习</div>2023-04-04</li><br/>
</ul>