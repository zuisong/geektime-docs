在认识DBMS篇中，我们讲解了Excel+SQL、WebSQL、SQLite以及Redis的使用，这些DBMS有自己适用的领域，我们可以根据需求选择适合的DBMS。我总结了一些大家常见的问题，希望能对你有所帮助。

## 关于Excel+SQL

### 答疑1：关于mysql-for-excel的安装

Excel是我们常用的办公软件，使用SQL做数据分析的同学也可以使用Excel+SQL作为报表工具，通过它们提取一些指定条件的数据，形成数据透视表或者数据透视图。

但是有同学在安装mysql-for-excel-1.3.8.msi 时报错，这里感谢**同学莫弹弹**给出了解答。解决这个问题的办法是在安装时需要Visual Studio 2010 Tools for Office Runtime 才能运行。

它的下载链接在这里： [https://www.microsoft.com/zh-CN/download/confirmation.aspx?id=56961](https://www.microsoft.com/zh-CN/download/confirmation.aspx?id=56961)

## 关于WebSQL

我在讲解WebSQL操作本地存储时，可以使用浏览器中的Clear Storage功能。有同学问到：这里只能用户手动删除才可以吗？

事实上，除了在浏览器里手动删除以外，我们完全可以通过程序来控制本地的SQLite。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/65/68bd8177.jpg" width="30px"><span>雪飞鸿</span> 👍（4） 💬（1）<div>根据业务来预判哪些数据是热数据，可提前写入redis。后续再根据访问频次（如，用有序集合记录访问次数）动态调整redis中缓存的数据。网上许多讨论热点Key的文章，所谈讨的情况还是比较复杂的。</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（3） 💬（1）<div>通过redis 的得分来进行存储热点数据</div>2019-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（1） 💬（1）<div>有些复杂的sql语句，如何转换成对应的sqlalchemy语句，有什么好的工具和方法吗</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（1） 💬（1）<div>老师，你好，用redis做缓存，那么如何保证与MySQL数据库数据一致呢，先存redis和先存mysql都会有问题</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（5） 💬（1）<div>1、这里，排行榜中如果要显示用户名称，需要放到有序集合中，这样就不需要再通过 MySQL 查询一次。这种需要实时排名计算的，通过 Redis 解决更适合。
----老师，这里不明白，有序集合里面不是已经存放了userId，如何再存放userName

2、第二个问题是，我们使用 Redis 作为 MySQL 的缓存，假设 MySQL 存储了 1000 万的数据，Redis 只保存有限的数据，比如 10 万数据量，如何保证 Redis 存储的数据都是热点数据呢？
----把查询到的数据保存一份到redis，使用有序集合，每次如果从redis获取到，则score+1，超过10w条数据，则删除。（好像也有问题）</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9b/d0/86aee34c.jpg" width="30px"><span>刘凯</span> 👍（1） 💬（0）<div>原来如此</div>2020-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJSYNNABBxXCme5FMGUYTPbvnT6IvpzPP3qiaSibZficAfabydnwWOV6LlQ4lAtF0aeN3ficv0S3iavmxQ/132" width="30px"><span>wumin</span> 👍（1） 💬（0）<div>我生成词云的时候报这个错误。内存是20G的
Traceback (most recent call last):
  File &quot;d:&#47;scripts&#47;python&#47;Python-mysql&#47;python-sqlite-weixin.py&quot;, line 61, in &lt;module&gt;
    content = get_content_from_weixin()
  File &quot;d:&#47;scripts&#47;python&#47;Python-mysql&#47;python-sqlite-weixin.py&quot;, line 53, in get_content_from_weixin
    content = content + str(temp)
MemoryError</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f7/9c/69c5c5dc.jpg" width="30px"><span>越锋利</span> 👍（0） 💬（0）<div>如何保证热点数据？需要页面置换算法，比如 LRU 或者 LFU。</div>2021-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ic8KF0sfxicsx4F25HZrtZwP2fQEibicfibFeYIQBibxnVlHIiaqkfictJuvLCKia0p7liaQvbTzCYWLibjJK6B8kc8e194ng/132" width="30px"><span>爱思考的仙人球</span> 👍（0） 💬（1）<div>热点数据就是访问率高的那些数据吧，我有一个笨方法，就是增加一个热点数据表，首先记录所有1000万数据的id，访问次数默认为0，然后每访问一次，次数+1，倒序排名，取前10万条。</div>2019-10-28</li><br/>
</ul>