你好，我是Chrono。

学到今天的这次课，我们的“入门篇”就算是告一段落了，有这些容器知识作为基础，很快我们就要正式开始学习Kubernetes。不过在那之前，来对前面的课程做一个回顾和实践，把基础再夯实一下。

要提醒你的是，Docker相关的内容很多很广，在入门篇中，我只从中挑选出了一些最基本最有用的介绍给你。而且在我看来，我们不需要完全了解Docker的所有功能，我也不建议你对Docker的内部架构细节和具体的命令行参数做过多的了解，太浪费精力，只要会用够用，需要的时候能够查找官方手册就行。

毕竟我们这门课程的目标是Kubernetes，而Docker只不过是众多容器运行时（Container Runtime）中最出名的一款而已。当然，如果你当前的工作是与Docker深度绑定，那就另当别论了。

好下面我先把容器技术做一个简要的总结，然后演示两个实战项目：使用Docker部署Registry和WordPress。

## 容器技术要点回顾

容器技术是后端应用领域的一项重大创新，它彻底变革了应用的开发、交付与部署方式，是“云原生”的根本（[01讲](https://time.geekbang.org/column/article/528619)）。

容器基于Linux底层的namespace、cgroup、chroot等功能，虽然它们很早就出现了，但直到Docker“横空出世”，把它们整合在一起，容器才真正走近了大众的视野，逐渐为广大开发者所熟知（[02讲](https://time.geekbang.org/column/article/528640)）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（17） 💬（3）<div>之前对docker的了解很杂乱，知识点很细碎、分散，没有一个整体、清晰的认知。

看过中文互联网上面别人的一些教程，要么照本宣科，要么浅尝辄止。

老师的课程虽然没有做到知识点的面面俱到，当然也不可能做到。但是，算是整体上帮我又重新梳理了一遍docker的整体架构，让我对其认识更加清晰了一些。</div>2022-07-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（10） 💬（1）<div>思考题：
1. 相较于之前只知道容器是用来环境隔离，看完入门篇后，对容器技术有了一个比较宏观和基本的了解，列出来如下：
 1）知道了什么是镜像，以及镜像和容器的关系
 2）知道了 DockerHub 这样的镜像仓库
 3）明白了容器和虚拟机的不同
 4）懂得如何通过 Dockerfile 来构建自己的镜像
 5）理解了 Docker 的整体内部框架 docker client -&gt; docker daemon -&gt; registry
 6) 知道了，也实际操作了一些常用的镜像以及容器相关的指令
。。。

感觉学习到的这些东西可以覆盖工作中大多数的场景了，但是这些知识只能说是运用于小规模的东西。想要把容器技术玩的得心应手，还需了解一些容器应用的最佳实践，和一些工程化的理念和工具

2. 感觉容器编排主要应用于大规模集成应用。可以类比分布式系统，入门篇中讲的知识用在单机应用上是没有问题的，但是规模一旦变大到系统层面，就会出现一些问题，比如如何保证数据一致性？如何保证负载均衡？如何尽可能减少网络故障所带来的影响？如何能保证数据（容器）的持久化等等。。。这些问题需要运用容器编排来解决


另外想请教老师 2 个问题

文章一开始提到容器运行时（Container Runtime）这个概念，该如何理解？这是和容器绑定的一门技术吗？

还有就是，我看你在 curl 指令中直接将本地 IP 127.0.0.1 简写成 127.1，是说 curl 中允许这样的简写，还是说这本身就是一个惯例？

谢谢老师 🙏</div>2022-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（6） 💬（1）<div>

q1: 容器编排技术是有价值的，我之前以为价值不大，只是改变启动和使用方式，增加一些命令。
q2： 容器编排解决的问题是：一些非自动化，而是需要强人工干预的东西，比如网络交互需要知道对方ip地址的情况，虽然可以写自动化脚本，但这个并不通用，所以是一套通用的自动化方案。另外多台机器，自动创建负载均衡，创建路由的配置问题。这些是编排的范围。
</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/ed/d50de13c.jpg" width="30px"><span>mj4ever</span> 👍（5） 💬（1）<div>老师的教程中，ng → wp → db，相互之间是通过容器的 IP 地址来访问，尝试以下两种方法，可以不指定 IP 地址，通过容器名：

1、启动容器时加入了自定义的网络 my_network，类型是 bridge；其原理是容器之间的互联是通过 Docker DNS Server；代码如下
docker run -d --rm --name db1 \
    --network my_network \
    --env MARIADB_DATABASE=db \
    --env MARIADB_USER=wp \
    --env MARIADB_PASSWORD=123 \
    --env MARIADB_ROOT_PASSWORD=123 \
    mariadb:10

docker run -d --rm --name wp1 \
    --network my_network \
    --env WORDPRESS_DB_HOST=db1 \
    --env WORDPRESS_DB_USER=wp \
    --env WORDPRESS_DB_PASSWORD=123 \
    --env WORDPRESS_DB_NAME=db \
    wordpress:5

vi wp.conf
server {
  listen 80;
  default_type text&#47;html;

  location &#47; {
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_pass http:&#47;&#47;wp1;
  }
}

docker run -d --rm --name ng1 \
    --network my_network \
    -p 80:80 \
    -v `pwd`&#47;wp.conf:&#47;etc&#47;nginx&#47;conf.d&#47;default.conf \
    nginx:alpine

2、启动 WordPress wp1 时，link 到 db1，即--link db1:db1，  启动 Nginx ng1 时，link 到 wp1，即--link wp1:wp1；其原理是容器之间的互联是通过容器里的 &#47;etc&#47;hosts；代码如下
docker run -d --rm --name db1 \
    --env MARIADB_DATABASE=db \
    --env MARIADB_USER=wp \
    --env MARIADB_PASSWORD=123 \
    --env MARIADB_ROOT_PASSWORD=123 \
    mariadb:10

docker run -d --rm --name wp1 \
    --link db1:db1 \
    --env WORDPRESS_DB_HOST=db1 \
    --env WORDPRESS_DB_USER=wp \
    --env WORDPRESS_DB_PASSWORD=123 \
    --env WORDPRESS_DB_NAME=db \
    wordpress:5

vi wp.conf
server {
  listen 80;
  default_type text&#47;html;

  location &#47; {
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_pass http:&#47;&#47;wp1;
  }
}

docker run -d --rm --name ng1 \
    --link wp1:wp1 \
    -p 80:80 \
    -v `pwd`&#47;wp.conf:&#47;etc&#47;nginx&#47;conf.d&#47;default.conf \
    nginx:alpine</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/bb/74/edc07099.jpg" width="30px"><span>柳成荫</span> 👍（5） 💬（1）<div>1. 刚开始学容器的时候觉得容器就是一个小的虚拟机，部署一套应用应该可以把中间件和应用都部署到同一个容器中，每个容器都应该对外暴露端口才能被访问，现在觉得有些应用可以不用暴露端口，反而更加安全
2. 容器编排应该会解决容器启动、维护的麻烦，应用集群等问题
请教一个问题，部署一个java应用，jdk应该安装在宿主机还是应用的容器里面呢？</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/3f/1f529b26.jpg" width="30px"><span>henry</span> 👍（4） 💬（1）<div>2022&#47;08&#47;16，docker pull mariadb:10，会有问题，docker run 时报错：[ERROR] [Entrypoint]: mariadbd failed while attempting to check config，Can&#39;t initialize timers.

docker pull mariadb:10.8.2  解决问题，参考如下：
https:&#47;&#47;github.com&#47;MariaDB&#47;mariadb-docker&#47;issues&#47;434</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/91/6606a3c5.jpg" width="30px"><span>A-Bot</span> 👍（4） 💬（2）<div>
docker run -d --rm \
    -p 80:80 \
    -v `pwd`&#47;wp.conf:&#47;etc&#47;nginx&#47;conf.d&#47;default.conf \
    nginx:alpine
老师，这个命令中 -v 后面跟的 &#39;pwd&#39; 什么意思？</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（4） 💬（1）<div>老师，有几个小问题：

Q1：k8s应该算是容易编排技术吧？如果学会了k8s的日常操作，关于docker的使用是不是就可以减少了。了解一个大概就好了，很多操作应该逐渐偏向对k8s的操作？

Q2: 对于容器化的应用来说，如果想从外部访问对应的服务，是不是必须要做端口映射这一步？宿主机的端口需要唯一性，容器应用的端口随意指定，即使多个容器应用有相同的端口。</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（2） 💬（1）<div>1.之前没有容器技术的时候，部署应用各种环境会存在各种的问题，尤其是我司有C++的项目，需要安装依赖，光调试环境就搞得很头疼，现在有了容器技术，打包成镜像，随处可用，很方便；
2.感觉容器编排就是为了大型应用服务的。我们目前有十几个镜像，是用docker-compose用来做项目交付，应对一般场景足够用。但很多公司要求HA，这时候感觉上k8s感觉好一点，可扩展性好，快速扩容，我们也在往这个方向发展，所以自己有空来学习学习。</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（1）<div>从头到尾跟到了现在，再加上本节课的实战，深切地感受到了容器化对于开发和运维方式的重塑。老师的课程深入浅出，受益匪浅~</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题：
Q1：镜像的“层”复用的问题：
--- 下载两个镜像A和B，这两个镜像都有一个层“M”，那么，这个层“M”在两个镜像中各存在一份，另外，docker会将此层“M”在宿主机上单独存一份，即在宿主机上，层“M”会存在三份，是这样吗？
--- 镜像A和B运行的时候，A的容器中有层“M”，B的容器中也有层“M”，是吗？
--- 镜像A在同一台宿主机上可以运行多个容器吗？如果可以，比如运行3个容器，那么，每个容器都有层“M”，对吗？
Q2：用rmi删除镜像后，镜像不存在了，但其包含的层还存在宿主机上，对吗？
这个问题和Q1有点关联，比如下载镜像A，其中含有层“M”，用rmi删除镜像后，镜像不存在了，其包含的层“M”不存在了，但宿主机上其实还有一份层“M”，对吗？
Q3：wordpress例子中，为什么nginx可以访问WP？
Wp没有对外暴露端口，而nginx对于WP来说就是外部访问者啊，应该不能访问才对啊。
Q4：小贴士的第一项中，挂载用法问题： 
 --- 挂载方法：  -v   &#47;home&#47;zhangsan   &#47;var&#47;lib&#47;registry， 其中&#47;home&#47;zhangsan是宿主机上的目录，是这样用吗？  
--- 挂载后，是把镜像本身放到&#47;home&#47;zhangsan下面吗？ 还是说，镜像不放在&#47;home&#47;zhangsan下面，但会把镜像用到的数据放到&#47;home&#47;zhangsan下面？</div>2022-07-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ1VPGSQg7SqrN1Gutx31Kicks2icZjTCg1gZoDLfEcSSricYD6l5qQgE3MkMpqlhkM4gMicymOYzaudg/132" width="30px"><span>可可</span> 👍（1） 💬（1）<div>当我对wp.conf文件做了修改之后，执行nginx -t成功，但执行nginx -s reload却提示nginx 29#29: signal process started，发现修改并未生效。请问老师和其他同学遇到过这种情况吗？
我的解决办法是只能删除nginx容器后重新创建，这时候wp.conf就是生效的。但总不可能每次修改配置文件都重新创建nginx容器吧，寻求答案中……</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>小贴士总能带来惊喜</div>2022-07-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqF6ViaDyAibEKbcKfWoGXe8lCbb8wqes5g3JezHWNLf4DIl92QwXX43HWv408BxzkOKmKb2HpKJuIw/132" width="30px"><span>Geek_b537b2</span> 👍（1） 💬（1）<div>老师请问下使用Docker Registry搭建本地镜像仓库后用docker pull拉取镜像怎么不是去共有仓库拉取而是默认去本地私有仓库拉取，这中间是不是自动配置的镜像源地址</div>2022-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqw0R25Bt0iahFhEHfnxmzr9iaZf0eLsDQtFUJzgGkYwHTqicU9TydMngrJ4yL7D50awD2VibHBAdqplQ/132" width="30px"><span>Geek_18dfaf</span> 👍（1） 💬（1）<div>什么时候更新下一课</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（1） 💬（1）<div>老师，看了图中的nginx ，wd，mariadb 网络架构图
想问下：是三个容器共同用一个docker 运行时吗？  在网络方面用bridge模式下，它们三也是独立网络环境吧？</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/e1/f663213e.jpg" width="30px"><span>拾掇拾掇</span> 👍（1） 💬（2）<div>1.之前都是单个运行mysql容器或者redis容器，没怎么多容器之前联动。今天搭建wordpress让我对容器隔离环境、随意删除、随意构建有了更深的感受
2.容器编排解决的应该是一组容器批量构建、整体维护吧</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（1） 💬（1）<div>老师好，最近遇到一个很奇怪的容器问题。那就是同一个镜像，在不同的机器上，里面的文件权限存在不同，但我们记忆中只修改了宿主机的权限，宿主机的文件目录权限不是和容器完全隔离吗，老师有相关思路吗</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/11/c8/9c92c1ac.jpg" width="30px"><span>LHANGRONG</span> 👍（0） 💬（1）<div>老师您好，我在启动nginx容器时候，没有报错返回了CONTAINER ID，但是用docker ps查看却看不到这个容器，这是怎么回事呢</div>2024-04-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoREZlw6JWh1OXYvcKhOToBPCSqVr33Vhc0gmW9jNT3JHtW7NtaiaiaNJicjjxyVia7Oec3Qq1bzLGreQ/132" width="30px"><span>Geek_07ead6</span> 👍（0） 💬（1）<div>老师您好，expose暴漏的端口和-v映射的端口有什么不同？</div>2024-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>要是有docker compose相关知识就完美了</div>2024-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（1）<div>我们以上学过的所有操作都是在单机或者极少数容器的情况下使用的。而在面临大规模集群的时候，就需要容器编排技术了。</div>2023-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（0） 💬（1）<div>搭建成功！</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（2）<div>引用：
`curl 127.1:5000&#47;v2&#47;_catalog
curl 127.1:5000&#47;v2&#47;nginx&#47;tags&#47;list`
地址错误，应该是127.0.0.1吧
</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/18/9f35fddb.jpg" width="30px"><span>后三排</span> 👍（0） 💬（1）<div>Docker 内安装了 snap，然后 snap install core. 报错 error: cannot communicate with server: Post &quot;http:&#47;&#47;localhost&#47;v2&#47;snaps&#47;core&quot;: dial unix &#47;run&#47;snapd.socket: connect: no such file or directory.

这？</div>2023-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/18/9f35fddb.jpg" width="30px"><span>后三排</span> 👍（0） 💬（1）<div>对于遇到 System has not been booted with systemd as init system (PID 1). Can&#39;t operate.
Failed to connect to bus: Host is down，这样的问题如何处理最好呢？</div>2023-01-08</li><br/><li><img src="" width="30px"><span>Geek_da5fa5</span> 👍（0） 💬（1）<div>老师 通过 docker run -d \
&gt; --env WORDPRESS_DB_HOST=172.17.0.13 \
&gt; --env WORDPRESS_DB_USER=wp \
&gt; --env WORDPRESS_DB_PASSWORD=123 \
&gt;  --env WORDPRESS_DB_NAME=db \
&gt;  wordpress:5
ab9978554b0e56cadbb91525e07474e50b467940bb9debd35abde0d1a45ef5c4
没有问题，但是在查找docker inspect ab9|grep IPAddress
        &quot;IPAddress&quot;: &quot;&quot;,显示并没有开启，这种一般是什么原因呢
</div>2023-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIBrZt8rUzS2xDK4lRF3goQb8UCGB8bb5DPXRfOo4ljRtLxfp2njjjQQicOSNLZJHAiaLyeSsC8fVQw/132" width="30px"><span>wangbei0907</span> 👍（0） 💬（1）<div>🐂，抽丝剖茧，层层递进，一个问题引出一个问题，🐂🐂，就喜欢这种把读者当成`傻子`的老师🐂🐂🐂。</div>2023-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/da/5f/f72f0ffd.jpg" width="30px"><span>HD</span> 👍（0） 💬（1）<div>老师，-v `pwd`&#47;wp.conf:&#47;etc&#47;nginx&#47;conf.d&#47;default.conf \
请问这里加了`pwd`是什么意思？</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/da/5f/f72f0ffd.jpg" width="30px"><span>HD</span> 👍（0） 💬（1）<div>老师，这么说，两个容器进程间是可以直接通信的吗？</div>2022-12-08</li><br/>
</ul>