你好，我是黄鸿波。

上节课，我们主要了解了数据库的来源和形式，但凡是数据都离不开存储。说到数据库，我们最常用到的就是MongoDB和Redis。

推荐系统中的原始数据一般分成两大类，用户数据和内容数据。这两类数据服务于推荐算法，最终我们会得到用户特征与画像。对于用户画像这类的信息，最好使用字段可变的文档型数据库，比较常见的就是MongoDB数据库。

这节课我们就来详细地介绍一下MongoDB数据库。看看它是什么、有什么特点、应该如何安装。

## 什么是MongoDB数据库？

MongoDB是一个开源的基于分布式文件存储的数据库（C++语言编写），最初是为Web应用提供可扩展的高性能数据存储解决方案。MongoDB最大的优点是可扩展性强、高效的查询方式和非常出色的安全性。

![](https://static001.geekbang.org/resource/image/ec/52/ec37cf94b227833379c7152f71ce2d52.png?wh=2000x600)

### MongoDB数据库的特性

由于MongoDB开源且分布式，因此，它在可扩展性方面一直是所有NoSQL数据库中的佼佼者。MongoDB数据库可以通过分片数据来提高整个数据库的吞吐量，并且由于它以文档结构来存储数据，所以在编写和使用查询语句时非常容易。

我们这里所说的文档结构，是一种类似于JSON类型的BSON文档。在实际使用过程中，我们可以把它当作JSON的形式使用，因为这二者从使用和长相上来看基本没有区别，而我们在日常开发中也比较喜欢使用JSON对象作为传输格式，因此，MongoDB数据库与程序的对接就变得容易多了。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/69/7b/62c46d44.jpg" width="30px"><span>👂🏻阿难👂🏻</span> 👍（11） 💬（6）<div>能不能提个建议，比如这节课，讲了一个工具的安装和一个使用demo，这个内容个人感觉很单薄，其实网上搜索一下就有很多教程，作为学员其实希望了解更多的是：1当前用户在推荐系统中都会和其他模块如何交互，它在推荐架构中的作用是什么？
2为什么选用了mgdb而不是其他的db？有哪些考虑？ 
3 实际推荐系统中，和当前技术有关的技术“坑”有哪些？老师啥如何解决的。
能围绕以上问题做教学对于学习者来说才有真正的价值。 谢谢</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/60/ecdb8ff9.jpg" width="30px"><span>云中君</span> 👍（3） 💬（1）<div>mongo安装与使用，放一个链接就可以…建议以后的安装与使用不用重点讲，多讲点推荐核心点</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/5f/25942dfb.jpg" width="30px"><span>地铁林黛玉</span> 👍（2） 💬（1）<div>我感觉这节可以直接略过，docker直接一键安装即可。</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（0） 💬（3）<div>我想知道为什么选用MongoDB? 而不是其他NoSQL数据库</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>老师这节课真的很详细，一步一步，每一步都很详细，对于基础薄弱的同学尤其有用，必须赞一个！
另外，请教几个问题：
Q1：讲“Field”部分时，有一句话“在 Document 中嵌套 Document 等，因此，它的 Field 类型更加灵活”。应该是Field嵌套，不是Document嵌套吧，也许是笔误。
Q2：MongoDB是分布式，多个节点会有一个中心节点吗？
Q3：MongoDB的可扩展性，体现在哪里？是体现在“列”可以任意扩展吗？还是体现在分布式应用时可以任意增加节点？</div>2023-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（0）<div>为什么选用了MongoDB而不是其他的db如ES？有哪些考虑？ 能否列一个表格做一个对比？做对比后感觉整篇文章就更好了。</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/5f/25942dfb.jpg" width="30px"><span>地铁林黛玉</span> 👍（0） 💬（0）<div>这是我的docker安装mongo的命令；
docker run -v &#47;Users&#47;apple&#47;data&#47;mongo&#47;data:&#47;data&#47;db -v &#47;Users&#47;apple&#47;data&#47;mongo&#47;backup:&#47;data&#47;backup -v &#47;Users&#47;apple&#47;data&#47;mongo&#47;conf:&#47;data&#47;configdb --name mongod -p 27017:27017 -d mongo --auth
创建用户：
db.createUser({user: &#39;admin&#39;, pwd: &#39;123456&#39;, roles: [ {role: &#39;userAdminAnyDa&#39;} ]}) db.createUser({user: &#39;admin&#39;, pwd: &#39;123456&#39;, roles: [ {role: &#39;userAdminAnyDat&#39;} ]})db.createUser({user: &#39;admin&#39;, pwd: &#39;123456&#39;, roles: [ {role: &#39;userAdminAnyData&#39;} ]}db.createUser({user: &#39;admin&#39;, pwd: &#39;123456&#39;, roles: [ {role: &#39;userAdminAnyDat&#39;} ]})db.createUser({user: &#39;admin&#39;, pwd: &#39;123456&#39;, roles: [ {role: &#39;userAdminAnyDa&#39;} ]}) &#39;} ]})
+++++++
db.createUser({ user:&#39;admin&#39;,pwd:&#39;123456&#39;,roles:[ { role:&#39;userAdminAnyDatabase&#39;, db: &#39;admin&#39;},&quot;readWriteAnyDatabase&quot;]});
+++++++
db.auth(&#39;admin&#39;, &#39;123456&#39;)</div>2023-05-04</li><br/>
</ul>