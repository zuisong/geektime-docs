你好，我是LMOS。

在前面的课程中，我们已经实现了Cosmos下的文件系统rfs，相信你已经感受到了一个文件系统是如何管理文件的。今天我们一起来瞧一瞧Linux是如何管理文件，也验证一下Linux那句口号：一切皆为文件。

为此，我们需要首先搞清楚什么是VFS，接着理清为了实现VFS所用到的数据结构，然后看看一个文件的打开、读写、关闭的过程，最后我们还要亲自动手实践，在VFS下实现一个“小”且“能跑”的文件系统。

下面让我们开始吧！这节课的配套代码，你可以从[这里](https://gitee.com/lmos/cosmos/tree/master/lesson35)下载。

## 什么是VFS

VFS（Virtual Filesystem）就像伙伴系统、SLAB内存管理算法一样，也是SUN公司最早在Sloaris上实现的虚拟文件系统，也可以理解为通用文件系统抽象层。Linux又一次“白嫖”了Sun公司的技术。

在Linux中，支持EXT、XFS、JFS、BTRFS、FAT、NTFS等多达十几种不同的文件系统，但不管在什么储存设备上使用什么文件系统，也不管访问什么文件，都可以统一地使用一套open(), read()、write()、close()这样的接口。

这些接口看上去都很简单，但要基于不同的存储设备设计，还要适应不同的文件系统，这并不容易。这就得靠优秀的VFS了，它提供了一个抽象层，让不同的文件系统表现出一致的行为。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（8） 💬（1）<div>请说一说 super_block，dentry，inode 这三个数据结构 ，一定要在储存设备上对应存在吗？

不需要严格对应，之所以要对应是为了使用、维护更加方便，抽象是软件设计最大的魅力。</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（7） 💬（1）<div>一、数据结构
1、四大基本结构
A、超级块管理为super_block，用于描述存储设备上的文件系统，可以从super_block出发把存储设备上的内容读取出来
B、目录结构管理为dentry，通过其来组织整个目录结构
C、文件索引节点管理为inode，可以先把它看作是存储设备上的具体对象，一个inode可以对应多个dentry【比如link】
D、文件管理为file，描述进程中的某个文件对象

2、Linux在挂载文件系统时，会读取文件系统超级块super_block，然后从超级块出发读取并构造全部dentry目录结构；dentry目录结构指向存储设备文件时，是一个个的inode结构。

3、应用程序在打开文件时，在进程结构task_struct-&gt;fs_struct中，记录进程相关的文件系统信息，这样就可以对文件系统，进行新增、删除、打开、关闭等相关操作。

4、同时，在进程结构task_struct-&gt;files_struct-&gt;fdtable-&gt;file，保存全部打开的文件指针，文件指针file结构中，会保存inode指针，从而可以获取文件权限、文件访问记录、文件数据块号的信息，进一步可以从文件读取文件信息。

二、trfs demo
1、除上面的结构外，内部使用了两个结构：文件描述fileinfo，目录描述dir_entry
A、fileinfo记录在了inode的私有数据中，这样通过inode就可以方便的找到fileinfo
B、如果是文件，fileinfo.data中记录的就是文件内容
C、如果是文件夹，fileinfo.data记录的就是一个个dir_entry

2、trfs基于非连续内存
A、由MAX_FILES+1个fileinfo组成，记录在全局变量finfo_arr中，但第0和第MAX_FILES个好像没有使用
B、每个fileinfo中包含一个文件块，大小为MAX_BLOCKSIZE
C、并没有使用单独的位图，而是通过每个fileinfo来记录其使用情况的

3、初始化
A、初始化了finfo_arr结构
trfs_init-&gt;init_fileinfo

B、超级块创建，占用了finfo_arr[1]
trfs_mount-&gt;mount_nodev-&gt;trfs_fill_super

4、使用
A、每次新建文件或文件夹，就占用一个空闲的fileinfo
B、删除文件或文件夹，就将一个fileinfo设置为可用
C、读写文件就是通过file找到fileinfo.data
D、查找和枚举就是通过file找到fileinfo.data，然后访问其中的每个dir_entry</div>2021-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（2）<div>请说一说 super_block，dentry，inode 这三个数据结构 ，一定要在储存设备上对应存在吗？

要的。
</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/16/21/ad5b7927.jpg" width="30px"><span>蓝色梦幻</span> 👍（0） 💬（1）<div>请教一下：＂有了上述代码，挂载 trfs 到 &#47;mnt 下，我们就可以用 touch 建立一个文件，然后用 cat 读取这个文件了。＂
这里具体要怎么操作呀？我可以用findmnt 查看到trfs系统的挂载，后续要怎么操作呢？

TARGET                       SOURCE     FSTYPE          OPTIONS
├─&#47;mnt                                none       trfs            rw,relatime
</div>2022-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（0） 💬（1）<div>打卡</div>2022-05-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/05Wiazxo0OS5w9KdJ4OQAe7RzgyHLuBCMNrZicDAQ8ZlSMx4NNdAgSLBYPJGn9W1y45ZTtUMlCxsQHqD7ycicQJyg/132" width="30px"><span>Geek_cb2b43</span> 👍（0） 💬（1）<div>请问在一个新建的空文件，从100兆的位置写200兆数据，操作的流程是什么，文件的大小是300兆吗？</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/58/ef/e7c7f2b4.jpg" width="30px"><span>不及胜于过之</span> 👍（0） 💬（1）<div>文件系统就是 super_block&#47;和super_operations，dentry和dentry_operations，inode和inode_operations，file 和 file_operations，真的是醍醐灌顶，大佬可以按这个表述风格，详细说下mount 嘛， 一直理解的不是很深刻，尤其是容器用到的union mount</div>2021-08-08</li><br/>
</ul>