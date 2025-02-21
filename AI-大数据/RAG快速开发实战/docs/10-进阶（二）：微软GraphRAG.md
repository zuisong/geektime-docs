> 本课程为精品小课，不标配音频

你好，我是常扬。

在关于 Modular RAG 的课程中，我们提到了 RAG 结合 **Knowledge Graph （知识图谱）**的概念。微软对此进行了深入的验证和项目实践，并于 2024 年 2 月发布了博客《[GraphRAG: Unlocking LLM Discovery on Narrative Private Data](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)》，同年 4 月又发布了论文《[From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/pdf/2404.16130)》，深入探讨了和验证了 RAG 结合知识图谱的技术效果。最终，他们在 7 月初通过 GitHub 开源了 [GraphRAG 项目](https://github.com/microsoft/graphrag)，迅速获得了业界的广泛关注。

微软提出，在实际应用中，RAG 在使用向量检索时面临两个主要挑战。

1. **信息片段之间的连接能力有限**：RAG 在跨越多个信息片段以获取综合见解时表现不足。例如，当需要回答一个复杂的问题，必须通过共享属性在不同信息之间建立联系时，RAG 无法有效捕捉这些关系。这限制了其在处理需要**多跳推理**或整合多源数据的**复杂查询**时的能力。
2. **归纳总结能力不足**：在处理大型数据集或长文档时，RAG 难以有效地**归纳和总结复杂的语义概念**。例如，试图从一份包含数百页的技术文档中提取关键要点，对 RAG 来说是极具挑战性的。这导致其在需要全面理解和总结复杂语义信息的场景中表现不佳。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>第10讲打卡~
感谢老师高质量的课程，受益匪浅~</div>2024-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/fe/87fd3eb5.jpg" width="30px"><span>柏颍</span> 👍（1） 💬（1）<div>老师好，我读过GraphRAG这篇论文，我看他好像还有抽取event(covariate)，可以解释一下这是什麽吗?</div>2024-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/b8/f6/e8f58f5e.jpg" width="30px"><span>ACY</span> 👍（0） 💬（1）<div>结课打卡，不知道使用自己部署的大模型做graph rag资源要求怎么样。</div>2024-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>答思考题作业，降低大模型成本，或者使用开源的大模型部署到本地，以节约成本。不使用OPENAI，</div>2024-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>知识图谱是一个很专业的工作，这个一个很高的成本，如果没有高质量领域的知识图谱怎么办。
</div>2024-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/46/42c2e559.jpg" width="30px"><span>煜寶</span> 👍（0） 💬（1）<div>微软的这个GraphRAG安全性如何呢。。。想用本地自己部署的，但是不知道这个数据安全性是否有猫腻，很多内部资源都不适合对外的</div>2024-11-10</li><br/>
</ul>