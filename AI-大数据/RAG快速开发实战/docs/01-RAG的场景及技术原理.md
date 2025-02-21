> 本门课程为精品小课，不标配音频

你好，我是常扬。

在探讨RAG技术之前，我们先看在开发大语言模型（LLM）应用时会遇到的典型场景问题。比如，当设计一个LLM问答应用，模型需要处理用户的领域问题时，尽管大模型通常表现出色，但有时提供的答案并不准确，甚至可能出现错误。当用户需要获取实时信息时，模型无法及时提供最新的答案。这种现象在LLM应用中较为常见。

随着ChatGPT、文心一言、通义千问、LLama系列等大模型的广泛应用，各行业尝试将其引入业务流程。这些模型在知识、理解和推理方面展现了卓越的能力，在复杂交互场景中表现尤为突出。

然而，这些模型仍然存在一些无法忽视的局限性。其中，**领域知识缺乏**是最明显的问题。大模型的知识来源于训练数据，这些数据主要来自公开的互联网和开源数据集，无法覆盖特定领域或高度专业化的内部知识。**信息过时**则指模型难以处理实时信息，因为训练过程耗时且成本高昂，模型一旦训练完成，就难以获取和处理新信息。

此外，**幻觉问题**是另一个显著的局限，模型基于概率生成文本，有时会输出看似合理但实际错误的答案。最后，**数据安全性**在企业应用中尤为重要，如何在确保数据安全的前提下，使大模型有效利用私有数据进行推理和生成，是一个具有挑战性的问题。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（7） 💬（5）<div>1. RAG模式:
场景:实时新闻总结与分析
原因:新闻信息更新频繁,需要实时检索最新信息,结合大模型的理解能力生成洞见。

2. 微调模式:  
场景:专业领域诊断系统(如工业设备故障诊断)
原因:故障模式相对固定,通过微调可以让模型深度掌握专业知识和诊断流程。

3. RAG+微调模式:
场景:个性化教育助手
原因:结合RAG检索教材知识,微调则针对不同学习风格优化输出,实现个性化辅导。</div>2024-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（1）<div>第1讲打卡~</div>2024-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/f7/228a6c37.jpg" width="30px"><span>江湖上</span> 👍（0） 💬（1）<div>”选择 RAG 而不是直接将所有知识库数据交给大模型处理，主要是因为模型能够处理的 token 数有限“，RAG检索到的信息也需要交给大模型做处理的吧？</div>2025-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/eb/8a2c26ab.jpg" width="30px"><span>王海</span> 👍（0） 💬（1）<div>我的学习笔记（思维导图）：
https:&#47;&#47;www.processon.com&#47;view&#47;link&#47;66f25623ebac4f017e4ab62b?cid=66f21f10da38ea3e04966645</div>2024-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2a/e6/c788257f.jpg" width="30px"><span>geek_arong2048</span> 👍（0） 💬（1）<div>很赞，配图详细说明完整</div>2024-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/02/60c52ddc.jpg" width="30px"><span>冰炎</span> 👍（0） 💬（1）<div>微调：切词&#47;词性标注&#47;分类，翻译</div>2024-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2d/13/bd7c990f.jpg" width="30px"><span>是希望</span> 👍（3） 💬（1）<div>希望老师能够在每节课程的末尾提供一些高质量的课外阅读资料</div>2024-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/18/f486f2fb.jpg" width="30px"><span>ttp的小跟班</span> 👍（0） 💬（0）<div>有个问题，就是通过RAG、微调、以及 RAG+ 微调这三种模式对LLM，怎么再次系统评估其效果呢，作者有啥推荐的方案么？
我们现在的AI助手就面临这个问题，现在就是在领域内，人工挑一些典型的case去跑，但是感觉还是人工介入太多了</div>2025-02-19</li><br/>
</ul>