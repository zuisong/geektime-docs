我在上一篇文章中讲了WebSQL，当我们在Chrome、Safari和Firefox等浏览器客户端中使用WebSQL时，会直接操作SQLite。实际上SQLite本身是一个嵌入式的开源数据库引擎，大小只有3M左右，可以将整个SQLite嵌入到应用中，而不用采用传统的客户端／服务器（Client/Server）的架构。这样做的好处就是非常轻便，在许多智能设备和应用中都可以使用SQLite，比如微信就采用了SQLite作为本地聊天记录的存储。

今天我们就来深入了解一下SQLite，今天的内容主要包括以下几方面：

1. SQLite是什么？它有哪些优点和不足？
2. 如何在Python中使用SQLite？
3. 如何编写SQL，通过SQLite查找微信的聊天记录？

## SQLite是什么

SQLite是在2000年发布的，到目前为止已经有19年了。一直采用C语言编写，采用C语言而非C++面向对象的方式，可以提升代码底层的执行效率。但SQLite也有一些优势与不足。

它的优势在于非常轻量级，存储数据非常高效，查询和操作数据简单方便。此外SQLite不需要安装和配置，有很好的迁移性，能够嵌入到很多应用程序中，与托管在服务器上的RDBMS相比，约束少易操作，可以有效减少服务器的压力。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/64/94737463.jpg" width="30px"><span>我</span> 👍（25） 💬（1）<div>年底可以导出聊天记录做个词云</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（12） 💬（1）<div>😄，微信聊天记录，涨姿势了</div>2019-09-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（2） 💬（1）<div>涨姿势了，可以导出微信聊天记录了</div>2020-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（1）<div>这个聊天记录文件应该是不可编辑和替换的吧？</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>学习了，老师。</div>2019-09-05</li><br/><li><img src="" width="30px"><span>小虾米</span> 👍（10） 💬（1）<div>现在已经不行了吧？

在Wechat文件下的MicroMsg.db 已经不能用navicat或者sqlite导入了，需要密码了，而且不是微信密码。。</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/59/1d/c89abcd8.jpg" width="30px"><span>四喜</span> 👍（5） 💬（0）<div>微信居然没有对数据库进行加密吗？为什么呢</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/f1/16545faf.jpg" width="30px"><span>学习</span> 👍（4） 💬（2）<div>Navicat如何导入那个wenxin.db呢，有点不太明白，可以说个步骤吗？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/bf/a200e7a7.jpg" width="30px"><span>和白白</span> 👍（3） 💬（0）<div>我测试的结果是，备份文件在 messsage_1.sqlite 文件中，可以将 原先的查询SQL 替换成 SELECT * FROM Files WHERE relativePath LIKE &#39;%message\__.sqlite&#39; ESCAPE &#39;\&#39;;  
</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/cf/d5382404.jpg" width="30px"><span>RRR</span> 👍（2） 💬（0）<div>Chrome 的密码管理也是使用的 SQLite</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/f0/a73607b3.jpg" width="30px"><span>victor666</span> 👍（2） 💬（0）<div>安卓开发默认的存储就是sqlite</div>2020-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIR9QrAn9TZOrJMSYMyN96PAuAjETVrN5SPp3hMbfUAGIWtHceWPEoQtPdXeuBn7VB7dagtxynAIA/132" width="30px"><span>ballgod</span> 👍（2） 💬（1）<div>电脑端只找到了Msg.db的文件，无法导入到navicat中，并且使用notepad打开是乱码，请教老师如何解决，谢谢</div>2019-12-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1r98FrLibt2JkibgLGPuLxxyn2etGbDeo7pEByourpvvZL580RFmA4S1bwPgGOkIqtsmFfFCktgLEzC2UnH9DqMQ/132" width="30px"><span>Hanqiu_Tan</span> 👍（2） 💬（0）<div>Use &quot;.open FILENAME&quot; to reopen on a persistent database.
sqlite&gt; .open Manifest.db
sqlite&gt; .tables
Error: file is not a database
sqlite&gt;
这边试了打不开文件是怎么回事呢？</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（1） 💬（0）<div>微信聊天记录这个涨姿势了😆</div>2020-01-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIR9QrAn9TZOrJMSYMyN96PAuAjETVrN5SPp3hMbfUAGIWtHceWPEoQtPdXeuBn7VB7dagtxynAIA/132" width="30px"><span>ballgod</span> 👍（1） 💬（0）<div>请问老师，安卓和电脑端的微信记录怎么找，查资料有说需要root的</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>长见识了</div>2024-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/87/d26efb2e.jpg" width="30px"><span>SuperSnow</span> 👍（0） 💬（0）<div>老师，微信和QQ的电脑版的本地聊天内容也是用sqllite吗？</div>2021-10-16</li><br/>
</ul>