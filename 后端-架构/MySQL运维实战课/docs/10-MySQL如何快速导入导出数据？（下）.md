你好，我是俊达。

上一讲我介绍了mysqldump和MySQL Shell的Dump工具。使用mysqldump导出的，实际上是一个SQL文件，将这个文件直接拿到数据库中执行，就可以完成数据导入。MySQL Shell Dump工具将建表语句、表中的数据导出到了不同的文件中，而且数据以文本文件的形式存储，需要使用MySQL Shell配套的Load工具，或者使用Load Data命令导入数据。

这一讲我们来学习MySQL Shell Load工具的使用方法，以及导出和导入单个表数据的一些其他方法。

## MySQL Shell Load工具

### 使用load\_dump导入

MySQL Shell Dump导出的数据，可以用MySQL Shell Load工具导入。load\_dump有两个参数，第一个参数是Dump文件的路径。第二个参数是一个字典，用来指定导入的各个选项。

```go
util.load_dump("/data/backup/db_backups", {})
```

load\_dump默认会导入Dump路径下的所有文件。你可以使用includeSchemas、includeTables来指定需要导入的库和表，用excludeSchemas、excludeTables忽略指一些库和表。这里includeTables和excludeTables中表名的格式为"db\_name.table\_name"。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（2） 💬（1）<div>思考题：

可以通过Oracle工具多线程导出整个数据库实例，设置开启事务，短暂的获取全局锁后进行快照导出，将数据导出到指定目录中，并且每个库表的ddl和数据都是分开存放，方便后面的并行导入；

导入过程中使用import_table，指定线程数，具体的线程数据还是要根据目标数据库的并发写性能来确定，尽可能的缩短时间;

对于导出导入过程中的增量数据，可以在导出开始的时候记录binlog位置或GTID的全局事务id，导入增量数据的时候可以通过binlog位置和GTID来恢复增量数据，且导出数据的过程尽量在用户量少的时间操作，确保增量的数据尽可能少，同时来减少导入增量数据时业务库的停机时间；</div>2024-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（0） 💬（1）<div>也可以看数据变化程度，如果历史数据几乎不会改变，可以直接oracle 并发导出csv ，然后mysql  并发导入csv，最后检查数据</div>2024-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（0） 💬（1）<div>借用ogg 先实时同步 Oracle和MySQL的数据，切换窗口时间用来检测数据同步是否正确。</div>2024-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/4e/44/49b29792.jpg" width="30px"><span>Geek_0126</span> 👍（0） 💬（1）<div>异构数据源之间的同步问题，就要借助同步工具了，例如DataX、cloudcanal等，可以先进行全量迁移，然后再开启增量同步。不过其中需要注意的细节太多了，比如数据类型及各种数据库对象之间的转换。</div>2024-09-09</li><br/>
</ul>