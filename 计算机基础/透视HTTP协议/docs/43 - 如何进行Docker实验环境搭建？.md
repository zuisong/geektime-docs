你好，我是Chrono。

《透视HTTP协议》这个专栏正式完结已经一年多了，感谢你的支持与鼓励。

这一年的时间下来，我发现专栏“实验环境的搭建”确实是一个比较严重的问题：虽然我已经尽量把Windows、macOS、Linux里的搭建步骤写清楚了，但因为具体的系统环境千差万别，总会有各式各样奇怪的问题出现，比如端口冲突、目录权限等等。

所以，为了彻底解决这个麻烦，我特意制作了一个Docker镜像，里面是完整可用的HTTP实验环境，下面我就来详细说一下该怎么用。

## 安装Docker环境

因为我不知道你对Docker是否了解，所以第一步我还是先来简单介绍一下它。

Docker是一种虚拟化技术，基于Linux的容器机制（Linux Containers，简称LXC），你可以把它近似地理解成是一个“轻量级的虚拟机”，只消耗较少的资源就能实现对进程的隔离保护。

使用Docker可以把应用程序和它相关的各种依赖（如底层库、组件等）“打包”在一起，这就是Docker镜像（Docker image）。Docker镜像可以让应用程序不再顾虑环境的差异，在任意的系统中以容器的形式运行（当然必须要基于Docker环境），极大地增强了应用部署的灵活性和适应性。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/57/6e/f7fa7278.jpg" width="30px"><span>Howard.Wundt</span> 👍（5） 💬（2）<div>首先祝老师教师节快乐！很期待着与老师的重逢。有个问题请教老师：轻量化虚拟机技术除了Docker 外还有其他选择吗？Docker 现在的政治化让人很不舒服。</div>2020-09-10</li><br/><li><img src="" width="30px"><span>Geek_78044b</span> 👍（3） 💬（1）<div>老师确实很敬业，最近刚买了课程，一周多时间快速学习了一篇，开始的破冰篇确实特别基础，我还以为这门科是只针对的初学者的，没什么难度，后面讲http1.1， 2， 3， 安全篇等都还是比较有深度，感谢老师的付出。</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/27/a3737d61.jpg" width="30px"><span>Shanks-王冲</span> 👍（2） 💬（1）<div>谢谢老师的Docker tutorial quick guide，让我对Docker有了fist touch；前几天看Android开发的技术博客时，不知怎么地就跳到Docker官网，并瞧了瞧，没敢下载来玩；但今天又机缘巧合看到这篇文章，I just pulled，感谢老师！</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/51/a0/5db02ac2.jpg" width="30px"><span>點點點，点顛</span> 👍（2） 💬（1）<div>老师教师节快乐😁。感谢老师还记得我们</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（1） 💬（1）<div>Chrono老师，是我在极客时间见过的最负责的老师。</div>2021-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/eHNmzejyQW9Ag5g3EELS1d9pTgJsvxC7CxSCxIFQqeFLXUDT52HWianQWzw14kaAT4P9UhTUSNficc9W5DlWZWJQ/132" width="30px"><span>silence</span> 👍（1） 💬（3）<div>老师请问我在测试tcpdump抓包的时候，将您的命令粘贴进去
tcpdump tcp port 443 -i lo -w &#47;tmp&#47;a.pcap
报了以下错误怎么解决呢？
tcpdump: lo: SIOCETHTOOL(ETHTOOL_GET_TS_INFO) ioctl failed: Function not implemented</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（1） 💬（1）<div>HTTP&#47;3会有个正式的发布会吗。。。我看现在快手和百度，HTTP3都已经在线上用了</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/90/de8c61a0.jpg" width="30px"><span>dongge</span> 👍（1） 💬（1）<div>好敬业。</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（1） 💬（1）<div>
期待再次与老师相会，
谢谢老师！</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，很棒👍🏻！</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/e9/d05b5434.jpg" width="30px"><span>朝阳</span> 👍（0） 💬（1）<div>求教个线上问题:PHP使用curl请求内部地址频繁偶现connect time  out 问题
几个疑问点
①服务请求少出现概率大，请求多出现概率小
②同一项目请求另外一个服务就没有connect timeout  
③其他java服务请求有问题的内部服务没没出现connect timeout 
跪求排查方向～PHP服务是使用contos  docker搭建的</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>打卡</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（0） 💬（1）<div>又学了一点点docker，很棒的体验，认真负责</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/20/491dd5cc.jpg" width="30px"><span>zha.qiang</span> 👍（0） 💬（1）<div>Found a typo:

```
cu加l https:&#47;&#47;www.chrono.com&#47;30-1 -k --tlsv1.2
```</div>2020-10-19</li><br/><li><img src="" width="30px"><span>candy</span> 👍（0） 💬（2）<div>谢谢老师，节日快乐！还建立了镜像，学习更方便了</div>2020-09-10</li><br/>
</ul>