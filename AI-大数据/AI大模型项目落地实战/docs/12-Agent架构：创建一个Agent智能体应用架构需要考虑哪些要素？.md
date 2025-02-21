你好，我是金伟。

如果你已经跟着开发了整个Agent底层框架，那对Agent这个领域应该已经有非常深入的了解。不过做为一个知其然，还要知其所以然的工程师，可能还是会产生疑问：为什么说Agent智能体这种开发范式逐渐成为了大模型AI开发的标准呢？

这节课，我会从最简单的例子开始，回归Agent核心原理，一步步拆解Agent智能体的能力，确保任何业务做智能体的时候都有思路参考。

我们将始终围绕一组核心概念展开，也就是Agent智能体四要素：**感知**、**决策**、**规划**、**执行**。

![图片](https://static001.geekbang.org/resource/image/3a/63/3afb9e9ecef886b675e57d4ee9890b63.png?wh=1920x409)

## 重新理解智能体

Agent智能体这个概念并没有统一的标准，而Agent这个词在AI领域就是智能体的意思。接下来我说的智能体概念是我在实战中理解到的。

### 提示词也是智能体？

从最简单的情况来说，大模型+提示词就是一个智能体，举个例子。

```plain
你是一名C语言老师，你负责学生C语言答疑，当我给你一段有bug的C语言代码的时候，你要帮我解答，告诉我问题在哪里，你清楚了吗。
```

在大模型基础上，仅仅通过一段提示词，就能让大模型成为你的老师，这在以往是不可想象的。这个基于大模型的助教至少可以完成一部分人类老师的工作，就可以称为智能体。

智能体最大的特点就是可以像人类一样独立完成**感知**、**决策**、**规划**、**执行**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（2）<div>大概理一下这个工作流。
1. 首先,用户提出一个问题或要求。
2. 这个问题传给了AI助手。
3. AI助手会思考:&quot;这个问题我能直接回答吗,还是需要更复杂的处理?&quot;
4. 如果问题简单,AI助手就直接回答用户。
5. 如果问题复杂,AI助手会启动一个叫&quot;工作流&quot;的特殊程序来处理。
6. 这个&quot;工作流&quot;程序可以使用很多工具,比如查资料、写代码、上网搜索等,来解决复杂问题。
7. 最后,&quot;工作流&quot;会给出答案,AI助手再把这个答案传达给用户。</div>2024-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>100%的可靠性技术上实现不了吧..</div>2024-09-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJauibzuFRY5E2Pyh24uPsMCTtaDjWmstBR7bIdqYn9dNlibj8vl3NKpR3mjfjLMIgpAU6mhOY2R2mQ/132" width="30px"><span>littleboy</span> 👍（0） 💬（0）<div>老师文章里面的图是哪个软件画的？</div>2025-01-11</li><br/><li><img src="" width="30px"><span>Geek_3b5445</span> 👍（0） 💬（0）<div>还是看场景, 有些场景传统图形化程序员更直接高效交互,大模型的落地机会是满足传统程序不好用的场景.</div>2024-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c5/52/63008fc7.jpg" width="30px"><span>xuwei</span> 👍（0） 💬（0）<div>chain不等于智能体吧，老师这里有特别的含义吗</div>2024-11-13</li><br/>
</ul>