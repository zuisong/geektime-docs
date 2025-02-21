你好，我是徐昊，欢迎你和我一起学习AI时代的软件工程。

随着2022年底大语言模型（Large Language Model）进入技术爆炸期，LLM也对软件研发产生了巨大的冲击。无论是使用ChatGPT直接从头生成应用，还是在Github Copilot辅助下在已有代码库中编码，每一次与LLM有关的新闻都刺激着从业人士的神经，好像过不了几天，工作就会被AI取代了。

## 通过ChatGPT编写生产代码

然而实际使用起来，是怎样的呢？让我们看一个例子，如果要做一个产品目录的服务（Product Catalog），通过API的调用返回产品信息。这是一个非常简单的RESTful API服务。大多数人可能会想到通过下面的提示词（Prompt），让ChatGPT帮助我们编写代码：

```plain
目前我们在编写一个产品目录服务，通过API提供所有可售商品的详细信息，使用Java编写。
请提供代码和对应的功能测试。
```

在这个提示词中，我们简要地描述了需求。因为ChatGPT的回答并不是确定的，以下是我得到的结果：

![](https://static001.geekbang.org/resource/image/d3/28/d30fd6113204707983cbec9e95378828.jpg?wh=1683x6638)

比起可以使用的生产代码，这更像一份在给定上下文（产品目录）下的Spring Boot教程。离生产代码还有很大差距。我们需要在现有结果的基础上给予ChatGPT反馈，让ChatGPT做出调整。比如，告诉ChatGPT这个API不允许修改或增加目录中的产品，并要求ChatGPT补充其他功能测试。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e8/c9/59bcd490.jpg" width="30px"><span>听水的湖</span> 👍（0） 💬（0）<div>购买专栏后，请添加小助手微信号：geektime004，回复「徐昊」，立即进入专栏交流群，以免错过直播通知信息。
课程意见收集链接（用户反馈将作为直播查看）：https:&#47;&#47;jinshuju.net&#47;f&#47;YzTEQa

</div>2024-04-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/VSylTssVXGVH10P32wfThTploZBuG9meyufz7wyVNUvmsFgMoEZlQl5lx7Ge5hhR5wSPloRy8GZAhEc4yD9fbA/132" width="30px"><span>JJPeng</span> 👍（4） 💬（1）<div>请问老师，那10％的技能是哪方面的技能呢？我们该如何习得这部分技能呢？</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a8/22/09c4211e.jpg" width="30px"><span>水木</span> 👍（3） 💬（4）<div>在3月9日央视的《对话》·开年说节目上，百度创始人、董事长兼CEO李彦宏表示，以后不会存在“程序员”这种职业了，因为只要会说话，人人都会具备程序员的能力。“未来的编程语言只会剩下两种，一种叫做英文，一种叫做中文。”</div>2024-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（1） 💬（1）<div>看完老师关于软件开发核心的论述,重新审视自己的开发构建过程,确实是有大量的时间是花在获取和学习知识这个过程上.
知识管理与编码相比是一项更加通用的技能,习得此技貌似可以向更多方向上转型.</div>2024-03-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIRLM0nibsyQdl0y5cl8ntdVzgxQWlqjHniaicjNwuDqiaicXUbLNGhRcg8QOF5wPJziadeQXu2MzhyVK1A/132" width="30px"><span>Geek_d19870</span> 👍（1） 💬（2）<div>对个人而言，还是需要有一种甄别能力，甄别LLM编写的代码是否高效、可用</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/f1/01/0b0d8a5f.jpg" width="30px"><span>小林</span> 👍（0） 💬（1）<div>如果代码编写真的可以由GPT替代，是否意味着每个人都可以构建属于自己的软件，毕竟业务方更清晰的理解自己想要什么，而不是跟研发团队对接，业务方直接告诉GPT自己的想法，生成软件，运行即可。目前微软的AutoDev是否有这方面的想法？
    同时，需要一个大型软件的场景其实很少，大多数只是需要解决一个不大的问题而已。</div>2024-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7c/25/70134099.jpg" width="30px"><span>许凯</span> 👍（0） 💬（2）<div>真心期待，一直在数字化、网络化、智能化的方向上裸奔，希望可以在智能化方面有所提升，成为今年年会ppt上的一个亮点</div>2024-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（16） 💬（1）<div>看完第一感觉：不用担心失业了
第二感觉：要用 AI 开挂了「传奇程序员 Kent Beck 所言，LLM 让我 90% 的技能无用了，却让 10% 的技能放大了 1000 倍」</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（6） 💬（2）<div>🤔☕️🤔☕️🤔
【R】提示词中，要提供丰富的上下文信息 = 业务上下文 + 业务功能描述 + 技术规范 + 最佳实践 + 技术栈 + 代码范围 + 交付物要求 + …
【.I.】跟ChatGPT聊天，最尴尬的事情，不是对方输出不是我所想要的，而是三轮问下来，答案我没得到，却把自己给问穷了，再也想不出问题，能够把这个对话给继续，如此尴尬之下，缓解的方式，居然是说它不行，而不是自己不灵。回头想来，尬问之后的惶恐，只有自己知道有多忐忑。这就好像，屏幕后面可能是苏格拉底、阿奎那、伽利略、牛顿、欧拉、高斯、图灵、爱因斯坦、冯诺依曼，屏幕后面的模型里携带者人类全部精英的智慧，而我，却只能跟他们聊，今天的天气怎样，不把天聊死才怪。
【R】软件是载体，其中包含的知识，才是真正的产品；软件开发的核心，是知识的获取与学习，并通过软件的代码表达出来。
知识工程（Knowledge Engineering），更准确表示用LLM来改造软件工程，提取组织知识给LLM，再通过LLM将知识表达为软件的代码，从自己掌握知识、自己编码，改变为掌握知识、表达给LLM去做编码工作。
【Q】敲代码，软件开发的典型样子，不敲代码，总有点缺少软件开发的自信感。这样的刻板印象来自哪里？
    — by 术子米德@2024年3月11日
</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/86/73/5190bbde.jpg" width="30px"><span>苏果果</span> 👍（4） 💬（0）<div>缓解焦虑的好课👍</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（3） 💬（1）<div>资料补充：

写代码在软件开发中只占很小的比例，甚至还不是最困难的根本复杂度：https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;399057

90% of My Skills Are Now Worth $0 - by Kent Beck： https:&#47;&#47;tidyfirst.substack.com&#47;p&#47;90-of-my-skills-are-now-worth-0


现场管理：https:&#47;&#47;wiki.mbalib.com&#47;wiki&#47;%E7%8E%B0%E5%9C%BA%E7%AE%A1%E7%90%86</div>2024-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（2） 💬（3）<div>我注意到，老师用了不同的词汇，不知道是否是故意区分的？

老师一开始说：
“最有价值的部分：获取、学习并传递知识。”

然后说：
“提取知识、组织知识为 LLM 更易于理解的形式。”


所以，想问下老师，“获取知识”和“提取知识”是一样的嘛？“传递知识”和“组织知识”是一样的嘛？如果不一样，这之间的联系是什么呢？

我自己的想法是：
1、提取是获取的细化，组织是传递的细化。
2、为什么要细化？为了更好的用LLM。</div>2024-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/3e/7f3a9c2b.jpg" width="30px"><span>Jaising</span> 👍（1） 💬（1）<div>特别喜欢 8x 强调的软件工程的核心是知识工程。对于掌握大量业务知识的需求人员和掌握大量技术积累的工程师而言，AI 加持下前者更具优势，因为软件落地成本得到极大降低。对工程师而言，生产力革命大幅提升生产力也会大量替代陈旧生产资料。

就像每个人都可以讲 5 分钟脱口秀一样，AI 时代每个人都可以拥有属于自己的软件产品。</div>2024-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/de/cf/ef2e0501.jpg" width="30px"><span>奇小易</span> 👍（1） 💬（0）<div>收获：作为软件工程师不能只停留在编码环节，也不要被 LLM 的出现搞得自己没有未来了一样。实际情况是我们需要将关注点放到更有价值的地方，因为知识本身是为了解释世界、解决问题，软件是知识的载体，那么他们的目的都是一样，有了 LLM 之后，软件工程师能够有更多的精力去改造世界🥳。</div>2024-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（1） 💬（0）<div>知识工程，期待刷新认知！</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/c3/d1/1540d0ca.jpg" width="30px"><span>雪花神剑</span> 👍（0） 💬（0）<div>软件不是产品，只是载体。做好的产品，产品开发涉及太多创造性的活动。绝不是写好代码那么简单。</div>2024-12-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7yVSTIKIQnA5gHpG1G1gVAyWicnwia43rhMbPiaadwNlP70uHMLwQ2fv43t5SnwBtOD5k7zZRegI2Q/132" width="30px"><span>Geek_huan</span> 👍（0） 💬（0）<div>请问什么是现场管理框架 ？和我们这个课程讨论的如何结合起来理解？</div>2024-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c5/e6/50c5b805.jpg" width="30px"><span>欠债太多</span> 👍（0） 💬（0）<div> 众所周知的原因，我们平时怎么才能用到ChatGPT4呢？</div>2024-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/7c/25abe455.jpg" width="30px"><span>stars</span> 👍（0） 💬（0）<div>就是怕失业，赶紧冲一下电。</div>2024-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（0） 💬（0）<div>看了例子，还是觉得只有业务上下文以及功能描述是需要人描述的，其他都可以作为固定模板呈现。</div>2024-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/6e/efb76357.jpg" width="30px"><span>一只豆</span> 👍（0） 💬（0）<div>之前的“数字化”好像是技术未成熟阶段的种种费劲的努力，包括“软件是知识的封装”这类精彩观点。 现在 LLM 来了，“数字化”和“知识经济”的真正春天才到了～～ 
从图灵机到此刻，好像那些都是前戏。。。感谢徐昊老师带来产业高潮中的认知高潮 ：）</div>2024-03-12</li><br/>
</ul>