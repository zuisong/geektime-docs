你好，我是俊达

这一讲中，我们接着上一讲的内容，介绍InnoDB中B+树的物理结构，以及InnoDB管理数据文件的一些数据结构。

先创建一个测试表，写入一些数据。

```plain
CREATE TABLE t_btree (
  id varchar(100) NOT NULL,
  a varchar(100),
  padding varchar(1024),
  PRIMARY KEY (id),
  KEY idx_a (a)
) ENGINE=InnoDB;


insert into t_btree(id, a, padding)
select concat('PK', rpad('', 93, '-'), 10000 + n), 
    concat('KEY', rpad('', 92, '-'), 10000 + n), 
    rpad('', 512, 'DATA')
from numbers
order by n;
```

## InnoDB中的B+树

之前我们提到过，InnoDB中表和索引都是B+树的结构，下面就是B+树的一个简单示意图。

![图片](https://static001.geekbang.org/resource/image/e1/61/e13e508ac2e765a9620c1918590c7d61.jpg?wh=1384x701)  
B+树由根节点（root page）、分支节点（branch page）和叶子节点（leaf page）组成。每个页面由头部信息和页面记录组成。分支页面的记录中，有指向下一个层级的页面编号。页面头部还记录了同一层级中相邻页面的编号，这些页面组成一个双向链表。页面记录包含Key和Value两个部分。对于主键，Key就是组成Primary Key的字段，分支页面中的Value值是页面编号（Page Number），叶子页面中，Value值包括隐藏字段DB\_TRX\_ID，DB\_ROLL\_PTR，以及表结构中Primary Key之外的字段。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM59PTNiaDASVicbVaeWBU1WKmOgyHcqVtl85nDwAqDicib1EUKE2RRoU0x0vZctZO4kbPDUTTke8qKfAw/132" width="30px"><span>binzhang</span> 👍（1） 💬（1）<div>为啥在二级索引的root和branch page上要存储主键列的值？ 感觉没必要啊</div>2024-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（0） 💬（1）<div>我觉得和系统表空间 ibdata1 有关系，系统表 mysql.indexes 在实例初始化时生成，其元数据信息（如根页面编号）可能被存储在系统表空间里，Innodb 在启动时可以直接访问这些位置，而不需要依赖数据字典。</div>2024-10-21</li><br/>
</ul>