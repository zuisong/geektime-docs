你好，我是俊达。

在第一讲中，我们使用了一个极简的配置文件，只包含了最基本的一些参数，使MySQL能正常运行起来，便于我们进行测试、熟悉MySQL。但是供正式环境使用的MySQL就不能仅仅依赖这个基础的配置了，我们需要根据部署MySQL的主机配置、使用MySQL的业务场景等因素，设置合理的参数，使MySQL能以比较高的性能运行，并满足业务对数据一致性的要求。

这一讲中，我们会介绍MySQL参数配置的基本机制。然后再介绍一些比较重要的参数，讲解这些参数的作用是什么，如何合理地设置这些参数。你可以根据这里提供的基本方法，为自己的MySQL设置一个相对合理的配置。

## MySQL参数设置机制

MySQL 8.0总共有六百多个配置参数。有时候我们也将这些参数称为变量，因为官方文档中的术语是Variables。同时在MySQL中，我们使用命令show variables查看参数的当前值。因此在这一系列的课程中，“参数”和“变量”很多时候指的都是同一个概念。

### 设置参数

有几个方法都可以用来设置参数。首先mysqld进程启动时，可以指定一系列的命令行参数。下面是一个比较典型的例子。

```go
$ ps -elf | grep mysqld
... /usr/local/mysql/bin/mysqld \
    --defaults-file=/data/mysql01/my.cnf \
    --basedir=/usr/local/mysql \
    --datadir=/data/mysql01/data \
    --plugin-dir=/usr/local/mysql/lib/plugin \
    --user=mysql \
    --log-error=/data/mysql01/log/alert.log \
    --open-files-limit=1024 \
    --pid-file=/data/mysql01/run/mysqld.pid \
    --socket=/data/mysql01/run/mysql.sock
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/53/18/de532447.jpg" width="30px"><span>范特西</span> 👍（2） 💬（1）<div>在 linux 系统里面 lower_case_table_names 只支持设置为 0 或者 1，设置为 0 表示区分大小写，按照用户输入存储，设置为 1 表示不区分大小写，用户创建表名为大写时会按照小写存储，设置为 0 可能会出现两种命名方式，驼峰或者下划线，从标准化的角度想，希望表命名规则是统一的，可读性高，设置为 1 时，相当于数据库表名只能有下划线一种规则，所以推荐为 1</div>2024-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/4a/fe/7b6bd101.jpg" width="30px"><span>笙 鸢</span> 👍（1） 💬（2）<div>select file_id, start_lsn, end_lsn from innodb_redo_log_files;老师，这条命令在我的8.0版本没有找到这个表，我看一些文档说明是在perfmance_schema库下，但是不是跟版本有关，8.0.30才有的这个表？若是之前版本怎么能查看相对应的redolog lsn信息呢</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/4e/44/49b29792.jpg" width="30px"><span>Geek_0126</span> 👍（1） 💬（1）<div>lower_case_table_names参数一般推荐设置成1，这样库名表名不区分大小写。</div>2024-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/4d/161f3779.jpg" width="30px"><span>ls</span> 👍（0） 💬（1）<div>在 Unix 上lower_case_table_names的默认值为 0。在Windows上默认值为 1。在macOS 上默认值为 2
0表示，表在文件系统存储的时候，对应的文件名是按建表时指定的大小写存的，MySQL 内部对表名的比较也是区分大小写的；
1表示，表在文件系统存储的时候，对应的文件名都小写的，MySQL 内部对表名的比较是转成小写的，即不区分大小写；
2表示，表在文件系统存储的时候，对应的文件名是按建表时指定的大小写存的，但是 MySQL 内部对表名的比较是转成小写的，即不区分大小写。

0适用于区分大小写的系统，1都适用，2适用于不区分大小写的系统。</div>2024-08-26</li><br/>
</ul>