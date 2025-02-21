你好，我是张磊。今天我和你分享的主题是：白话容器基础之重新认识Docker容器。

在前面的三次分享中，我分别从Linux Namespace的隔离能力、Linux Cgroups的限制能力，以及基于rootfs的文件系统三个角度，为你剖析了一个Linux容器的核心实现原理。

> 备注：之所以要强调Linux容器，是因为比如Docker on Mac，以及Windows Docker（Hyper-V实现），实际上是基于虚拟化技术实现的，跟我们这个专栏着重介绍的Linux容器完全不同。

而在今天的分享中，我会通过一个实际案例，对“白话容器基础”系列的所有内容做一次深入的总结和扩展。希望通过这次的讲解，能够让你更透彻地理解Docker容器的本质。

在开始实践之前，你需要准备一台Linux机器，并安装Docker。这个流程我就不再赘述了。

这一次，我要用Docker部署一个用Python编写的Web应用。这个应用的代码部分（`app.py`）非常简单：

```
from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route('/')
def hello():
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"           
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
```

在这段代码中，我使用Flask框架启动了一个Web服务器，而它唯一的功能是：如果当前环境中有“NAME”这个环境变量，就把它打印在“Hello”之后，否则就打印“Hello world”，最后再打印出当前环境的hostname。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/2a/07/74b3c14a.jpg" width="30px"><span>黄文刚 </span> 👍（81） 💬（4）<div>收货很大，感谢张磊！请教一个问题，请问在容器内部如何获取宿主机的IP? 谢谢。</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（38） 💬（1）<div>所以说 docker exec 每次都会创建一个和容器共享namespace的新进程？</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/61/78d5d09a.jpg" width="30px"><span>long904</span> 👍（26） 💬（4）<div>图中不太明白为什么&#39;CMD&#39;属于只读层，那如果 dockfile 里面 yum install 并且 commit 的话，这些 CMD 执行的 yum 命令修改的内容还属于只读层？</div>2018-09-13</li><br/><li><img src="" width="30px"><span>Geek_9ca34e</span> 👍（25） 💬（3）<div>；老师，有个地方还是不太明白,以下是你些的原文：
注意：这里提到的 &quot; 容器进程 &quot;，是 Docker 创建的一个容器初始化进程(dockerinit)，而不是应用进程 (ENTRYPOINT + CMD) dockerinit 会负责完成根目录的准备、挂载设备和目录、配置 hostname 等一系列需要在容器内进行的初始化操作。 最后，它通过 execv() 系统调用，让应用进程取代自己，成为容器里的 PID=1的进程。
我有以下疑问：
 1、dockerinit 是一个进程，完成初始化之后 ，让应用进程取代自己，那么dockerinit 进程会自动销毁么？
2、这里的dockerinit和应用进程在宿主机中是两个不同的进程id么？
3、执行 docker exec -it container bin&#47;sh   命令后，bin&#47;sh 命令创建的进程只是加入了container的namespace，但是从宿主机的角度它是一个独立的进程，只是共享了namespace信息么？
4、一个容器内部是否只有一个进程？，或者说容器只是一个房间（由namespace和cgroup组成），而其他的进程都是走进了这个房间，让大家以为这个房间就是一个系统，里面包含了这么多进程，其实在宿主机的角度他们都是一个个进程，只是共享了namespace和cgroup 而已，这样理解对么？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/32/0b81fc39.jpg" width="30px"><span>陶希阳</span> 👍（24） 💬（5）<div>想知道云服务器等技术是不是也是通过namespace + cgroup实习的？</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/f7/a4de6f64.jpg" width="30px"><span>大卫</span> 👍（18） 💬（1）<div>张老师，当Dockerfile中使用sh脚本启动，而不是exec启动java应用时，若通过docker stop不能优雅的停掉Java进程。查资料说可用trap接受信号处理，这个有什么其他好的解决办法没？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/47/8da914be.jpg" width="30px"><span>Geek_1264yp</span> 👍（13） 💬（2）<div>老师好，又来问您问题了。生产中有没有什么好的工具管理本地的docker registry，比如磁盘满了想清理等等的操作。期待老师的回复，谢谢！</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4e/e3/1a2e379f.jpg" width="30px"><span>蔡鹏飞</span> 👍（13） 💬（5）<div>docker run 时指定-v挂载宿主机目录到容器目录，即使容器原有目录内有数据，也会被我宿主机目录数据替代的呀。难道是和我使用的storage-driver有关？我用的是overlay存储。</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/7a/ee21df2d.jpg" width="30px"><span>ShJin、Cheng</span> 👍（11） 💬（1）<div>那么老师，请问有没有办法禁止通过exec -it的方式进入容器？</div>2018-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（11） 💬（1）<div>请问docker挂载有何限制没，是否随便一个目录都可以挂载？在容器里应该是root用户，岂不是可以对目录无节制地操作，哪怕原本主机目录中有些文件并不允许当前用户访问？是否可以相应限制</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/ba/2c8af305.jpg" width="30px"><span>Geek_zz</span> 👍（9） 💬（1）<div>你好，可读写层的修改数据保存的话，会保存到哪里</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（9） 💬（2）<div>对于linux大部分容器做不到在运行容器中动态添加宿主机目录，那在什么特定场合下可以做到呢？给个大致思路即可，谢谢。</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/1d/7d8115ec.jpg" width="30px"><span>王雅光</span> 👍（7） 💬（2）<div>老师，如果在docker运行的服务上，修改其配置文件，比如tomcat配置文件，或者webapp下面spring-mvc.xml等配置文件，是否都是以volumn绑定挂载的形式做修改！这个跟init层的区别在哪里！</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/07/6e1ff111.jpg" width="30px"><span>蓝色天际</span> 👍（6） 💬（1）<div>Linux基础薄弱，理解起来有点吃力</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/40/e592d386.jpg" width="30px"><span>Jackson Wu</span> 👍（5） 💬（1）<div>我想请教一个问题，为啥子镜像的entrypoint会覆盖母镜像的entrypoint的呢？</div>2018-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（5） 💬（1）<div>这样，我们新启动的这个容器，就会直接加入到 ID=4ddf4638572d 的容器，也就是我们前面的创建的 Python 应用容器（PID=25686）的 Network Namespace 中。所以，这里 ifconfig 返回的网卡信息，跟我前面那个小程序返回的结果一模一样，你也可以尝试一下。
---------------
容器加入容器？不是把ifconfig 这个进程加入到ID=4ddf4638572d 的容器里吗？</div>2018-09-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLh73kPzAKhz7YxUribqF6QKFiahhVAbwpgVLSRicA68c6ZFA7vUBJY1ves3LVvibrypROyI7awv47eSA/132" width="30px"><span>ZYecho</span> 👍（4） 💬（1）<div>rootfs通过chroot（等同于mount根目录的过程？）也是发生在mnt namespace产生之后，为什么容器rw层在commit的时候就对宿主机可见呢？和挂数据卷不一样么？都是在mnt namespace产生后？</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/94/dd/c8cf5e3c.jpg" width="30px"><span>黄明辉</span> 👍（4） 💬（1）<div>请问老师，容器的进程为什么需要在前台运行呢？</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/05/d8/cd269378.jpg" width="30px"><span>一叶</span> 👍（4） 💬（1）<div>你好，磊哥，谢谢你讲得这么详细，我有一点不是很清楚：
容器中的主进程在系统调用或调用一些lib时，调用到的和容器只读层提供的lib吗？</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（4） 💬（2）<div>1. 如果使用user namespace的话，容器里的root是否还是对文件有权限？
2. centos 7貌似目前还不支持 user namespace
3. 现在部署k8s会考虑用centos吗？特别是对gpu有需求的场景</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/f9/791d0f5e.jpg" width="30px"><span>netwyh</span> 👍（4） 💬（1）<div>如果在docker容器中部署oracle，实际生产环境有没有人这么干？</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（3） 💬（1）<div>我遇到一个问题，如何才能在运行的容器中动态挂载宿主机上的目录呢？</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/17/f67e0d3a.jpg" width="30px"><span>阳雨杭</span> 👍（2） 💬（1）<div>张磊老师好，对于Volume机制，您说：Docker又是如何做到把一个宿主机上的目录或者文件，挂载到容器里面去呢？难道又是 Mount Namespace的黑科技吗？实际上，并不需要这么麻烦。
但是我觉得，Volume机制实质上也是使用的Mount Namespace技术啊，只是在mount操作时，加上了mount-bind机制，可以绑定挂载一个目录到另外一个目录。
Mount Namespace技术就是新建一个子进程时，加上CLONE_NEWNS的参数，再运行一个一个的mount（）函数，重新挂载容器进程的mount点（包括Volume和rootfs）。
以上是我的理解，有错误还请指正，谢谢。</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/25/6ac2f111.jpg" width="30px"><span>孙磊</span> 👍（2） 💬（3）<div>1. 4.6内核之前，查看&#47;proc&#47;$PID&#47;cgroup，或者挂载cgroup时，在容器中会看到整个系统的cgroup，存在安全隐患，4.6内核之后新增cgroup namespace ，每个namespace中的进程都有自己的cgroup了；
2. 这个问题感觉像陷阱，挂载后改变的是home目录的inode值（&#47;test的inode），有数据就很正常了；</div>2018-10-16</li><br/><li><img src="" width="30px"><span>豆沙包</span> 👍（2） 💬（2）<div>你好 我用docker run起了app这个容器之后，查看aufs里层的信息，读写层为什么会和init层是同一个层呢？不是一个会被打包 一个不会被打包么？
# cat &#47;sys&#47;fs&#47;aufs&#47;si_cc04a4d4a9a38631&#47;br[0-9]*
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;fcacef659a1dee2d16c584979fddcd584971507cd7845316e7fca768069e9295=rw
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;fcacef659a1dee2d16c584979fddcd584971507cd7845316e7fca768069e9295-init=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;d2a9b0eca68f7bcd061648edace2f0f5e7e50ba8bb556cae0ab408681cb4ea02=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;6d5cd3d3a45e40517745c86e363756021286100ae0fb5db7a1cb6a7ec8cd4411=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;684b4a4ca733a7b66b46e8c1e5fe841a36af14f237a3fa82724832a335279122=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;d5e965276684d42d69c3f12bb0bfeeaa3c79f2b95cf6251e6779014a73430a86=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;ce080aadd734de0ddcd0cce2f65a6b79e4d41c736ddde97e48dc923fd6c5d067=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;d4672d8b1865d99adebeb807a5b161fb4558d8ff8b0164747a6dc22f2f09c428=ro+wh
&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff&#47;b651ff0b03fec7f0f69669473589d4ed8c3ffd84d5a509b41f71b19f687425c8=ro+wh</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a6/23/91e74c43.jpg" width="30px"><span>leo</span> 👍（2） 💬（2）<div>第三章并没有说明&#47;var&#47;lib&#47;docker&#47;aufs&#47;mnt&#47;6e3be5d2ecccae7cc0fcfa2a2f5c89dc21ee30e166be823ceaeba15dce645b3e的来源，而是直接告知ubuntu:latest就是挂载在这个目录。
如果我想查看alpine:latest的挂载目录，应该如何查找？
换句话说就是如何通过docker image的唯一id来查找出内部id(si_xxx)？
感谢解答！</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5c/49/4e7f0bb4.jpg" width="30px"><span>聪小弟</span> 👍（1） 💬（1）<div>其实可以根据container找到其需要挂载的rootfs目录的，

根据container pid，查看其mountinfo，cat &#47;proc&#47;{PID}&#47;mountinfo  | grep -w si可以获取到si

然后cat &#47;proc&#47;mounts | grep {SID ID}，这样就能找到其rootfs挂载点拉，&#47;var&#47;lib&#47;docker&#47;aufs&#47;mnt&#47;{ID}

还有-v额外挂载时候，其实也说得不算很清楚，按我的理解是挂载了的这个目录是在&#47;var&#47;lib&#47;docker&#47;aufs&#47;diff这一层，且被作为&quot;可读写&quot;层 union 到&#47;var&#47;lib&#47;docker&#47;aufs&#47;mnt&#47;{ID}的rootfs里面，这样container就能通过rootfs看到额外挂载的目录啦</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/47/8da914be.jpg" width="30px"><span>Geek_1264yp</span> 👍（1） 💬（1）<div>挂载文件夹能理解，但是如果挂载宿主机的某一文件到容器，为什么需要容器事先存在同名的这个文件呢？</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/1a/eb8021c3.jpg" width="30px"><span>追寻云的痕迹</span> 👍（1） 💬（1）<div>docker-ee的实现不是基于Hyper-V吧</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/09/5acaeb40.jpg" width="30px"><span>gao</span> 👍（1） 💬（2）<div>docker容器挂载目录在commit后再次进入image，还是能看到之前挂载目录下的文件的，有点奇怪。
抱歉：再次进入image 还是docker run image，但没有指定volumn。</div>2018-09-16</li><br/>
</ul>