你好，我是Chrono。

在上一次课里，我们了解了容器技术中最核心的概念：容器，知道它就是一个系统中被隔离的特殊环境，进程可以在其中不受干扰地运行。我们也可以把这段描述再简化一点：**容器就是被隔离的进程**。

相比笨重的虚拟机，容器有许多优点，那我们应该如何创建并运行容器呢？是要用Linux内核里的namespace、cgroup、chroot三件套吗？

当然不会，那样的方式实在是太原始了，所以今天，我们就以Docker为例，来看看什么是容器化的应用，怎么来操纵容器化的应用。

## 什么是容器化的应用

之前我们运行容器的时候，显然不是从零开始的，而是要先拉取一个“镜像”（image），再从这个“镜像”来启动容器，像[第一节课](https://time.geekbang.org/column/article/528619)这样：

```plain
docker pull busybox      
docker run busybox echo hello world
```

那么，这个“镜像”到底是什么东西呢？它又和“容器”有什么关系呢？

其实我们在其他场合中也曾经见到过“镜像”这个词，比如最常见的光盘镜像，重装电脑时使用的硬盘镜像，还有虚拟机系统镜像。这些“镜像”都有一些相同点：只读，不允许修改，以标准格式存储了一系列的文件，然后在需要的时候再从中提取出数据运行起来。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WrANpwBMr6DsGAE207QVs0YgfthMXy3MuEKJxR8icYibpGDCI1YX4DcpDq1EsTvlP8ffK1ibJDvmkX9LUU4yE8X0w/132" width="30px"><span>星垂平野阔</span> 👍（28） 💬（1）<div>作业1：
容器镜像比起这些安装包的差别就在于通用，不同linux版本下的安装包还不同。
作业2:
run是针对容器本身启动，而exec是进入了容器内部去跑命令，相当于进去操作系统跑应用。</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/8a/e7c5a7e2.jpg" width="30px"><span>sky</span> 👍（10） 💬（1）<div>还有一些命令docker  save,docker  load,docker stats,docker cp也很有用</div>2022-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（8） 💬（1）<div>老师后面的课程是会用k8s带领我们模拟真实场景，部署应用吗？

「纸上得来终觉浅」。</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/e1/f663213e.jpg" width="30px"><span>拾掇拾掇</span> 👍（7） 💬（3）<div>我实操了下，nginx:alpine 和 nginx:1.21-alpine image_id是不一样的，我猜是被更新了导致image_id不一样了，因为created也不一样</div>2022-06-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJk3PElN2J96DtyWuIg6xPSs3zRFsIMibOvIn5kuRkESORsRIkDJMUekymI2wiaYiaP0UzibXWEl0aLYw/132" width="30px"><span>Bill</span> 👍（7） 💬（4）<div>1.容器镜像通过分层打包，安装所有依赖包，并可以在主机上共享使用，减少存储空间需求，它与 rpm、deb 安装包作为某一个功能的所有依赖包安装，聚焦某个命令的上下文，容器是整个应用的打包。
2.docker run利用镜像运行容器，拥有丰富的启动参数，如挂载volume，端口映射等。是容器运行启动的基础。docker exec启动session，在一个已运行的容器中执行命令，仅当PID 1进程存在时运行，容器重启后，session将失效。</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（6） 💬（1）<div>苦于没有docker入门，耗费大量时间，这教程真是太creat了。
大佬的课我全入了，对你的讲述感觉十分易懂，不需要绕弯理解，nice的。
等我cpp入门，去试试你们公司</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（5） 💬（1）<div>1. 课外贴士的第四条，有同学问了，怎么删除，老师的回答我没太明白，最佳实践是如何操作呢？

2. 想听听老师的回答：docker run 和 docker exec 的区别在哪里？</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（4） 💬（2）<div>老师，课外贴士中的第4条如何删除呢？有时候强制删除也没用</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/fb/96/791d0f5e.jpg" width="30px"><span>小伙儿</span> 👍（3） 💬（1）<div>docker镜像和rpm包的区别

镜像在打包推送到仓库后不管在那个操作系统中都能运行，而rpm包不行
docker镜像中包含了完整的应用依赖和系统环境，而rpm包则没有
镜像比较能节约磁盘空间，如果镜像的部分层已经在本地中有了，就可以直接复用，rpm包不行


docker的run和exec的区别

run是从镜像创建运行一个容器的必备命令，exec则是在已经运行的容器中执行另外一个程序，他们的优先级是先run后exec。</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（3） 💬（1）<div>老师好，想问一个问题，那就是k8s的container和docker容器有什么区别吗，我使用dockerfile打包一个镜像，在docker环境中是可以打包成功，但是放到使用k8s的jenkins流水线上，就无法打包成功，云平台相关工程师告诉我可能是k8s和docker的不兼容导致的，想请问一下这个问题</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（2） 💬（1）<div>之前一直以为IMAGE ID是随机的，又学到了，原来是跟镜像文件相关的，特意去看了一下，不同的机器上的同一个image的同一个tag，IMAGE ID确实是一样的</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/86/23/fe95fdf7.jpg" width="30px"><span>Jarvis Chan</span> 👍（1） 💬（1）<div>chrono真的太牛了，真的是小白都能快速上手，沉淀多年才有这么深入浅出的能力</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（1） 💬（1）<div>问题1: 说一说你对容器镜像的理解，它与 rpm、deb 安装包有哪些不同和优缺点。
主要在可移植性和隔离性上不同: 容器镜像依赖于容器环境, 一次打包处处运行; 而rpm,deb等安装包依赖与特定的操作系统环境.

优缺点对比: 可移植性与隔离性强的容器技术, 在性能上肯定不如直接安装在本地的应用包, 是优点也是缺点.看解决的问题场景是什么.

如果要解决的问题是移植性, 打包部署的方便, 当然选择容器技术. </div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（1） 💬（1）<div>补充一下：
一次停止所有容器：docker stop `docker ps -a -q`
一次删除所有容器：docker rm    `docker ps -a -q`</div>2023-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/21/56/91669d26.jpg" width="30px"><span>ReCharge</span> 👍（1） 💬（1）<div>买了老师很多的专栏了，每次都受益匪浅，老师能分享下学习新知识的方法么？如何能够做到这么深入浅出的。。</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/91/6606a3c5.jpg" width="30px"><span>A-Bot</span> 👍（1） 💬（1）<div>为什么我刚执行docker run -it --name ubuntu ad0 sh  ，用docker ps -a 查到他的状态就是Exited？</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（1） 💬（1）<div>docker 镜像运行以后，如果想要删除镜像，需要通过 docker rm [xxx containerId]（可以通过 docker ps -a 查看 containerId）删除容器，才能通过 docker rmi [xxx imageId] 删除镜像。</div>2022-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/07/7804f4cc.jpg" width="30px"><span>逗逼师父</span> 👍（1） 💬（1）<div>1. 容器镜像就是预先配置好的一个带有操作系统的环境；rpm, deb包与当前操作系统是强依赖关系，还会依赖于其他应用等，而容器镜像只要在装有docker的机器上pull下来就能用了，运行起来就是一套独立的环境。
2. run是用指定镜像创建一个新的容器并运行；exec是在已经运行的容器中执行命令。</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，执行docker images 命令，展示栏的 CREATED 代表的是这个 镜像仓库最近的版本更新情况吗？</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3e/57/51/b69b3a7a.jpg" width="30px"><span>小天才清歌</span> 👍（0） 💬（1）<div>思考题【一】：
镜像不但包含了基本的可执行文件，还包含了运行环境，这让镜像有很好的跨平台和兼容性
（老师文章中间黑体加粗部分）
思考题【二】：
docker run 把静态应用动起来，变成动态的容器，即：容器化的应用
docker exec  在容器中内执行另一程序
</div>2025-02-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/gdrRWp2Q9wJ4P2NcLxLicuvhHKwFSk7QkeBOEAo0hJtPo9Y94hrRm631o7mtBaBclBZvZko7oHXecURpWuBJBQA/132" width="30px"><span>Geek_6e3c78</span> 👍（0） 💬（1）<div>1、rpm包这些依赖操作系统安装其他基础软件，比如gc++等，而镜像只对操作系统架构有依赖；
2、docker run 是生成一个容器并执行命令，docker exec 是基于一个已运行的容器执行命令；docker exec我常用于进入容器终端</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/0f/acc7342c.jpg" width="30px"><span>shadow</span> 👍（0） 💬（1）<div>老师，有视频课程么？</div>2023-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（1）<div>总是听说 docker 会把应用的依赖和环境都打包好，然后又听说 docker 是基于宿主机的内核的，和虚拟机不同。
这里就比较懵了，docker 打包的到底是什么东西呢？</div>2023-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（1）<div>1. 说一说你对容器镜像的理解，它与 rpm、deb 安装包有哪些不同和优缺点。
容器镜像具有一个一次打包，到处运行的特点。而其他的安装包在不同的操作系统上是不同的。
2. 你觉得 docker run 和 docker exec 的区别在哪里，应该怎么使用它们？
docker run 是针对镜像而言，基于一个镜像启动一个容器；
docker exec 是针对已经启动的容器而言，执行命令和操作。</div>2023-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（1）<div>1.容器镜像更像是一个完整的操作系统+环境、rpm、deb是软件安装包；
2.docker run是运行一个容器，docker exec是进入容器；</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/0c/a5/344c1ea2.jpg" width="30px"><span>V.</span> 👍（0） 💬（3）<div>&quot;docker run -it --name ubuntu 2e6 sh   # 使用IMAGE ID，登录Ubuntu18.04&quot;
这个是不是错了呀 会提示找不到2e6 这个镜像，我改成“--name 2e6 ubuntu ” 就可以启动了</div>2023-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/50/8d/ded8482f.jpg" width="30px"><span>一久</span> 👍（0） 💬（1）<div>问题一：
容器镜像可以是一个打包好的应用系统文件，里面包含了基础镜像和服务依赖，可以跨同架构的多个发行版Linux系统上运行；rpm和deb包是Linux某个功能的安装包文件，在支持相应包管理的系统下才可以安装使用
问题二：
docker run是运行一个容器；docker exec是进入已运行的容器</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/e4/7061abd5.jpg" width="30px"><span>Mr.J</span> 👍（0） 💬（1）<div>镜像运行起来是容器？那容器stop掉之后又是什么？还是有点模糊
另外exec是进入已有的容器，无论容器是运行中还是stop的？</div>2023-01-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/prLO6VIcvsXMibOichyNgeMmgDlh8nS7q4F9a0PCkrL0OypFj0dQicDMRH0El7sdOF6srhJyKsfRNQJe10IJwHhoQ/132" width="30px"><span>一行</span> 👍（0） 💬（1）<div>思考1：说一说你对容器镜像的理解，它与 rpm、deb 安装包有哪些不同和优缺点。
容器的技术基础是 namespace、cgroup、chroot，实现了对应用依赖、运行环境的打包，并且可以对应用运行所需的资源进行限制。 可以快速运行在任何有容器的环境中。 一处打包，处处运行。
rpm、deb是linux支持的一种应用打包方式，只能在特定的发行版本中运行，对应用运行时的依赖处理比较麻烦。

思考2：你觉得 docker run 和 docker exec 的区别在哪里，应该怎么使用它们？
类似 linux系统中的 su 与 sudo 命令。</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（0） 💬（1）<div>容器底层原理使用三件套，容器镜像也能附带其他操作系统或其他版本的库，在容器实际执行时候，是否会与源系统库打架的问题？镜像中老是重复保存相同的操作系统库，是不是也是一种浪费？</div>2022-12-07</li><br/>
</ul>