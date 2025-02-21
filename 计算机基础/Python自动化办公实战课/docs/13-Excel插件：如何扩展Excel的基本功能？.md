你好，我是尹会生。

我们在讲了怎么利用Python优化Excel的输入和计算效率之后，相信你已经知道该怎么使用Python的循环和文件库进行多个文件的处理，怎么使用正则表达式对内容进行查找和替换。

但是有时会因为临时的需求，为了得到查询的结果而进行一次性的表格处理，这时候如果用Python来解决，估计你有一种“杀鸡用牛刀”的感觉，未免小题大做了。

所以在接下来的三节课里，我会利用Excel中自带的插件和更简单的两个脚本工具，来完成这种临时的、简单的重复性任务，让你用更便捷的方式实现办公自动化。

今天这节课呢，我就给你介绍一个在Excel中非常著名的Power Query插件，利用这个插件你可以完成我们经常遇到的数据清理工作。

## Power Query的主要用途

我先来介绍一下Power Query这个插件。从它的名字，你应该就能猜到它的主要用途，那就是**在查询方面对Excel进行优化。**

**我所说的**查询优化是泛指，它的涵盖范围比较广。为了方便使用Excel统计数据，往往需要在统计数据前去调整Excel表格的格式、内容以及字段类型，这些在Excel中统称为**查询操作。**

如果能够把新增数据自动更新到已经处理的数据中，还能自动化地按照之前的操作步骤对表格中的数据进行调整，这就是Power Query比手动调整Excel更有效率的地方**。**
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（1） 💬（1）<div>关于思考题，由于我还没有研究透Power Query的用法，所以我用的是比较笨的方法，就是Power Query与Python相结合。先用Power Query将订单日期拆分成年、月、日，然后再用python中的groupby函数分别计算每个月的销售额和每个品种半年的销售额。</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0a/e9/6fad9109.jpg" width="30px"><span>宁静志远</span> 👍（0） 💬（1）<div>尹老师，您好，点击“合并文件到 Excel.rar”，提示网盘链接不存在。</div>2023-07-31</li><br/><li><img src="" width="30px"><span>Geek_818431</span> 👍（0） 💬（0）<div>老师您好 网盘链接不存在  github上也没有这个压缩包</div>2024-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/06/32/3de6a189.jpg" width="30px"><span>范</span> 👍（0） 💬（0）<div>power query适合于一次性的查询操作；python适合于多次的，自动化操作。excel真心功能强大</div>2021-04-14</li><br/>
</ul>