你好，我是朱晓峰。今天，咱们来聊一聊MySQL的时间函数。

顾名思义，时间函数就是用来处理时间的函数。时间，几乎可以说是各类项目中都会存在的数据，项目需求不同，我们需要的时间函数也不一样，比如：

- 如果我们要统计一天之中不同时间段的销售情况，就要获取时间值中的小时值，这就会用到函数HOUR()；
- 要计算与去年同期相比的增长率，这就要计算去年同期的日期时间，会用到函数DATE\_ADD()；
- 要计算今天是周几、有没有优惠活动，这就要用到函数DAYOFWEEK()了；
- ……

这么多不同类型的时间函数，该怎么选择呢？这节课，我就结合不同的项目需求，来讲一讲不同的时间函数的使用方法，帮助你轻松地处理各类时间数据。

## 获取日期时间数据中部分信息的函数

我先举个小例子。超市的经营者提出，他们希望通过实际的销售数据，了解到一天当中什么时间段卖得好，什么时间段卖得不好，这样他们就可以根据不同时间的销售情况，合理安排商品陈列和人员促销，以实现收益最大化。

要达到这个目标，我们就需要统计一天中每小时的销售数量和销售金额。

这里涉及3组数据，分别是销售单头表（demo.transactionhead)、销售单明细表 (demo.transactiondetails)和商品信息表（demo.goodsmaster）（为了便于你理解，表的结构和表里的记录都是经过简化的）。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLZKoB7sooIiaCHqcdNGI97WI3ZJLJph4mibIiat1qRvrBmkicZTEYvyT5iax1vlLFFgk2xgUibmnWvkicWA/132" width="30px"><span>朱晓峰</span> 👍（1） 💬（3）<div>你好，我是朱晓峰，下面我就来公布一下上节课思考题的答案：

上节课，我们学习了聚合函数。下面是思考题的答案：

SELECT 
    goodsname, COUNT(*) 
FROM
    demo.goodsmaster
GROUP BY goodsname;</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/af/7f/584e1327.jpg" width="30px"><span>岁月静好</span> 👍（4） 💬（2）<div>select date_format(&#39;2021-03-31&#39;,&#39;%W %M %Y&#39;);
+--------------------------------------+
| date_format(&#39;2021-03-31&#39;,&#39;%W %M %Y&#39;) |
+--------------------------------------+
| Wednesday March 2021                 |
+--------------------------------------+</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/53/7e/b6829040.jpg" width="30px"><span>SevenMonths</span> 👍（1） 💬（1）<div>&#47;&#47;时间里获取 年 月 日 时 分 秒
EXTRACT(SECOND FROM Now())  SECOND(Now())
EXTRACT(MINUTE FROM Now())  MINUTE(Now())
EXTRACT(HOUR FROM Now())  HOUR(Now())
EXTRACT(DAY FROM Now())   DAY(Now())
EXTRACT(MONTH FROM Now()) MONTH(Now())
EXTRACT(YEAR FROM Now())  YEAR(Now())

&#47;&#47;增加 同 ADDDATE()
DATE_ADD(&#39;2020-12-10&#39;, INTERVAL - 1 YEAR) &#47;&#47;2019-12-10
DATE_ADD(&#39;2020-12-10&#39;, INTERVAL + 1 YEAR) &#47;&#47;2021-12-10
&#47;&#47;当月最后一天
LAST_DAY(&#39;2020-12-10&#39;) &#47;&#47;2020-12-31

&#47;&#47;减少 同 SUBDATE()
DATE_SUB(&#39;2020-12-10&#39;, INTERVAL + 1 YEAR) &#47;&#47;2019-12-10
DATE_SUB(&#39;2020-12-10&#39;, INTERVAL - 1 YEAR) &#47;&#47;2021-12-10

&#47;&#47;当前日期 ：YYYY-MM-DD
CURDATE()：2019-02-12

&#47;&#47;格式化时间：
DATE_FORMAT
DATE_FORMAT(&quot;2020-12-01 13:25:50&quot;,&quot;%T&quot;) &#47;&#47; 01:25:50 PM

&#47;&#47;时间差
DATEDIFF(max,min)
DATEDIFF(&quot;2021-02-01&quot;,&quot;2020-12-01&quot;) &#47;&#47; 62

&#47;&#47;周几
DAYOFWEEK(Now()):1 表示周日，以此类推，直到 7 表示周六。

&#47;&#47;如果等于 0 表示为周日，其他为正常周几
CASE DAYOFWEEK(CURDATE()) - 1 WHEN 0 THEN 7 ELSE DAYOFWEEK(CURDATE())</div>2021-09-01</li><br/><li><img src="" width="30px"><span>Geek_58516f</span> 👍（1） 💬（1）<div>老师您好，我需要获得每天从凌晨12点到晚上12点，24个小时，每个小时整点的时间（比如1点，2点...），怎么做呢</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/56/bd/13d32273.jpg" width="30px"><span>西云关二爷</span> 👍（1） 💬（3）<div>老师，您是否能提供下测试的表结构和测试数据。谢谢，每次手动建表做测试数据比较花费时间。</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/ce/1297d273.jpg" width="30px"><span>安全着陆_</span> 👍（0） 💬（1）<div>select case DAYOFWEEK(CURDATE())-1 when 0 then &#39;周日&#39; 
 when 1 then &#39;周一&#39; 
 when 2 then &#39;周二&#39;
 when 3 then &#39;周三&#39;
 when 4 then &#39;周四&#39;
 when 5 then &#39;周五&#39;
 when 6 then &#39;周六&#39;
else DAYOFWEEK(CURDATE())-1 
end
;</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f6/c4/e14686d4.jpg" width="30px"><span>shk1230</span> 👍（0） 💬（1）<div>select date_format(curdate(),&#39;%W&#39;);</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/c8/92/408a23d4.jpg" width="30px"><span>zhuyuping</span> 👍（0） 💬（1）<div>发现一个小错误：总结板块，图片中的表格的第10行，DDDATE 应该是 ADDDATE，少了一个A。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/3f/92828807.jpg" width="30px"><span>伍华龙</span> 👍（0） 💬（1）<div>老师，您好。最后的汇总表格貌似有2次笔误，麻烦确认一下：
1. 「日期时间计算函数」的第2个函数&quot;ADDDATE&quot;漏了开头的A，写成&quot;DDDATE&quot;了。
2. 「其他时间函数」的第2个函数&quot;WEEKOFDAY&quot;我查看mysql手册没找到，应该是&quot;DAYOFWEEK&quot;。另外我也发现有个类似的函数&quot;WEEKDAY&quot;，跟&quot;DAYOFWEEK&quot;类似，只是星期几与数字之间的映射不一样。</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/bd/6d/7010f98e.jpg" width="30px"><span>SharpBB</span> 👍（0） 💬（1）<div>虽然时间函数很有用 但是在处理复杂逻辑的时候 还是建议在业务层面进行逻辑运算</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/bd/6d/7010f98e.jpg" width="30px"><span>SharpBB</span> 👍（0） 💬（1）<div>1.从日期中获取时间
	获取用户的创建小时
		SELECT EXTRACT(HOUR FROM create_time) time , FROM user;
	使用函数
		SELECT HOUR(create_time) time ,`name` FROM user;
2.计算日期时间的函数
	DATE_ADD
		SELECT DATE_ADD(&#39;2022-2-10&#39;,interval 1 day) date;   
			输出2022-2-11
	DATE_SUB
		查找上个月到现在的用户创建记录
			SELECT * from user where create_time&gt;DATE_SUB(now(),interval 1 MONTH) ;   
	CURDATE()
		获取当前的日期
			如2022-2-10
	DAYOFWEEK(date)
		获取某天是周几
			从周日开始为1
	DATE_FORMAT()
		SELECT DATE_FORMAT(now(),&#39;%T&#39;);
			24小时制格式化时间
		SELECT DATE_FORMAT(now(),&#39;%r&#39;);
			12小时制格式化时间
	DATEDIFF(date1,date2)
		DATEDIFF(&quot;2021-02-01&quot;,&quot;2020-12-01&quot;);
			返回相差几天
3.分布式系统时间差异解决办法
	1.设置Windows 系统自带的网络同步
	2.统一从总部MySQL服务器获取时间</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e0/0b/6f667b2c.jpg" width="30px"><span>枫林血舞</span> 👍（0） 💬（1）<div>交作业：
select date_format(sysdate(), &#39;%W %M %Y&#39;);</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/ed/a0/cc89c128.jpg" width="30px"><span>大聖</span> 👍（0） 💬（1）<div>思考题：select dayname(curdate());</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fb/85/f3fd1724.jpg" width="30px"><span>PHP菜鸟</span> 👍（0） 💬（1）<div>我们公司的要求是不允许在Sql中用各种的聚合函数,这可咋办......</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/52/5951ffb4.jpg" width="30px"><span>Sinvi</span> 👍（0） 💬（1）<div>select DATE_FORMAT(curdate(), &#39;%W&#39;);</div>2021-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（14） 💬（1）<div>老师这一讲保持了之前一贯的细致入微。常用的时间日期处理方法和函数大部分都讲到了。包括CASE这种开发中较少看到的用法。

很多人把时间日期的相关计算放到编程语言层面去处理，虽然MySQL也能实现同样功能，但是会让SQL语句复杂度上升，维护成本上升。放到编程语言上去处理，相对来说更容易维护。</div>2021-03-27</li><br/>
</ul>