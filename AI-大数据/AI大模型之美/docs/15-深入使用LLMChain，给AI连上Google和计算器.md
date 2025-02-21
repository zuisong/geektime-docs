你好，我是徐文浩。

上一讲里，我们一起学习了怎么通过LangChain这个Python包，链式地调用OpenAI的API。通过链式调用的方式，我们可以把一个需要询问AI多轮才能解决的问题封装起来，把一个通过自然语言多轮调用才能解决的问题，变成了一个函数调用。

不过，LangChain能够帮到我们的远不止这一点。前一阵，ChatGPT发布了 [Plugins](https://openai.com/blog/chatgpt-plugins) 这个插件机制。通过Plugins，ChatGPT可以浏览整个互联网，还可以接上Wolfram这样的科学计算工具，能够实现很多原先光靠大语言模型解决不好的问题。不过，这个功能目前还是处于wait list的状态，我也还没有拿到权限。

不过没有关系，我们通过LangChain也能实现这些类似的功能。今天这一讲，我们就继续深入挖掘一下Langchain，看看它怎么解决这些问题。

## 解决AI数理能力的难题

很多人发现，虽然ChatGPT回答各种问题的时候都像模像样的，但是一到计算三位数乘法的时候就露馅儿了。感觉它只是快速估计了一个数字，而不是真的准确计算了。我们来看下面这段代码，我们让OpenAI帮我们计算一下 352 x 493 等于多少，你会发现，它算得大差不差，但还是算错了。这就很尴尬，如果我们真的想要让它来担任一个小学数学的助教，总是给出错误的答案也不是个事儿。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/56/b3/29c814af.jpg" width="30px"><span>君为</span> 👍（8） 💬（2）<div>老师你好，chain和pipe的原理还是比较像，学完这讲打开了我对ChatGPT可应用空间。实际应用中最大的问题还是api 的响应速度和接口限流。
请问老师有没有更好的解决办法？目前我知道的是多个账号负载均衡和调用容错重试。</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/e6/1effba61.jpg" width="30px"><span>hhh</span> 👍（4） 💬（1）<div>浩哥，文稿中代码、类库都是python脚步的，有java相关的生态推进吗？</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/65/22a37a8e.jpg" width="30px"><span>Yezhiwei</span> 👍（3） 💬（1）<div>之前自己试过 LangFlow 非常简单，把步骤记录下来了，难道在网络，如果网络稳定，很快看到效果 
https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;jjNkkoUu-q8Yb1J6_u6WGg</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ca/58/6fe1854c.jpg" width="30px"><span>金</span> 👍（2） 💬（2）<div>怎么让模板更通用呢？比如那个算术问题，如何判断是个计算问题，感觉模板只能解决调用问题.</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/9f/5e/791d0f5e.jpg" width="30px"><span>自然卷的Neil</span> 👍（1） 💬（3）<div>&quot;url&quot;: &quot;https:&#47;&#47;www.google.com&#47;search?q=&quot; + question.replace(&quot; &quot;, &quot;+&quot;)
这一段代码为什么需要加上+ question.replace(&quot; &quot;, &quot;+&quot;)
我看了langchain的手册也是这么写的，
如果输入是&#39;query&#39;: &#39;What are the Three (3) biggest countries, and their respective sizes?&#39;,
输出会变成&#39;url&#39;: &#39;https:&#47;&#47;www.google.com&#47;search?q=What+are+the+Three+(3)+biggest+countries,+and+their+respective+sizes?&#39;
不太理解这样做的意义是啥</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ca/58/6fe1854c.jpg" width="30px"><span>金</span> 👍（1） 💬（1）<div>这个确实不错，我一直在思考如何让chatgpt优雅的完成最后一步，langchain这个工具能很大程度解决这个问题。这个工具支持清华的那个开源大模型吗？</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/92/69c2c135.jpg" width="30px"><span>厚积薄发</span> 👍（0） 💬（1）<div>from langchain.chains import LLMRequestsChain

template = &quot;&quot;&quot;在 &gt;&gt;&gt; 和 &lt;&lt;&lt; 直接是来自Google的原始搜索结果.
请把对于问题 &#39;{query}&#39; 的答案从里面提取出来，如果里面没有相关信息的话就说 &quot;找不到&quot;
请使用如下格式：
Extracted:&lt;answer or &quot;找不到&quot;&gt;
&gt;&gt;&gt; {requests_result} &lt;&lt;&lt;
Extracted:&quot;&quot;&quot;

PROMPT = PromptTemplate(
    input_variables=[&quot;query&quot;, &quot;requests_result&quot;],
    template=template,
)
requests_chain = LLMRequestsChain(llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=PROMPT),verbose=True)
question = &quot;今天上海的天气怎么样？&quot;
inputs = {
    &quot;query&quot;: question,
    &quot;url&quot;: &quot;https:&#47;&#47;www.google.com&#47;search?q=&quot; + question.replace(&quot; &quot;, &quot;+&quot;)
}
result=requests_chain(inputs)
print(result)
print(result[&#39;output&#39;])

老师，我测试这段代码，返回值是找不到 ，是什么原因哈
</div>2023-05-11</li><br/><li><img src="" width="30px"><span>Geek_9691fb</span> 👍（0） 💬（1）<div>ecommerce_faq.txt 在哪里可以找到</div>2023-05-06</li><br/><li><img src="" width="30px"><span>沐瑞Lynn</span> 👍（0） 💬（2）<div>用LLMRequestsChain想谷歌提问，总是回答找不到；然后用requests直接写了个程序调google 页面，发现可能被拦截。然后问题了GPT，得到回答
“这段代码使用 requests 模块向 Google 搜索发出 GET 请求来获取指定问题的搜索结果页面的 HTML 代码。然后使用 print() 函数将 HTML 代码打印出来。
但是使用该方法获取 Google 搜索结果可能会被 Google 识别为机器行为，并被阻拦。建议使用 Google 提供的 API 来获取搜索结果。” 记录一下，看看大家是不是有同样的问题吧。</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/b4/4768f34b.jpg" width="30px"><span>旭</span> 👍（0） 💬（1）<div>如果是提供服务的话，链式计算中间步骤的容错性有没有好办法保证？</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/ed/08/fe7910e2.jpg" width="30px"><span>慕枫</span> 👍（0） 💬（1）<div>RequestsChain怎么判断是问题是否需要调用外部api？</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/cc/da91bd47.jpg" width="30px"><span>凝望</span> 👍（0） 💬（4）<div>RAyH4c
微博
给开发和使用LLM应用的各位提个醒，各路聊天
机器人和ChatXXx应用都使用的LangChain库，
对输入的提示词包了一层exec和eval函数，导致
所有提示词都能远程执行任意python代码...

老师好，看微博有人说这个问题，请问影响大吗？</div>2023-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/fa/e0dcc1bf.jpg" width="30px"><span>榕</span> 👍（0） 💬（2）<div>老师好，通过langchain等武器库确实给了我们使用大语言模型很大的想象空间，但前提得有大语言模型支持。对于地区限制访问的问题，那对于国内的个人或企业要真正落地这些能力，目前是通过哪些方式来做呢？谢谢</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（1）<div>老师这段代码里面:


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import SpacyTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import TextLoader

llm = OpenAI(temperature=0)
loader = TextLoader(&#39;.&#47;data&#47;ecommerce_faq.txt&#39;)
documents = loader.load()
text_splitter = SpacyTextSplitter(chunk_size=256, pipeline=&quot;zh_core_web_sm&quot;)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_documents(texts, embeddings)

faq_chain = VectorDBQA.from_chain_type(llm=llm, vectorstore=docsearch, verbose=True)

可以把索引给保存到数据库吗? 以后再继续使用?</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（2）<div>老师,我有个问题可以解答一下吗?我们目前开发的一款app,就有客户问到类似的问题,比如今天的时间,Chatgpt就没办法完整的回答,我看到上面的编译Python的方式似乎可行,但是似乎用户的问题千奇百怪,比如有的又会问到数学...而有的llm直接就能解决,在这种情况下,我要怎么实现会更好?</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（5） 💬（0）<div>ChatGPT被作为一种能力去使用，也就是X+AI模式，确实有不小的想象空间。
但反过来，如有一个大模型，能快速整合各种外部能力，从X+AI，变成AI+X、Y、Z，很可能会成为下一代互联网的入口，并从各种维度给人类带来全新体验，期待这个时代能尽快到来。</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/30/eb380376.jpg" width="30px"><span>月狼葱葱</span> 👍（3） 💬（0）<div>跑代码的时候发现UserWarning: `VectorDBQA` is deprecated - please use `from langchain.chains import RetrievalQA`

修改代码如下：

from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0), chain_type=&quot;stuff&quot;, retriever=docsearch.as_retriever())
question = &quot;请问你们的货，能送到三亚吗？大概需要几天？&quot;
result = qa.run(question)

print(result)

参考文档：https:&#47;&#47;www.langchain.com.cn&#47;modules&#47;chains&#47;index_examples&#47;vector_db_qa</div>2023-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/c5/92017a7b.jpg" width="30px"><span>硕果阳光</span> 👍（2） 💬（0）<div>btw VectorDBQA 已经被deprecated and replaced by RetrivalQA
https:&#47;&#47;python.langchain.com&#47;docs&#47;modules&#47;chains&#47;popular&#47;vector_db_qa</div>2023-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/19/0a3fe8c1.jpg" width="30px"><span>Evan</span> 👍（1） 💬（0）<div>RequestsChain 非常有效的，能调用外部接口的</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/82/f1/6f8bf660.jpg" width="30px"><span>蒸发杰作</span> 👍（0） 💬（0）<div>感觉到了AI确实在蓬勃发展，一大堆类库，目前还在蓄势待发</div>2024-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/a5/56/b3cf71a9.jpg" width="30px"><span>Penguin Shi</span> 👍（0） 💬（0）<div>&quot;通过 VectorDBQA 来实现先搜索再回复的能力&quot;后面的第一段代码，由于langchain RetrievalQA模块使用变化，调试很久，才可运行。可运行的代码如下，供参考：
from langchain.llms import OpenAI
from langchain import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import SpacyTextSplitter

from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.vectorstores.base import VectorStoreRetriever


llm = OpenAI(temperature=0)
loader = TextLoader(&#39;.&#47;data&#47;ecommerce_faq.txt&#39;)
documents = loader.load()
text_splitter = SpacyTextSplitter(chunk_size=256, pipeline=&quot;zh_core_web_sm&quot;)
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_documents(texts, embeddings)
retriever = VectorStoreRetriever(vectorstore=docsearch)
faq_chain = RetrievalQA.from_llm(llm=llm, retriever=retriever, verbose=True)</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/f3/69fdc9c8.jpg" width="30px"><span>zgxx</span> 👍（0） 💬（0）<div>final_result = final_chain.run(inputs)

inputs是哪里来的</div>2023-05-24</li><br/>
</ul>