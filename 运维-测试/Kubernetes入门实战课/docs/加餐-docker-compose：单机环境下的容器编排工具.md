你好，我是Chrono。

我们的课程学到了这里，你已经对Kubernetes有相当程度的了解了吧。

作为云原生时代的操作系统，Kubernetes源自Docker又超越了Docker，依靠着它的master/node架构，掌控成百上千台的计算节点，然后使用YAML语言定义各种API对象来编排调度容器，实现了对现代应用的管理。

不过，你有没有觉得，在Docker和Kubernetes之间，是否还缺了一点什么东西呢？

Kubernetes的确是非常强大的容器编排平台，但强大的功能也伴随着复杂度和成本的提升，不说那几十个用途各异的API对象，单单说把Kubernetes运行起来搭建一个小型的集群，就需要耗费不少精力。但是，有的时候，我们只是想快速启动一组容器来执行简单的开发、测试工作，并不想承担Kubernetes里apiserver、scheduler、etcd这些组件的运行成本。

显然，在这种简易任务的应用场景里，Kubernetes就显得有些“笨重”了。即使是“玩具”性质的minikube、kind，对电脑也有比较高的要求，会“吃”掉不少的计算资源，属于“大材小用”。

那到底有没有这样的工具，既像Docker一样轻巧易用，又像Kubernetes一样具备容器编排能力呢？
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（4） 💬（1）<div>相比于 kubernetes，docker-compose 不就是大道至简吗？</div>2022-11-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rURvBicplInVqwb9rX21a4IkcKkITIGIo7GE1Tcp3WWU49QtwV53qY8qCKAIpS6x68UmH4STfEcFDJddffGC7lw/132" width="30px"><span>onemao</span> 👍（4） 💬（1）<div>docker compose对开发来说最大的作用就是本地快速拥有数据库，消息中间件等等，无需单独安装，随时用随时删除。而且只要写好文件放到repo,idea中点一下可以一键运行和初始化，也极大方便本地开发与本地集成测试。</div>2022-08-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIaexL1b8o76RqM4F2PZhWYGxsic2EuFSWWh5IhibqfdjcDzJbhlcag1z0rECfUo0vZREbMyiaW7P8XA/132" width="30px"><span>青储</span> 👍（4） 💬（1）<div>这个可以用在小型公司生产线上吗？</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>docker-compose 的默认配置文件名称为： docker-compose.yml
 -f, --file FILE             Specify an alternate compose file
                              (default: docker-compose.yml)

2. </div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题：
Q1：docker-compose只能用在单机环境，不能用在集群吗？
Q2：文中创建的第一个docker是干什么用的？
文中用了这个命令“docker run -d -p 5000:5000 registry”，请问创建这个有什么用？
是不是这样：用“docker run -d -p 5000:5000 registry”可以启动一个容器。用yaml文件，用“docker-compose -f reg-compose.yml up -d”，也可以达到同样的目的。

Q3：需要先搭建一个本地registry吗？
执行“docker push 127.0.0.1:5000&#47;nginx:v1”后报错：
The push refers to repository [127.0.0.1:5000&#47;nginx]
Get &quot;http:&#47;&#47;127.0.0.1:5000&#47;v2&#47;&quot;: dial tcp 127.0.0.1:5000: connect: connection refused
突然感觉Q2中创建的应用就是本地registry，对吗？</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8f/52/3eebca1e.jpg" width="30px"><span>Max</span> 👍（1） 💬（2）<div>docker-compose转写成k8s yaml有什么建议吗？
尝试使用了kompose convert工具，发现还是有很多配置无法覆盖到，比如env的引入方式就不一样。</div>2023-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（1）<div>原来 docker-compose 从 v1.27 版本开始将 version 字段给“干掉”了，再也不用理会 version: &quot;3&quot;，version: &quot;3.9&quot;，version: &quot;2&quot; 了 😂 。

为啥我之前没觉得这玩意有点反人类呢？嗯，缺少批判性思维。</div>2022-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（1） 💬（1）<div>apt install docker-compose 
为docker-compose version 1.29.2, build unknown
不是最新版的</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（1） 💬（2）<div>如果安装成docker compose plugin的形式，即没有中间的横线，harbor安装会有问题，因为检测不到docke-compose😂</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>我说怎么安装docker-compose教程差异那么大 有的要下载python 有的直接下来个可执行文件 </div>2024-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>mac笔记本... 好久前安装的, Docker Desktop 直接内部带了docker compose , 适用命令,  没有中划线-

--停止
docker compose -f docker-compose-wp.yml down
--启动
docker compose -f docker-compose-wp.yml up -d 

-- 进入到容器内
docker compose -f docker-compose-wp.yml exec nginx sh</div>2024-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/42/a994666a.jpg" width="30px"><span>黄涵宇看起来很好吃</span> 👍（0） 💬（1）<div>docker-compose -f docker-compose.yml exec -it 无法生效
docker exec -it 可以生效
原因可能是什么</div>2023-03-28</li><br/>
</ul>