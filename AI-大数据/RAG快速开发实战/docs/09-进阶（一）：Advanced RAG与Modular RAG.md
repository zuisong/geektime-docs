> 本门课程为精品小课，不标配音频。

你好，我是常扬。

在之前的课程中，我们已经详细讨论了RAG（Retrieval Augmented Generation）检索增强生成的技术架构以及相关的效果优化技术，涵盖了其核心流程：索引（Indexing）、检索（Retrieval）和生成（Generation）。这些流程共同作用，提升了大模型的领域知识生成能力。这节课我们将深入介绍 **Advanced RAG（进阶 RAG）**与 **Modular RAG（模块化 RAG）**，进一步加深对 RAG 技术范式发展的理解，为进一步优化和提升RAG产品的效果提供研发基础。

RAG技术在适应复杂应用场景和不断发展的技术需求中，经历了从最初的 **Naive RAG （朴素 RAG）**，到流程优化的 **Advanced RAG**，再到更具灵活性的 **Modular RAG** 的演变。值得注意的是，这三个范式之间具有**继承与发展**的关系：Advanced RAG 是 Modular RAG 的一种特例形式，而 Naive RAG 则是 Advanced RAG 的基础特例。通过这种逐步演进，RAG技术不断优化，以应对更复杂的任务和场景需求，如下图所示。

![图片](https://static001.geekbang.org/resource/image/7c/a0/7c3ebbe6ec9d9f2886881d7e534396a0.jpg?wh=1920x1129 "图片源自于 https://arxiv.org/pdf/2312.10997")

Naive RAG 是最基础的形式，它依赖核心的索引和检索策略来增强生成模型的输出，适用于一些基础任务和产品 MVP（Minimum Viable Product，最小可用版本）阶段。Advanced RAG 则通过增加检索前、检索中以及检索后的优化策略，提高了检索的准确性和生成的关联性，特别是在复杂任务中表现更为出色。Modular RAG 则进一步打破了传统的链式结构，允许不同模块之间的灵活组合以及流程的适应性编排，提供了更高的灵活性和可扩展性，用于处理多样化的需求和复杂任务。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3c/4f/93/76d800ca.jpg" width="30px"><span>i33</span> 👍（3） 💬（1）<div>你好  我是刚做RAG相关开发，目前遇到一个项目中涉及技术是将长句切分成短句和query做匹配，然后返回来找对应的长句 类似于句子窗口检索 小到大检索  这种目前有实现的设计吗  想学习一下</div>2024-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/02/60c52ddc.jpg" width="30px"><span>冰炎</span> 👍（0） 💬（1）<div>对于近义词查询扩展如果把原始问题，原始问题检索结果、近义词查询扩展结果送给交叉编码器进行重排序会不会存在模型倾向于给与原始查询召回的文档更高的相关性评分、而相对忽略了通过近义词扩展召回的文档的风险</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/02/60c52ddc.jpg" width="30px"><span>冰炎</span> 👍（0） 💬（1）<div>您好，请问对于查询扩展（比如同义词扩展）应如何输出？是组成新查询去检索并重排序还是说各自检索并重排然后使用最大值或平均值或加权平均输出？业界有没有相关的一些探索或论文</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>请问Advanced RAG 与Modular RAG章节的代码案例有吗？</div>2024-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d0/e676ac19.jpg" width="30px"><span>梦典</span> 👍（0） 💬（1）<div>1.请问检索后优化策略之知识注入没有很理解，能举个例子更加详细描述一下吗？
2.针对思考题，我觉得业务场景比较多，并且各个场景需要的RAG策略并不相同，并且对输出时间要求并不苛刻，非常适合Modular RAG，提升最终生成效果，并且能够自适应；Modular RAG有代码实现吗？</div>2024-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/83/4a/3e08427e.jpg" width="30px"><span>药师</span> 👍（0） 💬（2）<div>老师您好，动态嵌入这项是否大部分模型都是支持的，还是需要做定制处理呢？</div>2024-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第9讲打卡~</div>2024-10-29</li><br/>
</ul>