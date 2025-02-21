你好，我是程远。

在[上一讲](https://time.geekbang.org/column/article/326253)里，我们学习了Linux capabilities的概念，也知道了对于非privileged的容器，容器中root用户的capabilities是有限制的，因此容器中的root用户无法像宿主机上的root用户一样，拿到完全掌控系统的特权。

那么是不是让非privileged的容器以root用户来运行程序，这样就能保证安全了呢？这一讲，我们就来聊一聊容器中的root用户与安全相关的问题。

## 问题再现

说到容器中的用户（user），你可能会想到，在Linux Namespace中有一项隔离技术，也就是User Namespace。

不过在容器云平台Kubernetes上目前还不支持User Namespace，所以我们先来看看在没有User Namespace的情况下，容器中用root用户运行，会发生什么情况。

首先，我们可以用下面的命令启动一个容器，在这里，我们把宿主机上/etc目录以volume的形式挂载到了容器中的/mnt目录下面。

```shell
# docker run -d --name root_example -v /etc:/mnt  centos sleep 3600
```

然后，我们可以看一下容器中的进程"sleep 3600"，它在容器中和宿主机上的用户都是root，也就是说，容器中用户的uid/gid和宿主机上的完全一样。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（14） 💬（8）<div>最近在使用Helm部署gitlab服务的过程中,就发现了 postgresql 和 redis 组件默认是不以root用户执行的,而是一个 User ID 为1001的用户在执行.
这样做,就需要有个k8s的 initContainer 容器先以root用户权限去修改存储目录的权限. 否则后面服务的1001号用户可能就没有权限去写文件了.
------------------

最近遇到一个问题,想咨询一下老师:
你们有使用过 容器资源可视化隔离方案(lxcfs) 么, 有没有什么坑?
通俗点就是:让容器中的free, top等命令看到容器的数据，而不是物理机的数据。
------------------

我遇到的问题是在容器内执行类似`go build&#47;test`命令时,默认是根据当前CPU核数来调整构建的并发数.
这就导致了实际只给容器分配了1个核,但是它以为自己有16个核.
然后就开16个link进程,互相之间除了有竞争,导致CPU上下文切换频繁,更要命的是把磁盘IO给弄满了.影响了整台宿主机的性能.
(由于项目比较大,需要构建的文件比较多,所以很容器就让宿主机的IO达到了云服务器SSD磁盘的限制 160MB&#47;s)

我知道在我这个场景下,可以通过指定构建命令`-p`来控制构建的并发数.
(https:&#47;&#47;golang.org&#47;cmd&#47;go&#47;#hdr-Compile_packages_and_dependencies)
实际也这么尝试过,效果也不错.
但问题是,我的项目会很多,每个人构建命令的写法都完全不一样,如果每个地方都去指定参数,就会比较繁琐,且容易遗漏.

------------------
后来,我看到一篇文章: 容器资源可视化隔离的实现方法
(https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;SCxD4OiDYsmoIyN5XMk4YA)

之前也在其他专栏中看老师提到过 lxcfs.
我在想,老师在迁移上k8s的过程中,肯定也遇到过类似的问题,不知道老师是如何解决的呢?

</div>2020-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/86/4ff2a872.jpg" width="30px"><span>Sun</span> 👍（2） 💬（2）<div>
user limit 是session的？每个容器及时使用相同的user id ，也不会当做累计？

User resource limits dictate the amount of resources that can be used for a particular session. The resources that can be controled are:

maximum size of core files
maximum size of a process&#39;s data segment
maximum size of files created
maximum size that may be locked into memory
maximum size of resident memory
maximum number of file descriptors open at one time
maximum size of the stack
maximum amount of cpu time used
maximum number of processes allowed
maximum size of virtual memory available
It is important to note that these settings are per-session. This means that they are only effective for the time that the user is logged in (and for any processes that they run during that period). They are not global settings. In other words, they are only active for the duration of the session and the settings are not cumulative. For example, if you set the maximum number of processes to 11, the user may only have 11 processes running per session. They are not limited to 11 total processes on the machine as they may initiate another session. Each of the settings are per process settings during the session, with the exception of the maximum number of processes.
</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（1） 💬（3）<div>老师 docker -u 参数 是不是就是 通过user namespace 进行隔离</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（0） 💬（1）<div>&quot;由于用户 uid 是整个节点中共享的，那么在容器中定义的 uid，也就是宿主机上的 uid，这样就很容易引起 uid 的冲突。&quot;老师这句话怎么理解，容器内uid与宿主机uid是怎么样的关系呢</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/08/0287f41f.jpg" width="30px"><span>争光 Alan</span> 👍（0） 💬（1）<div>老师，感谢您的分享，学到了很多知识，也感谢解答了很多疑问，有个小小的请求：能公布个微信群之类的吗？把学员加一起相互讨论问题，交流心得</div>2021-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（4） 💬（0）<div>Kubernetes v1.25 添加了对容器 user namespaces 的支持</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7e/c0/1c3fd7dd.jpg" width="30px"><span>朱新威</span> 👍（4） 💬（1）<div>老师，我发现一个很有趣的现象，有点困惑；

在宿主机上：
以root用户运行capsh --print
发现Current字段包含许多capabilities

以非root用户运行capsh --print
发现Current 字段包含零个capabilities，说明非root用户启动的进程缺省没有任何capabilities

docker容器内：
root用户运行capsh --print
发现Current 字段包含14个capabilities，比宿主机上少了一些，对宿主机的&#47;etc&#47;shadow有读写权限

非root用户运行capsh --print
发现Current字段仍然包含14个capabilities，对宿主机的&#47;etc&#47;shadow没有读写权限

这就让我感觉有点困惑了，原本预期容器内非root用户运行capsh  --print的capabilities应该为空呀，或者知道少于root用户的capabilities吧？</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>install slirp4netns and Podman on your machine by entering the following command:

$ yum install slirp4netns podman -y
We will use slirp4netns to connect a network namespace to the internet in a completely rootless (or unprivileged) way.</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/bf/cd6bfc22.jpg" width="30px"><span>自然</span> 👍（0） 💬（0）<div>有个场景：用jenkins  在 openjdk镜像里 maven 编译java项目, 一个 maven目录（在主机上，而且还有其他很多工具），一个项目源码目录  需要映射到  openjdk镜像里（普通用户启动docker），jenkins 里的pipline 是大家都可以写的。 如何防止 加载主机上目录 在docker镜像里 root用户 随意修改呢（ 比如 我不想他删除 主机上的maven）？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0b/37/20ac0432.jpg" width="30px"><span>sunnoy</span> 👍（0） 💬（0）<div>如果容器内的用户uid在宿主机上不存在呢，这个时候描述符的分配是怎么样的呢</div>2022-04-24</li><br/>
</ul>