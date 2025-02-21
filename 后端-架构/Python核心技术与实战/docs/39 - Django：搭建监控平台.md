你好，我是景霄。

通过前几节课的学习，相信你对量化交易系统已经有了一个最基本的认知，也能通过自己的代码，搭建一个简单的量化交易系统来进行盈利。

前面几节课，我们的重点在后台代码、中间件、分布式系统和设计模式上。这节课，我们重点来看前端交互。

监控和运维，是互联网工业链上非常重要的一环。监控的目的就是防患于未然。通过监控，我们能够及时了解到企业网络的运行状态。一旦出现安全隐患，你就可以及时预警，或者是以其他方式通知运维人员，让运维监控人员有时间处理和解决隐患，避免影响业务系统的正常使用，将一切问题的根源扼杀在摇篮当中。

在硅谷互联网大公司中，监控和运维被称为 SRE，是公司正常运行中非常重要的一环。作为 billion 级别的 Facebook，内部自然也有着大大小小、各种各样的监控系统和运维工具，有的对标业务数据，有的对标服务器的健康状态，有的则是面向数据库和微服务的控制信息。

不过，万变不离其宗，运维工作最重要的就是维护系统的稳定性。除了熟悉运用各种提高运维效率的工具来辅助工作外，云资源费用管理、安全管理、监控等，都需要耗费不少精力和时间。运维监控不是一朝一夕得来的，而是随着业务发展的过程中同步和发展的。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（29） 💬（0）<div>常用的认证方式有，HTTP Basic Auth，OAuth，Cookie Auth，Token Auth，而 Django Restful 一种常用的方式是 JSON Web Token（JWT），这是一个非常轻巧的规范，可以参考 https:&#47;&#47;github.com&#47;jpadilla&#47;django-rest-framework-jwt.</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（6） 💬（1）<div>老师，我本地的django版本是1.11.8，没法运行你的最新版本。
指出一个错误：不用手动创建migrations文件夹。执行python3 manage.py makemigrations命令就会生成了。
有个问题：这个url的正则表达式我不太懂“path(&#39;positions&#47;&lt;str:asset&gt;&#39;, views.render_positions)”，&lt;str:asset&gt;不是一般都写成(?P&lt;asset&gt;[a-zA-Z]+)这样子的嘛？
作业回答：
因为http协议是无状态的，每次请求都是一次新的请求，不会记得之前通信的状态。所以需要一些特殊手段来记录状态。
方法一：把userinfo存储在request.session中，每次请求进行验证userinfo；
方法二：jwt生成一个包含用户信息的token令牌，并设置过期时间，每次处理客户端请求先验证是否请求头中带有token，要是有token解析出来的用户信息是否正确，以此来确定用户的登录状态。</div>2019-09-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（4） 💬（1）<div>目前流行前后端分离，通过http通信，独立部署，不知在fackbook也是这样，另外想了解下python做后端有什么比较好的推荐书籍可供学习吗</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/6d/915ce951.jpg" width="30px"><span>Kuzaman</span> 👍（33） 💬（1）<div>建议老师以后能专门出一个实战栏目，必顶</div>2019-08-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（21） 💬（0）<div>MVC在Django中对应的是MTV</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/95/3960d10e.jpg" width="30px"><span>奥特虾不会写代码</span> 👍（16） 💬（4）<div>老师的专栏是我在极客时间看过的质量最高的专栏了，文字简单易懂，又不失深度，不知道以后会不会专门出一个量化交易的专栏，一定支持！</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（6） 💬（2）<div>貌似还缺少一步，添加相关数据。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8d/e3/c3ed083a.jpg" width="30px"><span>夜月不挂科</span> 👍（5） 💬（1）<div>django会自动生成一个csrf字段用来认证。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fe/9e/8165b0a0.jpg" width="30px"><span>路伴友行</span> 👍（2） 💬（0）<div>DRF 有自带的token验证，也可以自己写中间件实现拦截</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/17/69cca649.jpg" width="30px"><span>旗木卡卡</span> 👍（2） 💬（0）<div>不知不觉已经学习了40讲，专栏马上就结束了，还没学够！</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1f/21/da776587.jpg" width="30px"><span>山雨淋淋</span> 👍（1） 💬（0）<div>监控系统的稳定性谁来保证，监控监控系统本身？</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b4/37/5d2a5288.jpg" width="30px"><span>8849</span> 👍（1） 💬（0）<div>Django是MVT，虽然是从MVC演变的，但还是有必要区别开</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/29/e0/35835788.jpg" width="30px"><span>Rs先生</span> 👍（1） 💬（0）<div>请教老师一个问题，我用的是python2.7，然后Django的版本为1.11.29，但是在最后访问url的是时候的显示page not found。这个是什么原因呢？
</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（1）<div>
pip3 install Django
django-admin --version

########## 输出 ##########

2.2.3
老师  django的这些命令再Windows CMD命令框执行后不行，访问不了https:&#47;&#47;127.0.0.1:8000,  再centos 执行完所有代码  启动后django 服务，命令显示[root@localhost TradingMonitor]# python3 manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 12, 2020 - 15:59:14
Django version 3.1, using settings &#39;TradingMonitor.settings&#39;
Starting development server at http:&#47;&#47;127.0.0.1:8000&#47;
Quit the server with CONTROL-C. ，但是浏览器访问失败 是什么原因</div>2020-08-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/8KpWhCMxgVgqKMxNT9zuJuVnz1gNBzYlWrZCO4hlF4OQibhawvn0hpHhHgHr4kSXfVNjeuE4StuvTR54NGcE4Zg/132" width="30px"><span>Geek_aa780e</span> 👍（1） 💬（0）<div>可以讲一下在web项目中，对于非法情况，比如说数据库链接错误报的异常，该怎么处理吗？ 是直接抛到handler层，还是在哪进行捕获？ </div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/a2/6c0ffc15.jpg" width="30px"><span>皮皮侠</span> 👍（1） 💬（0）<div>django好像是基于MVT模型，不过跟MVC差不多</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/91/f5/6881f336.jpg" width="30px"><span>姑苏小沈🏃🎸</span> 👍（1） 💬（0）<div>请教一个Sqlalchemy的更新数据问题：
我创建一个session后，session. query(User). filter(ID=user_id). first()
明明能找到一条数据，但是执行 user.Name = &#39;my nam&#39;
session. commit()时却提示 expected to update 1 row: 0 were matched</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/e1/f663213e.jpg" width="30px"><span>拾掇拾掇</span> 👍（1） 💬（0）<div>DRF好像好久没更新了，不支持Django2.0。不知道有什么框架可以替代</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第39讲打卡~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a9/cc/1183d71f.jpg" width="30px"><span>无</span> 👍（0） 💬（0）<div>前后分离的话用哪个框架比较好
</div>2024-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5d/71/4f6aad17.jpg" width="30px"><span>Sophia-百鑫</span> 👍（0） 💬（0）<div>缺少 insert 数据部分，老师能否更新下内容呢
感谢ing</div>2023-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/5b/30281476.jpg" width="30px"><span>落雨</span> 👍（0） 💬（0）<div>按照文档操作,最后一直提示no such table: TradingMonitor_position .感觉很多地方都没讲清楚.这课感觉有点不值</div>2021-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/O1kSTJtNUNtpehQmFxbSVHiaOHbibYR3dB2Ms9LgmfkGFxLfpM8QCcyge1OP5HLCpxXtFcy1jXcc3ibiaTcfaQ0pmg/132" width="30px"><span>Geek_a86175</span> 👍（0） 💬（0）<div>有的文章说创建项目后，还应该创建应用，一个大的业务模块作为一个APP，这个文章好像没有提及这块</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（0） 💬（0）<div>使用安全令牌。适用于服务器客户端程序。https:&#47;&#47;blog.csdn.net&#47;qw943571775&#47;article&#47;details&#47;82687843</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/12/06863960.jpg" width="30px"><span>稳</span> 👍（0） 💬（0）<div>Django自带的是通过session来认证的，DRF里支持Token等形式，大多通过中间件、dispatch、装饰器来实现</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/17/69cca649.jpg" width="30px"><span>旗木卡卡</span> 👍（0） 💬（0）<div>通过 Session or auth or Token来实现？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（0） 💬（0）<div>可以用drf 或者自己做数据 通过路由和方法自己组织</div>2019-08-07</li><br/>
</ul>