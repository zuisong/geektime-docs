Cassandra是大数据时代中非常具有影响力的一个开源项目，DataStax则是背后支持开源Cassandra并将其商业化的公司。今天我们就来聊一下Cassandra和Datatax的故事。

我们都知道，在大数据发展历史上，谷歌的“三驾马车”：谷歌文件系统、 MapReduce、 BigTable。三者都曾经扮演了非常重要的角色，Hadoop开源生态圈里也有对应的Hadoop文件系统，Hadoop MapReduce和HBase。

但是在大数据发展史上，还有一篇影响力几乎等同于谷歌“三驾马车”的论文。它讲的就是亚马逊发布的Dynamo系统。

2008年，Dynamo系统的作者之一阿维纳什·拉克希曼（Avinash Lakshman），跳槽去了Facebook。跳槽的阿维纳（Avinash）和Facebook网站的另外一个工程师普拉桑特·马利克（Prashant Malik），一起开发了Cassandra，一个Dynamo的开源山寨版。

Cassandra开发出来之后很快就被开源了。早期Facebook对于开源这件事还是非常支持的，但是它开源的Cassandra很快就受到了一次重大的打击，这个打击可以说是十分致命的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/3a/abb7bfe3.jpg" width="30px"><span>尹徐</span> 👍（0） 💬（2）<div>飞总能不能介绍下Cassandra目前的发展，国内饿了么和360虽然也在用，更多的拥趸都迈向Mongo了，那么国外怎么样</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/a6/dcd67a78.jpg" width="30px"><span>阿卡斯</span> 👍（3） 💬（0）<div>那篇2012年论文链接能粘贴出来么？</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/0e/abb7bfe3.jpg" width="30px"><span>xiaoc10</span> 👍（1） 💬（0）<div>这些Casandra系统拥有的弊端，是否也适用于dynamo? amazon是怎么解决的呢</div>2018-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/96/c735ad6b.jpg" width="30px"><span>滩涂曳尾</span> 👍（0） 💬（0）<div>Amazon: Dynamo

 --Avinash跳槽--&gt; 

Facebook: 开启Cassandra，后抛弃之，选择HBase

--&gt;

DataStax:
1. 接手并持续贡献Cassandra，使之成为Apache顶级开源项目；
2. 以Cassandra为核心整合诸多开源项目的主打产品DataStax Enterprise</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（0） 💬（0）<div>听故事，长见识</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/21/00600713.jpg" width="30px"><span>小侠</span> 👍（0） 💬（0）<div>无法保持一致性的问题现在还存在吗？</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/31/14f00b1c.jpg" width="30px"><span>燃</span> 👍（0） 💬（0）<div>datastax  enterprise要花钱买的吗？</div>2018-06-29</li><br/>
</ul>