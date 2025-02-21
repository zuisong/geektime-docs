你好，我是程远。从今天这一讲，我们进入到了容器安全的模块。

容器安全是一个很大的话题，容器的安全性很大程度是由容器的架构特性所决定的。比如容器与宿主机共享Linux内核，通过Namespace来做资源的隔离，通过shim/runC的方式来启动等等。

这些容器架构特性，在你选择使用容器之后，作为使用容器的用户，其实你已经没有多少能力去对架构这个层面做安全上的改动了。你可能会说用[Kata Container](https://katacontainers.io/)、[gVisor](https://gvisor.dev/) 就是安全“容器”了。不过，Kata或者gVisor只是兼容了容器接口标准，而内部的实现完全是另外的技术了。

那么对于使用容器的用户，在运行容器的时候，在安全方面可以做些什么呢？我们主要可以从这两个方面来考虑：第一是赋予容器合理的capabilities，第二是在容器中以非root用户来运行程序。

为什么是这两点呢？我通过两讲的内容和你讨论一下，这一讲我们先来看容器的capabilities的问题。

## 问题再现

刚刚使用容器的同学，往往会发现用缺省 `docker run`的方式启动容器后，在容器里很多操作都是不允许的，即使是以root用户来运行程序也不行。

我们用下面的[例子](https://github.com/chengyli/training/tree/main/security/capability)来重现一下这个问题。我们先运行`make image` 做个容器镜像，然后运行下面的脚本：
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（37） 💬（3）<div>getcap $(which ping)
setcap -r $(which ping)

顺便举个之前使用过的例子：普通用户默认没有 tcpdump 抓包权限，可添加 net_raw、net_admin caps：
sudo setcap cap_net_raw,cap_net_admin+ep $(which tcpdump)</div>2020-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7e/c0/1c3fd7dd.jpg" width="30px"><span>朱新威</span> 👍（7） 💬（3）<div>已经更新20讲了，莫名有点心慌，生怕这么好的专栏结束了🤪</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/39/4e95e7b9.jpg" width="30px"><span>morse</span> 👍（4） 💬（1）<div>老师, 您好, 我在 Ubuntu20.04 下删除 ping 的 capabilities 后, 切换别的用户后, 还是可以正常使用 ping 的, 我进行了以下操作. 
# getcap &#47;usr&#47;bin&#47;ping # 发现ping 具有cap_net_raw capability

&#47;usr&#47;bin&#47;ping = cap_net_raw+ep
# 删除全部 capabilites
# sudo setcap -r &#47;usr&#47;bin&#47;ping
# 切换普通用户 sudo su - appuser
# ping localhost # 可以正常工作
# capsh --print -- -c &quot;&#47;bin&#47;ping -c 1 localhost&quot; #可以看到还是具有cap_net_raw
Current: =
Bounding set =cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,cap_audit_read
....

# capsh --print # 打印当前用户全部 capabilities, 发现当前用户是具有 cap_net_raw 

给我的感觉, 在 Ubuntu 20.04 中, useradd appuser 创建好的用户, 初始就具有一定的 capabilites, 所以在运行程序的时候, 用户自身的 capabilities+程序的 capabliities 是最终的. 所以就算把文件的 capabilities 删除, 只要用户还具有这个能力, 那么还是可以正常执行的. 

那么我的问题来了, 我没有找到, 如何对一个用户限制这种 capabilities, 即我 useradd 一个 用户, 怎么限制这个用户的 capabilities.
</div>2021-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（2） 💬（1）<div>selinux是不是实际上就是限制cap权限的操作</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/4a/df/c1eb99cf.jpg" width="30px"><span>Tony</span> 👍（1） 💬（2）<div>老师你好。请问在Linux中（比如centos），在允许普通用户使用docker以后，如何如何限制用户不能读取，宿主机上非该普通用户的文件？</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/83/09/42c48319.jpg" width="30px"><span>老酒馆</span> 👍（6） 💬（0）<div>getcap &#47;usr&#47;bin&#47;ping 查看ping进程当前cap
setcap cap_net_admin,cap_net_raw+p &#47;usr&#47;bin&#47;ping 设置ping进程cap</div>2020-12-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq30mvo0eATZ3Yfm5POktwic3NJSRkiagtJt1vaxyvCS22PJRm8xrulXqaLJRWQWb6zNI4zL0G2QkCA/132" width="30px"><span>heyhd9475</span> 👍（1） 💬（0）<div>老师想问一下文件的capabilities是保存在什么地方呢，getcap应该也是从什么地方读取的这些信息吧，是inode,file,dentry？</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/98/b6f20c10.jpg" width="30px"><span>王皓月</span> 👍（1） 💬（0）<div>老师您好，我想要在容器中使用systemctl，除了启用特权模式还有别的办法吗？看到过大牛在docker run的时候加了&#47;sys&#47;fs&#47;cgroup:&#47;sys&#47;fs&#47;cgroup就可以在容器内使用systemctl，这个和特权模式有什么区别？</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>李老师，请教一个问题：“因为安全方面的考虑，容器缺省启动的时候，哪怕是容器中 root 用户的进程，系统也只允许了 15 个 capabilities。这个你可以查看runC spec 文档中的 security 部分，你也可以查看容器 init 进程 status 里的 Cap 参数，看一下容器中缺省的 capabilities。” 在这个例子当中，为什么容器中启动的 1 号进程的 CapPrm 是 00000000a80425fb？00000000a80425fb 只有 14 个 1，剩下的一个 1 哪里去了？</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/90/9b/0013cf16.jpg" width="30px"><span>段殷澄</span> 👍（0） 💬（0）<div>我ubuntu的root用户怎么默认只赋予了15个capabilities</div>2022-11-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJk3PElN2J96DtyWuIg6xPSs3zRFsIMibOvIn5kuRkESORsRIkDJMUekymI2wiaYiaP0UzibXWEl0aLYw/132" width="30px"><span>Bill</span> 👍（0） 💬（0）<div>Best ever</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/c5/84491beb.jpg" width="30px"><span>罗峰</span> 👍（0） 💬（0）<div>有的gpu容器需要privileged这个是啥原因呢</div>2021-08-30</li><br/>
</ul>