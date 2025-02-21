上一节我们讲了Docker的基本原理，今天我们来看一下，“看起来隔离的”技术namespace在内核里面是如何工作的。

既然容器是一种类似公司内部创业的技术，我们可以设想一下，如果一个创新项目要独立运营，应该成立哪些看起来独立的组织和部门呢？

首先是**用户管理**，咱们这个小分队应该有自己独立的用户和组管理体系，公司里面并不是任何人都知道我们在做什么。

其次是**项目管理**，咱们应该有自己独立的项目管理体系，不能按照大公司的来。

然后是**档案管理**，咱们这个创新项目的资料一定要保密，要不然创意让人家偷走了可不好。

最后就是**合作部**，咱们这个小分队还是要和公司其他部门或者其他公司合作的，所以需要一个外向的人来干这件事情。

对应到容器技术，为了隔离不同类型的资源，Linux内核里面实现了以下几种不同类型的namespace。

- UTS，对应的宏为CLONE\_NEWUTS，表示不同的namespace可以配置不同的hostname。
- User，对应的宏为CLONE\_NEWUSER，表示不同的namespace可以配置不同的用户和组。
- Mount，对应的宏为CLONE\_NEWNS，表示不同的namespace的文件系统挂载点是隔离的
- PID，对应的宏为CLONE\_NEWPID，表示不同的namespace有完全独立的pid，也即一个namespace的进程和另一个namespace的进程，pid可以是一样的，但是代表不同的进程。
- Network，对应的宏为CLONE\_NEWNET，表示不同的namespace有独立的网络协议栈。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（21） 💬（1）<div>nsenter、ip netns exec、docker exec命令均是通过系统调用setns实现。</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>这一讲让我对namespace在Docker中起什么作用的理解更深入了。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（0） 💬（1）<div>clone的时候，指定参数CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWIPC |CLONE_NEWPID | CLONE_NEWNET |
CLONE_NEWCGROUP是create一个namespace吧，不是六个？是不是说这个namespace里的进程网络都是独立于root namespace?
如果创建一个网络namespace是不是这个namespace里运行的进程属于root namespace?</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/94/0b969588.jpg" width="30px"><span>青年祭司</span> 👍（1） 💬（0）<div>有系统默认的namespace吗，刚启动操作系统的时候会进入namespace吗</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（1） 💬（0）<div>“当我们再次 echo” 后面的文本别用代码的形式呀！</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（1） 💬（0）<div>【unshare 是使当前进程加入新的 namespace】这一说法并不完全准确，CLONE_NEWPID是特例，不影响当前调用进场，仅作用于新建的children进程。</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（1） 💬（0）<div>越看越有意思，逐渐深入</div>2019-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（0） 💬（0）<div>前面部分的铺垫让我很舒服啊</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（2）<div>“Mount，对应的宏为 CLONE_NEWNS”，这个宏的命名感觉很诡异啊，为啥命名成这样？很容易让人混淆~~~</div>2020-03-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>怎么全程没有user namespace的参与呢？</div>2019-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（0） 💬（0）<div>太赞了</div>2019-08-16</li><br/>
</ul>