你好，我是俊达。

前面几讲，我花了比较多的篇幅介绍MySQL的数据复制。假设你的数据库都已经做了备库，有了完善的监控，为什么还要做数据库备份呢？

很重要的一个原因，是备库通常都和主库保持同步，如果在主库上执行了一个误操作，或者由于程序的Bug或外部攻击，导致数据被误删除或误更新了，这些操作很快会复制到备库，导致主库和备库的数据都有问题。如果没有备份，数据就有可能很难找回来。

从实现方式上看，备份可以分为逻辑备份和物理备份。[第 9 讲](https://time.geekbang.org/column/article/804980)、[第 10 讲](https://time.geekbang.org/column/article/806933)中我们介绍过一些MySQL逻辑备份的工具。当数据库特别大的时候，使用逻辑备份恢复数据，效率可能会比较低。在实践中，我们经常会使用物理备份工具，直接备份数据库的物理文件。物理备份在备份和恢复性能上有很大的优势。

所以这一讲中我会给你介绍怎么使用MySQL中最流行的一个开源的物理备份工具——xtrabackup，来备份和恢复数据库。

## 使用xtrabackup

### 安装xtrabackup

到 [percona 官网](https://www.percona.com/downloads)下载合适的版本。Xtrabackup分为几个大的版本，使用Xtrabackup 2.4备份MySQL 5.7，使用Xtrabackup 8.0备份MySQL 8.0，使用Xtrabackup 8.4备份MySQL 8.4。这一讲中，我们使用8.0版本。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/95/8c/c5de487c.jpg" width="30px"><span>浮生</span> 👍（0） 💬（1）<div>如提示Neither found #innodb_redo subdirectory, nor ib_logfile* files in .&#47; 可以指定.&#47;bin&#47;xtrabackup --defaults-file=&#47;data&#47;mysql3306&#47;my.cnf</div>2025-02-19</li><br/>
</ul>