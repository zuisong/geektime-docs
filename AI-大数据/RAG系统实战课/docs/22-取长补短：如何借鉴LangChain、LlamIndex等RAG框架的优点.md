你好，我是叶伟民。

上节课，我们学习了两种改进检索质量的方法——在用户交互层面提供精确信息，在业务逻辑层面提供精确信息。

但是仅仅靠这两种方法是不够的，那么我们如何去学习其他改进RAG质量的技术呢？授人以鱼不如授人以渔，这一节课我们就来学习一种很实用的方法，通过查看LangChain、LlamaIndex源码，学习改进RAG质量的技术。

## 我使用LangChain的经历

LangChain是最早的RAG框架之一，也是至今名气最响的RAG框架。你可以通过后面这个[链接](https://www.langchain.com/)进入到LangChain的官网。

我入门RAG的时候就使用了LangChain。但是正如开篇词里面所说到的，发现LangChain不支持微信小程序流式输出，于是这部分代码不再使用LangChain，改成自己实现。后来又发现当时的Langchain不支持百度文心，于是这部分代码也改成了自己实现。后来又发现LangChain不支持很多中国特有的场景……

不知不觉，我发现在我的RAG应用里面，LangChain占的比例极低。我也看过其他的国产RAG框架，也有各自的缺点，没有一个RAG框架可以满足我现实工作中20%的实际需求。这就是这门课程没有使用任何RAG框架的原因。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/c1/d0/0f6aba9c.jpg" width="30px"><span>Jamysp</span> 👍（0） 💬（0）<div>通过大模型，将C#代码转换为自己熟悉的代码，比如python</div>2024-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（0） 💬（0）<div>老师整合LlamaIndex代码能分享吗？</div>2024-10-24</li><br/>
</ul>