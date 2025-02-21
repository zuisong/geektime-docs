你好，我是何为舟。

在[13讲](https://time.geekbang.org/column/article/186777)中，我们讲了Linux系统安全。但是，当你在和同事讨论Linux系统安全的时候，同事表示，公司的服务都是通过Docker来进行容器化部署的。开发在操作中，并不会接触实际的Linux服务器，所以不会去关注Linux安全 。而且，因为容器是隔离的，就算容器被黑客攻击了，也只是容器内部受到影响，对宿主的Linux系统和网络都不会产生太大影响。

事实上，我知道很多人都有这种想法。但是，你在学习了安全专栏之后，可以试着思考一下，开发使用了Docker就一定安全吗？真的可以不用考虑安全问题了吗？

以防你对Doker还不是很了解，在解决这些问题之前，我先来解释一下这节课会涉及的3个概念，帮你扫清概念障碍。

- Docker服务：Docker所提供的功能以及在宿主机Linux中的Docker进程。
- Docker镜像：通过Dockerfile构建出来的Docker镜像。
- Docker容器：实际运行的Docker容器，通常来说，一个Docker镜像会生成多个Docker容器。Docker容器运行于Docker服务之上。

了解了这3个关键概念之后，我们今天就从这些概念入手，来谈一谈Docker的安全性。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/b9/740b3563.jpg" width="30px"><span>陈优雅</span> 👍（2） 💬（1）<div>由于容器里面也可以运行程序，怎么保证正在运行的容器不被篡改？或者怎么发现容器是否被入侵？</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/3a/5e/e69d10bd.jpg" width="30px"><span>liguoping</span> 👍（1） 💬（1）<div>何老师，看了dock安全服务讲解，对镜像、服务、进程有了初步安全理解，୧(๑•̀◡•́๑)૭。
我们在开发和上线部署运维中如何做一些安全设计、安全checklist等，请教下</div>2020-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（1）<div>     记得2019年11月GOPS问过胥峰老师：云与云之间的安全策略其实是需要考虑的，不过如何做没过多提及；这又是一个现在最常见的场景；不知道老师有没有什么好的策略分享一下，或者放在《特别加餐》里面帮大家解决一下这种公共场景，毕竟企业稍微大点就会出现这种情况-跨云之间的安全策略。
      谢谢老师今天的分享：希望老师能针对这种典型场景给大家分享一下老师的解决策略。 </div>2020-01-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7WkTI1IicbKvsPJng5vQh5qlrf1smbfl2zb7icHZfzcAk1k4lr8w8IDEAdrqq1NHW5XZMPXiaa1h7Jn1LGOWOCkIA/132" width="30px"><span>早起不吃虫</span> 👍（14） 💬（1）<div>老师每篇结尾的总结真的是太棒了！</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（3） 💬（0）<div>这节课很棒，目前学习了 Docker相关的知识，一直对安全这块了解的比较泛泛，现在有了一个相对系统的认识；</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f0/81/8d539cba.jpg" width="30px"><span>王凯</span> 👍（1） 💬（0）<div>学习了两个新知识点：
1. docker远程API
2. slim 或者 alpine标签的意义
谢谢</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/95/b6/20f1470d.jpg" width="30px"><span>小短腿儿</span> 👍（0） 💬（0）<div>看表格里面，docker是用capabilities来实现的namespace的意思？</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e3/d7/d7b3505f.jpg" width="30px"><span>官</span> 👍（0） 💬（0）<div>在单机上使用过Docker和Anaconda，说实话之前从没想过这类的安全问题，看来以后业务拓展需要上云得多加考虑了</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/47/fd/895f0c27.jpg" width="30px"><span>Cy23</span> 👍（0） 💬（0）<div>一直还没有考虑docker还得注意安全性问题，看来以后再看docker的时候需要注意一下。</div>2020-01-15</li><br/>
</ul>