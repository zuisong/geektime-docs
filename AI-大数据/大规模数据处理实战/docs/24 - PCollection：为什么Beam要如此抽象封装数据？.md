你好，我是蔡元楠。

今天我要与你分享的主题是“为什么Beam要如此抽象封装数据”。

很多人在刚开始接触Apache Beam的时候，都会觉得这里面的概念太抽象了。什么PCollection、PValue、Transform……这都是些什么？尤其是PCollection，完全和先前的技术知识找不到对应。

确实如此。同样作为数据的容器，PCollection却并不像Python/Java的List或者C++的vector。PCollection是无序的，Beam对于PCollection中元素的处理顺序不作任何保证。所以，你不可能说“我想处理PCollection中的第二个元素”，因为它就没有“第几个”这种概念。

PCollection也不像Python/Java的Set，或者C++的unordered\_set，PCollection不一定有固定的边界。所以，你也不能指望去查找一个PCollection的大小。在PCollection的世界里，也没有“固定大小”这样的概念。

作为程序员，我很讨厌重复造轮子，尤其是新瓶装旧酒。的确，有很多开发者为了体现自己项目的复杂度，故意强行引进了很多概念，让大家都似懂非懂的。这就像是为了体现自己知道茴香豆的“茴”有几种写法一样，故意用另一种写法来体现自己“有文化”。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/99/cc30e2ca.jpg" width="30px"><span>人唯优</span> 👍（8） 💬（1）<div>Beam的register机制是否和spark里面的kryo register是一样的概念？Beam为何不提前为基本类型注册好coder或者使用默认的java序列化反序列化机制？就像spark里面的java和kryo.register一样。这样读取基本的常见数据源比如mysql的表就不用单独注册了吧，不然不是有很多重复工作？</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/b6/3d8fcc2c.jpg" width="30px"><span>张凯江</span> 👍（6） 💬（0）<div>感觉跟rdd差不多。
一个天生设计成有界
一个天生设计成无界</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/b6/3d8fcc2c.jpg" width="30px"><span>张凯江</span> 👍（0） 💬（0）<div>参数是匿名内部类，而不是简单的操作。  匿名内部类可以应用外层或其它pc吧</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/07/38/d8c78f1b.jpg" width="30px"><span>胡墨</span> 👍（0） 💬（0）<div>请问后半部分的例子是否可以有Python实现呢？生物背景对Java一窍不通...</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（0） 💬（0）<div>请问PCollection和RDD的相同点和不同点都有哪些呢？</div>2019-06-17</li><br/>
</ul>