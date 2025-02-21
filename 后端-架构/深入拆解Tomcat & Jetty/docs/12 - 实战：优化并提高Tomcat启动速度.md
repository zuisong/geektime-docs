到目前为止，我们学习了Tomcat和Jetty的整体架构，还知道了Tomcat是如何启动起来的，今天我们来聊一个比较轻松的话题：如何优化并提高Tomcat的启动速度。

我们在使用Tomcat时可能会碰到启动比较慢的问题，比如我们的系统发布新版本上线时，可能需要重启服务，这个时候我们希望Tomcat能快速启动起来提供服务。其实关于如何让Tomcat启动变快，官方网站有专门的[文章](https://wiki.apache.org/tomcat/HowTo/FasterStartUp)来介绍这个话题。下面我也针对Tomcat 8.5和9.0版本，给出几条非常明确的建议，可以现学现用。

## 清理你的Tomcat

**1. 清理不必要的Web应用**

首先我们要做的是删除掉webapps文件夹下不需要的工程，一般是host-manager、example、doc等这些默认的工程，可能还有以前添加的但现在用不着的工程，最好把这些全都删除掉。如果你看过Tomcat的启动日志，可以发现每次启动Tomcat，都会重新布署这些工程。

**2. 清理XML配置文件**

我们知道Tomcat在启动的时候会解析所有的XML配置文件，但XML解析的代价可不小，因此我们要尽量保持配置文件的简洁，需要解析的东西越少，速度自然就会越快。

**3. 清理JAR文件**

我们还可以删除所有不需要的JAR文件。JVM的类加载器在加载类时，需要查找每一个JAR文件，去找到所需要的类。如果删除了不需要的JAR文件，查找的速度就会快一些。这里请注意：**Web应用中的lib目录下不应该出现Servlet API或者Tomcat自身的JAR**，这些JAR由Tomcat负责提供。如果你是使用Maven来构建你的应用，对Servlet API的依赖应该指定为`<scope>provided</scope>`。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（58） 💬（5）<div>调大vm xms xmx避免反复扩容堆内存
换上固态硬盘可以提速xml文件读取
server.xml去掉监听
去掉不要的ajp
去掉多余的连接器
线程池的核心线程设置延迟初始化
去掉access log，因为nginx里已有access log
减少项目里多余的jar
精确设置mvc注解的包扫描范围
xml spring bean设置延迟初始化
数据库连接池初始化数量减少</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（37） 💬（1）<div>请问老师，对于SpringBoot内嵌的Tomcat，怎么来优化呢？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/68/92caeed6.jpg" width="30px"><span>Shine</span> 👍（10） 💬（5）<div>老师，这种tomcat启动优化很少用到吧。貌似很多人都不太关心tomcat启动优化</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（7） 💬（1）<div>startStopThreads 的值表示你想用多少个线程来启动你的 Web 应用，如果设成 0 表示你要并行启动 Web 应用，像下面这样的配置。
startStopThreads=0默认会用多少个线程呢？是会用系统所有能调度的线程吗？</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/4e/2acbc3a8.jpg" width="30px"><span>vvsuperman</span> 👍（2） 💬（2）<div>压测的时8c8g，做的mock请求(空请求，立即返回)，并发500 tomcat 8 tps才600，如何提高tps呢？</div>2019-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/UPGlgUiaSPVEhqiboDqkTMY1oGAImROZRfyrCvnVfvDKrpaaQ15qBZsEn3Q83mKYYyiaUDib3qsyV31VlRqUibpjUmQ/132" width="30px"><span>小呆娃</span> 👍（2） 💬（1）<div>老师，请教您一个问题，tomcat启动的时候卡在loadClass，这个一般是什么问题呢？能给个排查的思路吗？谢谢老师</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/50/c23cf47d.jpg" width="30px"><span>李</span> 👍（1） 💬（1）<div>为什么要删除logs下不需要的日志文件</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/7f/b20cc3a6.jpg" width="30px"><span>小胖</span> 👍（5） 💬（0）<div>双哥能出个netty或者dubbo专栏吗😍</div>2020-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5XxiaGg3QRVLcQNw3jfzlVtXE6MbFD4nEQkIibEuM2ekic23qN1aGOZP58NhBeibHd8XN4x626icFSlw0VI5tMiauNWA/132" width="30px"><span>lulu</span> 👍（2） 💬（3）<div>请教一个问题。我对应用进行服务器的迁移，从上海机房迁移北京机房。发现Tomcat启动变得非常慢。原来在上海机房部署应用的Tomcat启动20482 ms，现在在北京机房216643 ms，时间变成了10倍。已经排除了redis、mysql连接的问题。也不是安全随机数慢的问题。通过strace、jstack也没有找到什么原因。请问老师我改怎么调查，怎么解决。谢谢。</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/08/66541a84.jpg" width="30px"><span>Visual C++</span> 👍（1） 💬（2）<div>我的环境是docker centos tomcat8，按你设置，还要20妙启动</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/d5/20/1aacda3c.jpg" width="30px"><span>困兽</span> 👍（0） 💬（0）<div>我有个问题。像JSP和websocket这种要扫描所有jar的逻辑应该只要扫描一次就可以获得它们两个功能要获得的东西了。不需要每个功能都扫描一遍。那如果是这样的话。只关闭JSP功能是不是没用。因为websocket功能还是需要扫描所有jar</div>2023-05-21</li><br/><li><img src="" width="30px"><span>边宸</span> 👍（0） 💬（0）<div>老师你用的版本是什么啊，我网上查了一下配置tld扫描是在context标签里面直接配processtlds=false</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/c8/8627f5c1.jpg" width="30px"><span>右耳朵猫咪</span> 👍（0） 💬（0）<div>老师，tomcat因为hikari连接超时而宕机是怎么回事儿呢？</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/fc/d3cecfb2.jpg" width="30px"><span>Vainycos</span> 👍（0） 💬（2）<div>老师您好，在提高tomcat启动效率的方法中，您提到可以删除不必要的默认应用：host-manager&#47;examples&#47;docs。但是默认的应用了还有ROOT以及manager，请问这两个应用是不能随便删的是吗，分别有他各自的作用还是会影响到部署的应用，请教一下老师。</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/23/73569bd7.jpg" width="30px"><span>xj_zh</span> 👍（0） 💬（0）<div>老师，可以把每一讲的资料单独整理成一片文章呢吗，这样方便快速查找。
比如：
tomcat的源码连接，推荐阅读的一些资料。谢谢！</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（0） 💬（0）<div>关于session ID的生成，tomcat为什么不默认指定采用非阻塞模式生成？</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/08/66541a84.jpg" width="30px"><span>Visual C++</span> 👍（0） 💬（0）<div>有没有更大优化空间?</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（0） 💬（0）<div>学到了</div>2019-06-06</li><br/>
</ul>