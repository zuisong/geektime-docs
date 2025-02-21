你好，我是郑晔！

我们都知道，这一波的 AI 浪潮始于 2022 年底的 ChatGPT 发布，有一幅图，很多人都见过，它说明 ChatGPT 是人类有始以来最快突破一亿用户的应用，用时仅仅 2 个月。

![](https://static001.geekbang.org/resource/image/63/d2/6358dde6a7f2d3263e281b7b85acc4d2.jpg?wh=2113x1460)

那么你是否想过这样一个问题，为什么ChatGPT能成为增长最快的应用？

一个重要的因素是 ChatGPT 是以聊天的形式呈现。拜诸如微信、WhatsApp 之类即时聊天工具所赐，人们已经非常习惯在文本框里输入文字的交流方式，这是普通人能够理解 ChatGPT 的基础，也是 ChatGPT 得以破圈的关键原因。

如果说最初吸引用户的原因是聊天模式的熟悉感，那么留住用户的就是 ChatGPT 的优异表现，这背后的支撑是 GPT 模型，它是大语言模型里最有代表性的一个。我们课程里 AI 应用开发主要用的就是大语言模型（Large Language Model，LLM）。

LLM 这个名字告诉我们三件事：

- 它是模型，是 AI 能力的核心。
- 它是语言模型，其核心能力在于语言能力。
- 它是大语言模型，与传统模型相比，它最大的特点就是“大”。

我们在这个专栏里谈论的 AI 应用，就是以 LLM 为核心的各种应用。如果从 API 的角度理解 GPT 模型，它最核心的参数就是输入一个或多个字符串，然后，大模型输出一个字符串，这是非常简单的。但是，与传统的应用开发不同的是，这个 API 并非是传统应用开发中按照特定预期处理的结果。换言之，使用传统的 API，我们需要关注的是接口文档，而想要发挥 LLM 的威力，我们需要对大模型有一定的了解。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（3） 💬（1）<div>第1讲打卡~
日常使用大模型的场景还是挺多的，比如 AI 搜索、图片生成、代码编写等，使用的关键就是设置准确的 Prompt，确实可以在很大程度上提高生产力~</div>2024-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（1） 💬（2）<div>我用ChatGPT，主要有下面两个场景：
1. 帮娃写作业，例如整理司马迁的生平大事，如何在南宋的时代背景下理解陆游的《示儿》，以前是百度之后自己整理，现在就完全交给LLM直接输出信息了，还能轻松控制答案内容长度。也可以让LLM根据孩子年级情况批量生成口算题，主打一个“省爸妈”。
2. 工作中在很大程度上代替了StackOverflow，各种技术问题抛给ChatGPT，基本都能得到答案，例如怎么设计复杂的正则表达式，编写一些小的功能代码片段，设计测试用例等等。

上周还用ChatGPT美化了一下简历，效果特别好！</div>2024-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（1）<div>“在 AI 领域中，一个模型能力强弱很大程度上取决于其训练数据量的多寡。大语言模型的“大”主要是指数据量大。”

我一开始理解大模型的“大”是指这些模型的神经网络参数很大，动不动就是几十B起步。现在看来，“大” 包含训练数据，模型参数，计算资源等。</div>2024-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/eb/364735a6.jpg" width="30px"><span>LPY</span> 👍（1） 💬（1）<div>大模型在2B应用上可能有哪些场景呢？提高企业效率方面，目前好像应用是自动生成代码、自动回答企业内部知识</div>2024-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8b/94/09dca97d.jpg" width="30px"><span>故事与酒</span> 👍（0） 💬（1）<div>我觉得可以把AI当人看 这样很多问题就都能理解了</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（0） 💬（1）<div>ChatGPT成功在于聊天形式与GPT模型表现。
LLM是AI应用开发核心，特点为模型、语言能力和数据量大。
GPT特点：知识丰富、知人晓事、知错就改、知法守法。
GPT能回答各类问题，提供个性化回答和方案。
GPT能理解上下文，提供个性化回答，适应不同对象和环境。
GPT能“知错就改”，重新分析处理问题。
GPT遵守道德法律，不回应危险、不道德或违法内容。</div>2024-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/ab/6fab2492.jpg" width="30px"><span>2018</span> 👍（0） 💬（1）<div>平时经常用一些AI辅助编程，问一些遇到的难题，早期会有一些回答不到位或者乱写代码的情况，后续就越来越精准了，及时纠错和学习能力确实是不错，希望可以通过这个课程把AI更好的融入生活和工作</div>2024-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（0） 💬（1）<div>大模型第一性原理:把AI当人看</div>2024-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/c8/1ccbb110.jpg" width="30px"><span>淡漠尘花划忧伤</span> 👍（0） 💬（0）<div>用户视角介绍大模型的基本概念和特性</div>2025-02-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erD8CwHKGGIia1HwRBxy5GxMLTfGGzOeLjrmZ6ich9Ng7bbPia89iaSibbldnV4uiaKNXFcO2vQ3ztibCrDw/132" width="30px"><span>Williamleelol</span> 👍（0） 💬（0）<div>写文档、写代码、替代搜索引擎</div>2025-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/1e/4a93ebb5.jpg" width="30px"><span>Aaron Liu</span> 👍（0） 💬（0）<div>不错不错，ai聊天，解决问题更快</div>2025-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/75/9f80409f.jpg" width="30px"><span>追梦</span> 👍（0） 💬（0）<div>1、知识检索，就通用知识而言，比百度、谷歌更为简洁、准确，且目前还没有广告的干扰；2、文案创作，完成相对开放、发散性的工作；3、专业知识，通常还只能做参考，需要自身进一步完善</div>2025-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/6d/13/a44d9888.jpg" width="30px"><span>五花肉</span> 👍（0） 💬（0）<div>从用户视角看看LLM是用在哪些方面：
1. 文字内容总结，帮忙生成小短文、年终总结等，优化文字；
2. 图片内容识别，开放考试截图问AI，准确率就是只能通过考试；
3. 工作，看看bug返回的信息等；
4. 有帮助优化论文、制作PPT等内容；

在想怎么才算用好了ai呢，怎么才能成为ai的高级用户</div>2024-12-26</li><br/>
</ul>