你好，我是Barry。

上节课，我们全面认识了数据库，对数据库的基本概念和操作都有了大致了解。不过虽然我们完成了数据库应用的准备阶段，但是还没有把数据库应用在我们的项目里。

这节课，我们继续深入学习数据库应用，熟悉SQL语言应用，并实现数据库与项目的联动。即使你之前没接触过SQL也没关系，只要你跟住我的节奏，就能更高效地掌握数据库的应用技巧。

## 数据库表的建立

我们都知道，在项目中需要通过编程语言来操作数据库，实现项目中的增、删、改、查等一系列功能。而操作数据库时最常用的就是SQL语言，所以熟练应用SQL是我们操作数据库时必备的一项技能。

在Flask中使用MySQL时，其实你不需要直接编写SQL语句来操作数据库。我们还可以通过ORM框架实现，它的作用是将面向对象编程语言（如Java、Python等）与关系型数据库（如MySQL、Oracle等）进行交互。

## 认识ORM

ORM本身就是一种编程技术，全称是“对象关系映射”。通俗地说，你可以把ORM看成一种“翻译”技术，它能把数据库中的数据转换成程序中的对象，这样我们就可以像操作对象一样来操作数据库，而不用写一堆复杂的SQL语句了。

实现的过程一般借助Flask中的SQLAlchemy扩展，SQLAlchemy是一个Python编程语言下的SQL工具包和ORM库，提供了SQL表达式操作和ORM映射操作的工具。借助这个工具，我们无需掌握SQL语句，即可实现数据库操作。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（1） 💬（1）<div>在项目开发中，不会对用户的信息直接从库中删除，而是通过一些字段标识进行软删除，比如国内一些应用注销账号的时候，会有一个确认期（半个月），如果在确认期内撤回注销账号，就可以很快的恢复数据；还可以对用户流失的分析提供数据支持</div>2023-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ae/f5/a17bbcc9.jpg" width="30px"><span>蜡笔小新爱看书</span> 👍（0） 💬（1）<div>db.Model的db怎么实例化的？完整代码能给一下吗，还有文件的命名，最好也给出一下</div>2023-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>你好，老师，这个是会自动建表，还是需要手动建表，然后再写ORM对象</div>2023-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（0） 💬（1）<div>现在都是逻辑删除，多增加一个已删除字段，默认为0，比如删除了就设置为1，这样也能保留原始信息，给用户也好给公司分析也好</div>2023-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>Q1：python是动态语言，是弱类型语言，对吗？
Q2：老师公司的视频网站，用什么推荐算法？</div>2023-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a3/45/8e9c6a69.jpg" width="30px"><span>因为有你心存感激</span> 👍（0） 💬（0）<div>创建的模型，怎么变成数据库中的表呀？</div>2024-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/20/9c/d49c2940.jpg" width="30px"><span>Sasori</span> 👍（0） 💬（1）<div>一般开发项目的过程中是用这种orm方式调用数据库还是直接写sql 哪种办法多呀</div>2024-10-30</li><br/>
</ul>