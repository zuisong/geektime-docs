你好，我是俊达。

前面我讲过，搭建一个备库，有一个核心的步骤是同步源库的初始状态。逻辑备份（比如使用mysqldump）和物理备份（比如使用xtrabackup）都可以用来初始化备库。MySQL 8.0中，还引入了Clone插件，也可以用来初始化一个备库。有了Clone插件，搭建备库会变得更加简单。MySQL MGR（Group Replication）也会使用Clone插件来初始化成员的数据。此外，还可以将整个数据库克隆到本地的一个目录中，这相当于是给数据库做了一个全量备份。

这一讲中，我们就来聊一聊Clone插件的一些用法，以及Clone插件的内部原理。

## Clone插件介绍

MySQL 8.0.17版本引入了clone插件。使用Clone插件可以对本地或远程的mysql实例进行克隆操作。Clone插件会拷贝InnoDB存储引擎表，克隆得到的是数据库的一个一致的快照，可以使用这个快照数据来启动新的数据库实例。Clone插件还会记录数据库的Binlog位点，可以将克隆得到的实例作为源实例的备库。

Clone插件支持本地克隆和远程克隆这两种模式。本地克隆将数据存放在源数据库所在主机上。远程克隆涉及到两个实例，提供数据的实例称为捐赠者（Donor），接收数据的实例称为接收者（Recipient）。捐赠者将整个数据库通过MySQL网络协议发送给接收者，接收者将数据存放到数据目录。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/53/18/de532447.jpg" width="30px"><span>范特西</span> 👍（1） 💬（1）<div>课后问题，我觉得应该查看：select * from performance_schema.clone_status 表</div>2024-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（0） 💬（1）<div>mysql.slave_master_info 表是不是有 Binlog 文件和位点信息？</div>2024-12-09</li><br/>
</ul>