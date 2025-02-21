你好，我是郑晔。

程序员是一个追求效率的群体，我们的日常工作就是为别人打造提升效率的工具，自然而然的，我们也会不断要求自己**优化自身工作效率**。《10x 程序员工作法》这个专栏，谈的就是程序员应该如何从方方面面努力提升自己的工作效率。但工作效率这件事在 ChatGPT 诞生之后，就需要重新讨论一下了。

ChatGPT 本身并不是一个为程序员准备的工具，但当 ChatGPT 破圈后，所有人都开始重新思考如何利用 AI 技术提升自己的工作效率，程序员当然也不例外。这里我加餐一篇，讨论一下程序员在提升效率这条路上是怎么一路走过来的。

## 从命令行开始

程序员在工作效率上的优化是从命令行开始的。最初，命令行是为了方便用户与操作系统进行交互，完成一些简单的任务。但程序员很快就发现，命令行也可以很好地提升工作效率。

举个例子，假设一个程序员需要从一个巨大的日志文件中提取出某些信息，并将其转化为 CSV 格式的文件，以便进一步进行分析。如果使用传统的文本编辑器完成这个任务，不仅效率低下，还很容易出错。但如果使用命令行工具，就可以轻松地完成这个任务。比如，我们使用下面这条命令。

```shell
grep "error" log.txt | awk -F ':' '{print $1 "," $3}' > output.csv
```
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（5） 💬（0）<div>拥抱 AI 时代，不断提升自己的工作效率。
--记下来
加油，奥利给!</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/4f/72ae1dc9.jpg" width="30px"><span>宏鬼</span> 👍（4） 💬（0）<div>居然还有更新，真是超值！
最近也在学习AIGC相关的东西，比较认同一句话：
AI替代不了人类，但将淘汰不会使用AI的人。</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（3） 💬（0）<div>他（郑老师）他（郑老师）他（郑老师）又双叒叕更新了！！
也在用github copilot，但是发现他对于涉及到跨多类的代码编写，还是有点吃力，比如有时候其他类的属性字段赋值，他就是不全。</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f6/4d/62105649.jpg" width="30px"><span>花落星移</span> 👍（1） 💬（2）<div>紧跟时代潮流，点赞
gpt现在我主要拿来做以下事项：
1）写sql
2）画plantuml格式的时序图
3）程序变量取名
</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（0） 💬（0）<div>把它当作一个结对编程的人</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/10/365ea684.jpg" width="30px"><span>聪明的傻孩子</span> 👍（0） 💬（0）<div>居然还有更新，惊喜；个人觉得未来AI会带来更高的效率提升</div>2023-06-12</li><br/>
</ul>