我们之前已经讲解了SQL的使用及优化，正常的SQL调用可以帮我们从数据库中获取想要的数据，然而我们构建的Web应用是个应用程序，本身也可能存在安全漏洞，如果不加以注意，就会出现Web安全的隐患，比如通过非正常的方式注入SQL。

在过去的几年中，我们也能经常看到用户信息被泄露，出现这种情况，很大程度上和SQL注入有关。所以了解SQL注入的原理以及防范还是非常有必要的。

今天我们就通过一个简单的练习看下SQL注入的过程是怎样的，内容主要包括以下几个部分：

1. SQL注入的原理。为什么用户可以通过URL请求或者提交Web表单的方式提交非法SQL命令，从而访问数据库？
2. 如何使用sqli-labs注入平台进行第一个SQL注入实验？
3. 如何使用SQLmap完成SQL注入检测？

## SQL注入的原理

SQL注入也叫作SQL Injection，它指的是将非法的SQL命令插入到URL或者Web表单中进行请求，而这些请求被服务器认为是正常的SQL语句从而进行执行。也就是说，如果我们想要进行SQL注入，可以将想要执行的SQL代码隐藏在输入的信息中，而机器无法识别出来这些内容是用户信息，还是SQL代码，在后台处理过程中，这些输入的SQL语句会显现出来并执行，从而导致数据泄露，甚至被更改或删除。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/90/4e/efaea936.jpg" width="30px"><span>墨禾</span> 👍（16） 💬（3）<div>
不规范的代码，比如拼接sql 却没有进行参数化验证，或者在前端验证完参数就以为是安全的输入，这些都很容易被绕过，导致sql注入。

防注入的方法：
1 参数化验证。不同的语言都应该封装了这种方法，比如说c#,java的sqlparameter .
2 对参数进行过滤。严格的白名单进行参数过滤。</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/49/27219a0f.jpg" width="30px"><span>zhxxmu</span> 👍（3） 💬（1）<div>在后端程序中采用参数化查询方式进行查询</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（3） 💬（2）<div>老师，你好，目前很少使用get方式提交了，差不多用post，而且输入参数都会校验的</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>涨知识了，谢谢老师的分享。</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（1） 💬（1）<div>https:&#47;&#47;blog.csdn.net&#47;weixin_41013322&#47;article&#47;details&#47;106290783 又记录了一下在这篇SQL注入过程中需要注意的地方 希望对各位有帮助😀</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/3f/06b690ba.jpg" width="30px"><span>刘桢</span> 👍（1） 💬（0）<div>学到了</div>2020-05-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/aianFlNnvpUaPUbYG9EjVbibgOgOCJYqgiapCbsbIhWHJG8BBm4fzo1ALNI8vqsL4mrGB9vWPWyUCct5yLp0neQDg/132" width="30px"><span>Geek_1c165d</span> 👍（1） 💬（1）<div>请问老师url后面的--+作用是啥？</div>2020-01-08</li><br/><li><img src="" width="30px"><span>Geek_186f56</span> 👍（0） 💬（0）<div>涨知识了</div>2022-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（0）<div>参数化查询，？ 代替掉需要执行的sql变量</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（0） 💬（0）<div>前段用户输入的所有数据都要做验证。</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2b/39/19041d78.jpg" width="30px"><span>😳</span> 👍（0） 💬（0）<div>1:参数话sql语句
2:存储过程
3:正则表达式</div>2020-02-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AGicQgKibwja1SxkQ7oXQE8hYH7yCpiaicNHw3qZRuNB81aVDOQm9P1zd5F75Jbtv66G15D6ZjbbqfnoETR4321Zdw/132" width="30px"><span>高泽林</span> 👍（0） 💬（0）<div>正需要！</div>2020-02-12</li><br/>
</ul>