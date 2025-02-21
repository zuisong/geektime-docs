你好，我是何为舟。

在上一讲中，我们介绍了XSS攻击。今天，我们来介绍另外一种常见的Web攻击：SQL注入。

在讲正文之前，让我们先来看一个案例。某天，当你在查看应用的管理后台时，发现有很多异常的操作。接着，你很快反应过来了，这应该是黑客成功登录了管理员账户。于是，你立刻找到管理员，责问他是不是设置了弱密码。管理员很无辜地表示，自己的密码非常复杂，不可能泄露，但是为了安全起见，他还是立即修改了当前的密码。奇怪的是，第二天，黑客还是能够继续登录管理员账号。问题来了，黑客究竟是怎么做到的呢？你觉得这里面的问题究竟出在哪里呢？你可以先自己思考一下，然后跟着我开始今天的学习！

## SQL注入攻击是如何产生的？

在上一讲中，我们讲了，XSS是黑客通过篡改HTML代码，来插入并执行恶意脚本的一种攻击。其实，SQL注入和XSS攻击很类似，都是黑客通过篡改代码逻辑发起的攻击。那么，不同的点是什么？SQL注入到底是什么呢？

通常来说，我们会将应用的用户信息存储在数据库中。每次用户登录时，都会执行一个相应的SQL语句。这时，黑客会通过构造一些恶意的输入参数，在应用拼接SQL语句的时候，去篡改正常的SQL语意，从而执行黑客所控制的SQL查询功能。这个过程，就相当于黑客“注入”了一段SQL代码到应用中。这就是我们常说的**SQL注入**。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/d9/cb12e020.jpg" width="30px"><span>豆豆</span> 👍（48） 💬（1）<div>之前只是知道些简单的 SQL 注入方式以及防范措施，今天文末的盲注确实涨了知识，关于思考题自己做了如下的练习。

首先盲注应该也是通过 web 端的输入来实现黑客的入侵目的的，那么黑客就可以通过观察页面的反应来动态修改自己的注入参数。比如一些提交输入框，当我们提交了参数之后页面反应正常那么就说明我们的猜测是正确的，否则继续猜。

我们都知道 MySQL 内部有一个 information_schema 的库，里面都是数据裤的元信息，那么我们就可以利用这个库进行猜测，通过观察页面的反应来验证自己的猜测是否正确。

第一步我们要知道数据的名字，那么就先猜测其长度。以下我们会用到 DATABASE(), LENGTH(), SUBSTRING(), ASCII() 四个内置函数。

1. 确定数据库长度

SELECT name FROM user WHERE id = 1 AND (SELECT LENGTH(DATABASE()) = 4);

得到数据库长度之后猜测数据库名字的每个字母。

2. 确定数据库名字 通过 ASCII 码方式

SELECT name FROM user WHERE id = 1 AND (SELECT ASCII(SUBSTRING(DATABASE(), 1, 1)) &lt; 128); 

根据 ASCII 码猜测是可以使用二分法来猜测。假设的到的结果是 test。

得到数据库名字之后，猜测 user 表有多少个列。

3. 获取该表有多少列

SELECT name FROM user WHERE id = 1 AND ((SELECT COUNT(*) FROM information_schema.COLUMNS WHERE table_name = &#39;user&#39; AND TABLE_SCHEMA = &#39;test&#39;) = 3);

获取到列的多少列之后，就可以获取到每一列的长度了。

4. 获取列长
SELECT name FROM user WHERE id = 1  AND ((SELECT LENGTH(column_name) FROM information_schema.COLUMNS WHERE table_name = &#39;user&#39; AND TABLE_SCHEMA = &#39;test&#39; LIMIT 0, 1) = 2);


最后，获取每一列的具体值。

5. 获取列名，同样是使用 ASCII 码方式
SELECT name FROM user WHERE id = 1  AND ((SELECT ASCII(SUBSTRING(column_name, 1, 1)) FROM information_schema.COLUMNS WHERE table_name = &#39;user&#39; AND TABLE_SCHEMA = &#39;test&#39; LIMIT 0, 1) &lt; 120)

为了故事的顺利发展这里我假设我们已知表名 user，但是我们可以根据同样的逻辑从 information_schema.TABLES 表中获取 test 库的所有表信息。

最后，我感觉这个方式有点傻啊，因为它依赖一些很特定的条件，比如后端没有做 SQL 注入的防护，而且还必须结合前端页面的反应。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（8） 💬（1）<div>研究了下盲注的文章，长见识了，以前只是大概知道sql注入，知道最简单的方式，盲注这种方法还是第一次接触，针对这个思考题，可以按如下方式获取其他字段，思路如下，可以写脚本实现，还有前提是能够进行盲注，
1. 先判断字段的第一个字符是否在a-z中，如下所示，

select Username from Users where UserId = 1 and 1 = (select 1 from information_schema.columns WHERE table_name=&#39;Users’ and COLUMN_NAME REGEXP &#39;^[a-z]&#39;)
如果结果显示Username那就说明字段的第一个字符在a到z中，

2. 使用二分查找法在a到z之间查找第一个字符，如下语句，

select Username from Users where UserId = 1 and 1 = (select 1 from information_schema.columns WHERE table_name=&#39;Users’ and COLUMN_NAME REGEXP &#39;^a[a-z]&#39;)

如果能显示Username，那么就说明a是第一个字符，再依次去查第二个字符，反之，换一个字符再试。

3. 以此类推，可以找到所有的字段名。

顺便说下，字段名中可能包含其他字符，如 _ 等，可以在正则表达式中同样去匹配。

</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（2） 💬（2）<div>现在SQL注入不常见了吧，现在的开发框架都可避免SQL注入了吧。比如基于python的Django。</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/49/01cebe31.jpg" width="30px"><span>sober</span> 👍（2） 💬（1）<div>希望老师能抽出一节讲讲登录实战，想真正了解一下整个登录如何应用加密，谢谢老师了</div>2019-12-24</li><br/><li><img src="" width="30px"><span>Gamer777</span> 👍（0） 💬（1）<div>通过使用 PreparedStatement，将 SQL 语句的解析和实际执行过程分开，只在执行的过程中代入用户的操作。分开执行还是无法防御SQL注入吗，不然为什么底层还是会对一些特殊符号进行转义操作？</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/0f/26c38307.jpg" width="30px"><span>HE明伟</span> 👍（0） 💬（1）<div>老师，现在的spring boot这些框架都能预防sql注入了吧</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/cd/d39e568c.jpg" width="30px"><span>felix</span> 👍（0） 💬（1）<div>如果是string,还是解决不了第一个password或的情况?</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/51/50/f5f2a121.jpg" width="30px"><span>律飛</span> 👍（0） 💬（1）<div>作为编程小白而言，学习难度有点大哦🙄。多看了好几篇盲注的文章，仍然是晕头转向的。豆豆已经提供了很好的答案。不过我还是来说说我的理解，不足之处请老师批评指正。

盲注其实就是结合SQL最基本的两种注入方式，不断去猜测并验证数据库可能的信息，最终获得答案的过程。这需要注入者简单的基础和丰富的经验，以及长时间频繁地跟数据库交互。

对于这种攻击，开发者采用PreparedStatment,存储过程，验证输入等方法就可以防范攻击。

请教老师：对于输入内容验证是不是还可以通过长度进行控制？对于盲注是不是可以通过单位时间内某个id跟数据库连接次数进行限制和预警？如果想动手试验，如何避免触碰红线？</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>可介绍下sqlmap吗？</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/12/15/874b9d62.jpg" width="30px"><span>Zhen</span> 👍（0） 💬（1）<div>了解了一下盲注，比较有意思，根据你SQL注入的攻击语句返回TRUE或者FALSE，可被用来一点点猜测获取数据库schema。 比如：如果 http:&#47;&#47;newspaper.com&#47;items.php?id=2 and 1=2   返回FALSE；http:&#47;&#47;newspaper.com&#47;items.php?id=2 and 1=1 返回正确，就说明后面输入的语句被服务器执行了   而且存在一个数字型的注入；那我们现在就可以开始盲注，判断它目前使用的数据库、版本、一点点猜测数据库内容。

另外有个很初级的问题想请教一下，SQL注入是不是所有SQL数据库固有的问题？为什么数据库本身不能自我完善做到输入参数的过滤和保护，而是要Java应用程序来通过PreparedStatement来做？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/47/fd/895f0c27.jpg" width="30px"><span>Cy23</span> 👍（0） 💬（2）<div>注册的时候看input的name都有什么，基本上就了解个大概有什么字段，然后尝试猜常用的字段，
或者查询显示的语句里注入查询表中所有字段名，然后替换字段名到显示输出的地方查看，
突然想起原来有个资源下载的网站，原来是免费的，后来收费了，有天无意将页面上下载所需要的分值改为负数，结果下载--为正给我加分了，然后尝试修改分值大小，结果我给自己充满了，我把这个漏洞告诉给站长，站长为了表示感谢奖励我1000分，然后我发现，我那999999999变成了1000。</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/69/791d0f5e.jpg" width="30px"><span>rocedu</span> 👍（0） 💬（1）<div>要是有个课题程配套虚拟机就更好了</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（0） 💬（1）<div>现在应该很多大部分开发都使用 PreparedStatement 了吧</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（1） 💬（0）<div>OWASP的 Enterprise Security API Java库好像可以搞定这些问题</div>2021-06-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLC4IhKmJDYdWhQms3dmZqJ5YMDGTlPa1o52DnKSErYjsqfc6iaRJrBDZpx0RqQx7eZAED797kiaV6aw/132" width="30px"><span>陈启航</span> 👍（0） 💬（0）<div>使用ORM操作数据库是不是也可以避免很大一部分sql注入呢?</div>2021-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（0）<div>这个万能密码&quot; or &quot;&quot;=&quot;，如果是字符串类型的，知道字段名的话直接当成参数查询，真的就是问题很大。
这个PreparedStatement之所以能做到屏蔽大多数SQL注入，其实是因为“负责任”，他把这些参数加了点料，比如添加一些转义字符。
试想一下，如果人家做的不是万能密码，而是修改数据这些，这个是真的挺可怕的一件事。</div>2020-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（0） 💬（0）<div>用preparedstatement把sql的解析和执行分开</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/89/f7d841c1.jpg" width="30px"><span>tardc</span> 👍（0） 💬（0）<div>要获取其他字段，可以利用盲注的方法猜测，如果页面有回显的话也可以使用Union查询来回显。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（0） 💬（0）<div>老师讲得很清楚，赞</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>   思考题的处理方式：最简单就是用存储过程；尤其如果开发语言是.net的话。sql注入问题的爆发应当是在2008-2009年左右，sql server当时的主流版本在2005；记得当时就是由于注入的爆发，导致当时大量的数据库代码从直接写改成了调用存储过程。</div>2019-12-30</li><br/>
</ul>