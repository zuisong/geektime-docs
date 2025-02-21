你好，我是俊达。

这一讲中我会介绍MySQL中导出数据和导入数据的一些方法，包括传统的mysqldump工具、MySQL shell提供的实例导出和导入工具、MySQL原生支持的LOAD DATA和SELECT INTO OUTFILE命令，以及mysql shell的单表export和并行import工具。这些工具有各自的特点，也有一些相通的地方，学习了这些工具的特点和使用方法后，你可以根据自己具体的需求，选择合适的方法来完成数据导出导入相关的任务。

## mysqldump

mysqldump是MySQL自带的一个命令行工具，可以用来导出整个数据库实例，也可以导出指定的库或表。mysqldump不仅能用来导出数据，还能用来导出数据库中的各类对象，如表结构、存储过程、函数、事件、数据库用户、权限。

### mysqldump使用场景

使用mysqldump备份整个数据库实例时，需要加上参数–all-databases。

```go
mysqldump -u user -hhost -psomepass --all-databases
```

如果你还想同时备份存储过程、触发器、事件，就要加上–routines、–triggers、–events这几个参数。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/53/18/de532447.jpg" width="30px"><span>范特西</span> 👍（1） 💬（1）<div>感谢老师的分享，文章末尾的问题，我会考虑修改一些参数来加快恢复，比如双一和关闭 binlog，一切为导入数据开绿灯。老师有更好的方法吗？</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（0） 💬（1）<div>对于备份这部分有个疑惑，我选择在12点整进行备份，12点整以后的数据变化就不在我备份的范围内了吧，就不在我需要关注的范围内了吧。可以这样理解吗</div>2025-02-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/QibEGk3tYWjeeWtdpg0hicxC769G81aIFEGHhvIuCjicwLiblYd3CW2HEeQhHIaZsYgBQtTZajI9KFianf7QmX52rRg5O2IdZ77sj6kaTc0hNhGk/132" width="30px"><span>Geek_56e0fa</span> 👍（0） 💬（1）<div>老师 我只用了--all-database 有一个Warning: A partial dump from a server that has GTIDs will by default include the GTIDs of all transactions, even those that changed suppressed parts of the database. If you don&#39;t want to restore GTIDs, pass --set-gtid-purged=OFF. To make a complete dump, pass --all-databases --triggers --routines --events.   这里明明是all database 为什么有partial dump的告警</div>2025-01-14</li><br/>
</ul>