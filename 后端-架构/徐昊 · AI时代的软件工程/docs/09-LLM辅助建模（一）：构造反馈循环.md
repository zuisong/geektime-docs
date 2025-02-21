你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

上节课，我们介绍了如何使用LLM辅助进行模型展开，从而应用业务知识。具体做法是通过Mermaid将业务模型转化为大语言模型（Large Language Model，LLM）易于理解的方式，再用半结构化自然语言补充上下文，让思维链的构造更加简单。

但是如果我们没有模型要怎么处理呢？利用LLM辅助建模是否也能比传统建模方法更有效率呢？这是我们今天要讨论的问题。

## 构造反馈循环

建模的过程，是学习业务知识并提炼知识的过程。我们在[第六节课](https://time.geekbang.org/column/article/760312)提到使用LLM时，可以通过缩短反馈周期提高知识学习的效率。那么我们可以通过构造一个反馈循环，使用LLM帮助我们完成建模的过程。

在反馈循环的过程中，我们处在复杂的认知模式下，也就是遵循**探测（Probe）- 感知（Sense）- 响应（Respond）**的认知行为模式。

我们之前提到过，由于**探测**环节费力费时，往往会成为整个反馈周期的瓶颈。但是有了LLM的辅助，我们可以在**探测**阶段快速产生初始结果，或是根据反馈重新执行任务。那么**感知**这一环节就可能会成为新的瓶颈。

在我们前面课程的例子里，我们希望LLM帮助我们把一个基于关系型数据的解决方案，改造为使用MongoDB的解决方案。**感知**就比较直接了：将LLM生成的代码直接执行就可以了。但对于模型就没有这么简单了。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/f6/eca921d9.jpg" width="30px"><span>赫伯伯</span> 👍（5） 💬（2）<div>能不能直接给大模型用户故事？让他根据用户故事建模</div>2024-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（1） 💬（1）<div>🤔☕️🤔☕️🤔
【R】建模时处于复杂认知模式，构造复杂认知模式的反馈循环，通过LLM加速建模过程、以及认知负担下降。
模板 = 建模任务 + 模型检查 + 模型展开。
关键 = 用户故事 + 反馈循环。
【.I.】建模 = 实体 + 关系 = 概要设计 = 总体设计 = 用户故事从自然语言、转变成结构化描述 = 对代码实现而言的半结构化描述。
【Q】用户故事，如果Clear，那么建模是否为Complicated，如果用户故事本身也Complicated，那么建模才是Complex？
— by 术子米德@2024年3月27日</div>2024-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（5） 💬（0）<div>这节课需要代码来反复生成 prompt，不过老师没贴代码，所以我让 GPT 写了一下，放到公众号了，希望对大家有帮助~

链接：
https:&#47;&#47;mp.weixin.qq.com&#47;s?__biz=Mzg3MDg5MzYyMA==&amp;mid=2247483819&amp;idx=1&amp;sn=64bb8ce513260a785e589ae45eccd19f&amp;chksm=ce8790f0f9f019e63aa26e10cba54eb8eab1def0af5f2a192c7566bb773541ffa1d9f2310098&amp;token=597248625&amp;lang=zh_CN#rd</div>2024-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>第二次学习收获

当处于一个陌生的领域时，可以

1. 简述需求，让 AI 生成 mermaid 的 class diagram
2. 将 mermaid 带入 CoT；补充用户故事、验收场景到 CoT；开始新一轮 RAG 任务获取更多缺失概念与不正确的概念
3. 验收与 AI 互动后的学习成果

以上三步分别对应文中的三个模板：建模任务模板 -&gt; 模型检查任务模板 -&gt; 模型展开任务模板</div>2024-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>我用 claude 做建模任务模板，还给了一个答案：缺少模型 Degree(学位):用户故事提到了&quot;获取学位的进度&quot;,但是当前模型中没有学位的概念。学位应该是一个独立的实体,包含学位名称、级别等属性。</div>2024-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>2024年05月03日11:51:10
蛮有意思的 3 个会话模板，有了模板关于就在于“用户故事”、“验收场景”这 2 个了</div>2024-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/62/78b45741.jpg" width="30px"><span>Morty</span> 👍（0） 💬（0）<div>一定要用三个 Session 吗？不能在一个对话里完成吗？</div>2024-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（0）<div>用国内的智谱清言走了一遍课程的流程，发现结果非常发散，不停的在增加实体，无法收敛。不知道这种情况算好事，还是坏事，如何让它停止发散，快速收敛。</div>2024-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（0）<div>我注意到模板里面有个“```plain”，这个是笔误还是为了和mermaid区分出来加的呢？</div>2024-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/eb/8a2c26ab.jpg" width="30px"><span>王海</span> 👍（0） 💬（0）<div>老师，可以把完整的 prompt 或者完整的 LLM 对话内容分享一下吗？文章中只有prompt模板。</div>2024-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（0）<div>【Q】检查模型的模板、展开模型的模板，输入一样、输出一样，它们的差别是啥？</div>2024-03-30</li><br/>
</ul>