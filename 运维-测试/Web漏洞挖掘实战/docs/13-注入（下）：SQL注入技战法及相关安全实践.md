你好，我是王昊天。

上节课我们学习了SQL注入的基本原理和基础动作，但想要完成SQL注入攻击，仅凭借基础知识是不够的。这节课我们就来深入分析不同场景下的SQL注入，来了解这些场景下都有哪些攻击方式。

事实上，即使同为SQL注入漏洞，由于攻击过程中可利用的条件和限制不同，所能够采取的攻击方式也是有差异的。比如在篮球比赛中，同样是上篮，由于防守队员的不同，甚至是防守人数的不同，都会有不同的动作。

## 注入技巧

![](https://static001.geekbang.org/resource/image/ec/a6/ece15f4c0fc0a854686fce1757ebcba6.png?wh=1034x543)

### 联合注入（UNION注入）

当SELECT语句中存在可以使用的SQL注入漏洞时，就可以用联合注入方法进行SQL注入，将两个查询合并为一个结果或结果集。

联合注入是在SQL注入中加入一个新的查询，在完成原始数据查询后，再进行一次查询，并将新的结果加入到原始查询的结果中，攻击者可以通过这种方式来获得目标数据。比如如下查询语句：

```sql
SELECT Name, Phone, Address FROM Users WHERE Id=$id
# http://www.example.com/product.php?id=10
```

这是一个简单的查询语句，目标是从`Users`表中查询指定`id`值的用户的姓名、密码以及地址信息。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rURvBicplInVqwb9rX21a4IkcKkITIGIo7GE1Tcp3WWU49QtwV53qY8qCKAIpS6x68UmH4STfEcFDJddffGC7lw/132" width="30px"><span>onemao</span> 👍（0） 💬（0）<div>有没有开源的sql注入的正则表达式包,java相关的,github上找了挺久没找到
</div>2024-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-03-11</li><br/><li><img src="" width="30px"><span>Geek_253f46</span> 👍（0） 💬（1）<div>参数化查询,能避免所有的sql注入吗</div>2022-06-19</li><br/>
</ul>