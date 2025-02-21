你好，我是轩脉刃。

一个 Web 应用，有很大部分功能是对数据库中数据的获取和加工。比如一个用户管理系统，我们在业务代码中需要频繁增加用户、删除用户、修改用户等，而用户的数据都存放在数据库中。所以对数据库的增删改查，是做 Web 应用必须实现的功能。而我们的 hade 框架如何更好地支持数据库操作呢？这两节课我们就要讨论这个内容。

## ORM

提到数据库，就不得不提ORM了，有的同学一接触 Web 开发，就上手使用 ORM 了，这里我们要明确一点：ORM 并不等同于数据库操作。

数据库操作，本质上是使用 SQL 语句对数据库发送命令来操作数据。而 ORM 是一种将数据库中的数据映射到代码中对象的技术，这个技术的需求出发点就是，**代码中有类，数据库中有数据表，我们可以将类和数据表进行映射，从而使得在代码中操作类就等同于操作数据库中的数据表了**。

ORM 这个概念出现的时间无从考究了，基本上从面向对象的编程思想出来的时候就有讨论了。但是到现在，是否要使用 ORM 的讨论也一直没有停止。

不支持使用 ORM 的阵营的观点基本上是使用 ORM 会影响性能，且会让使用者不了解底层的具体最终拼接出来的SQL，容易造成用不上索引或者最终拼接错误的情况。而支持使用 ORM 的阵营的观点主要是它能切切实实加速应用开发。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/ed/4e249c6b.jpg" width="30px"><span>Vincent</span> 👍（1） 💬（2）<div>对优秀的开源代码，应该吃透</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>fns 中 真正的 Create 里面有判断 dryRun </div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（1）<div>isDryRun := !db.DryRun &amp;&amp; db.Error == nil
		if !isDryRun {
			return
		}</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/07/482b7155.jpg" width="30px"><span>牛玉富</span> 👍（1） 💬（0）<div>本篇切入curd正题了😄</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/5e/72/791d0f5e.jpg" width="30px"><span>武汉行驶证查违章信息</span> 👍（0） 💬（0）<div>gorm 代码走读笔记
https:&#47;&#47;blog.csdn.net&#47;u013010890&#47;article&#47;details&#47;132613100</div>2023-08-31</li><br/>
</ul>