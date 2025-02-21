你好，我是尹会生。

你在办公中，一定遇到过需要数据持久化的问题。数据持久化，简单来说，就是当你关闭程序的时候，数据依然可以完整地保存在电脑中。你可能会想到用文本文件、Excel来存储这些数据，文本呢，没有办法按列读写数据，Excel呢，支持的默认API无法进行复杂查询。所以我今天要给你介绍一个功能强大，但编写代码又简单的数据库SQLite。

你可以用SQLite存储结构化的数据，把程序的处理结果保存到电脑中，便于下次或使用新的程序对这些数据进行访问。

用SQLite存储结构化的数据，包括增删改查这些操作。所以今天这节课，我就教你怎么来使用函数封装SQL语句，实现数据的读取和写入，下一节课我们再来学习如何通过类实现复杂的SQL语句的封装，以及如何更新和删除数据。

在讲解这些之前，考虑到SQLite在持久化数据存储的重要性，我想要先给你介绍SQLite的优势。

## 使用SQLite代替文本和Excel有哪些优势

也许你对SQLite这个名字还很陌生，但其实你早就在手机、智能电视、机顶盒等电子设备中用到过它了，比如手机上的通讯录，就是使用SQLite存储联系人的。

SQLite中存储的内容是结构化数据，像是通讯录、企业ERP数据、财务数据等这些存储和排列很有规律的数据，就被称作结构化数据。类似Excel的格式一样，分为“行”和“列”。以存储通讯录为例，每一列会提前指定好哪一列存放姓名、哪那一列存放电话号码，而每一行就是一个联系人的姓名和电话的具体记录。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（2） 💬（1）<div>思考题：使用fetchone()函数将返回第一条查询结果，使用fetchmany()函数返回多条查询结果，使用fetchall()函数返回所有查询结果。</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/21/9a/a40452c8.jpg" width="30px"><span>FILWY</span> 👍（0） 💬（1）<div>老师，excel的分类汇总功能有办法通过python实现吗，找了好久都没找到，网上找到的都是分类汇总到一张新的表，跟原生excel操作分类汇总产生的结果不一样</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/0f/09/e5221743.jpg" width="30px"><span>David</span> 👍（1） 💬（0）<div>干货满满！连SQL语句也讲到了，也让我明白了想提升IT技能是必须要打牢基础，再学东西才会融会贯通。期待老师的python训练营。</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-18</li><br/>
</ul>