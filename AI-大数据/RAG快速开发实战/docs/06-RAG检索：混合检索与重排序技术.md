你好，我是常扬。

我们本节课正式开始讲解 **RAG 检索流程**。当前主流的 RAG 检索方式主要采用**向量检索（Vector Search）**，通过语义相似度来匹配文本切块。这种方法在我们之前的课程中已经深入探讨过了。然而，向量检索并非万能，它在某些场景下无法替代传统关键词检索的优势。

例如，当你需要精准搜索某个订单 ID、品牌名称或地址，或者搜索特定人物或物品的名字（如伊隆·马斯克、iPhone 15）时，向量检索的准确性往往不如关键词检索。此外，当用户输入的问题非常简短，仅包含几个单词时，比如搜索缩写词或短语（如 RAG、LLM），语义匹配的效果也可能不尽理想。

这些正是传统关键词检索的优势所在。关键词检索（Keyword Search）在几个场景中表现尤为出色：**精确匹配**，如产品名称、姓名、产品编号；**少量字符的匹配**，用户习惯于输入几个关键词，而少量字符进行向量检索时效果可能较差；以及**低频词汇的匹配**，低频词汇往往承载了关键意义，如在“你想跟我去喝咖啡吗？”这句话中，“喝”“咖啡”比“你”“吗”更具重要性。

![](https://static001.geekbang.org/resource/image/57/15/57337062d6bf564a0116412f889c4615.jpg?wh=2000x916)

在上述案例中，虽然依靠关键词检索可以精确找到与“订单 12345”匹配的特定信息，但它无法提供与订单相关的更广泛上下文。另一方面，语义匹配虽然能够识别“订单”和“配送”等相关概念，但在处理具体的订单 ID 时，往往容易出错。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/02/60c52ddc.jpg" width="30px"><span>冰炎</span> 👍（3） 💬（2）<div>用bge-reranker-large重排后发现mrr值居然不如重排前直接使用bge和bm25混合检索得到的，不知道是哪里使用不当还是什么原因</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c5/52/63008fc7.jpg" width="30px"><span>xuwei</span> 👍（2） 💬（1）<div>老师，咨询下，我实际项目中，用的是问答对。将问题embedding存入向量库，召回使用的混合召回。如果用bge-reranker-large，是将用户的原始问题和检索出来的问题放到模型里做重排吗？然后根据重排结果，找到对应的答案吗？</div>2024-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/eb/8a2c26ab.jpg" width="30px"><span>王海</span> 👍（2） 💬（1）<div>混合检索中的关键词检索可以换成 ES 实现吗？</div>2024-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（1） 💬（1）<div>老师课程中的代码为何不使用LangChain中，`EnsembleRetriever`组件实现混合检索呢？</div>2024-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/b1/da/5602cb4b.jpg" width="30px"><span>king</span> 👍（0） 💬（1）<div>老师请问下加载重排序模型无法加载，是啥原因：huggingface_hub.errors.LocalEntryNotFoundError: An error happened while trying to locate the file on the Hub and we cannot find the requested files in the local cache. Please check your connection and try again or make sure your Internet connection is on.
</div>2024-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/68/9b/d53ebac5.jpg" width="30px"><span>Grain Buds</span> 👍（0） 💬（1）<div>请问为什么运行app_rag_lesson6_2.py ，在reranking阶段发生Bus error (core dumped)</div>2024-11-27</li><br/><li><img src="" width="30px"><span>Geek_8af4ba</span> 👍（0） 💬（1）<div>第一张图，向量检索和关键词检索是不是画反了？</div>2024-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（0）<div>第6讲打卡~
在LangChain中，可以使用`EnsembleRetriever`组件实现混合检索，支持指定检索器列表，并为每个检索器设置权重。</div>2024-10-24</li><br/>
</ul>