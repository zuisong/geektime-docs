你好，我是俊达。

这一讲我们来聊一聊MySQL中的锁。MySQL中，存在很多不同类型的锁，我们先来大致了解下不同锁的作用。

## MySQL中的锁

MySQL使用锁来控制多个并发的进程或线程对共享资源的访问。那么在MySQL中，有哪些共享资源呢？

我总结起来，大致有下面这几种类型。

- 内存中的数据结构。
  
  - 内存中的链表结构，如会话列表、活跃事务列表、InnoDB Buffer Pool 中LRU链表、Flush链表、Hash链表等等。
  - 内存中的变量，如REDO日志序列号、下一个事务的事务ID。
  - 缓存的页面。
- 元数据，包括表、SCHEMA、存储过程等。
- 表和表里的记录。

MySQL使用了不同类型的锁，来保护这些不同类型的共享资源，对于上面提到的这几类资源，MySQL分别使用了下面这些类型的锁。

- mutex和rw-lock，用于保护内存中的数据结构。使用show engine innodb status、show engine innodb mutex等命令可以查看到一些mutex的信息。
- 元数据锁（metadata lock），用于管理对数据库对象的并发访问。查询数据（Select）、修改数据（insert、update、delete）、修改表结构时都需要先获取表的元数据锁。