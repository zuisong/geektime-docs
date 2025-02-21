你好，我是Chrono。

先要说一声“抱歉”。由于工作比较紧张、项目实施频繁出差，导致原本预定的“答疑篇”迟迟没有进展，这次趁着“十一”长假，总算赶出了两期，集中回答几个同学们问得比较多的问题：Linux/Mac实验环境搭建（[第7讲](https://time.geekbang.org/column/article/100124)），URI查询参数（[第11讲](https://time.geekbang.org/column/article/102008)），还有DHE/ECDHE算法的原理（[第26讲](https://time.geekbang.org/column/article/110354)），后续有时间可能还会再陆续补充完善。

很高兴在时隔一个多月后与你再次见面，废话不多说了，让我们开始吧。

## Linux上搭建实验环境

我们先来看一下如何在Linux上搭建课程的实验环境。

首先，需要安装OpenResty，但它在Linux上提供的不是zip压缩包，而是各种Linux发行版的预编译包，支持常见的Ubuntu、Debian、CentOS等等，而且[官网](http://openresty.org/cn/linux-packages.html)上有非常详细安装步骤。

以Ubuntu为例，只要“按部就班”地执行下面的几条命令就可以了，非常轻松：

```
# 安装导入GPG公钥所需的依赖包：
sudo apt-get -y install --no-install-recommends wget gnupg ca-certificates


# 导入GPG密钥：
wget -O - https://openresty.org/package/pubkey.gpg | sudo apt-key add -


# 安装add-apt-repository命令
sudo apt-get -y install --no-install-recommends software-properties-common


# 添加官方仓库：
sudo add-apt-repository -y "deb http://openresty.org/package/ubuntu $(lsb_release -sc) main"


# 更新APT索引：
sudo apt-get update


# 安装 OpenResty
sudo apt-get -y install openresty
```

全部完成后，OpenResty会安装到“/usr/local/openresty”目录里，可以用它自带的命令行工具“resty”来验证是否安装成功：

```
$resty -v
resty 0.23
nginx version: openresty/1.15.8.2
built with OpenSSL 1.1.0k  28 May 2019
```

有了OpenResty，就可以从GitHub上获取http\_study项目的源码了，用“git clone”是最简单快捷的方法：
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/3f/96/ce0b9678.jpg" width="30px"><span>浪里淘沙的小法师</span> 👍（25） 💬（1）<div>讲一下用M1芯片 mac 搭建搭建环境的遇到的问题和解决方法。

1. 运行 .&#47;run.sh start 报错 &#47;usr&#47;local&#47;bin&#47;openresty: command not found
这是因为 M1 芯片mac 的 homebrew 安装软件的位置与以往不同，先通过 which openresty 查询 openresty 的位置 &#47;opt&#47;homebrew&#47;bin&#47;openresty，然后打开 run.sh 脚本替换一下老师写的位置
if [ $os != &quot;Linux&quot; ] ; then
    openresty=&quot;&#47;usr&#47;local&#47;bin&#47;openresty&quot;
fi
替换成
if [ $os != &quot;Linux&quot; ] ; then
    openresty=&quot;&#47;opt&#47;homebrew&#47;bin&#47;openresty&quot;
fi

2. 再运行 .&#47;run.sh start 报错 nginx: [emerg] could not build server_names_hash, you should increase server_names_hash_bucket_size: 32
网上查寻了一下，放大 bucket_size 即可，打开 www&#47;conf&#47;nginx.conf 文件添加这一句server_names_hash_bucket_size 64; 即可
# http conf
http {
    #include     http&#47;common.conf;
    #include     http&#47;cache.conf;
    #include     http&#47;resty.conf;
    #include     http&#47;mime.types;
    server_names_hash_bucket_size 64;
    
    include     http&#47;*.conf;

    include     http&#47;servers&#47;*.conf;

}</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8a/e7/a6c603cf.jpg" width="30px"><span>GitHubGanKai</span> 👍（7） 💬（2）<div>真好，又见到你了，而且我最近换个了mac，😊正愁这个。</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4a/7b/23da5db9.jpg" width="30px"><span>Luka!3055</span> 👍（3） 💬（1）<div>记录下问题：

brew install openresty&#47;brew&#47;openresty 后，报错：
curl: (7) Failed to connect to raw.githubusercontent.com port 443: Connection refused
Error: An exception occurred within a child process:
DownloadError: Failed to download resource &quot;openresty-openssl--patch&quot;
Download failed: https:&#47;&#47;raw.githubusercontent.com&#47;openresty&#47;openresty&#47;master&#47;patches&#47;openssl-1.1.0d-sess_set_get_cb_yield.patch

此时把 DNS 设置为 114.114.114.114 或者 8.8.8.8 就好了，最好再挂个梯子</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（2） 💬（2）<div>老师好，
按文章指导搭建了MAC的环境：
openresty -v
nginx version: openresty&#47;1.11.2.2

在~&#47;git&#47;http_study&#47;www目录下执行
 .&#47;run.sh start
Password:
nginx: [emerg] &quot;&#47;Users&#47;xiaodong&#47;git&#47;http_study&#47;www&#47;conf&#47;ssl&#47;ticket.key&quot; must be 48 bytes in &#47;Users&#47;xiaodong&#47;git&#47;http_study&#47;www&#47;conf&#47;nginx.conf:34
报了这个错误，在网上google没找到解决方法。
尝试在nginx.conf中注销相关代码，也会报其他错误。
老师能指点一下吗？</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（2） 💬（1）<div>这个专栏这么好玩，留言的人这么少，真可惜。
</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>谢谢分享</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/2c/0f7baf3a.jpg" width="30px"><span>Change</span> 👍（1） 💬（7）<div>老师请教个问题：Mac 环境下安装以后，按照命令.&#47;run.sh start 启动后访问 localhost 显示403 Forbidden：终端返回的错误信息是下面的错误信息，这是所有端口都被占用了？我查了一下好像也没有被占用啊，不知道这是啥原因
nginx: [emerg] bind() to 0.0.0.0:80 failed (48: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:8080 failed (48: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:443 failed (48: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:8443 failed (48: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:440 failed (48: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:441 failed (48: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:442 failed (48: Address already in use)
</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/29/bcf885b9.jpg" width="30px"><span>SmNiuhe</span> 👍（1） 💬（6）<div>这个大家有遇到嘛，是不是资源的问题
brew install openresty&#47;brew&#47;openresty ：DownloadError: Failed to download resource &quot;openresty-openssl--patch&quot;
Download failed: https:&#47;&#47;raw.githubusercontent.com&#47;openresty&#47;openresty&#47;master&#47;patches&#47;openssl-1.1.0d-sess_set_get_cb_yield.patch</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/78/c9/6ed5ad55.jpg" width="30px"><span>超轶主</span> 👍（0） 💬（2）<div>mac环境运行 run run.sh 返回 nginx version: openresty&#47;1.19.9.1
format : run.sh [start|stop|reload|list]是什么情况呢</div>2021-12-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/eHNmzejyQW9Ag5g3EELS1d9pTgJsvxC7CxSCxIFQqeFLXUDT52HWianQWzw14kaAT4P9UhTUSNficc9W5DlWZWJQ/132" width="30px"><span>silence</span> 👍（0） 💬（3）<div>请问安装好环境后在www目录执行.&#47;run.sh start 老是command not found怎么解决</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fa/51/5da91010.jpg" width="30px"><span>Miroticwillbeforever</span> 👍（0） 💬（2）<div>老师我有个问题。实验环境搭建好了。前两讲的实验也做成功了。
但是当我用浏览器 访问 www.chrono.com 时，它跳转到的 地址为 https:&#47;&#47;dp.diandongzhi.com&#47;?acct=660&amp;site=chrono.com 然后wireshark抓包并没有任何反应。我想问一下是我操作不当的原因还是怎么回事。课程大部分听完了。但是后面实验没做成挺难受的，没有去验证。等老师给个答复准备二刷！</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/55/aa/e05a5778.jpg" width="30px"><span>武安君</span> 👍（0） 💬（1）<div>老师你好、我安装好了openrestry后、启动服务说 nginx：invalid option：http，请问是怎么回事呀</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（0） 💬（2）<div>不行啊，老师，我的那个openresty界面出来了，就是抓不到包！用的wireshark .搞了好久。那个telnet也安装了。是不是那步出错了 ，我就直接运行openresty，然后用抓包工具过滤信息，然后浏览器输入localhost，浏览器洁界面也出来了。</div>2021-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/17/69cca649.jpg" width="30px"><span>旗木卡卡</span> 👍（0） 💬（3）<div>Mac电脑，耗费本人2个晚上的环境，终于搭好了，碰到了2个坑，第一个是dns查找不到，brew install openresty时，需要在本机的hosts文件，加上解析不到的url的ip地址，第二个是启动一直bind不上，nginx就自动启动了，但是很明显不是openresty，然后用root权限启动成功，也可以正常访问，发现是nginx.conf的user权限问题，修改成本机的用户user kaka(你的用户名) staff;即可。 </div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/18/b3/848ffa10.jpg" width="30px"><span>Jinlee</span> 👍（0） 💬（1）<div>Welcome to HTTP Study Page! 还好我看得迟，成功在ubuntu下搭建起环境😊😊😊</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（0） 💬（1）<div>最喜欢实验环境了，之前学习就是苦于没实验环境浪费了几年时间。</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（0） 💬（2）<div>Updating Homebrew...
==&gt; Auto-updated Homebrew!
Updated 1 tap (homebrew&#47;core).
==&gt; Updated Formulae
handbrake

==&gt; Installing openresty from openresty&#47;brew
==&gt; Downloading https:&#47;&#47;openresty.org&#47;download&#47;openresty-1.15.8.2.tar.gz
Already downloaded: &#47;Users&#47;hejunbin&#47;Library&#47;Caches&#47;Homebrew&#47;downloads&#47;4395089f0fd423261d4f1124b7beb0f69e1121e59d399e89eaa6e25b641333bc--openresty-1.15.8.2.tar.gz
==&gt; .&#47;configure -j8 --prefix=&#47;usr&#47;local&#47;Cellar&#47;openresty&#47;1.15.8.2 --pid-path=&#47;us
Last 15 lines from &#47;Users&#47;hejunbin&#47;Library&#47;Logs&#47;Homebrew&#47;openresty&#47;01.configure:
DYNASM    host&#47;buildvm_arch.h
HOSTCC    host&#47;buildvm.o
HOSTLINK  host&#47;buildvm
BUILDVM   lj_vm.S
BUILDVM   lj_ffdef.h
BUILDVM   lj_bcdef.h
BUILDVM   lj_folddef.h
BUILDVM   lj_recdef.h
BUILDVM   lj_libdef.h
BUILDVM   jit&#47;vmdef.lua
make[1]: *** [lj_folddef.h] Segmentation fault: 11
make[1]: *** Deleting file `lj_folddef.h&#39;
make[1]: *** Waiting for unfinished jobs....
make: *** [default] Error 2
ERROR: failed to run command: gmake -j8 TARGET_STRIP=@: CCDEBUG=-g XCFLAGS=&#39;-msse4.2 -DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT&#39; CC=cc PREFIX=&#47;usr&#47;local&#47;Cellar&#47;openresty&#47;1.15.8.2&#47;luajit

If reporting this issue please do so at (not Homebrew&#47;brew or Homebrew&#47;core):
  https:&#47;&#47;github.com&#47;openresty&#47;homebrew-brew&#47;issues

These open issues may also help:
Can&#39;t install openresty on macOS 10.15 https:&#47;&#47;github.com&#47;openresty&#47;homebrew-brew&#47;issues&#47;10
Fails to install OpenResty https:&#47;&#47;github.com&#47;openresty&#47;homebrew-brew&#47;issues&#47;5
The openresty-debug package should use openresty-openssl-debug instead https:&#47;&#47;github.com&#47;openresty&#47;homebrew-brew&#47;issues&#47;3

macOS 10.15.1 安装失败。参考给出的链接也没有解决问题，求老师解惑。</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/d6/76fe5259.jpg" width="30px"><span>Dream.</span> 👍（0） 💬（5）<div>Linux-CentOS 7下，修改了&#47;etc&#47;hosts的域名与IP的映射关系后

再使用.&#47;run.sh start启动OpenResty之后

curl localhost 或者 curl http:&#47;&#47;www.chrono.com都是返回403

按之前课程里的url访问https:&#47;&#47;www.chrono.com&#47;11-1什么的，都返回404

第一次接触OpenResty，麻烦老师回复下是哪里没配置好嘛？</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师又来了，很高兴再次见到老师。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a6/0b/d296c751.jpg" width="30px"><span>果果</span> 👍（0） 💬（1）<div>当初费了好些时间，才在mac上搭建了环境</div>2019-10-09</li><br/>
</ul>