这一讲是“破冰篇”的最后一讲，我会先简单地回顾一下之前的内容，然后在Windows系统上实际操作，用几个应用软件搭建出一个“最小化”的HTTP实验环境，方便后续的“基础篇”“进阶篇”“安全篇”的学习。

## “破冰篇”回顾

HTTP协议诞生于30年前，设计之初的目的是用来传输纯文本数据。但由于形式灵活，搭配URI、HTML等技术能够把互联网上的资源都联系起来，构成一个复杂的超文本系统，让人们自由地获取信息，所以得到了迅猛发展。

HTTP有多个版本，目前应用的最广泛的是HTTP/1.1，它几乎可以说是整个互联网的基石。但HTTP/1.1的性能难以满足如今的高流量网站，于是又出现了HTTP/2和HTTP/3。不过这两个新版本的协议还没有完全推广开。在可预见的将来，HTTP/1.1还会继续存在下去。

HTTP翻译成中文是“超文本传输协议”，是一个应用层的协议，通常基于TCP/IP，能够在网络的任意两点之间传输文字、图片、音频、视频等数据。

HTTP协议中的两个端点称为**请求方**和**应答方**。请求方通常就是Web浏览器，也叫user agent，应答方是Web服务器，存储着网络上的大部分静态或动态的资源。

在浏览器和服务器之间还有一些“中间人”的角色，如CDN、网关、代理等，它们也同样遵守HTTP协议，可以帮助用户更快速、更安全地获取资源。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/1a/abb7bfe3.jpg" width="30px"><span>cylim</span> 👍（157） 💬（12）<div>在Mac上，

拷贝项目（需要Git）
1. git clone https:&#47;&#47;github.com&#47;chronolaw&#47;http_study

安装OpenResty （推荐使用Homebrew）
1. brew tap openresty&#47;brew
2. brew install openresty 

运行项目
1. cd http_study&#47;www&#47;
2. openresty -p `pwd` -c conf&#47;nginx.conf

停止项目
1. openresty -s quit -p `pwd` -c conf&#47;nginx.conf</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（29） 💬（6）<div>对 cylim 的 mac 上运行 openresty 的教程进行补充：
按照 cylim 的做法，我遇到了访问 localhost 时，网页报 403 错误的情况，原因是没有 html&#47;index.html 文件的访问权限。我研究并找到了解决方案：
先 ls -la html，查看文件的权限，得到 user 和 group，我这里是 fstar 和 staff。

然后在 conf&#47;nginx.conf 文件的顶部添加

user fstar staff;

然后再启动 openresty 就可以正常访问了。</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/ac/e5e6e7f3.jpg" width="30px"><span>古夜</span> 👍（23） 💬（7）<div>我打赌很多人抓不到包，找不到本地回环地址，不知道最新版的wireshark是否修复了这个问题，如果出现以上问题，记得卸载重装wireshark，不要勾选它自带的ncap应该是这个名字，然后自己去单独下一个这个软件</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/8e/30/71b84ce7.jpg" width="30px"><span>geek桃</span> 👍（17） 💬（5）<div>送给后来的同学：
如果你按照步骤操作之后出现：start启动完成后，cmd窗口一闪而过，点击list启动时显示“没有运行的任务匹配制定标准”，请按任意键继续，当随便输入数据时，cmd窗口又没了；去查找www&#47;logs&#47;error.log，如果日志报错为“10013: An attempt was made to access a socket in a way forbidden by its access permissions”，说明你的80端口被占用了，按照下面步骤操作。
1.按键盘win+r 打开运行界面，输入cmd，确定，打开管理员界面
2.输入 netstat -aon | findstr :80 （有一条0.0.0.0的数据，记住这条数据最后的数字；我的是5884）
3.输入  tasklist|findstr &quot;5884&quot; （根据上一步查到的数字，找到5884端口对应的服务名称，我的是snv）
4.在控制台关闭服务
5.重新启动start.bat，成功！
</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4e/31/3a7e74c1.jpg" width="30px"><span>名曰蓝兮</span> 👍（17） 💬（1）<div>centos上的安装步骤，有错误请指出
wireshark：
1. yum install wireshark
    yum install wireshark-gnome
2. 如果不是root用户，启动后没有权限，做如下操作
    2.1 添加当前用户到wireshark组，我的用户叫&#39;zp&#39;：
          usermod -a -G wireshark zp
    2.2 然后给dumpcap读网卡的权限：
          setcap cap_net_raw,cap_net_admin+eip &#47;usr&#47;sbin&#47;dumpcap
完成后重启机器。

telnet：
yum install telnet

OpenResty:
官网有说明，按照说明一步步来
1. 添加OpenResty仓库：
    sudo yum install yum-utils
    sudo yum-config-manager --add-repo https:&#47;&#47;openresty.org&#47;package&#47;centos&#47;openresty.repo
2. 安装OpenResty:
    sudo yum install openresty
    sudo yum install openresty-resty
3. 在～目录下创建conf和logs文件夹：
    mkdir ~&#47;work
    cd ~&#47;work
    mkdir logs&#47; conf&#47;
4. 在conf文件夹下创建nginx.conf文件，内容如下：
worker_processes  1;
error_log logs&#47;error.log;
events {
    worker_connections 1024;
}
http {
    server {
        listen 8080;
        location &#47; {
            default_type text&#47;html;
            content_by_lua_block {
                ngx.say(&quot;&lt;p&gt;hello, world&lt;&#47;p&gt;&quot;)
            }
        }
    }
}
5. 添加OpenResty环境变量，注意冒号，别丢了:
    PATH=&#47;usr&#47;local&#47;openresty&#47;nginx&#47;sbin:$PATH
    export PATH
6. 在&#39;~&#47;work&#39;目录下启动OpenResty:
    nginx -p `pwd`&#47; -c conf&#47;nginx.conf
7. 验证安装：
    curl http:&#47;&#47;localhost:8080
    输出：
    &lt;p&gt;hello, world&lt;&#47;p&gt;</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/81/788cd471.jpg" width="30px"><span>珈蓝白塔</span> 👍（16） 💬（5）<div>Mac 开发环境的搭建参考《答疑篇41》，项目中已经有前辈写好的 shell 脚本，终端里直接运行就可以，不需要自己输入 openresty 命令啦；服务器启动以后访问 localhost 环境遇到了 403 问题，显示不出来 HTML，可参照留言区中提出的，在 conf&#47;nginx.conf 文件的顶部添加 user xxxx staff; 来解决，这个 xxxx 是自己的 mac 账户名；Wireshark(v3.2.3) 中选择环回地址时，选择 lockback：lo0 就可以啦，过滤器是和文中一样的，已成功搭建环境（2020年4月13日）</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/b8/e4b6a677.jpg" width="30px"><span>YUANWOW</span> 👍（12） 💬（4）<div>我一开始nginx一直起不来
后面看了error.log
发现本机443端口被占用了
netstat -ano | findstr &quot;443&quot;
看到一个 0.0.0.0:443  最后一列是进程的PID
查找到是vmware-hostd这个进程
后面谷歌搜索了下 
vmware的虚拟机共享会默认占用443端口
所以安装了vmware的把虚拟机共享关闭就好了  </div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（11） 💬（1）<div>破冰篇最后一篇，是马上开展破冰行动，抓捕林耀东了吗</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（11） 💬（2）<div>想请问下在 MacOs 或者是 Linux 上怎么搭建？（不是太想弄 Windows 虚拟机）</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3f/23/8ff389d2.jpg" width="30px"><span>郁方林</span> 👍（10） 💬（2）<div>start启动完成后，cmd窗口一闪而过，当我点击list启动时显示“没有运行的任务匹配制定标准”，请按任意键继续，当我随便输入数据时，cmd窗口又没了</div>2019-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLw9fVyja3eQLGQenLf5EqVaxGQoibo7rq8A7IRjlXED9FhicKukcn0ibCCtiaBqpEib4ZEIWfFOkiaGMSQ/132" width="30px"><span>Geek_d4dee7</span> 👍（7） 💬（1）<div>老师 最近我维护的一个网站打开速度非常慢  服务器CPU 负载0.5到0.8之间 有十多台web 服务器  redis  db  负载都正常 只是nginx 的链接数在出问题的时间点有上升  我目前不知道从哪下手排查这个问题 是用php symfony 开发的  能否给点思路 万分感谢</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/0b/73628618.jpg" width="30px"><span>兔嘟嘟</span> 👍（6） 💬（2）<div>windows上装的最新的3.4.7版，没有npcap，但是有一个Adapter for loopback traffic，用起来效果一样，就是抓到的Source是::1，猜测是这台电脑比较新，用上了IPv6的localhost</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（6） 💬（1）<div>老师，上面过程怎么没有用到telnet</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（5） 💬（1）<div>老师可以把环境打包成容器，我们进容器直接嗨，隔离更彻底</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（4） 💬（1）<div>在浏览器和服务器之间还存在“中间人”，这些中间人也都遵循http协议，我想问下，这些中间人是不是都工作在应用层？</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（4） 💬（1）<div>为啥有时候批处理stop不掉openresty？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/47/30d4b61e.jpg" width="30px"><span>不是云不飘</span> 👍（3） 💬（1）<div>建议还是能有win和Mac，逼近做开发的Mac不再少数。这些东西之前只有客户对接问题才会看到运维大哥在哪捣腾那时候看的一脸们逼，难得如此细致的了解。</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/27/35/ba972e11.jpg" width="30px"><span>因缺思厅</span> 👍（3） 💬（1）<div>这次环境搭建很顺利呀
</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9e/e7/2050698e.jpg" width="30px"><span>6欢</span> 👍（3） 💬（1）<div>建议环境搭建都在linux操作，哈哈</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/53/c29c2fc9.jpg" width="30px"><span>sdjdd</span> 👍（3） 💬（1）<div>正在学温铭老师的《OpenResty从入门到实战》，正好用上。</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/e5/4939b0c6.jpg" width="30px"><span>sunözil</span> 👍（2） 💬（1）<div>希望有个Mac环境搭建  谢谢老师</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/93/8135f895.jpg" width="30px"><span>bywuu</span> 👍（2） 💬（1）<div>成功了！这里需要下载wireshark，不过下载之后最好更新为最新版本3.0.x（最好翻墙），否则最好是重启，否则看不到。如果是先打开了localhost，那么应该刷新一下，才能在wireshark里面看到结果。
运行了stop脚本之后，再刷新浏览器，就会提示找不到页面了。这时的wireshark里面也都是红黑色的出错信息了。</div>2019-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iaV35C64GbQ9Zaos6U3r9zFJPZ7hcXQqlQbkOm8PxmkktsnJicJaDfKNPRsqAnYP4qqaUMHX8x95CrueszjjEW4g/132" width="30px"><span>xiaolin777</span> 👍（2） 💬（3）<div>老师，我的Npcap Loopback Adapter (port 80) 一直抓不到包怎么办，Npcap和wireshark都重装好几次了</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/bf/2635b2d2.jpg" width="30px"><span>仰望蓝天</span> 👍（2） 💬（1）<div>老师，我与 告辞同学 遇到了一样的问题，查看日志发现是80端口被占用了，用命令查看后发现是被System系统占用了，所以没法将这个进程杀掉。请问可以自己更改 http_study 项目中所使用的端口号吗？</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>不错，实践出真知</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/d0/4c/3e86714d.jpg" width="30px"><span>哦耶</span> 👍（1） 💬（1）<div>可以用node起的服务做实验吗</div>2022-04-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Lop0uAwiawHbqgRFYqIZv2YbFMJSeDePB0fia3j6joQQ3sddhvgpic6ibXLkva572O6dWS3QzicOibJGjr4QjrNXEgwg/132" width="30px"><span>忙了你个狗</span> 👍（1） 💬（1）<div>如果半天都改不了hosts文件的话，先属性，看看是不是把 只读 给勾选了，是的话先取消勾选</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/6a/6b96edbd.jpg" width="30px"><span>学不动了</span> 👍（1） 💬（1）<div>操作系统小白，用的Mac，怕听不懂看不明白老师的课程，就用Parallels装了windows和ubuntu的镜像，发现更吃力，最终还是换回Mac环境，在Mac安装遇到如下问题：
1. brew install的时候每次都是update失败，提示不支持当前系统版本，是因为之前改了镜像源，改回来就可以安装了
2.openresty启动之后访问403，正如Fstar所说，是因为权限问题，在nginx.conf第一行加上“user xiaofanhuang staff; ”即可，必须有分号！！！
3.wireshark 3.4.5 抓包：“...using this filter:”选择“tcp port http”，再双击下边的“Loopback: lo0” </div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（1） 💬（1）<div>老师 请问下 我找不到 ncap 但是又个叫adapter for loopback traffic capture 能用吗 ,一开始抓包,好像一大片的内容,还没访问网址</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/38/4c/5426e2e0.jpg" width="30px"><span>CJJ</span> 👍（1） 💬（1）<div>好奇怪，我使用老师http_study里面www文件夹里面的脚本启动不了openresty...o(╥﹏╥)o，不知道是不是我电脑系统的问题(win10)，比如，老师的start.bat脚本是这样的（start ..\openresty\nginx -p .），双击之后一闪而过，点击list.bat没看到nginx进程，后面我自己在控制台到目录下执行就可以，于是我就把start.bat改成这样：
cd ..&#47;openresty
start nginx -p .
结果这样就好了，有点迷惑，stop.bat同理也是，得先去到目录下，再执行命令。</div>2020-11-10</li><br/>
</ul>