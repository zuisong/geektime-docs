你好，我是LMOS。

通过上节课的学习，我们已经对Ext3文件系统的结构非常了解了。这种了解究竟正确与否，还是需要通过写代码来验证。这节课我会带你读取Ext3文件系统中的文件，帮你加深对Ext3的理解。

我假定你已经学会了怎么建立一个虚拟硬盘并将其格式化为Ext3文件系统。如果记不清了，请回到[上节课](https://time.geekbang.org/column/article/594921)复习一下。课程的配套代码，你需要从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson35~36)下载。

## 打开虚拟硬盘

想要从虚拟硬盘读取文件，首先要做的当然是打开虚拟硬盘。但我们的硬盘是个文件，所以这就变成了打开了一个文件，然后对文件进行读写就行。这些操作我们已经非常熟悉了，不过多展开。

这次我们不用read命令来读取虚拟硬盘文件数据，因为那样做还需要处理分配临时内容和文件定位的问题，操作比较繁琐。这里我们直接用mmap将整个文件映射到虚拟文件中，这样就能像访问内存一样很方便地访问文件了。

下面我们首先实现mmap映射读取文件这个功能，代码如下所示：

```plain
int init_in_hdfile()
{
	struct stat filestat;
	size_t len = 0;
	void* buf = NULL;
	int fd = -1;
	// 打开虚拟硬盘文件
	fd = open("./hd.img", O_RDWR, S_IRWXU|S_IRWXG|S_IRWXO);
	if(fd < 0)
	{
		printf("打开文件失败\n");
		return -1;
	}
	// 获取文件信息，比如文件大小
	fstat(fd, &filestat);
	// 获取文件大小
	len = filestat.st_size;
	// 映射整个文件到进程的虚拟内存中
	buf = mmap(NULL, len, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
	if(buf == NULL) 
	{
		printf("映射文件失败\n");
		return -2;
	}
	// 保存地址 长度大小 文件句柄 到全局变量
	hdaddr = buf;
	hdsize = len;
	hdfilefd = fd;
	return 0;
}
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/ae/c3/d930693b.jpg" width="30px"><span>LockedX</span> 👍（2） 💬（1）<div>可以通过innode节点来恢复数据，innode节点在发生变化的时候会记录在日志文件中，如果存储改文件的快还没有被覆盖，就可以通过日志文件来恢复innode节点这样文件就恢复了。老师放心，我比较老实不会去做坏事的，嘿嘿……</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（1） 💬（1）<div>有几个疑问想请教一下老师：
1. 根目录的目录项存放在inode节点列表的第二个inode这是规范吗？第一个inode存放什么呢？
2. 如果目录项个数超过一个inode能表示的范围是不是像数据节点inode那样使用一级间接存储块、二级间接存储卡以及三级呢？</div>2022-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>inode相对于块组的啊</div>2022-10-24</li><br/>
</ul>