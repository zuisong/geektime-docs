你好，我是邢云阳。

我上大学时有一位老师，他与各行各业的人都能比较专业的聊上几句，且还能推荐出相关的书籍。他曾给我们讲过，如何快速地进入一个行业领域，第一步就是先掌握这个领域的一些名词的含义。

因此我在第一节课，给你介绍了 Function Calling，在第二节课介绍了 Agent。在本节课，我将介绍 CoT、ReAct 等等这些常常在 AI 相关的场合听到的名词。在学完这三节课后，你就已经掌握了 AI Agent 理论的精髓，后续会开启实战。

## CoT（Chain of Thoughts）

CoT 中文名称是思维链。最早是来自于人类向大模型提问时，无意中发现，如果加上一句 “Let’s think step by step”，大模型回答的效果就会有大幅增强。我们用 Kimi 大模型去测试一下。

首先不使用思维链：

![图片](https://static001.geekbang.org/resource/image/ea/3b/eae7c1cb2037d92878b13155dbffa23b.png?wh=1252x469)

使用思维链：

![图片](https://static001.geekbang.org/resource/image/b9/17/b9167eaa8ab47f32a967f101c0bc7717.png?wh=1186x538)

可以看到虽然使用和不使用思维链，这道题都算对了，但是，在用了思维链后，大模型把任务做了拆分并展示了每一步思考的过程。如果是一个复杂任务，或者我们想知道某个问题的具体解决步骤，那显然使用思维链效果会更好。

这其实就是让大模型不要着急回答问题，而是先推理拆解问题，然后再回答，这样一句简单的 prompt 就让大模型有了推理能力。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/73/ce/23bd3997.jpg" width="30px"><span>Wiggins</span> 👍（5） 💬（2）<div>ReWOO 中如果大模型能一次性的把所有步骤都告诉人类，人类把每个步骤对应的工具调用结果一次性返回给大模型，不就可以只提问一次就解决问题了吗？

这段其实不是很明白，老师可以帮忙举个例子么</div>2024-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/a3/4bcf1b59.jpg" width="30px"><span>大宽</span> 👍（0） 💬（1）<div>那么你认为，大模型能通过训练具备 ReAct 等更高级的思想吗？
应该不能吧，React这种需要针对每次对话给出人类反馈再调整，大模型不能通过事先的知识学习到</div>2025-02-12</li><br/>
</ul>