你好，我是俊达。这一讲我们来了解下InnoDB的物理存储格式。

了解物理存储格式有什么作用呢？有时，由于系统表空间或其他物理文件损坏，数据库可能无法启动，即使设置了参数innodb\_force\_recovery还是无法启动。有时，由于误操作把表DROP了，或者是在文件系统层面把ibd文件删除了。

解决这些问题，正规的做法是做好备份、备库。但是在一些极端情况下，没有备份和备库，你还能把数据找回来吗？掌握InnoDB数据文件的格式后，理论上你可以解析ibd文件，提取出里面的数据。如果ibd文件被删除了，可以先使用文件恢复工具找回文件，然后再解析ibd文件。

另外，理解物理文件格式，也能帮你更好地掌握InnoDB内部原理，比如B+树在物理上是怎么存储的，插入、删除、更新等操作具体做了什么，Buffer Pool的结构到底是怎样的，Redo和Undo是如何保证数据不丢的。

要理解InnoDB的物理存储结构，最好的方法是创建一些测试表，写入一些数据，然后用一些工具打开文件，理解文件中的每一个字节的含义。

我们先创建一个测试表，写入几行数据。

```plain
create table t_dynamic(
  id varchar(30) not null,
  c1 varchar(255),
  c2 varchar(255),
  c3 varchar(8200),
  c4 text,
  primary key(id)
) engine=innodb row_format=dynamic charset=latin1;

insert into t_dynamic(id, c1, c2, c3, c4) 
values
 ('ROW_001', rpad('', 5, 'A1'), rpad('', 13, 'A2'), 
      rpad('',8123,'A3'), rpad('', 8124, 'A4')),
 ('ROW_003', rpad('', 5, 'B1'), rpad('', 13, 'B2'), null, rpad('', 129, 'B4')),
 ('ROW_002', rpad('', 5, 'E1'), rpad('', 13, 'E2'), null, rpad('', 22, 'E4')),
 ('ROW_007', rpad('', 5, 'D1'), rpad('', 13, 'D2'), null, rpad('', 27, 'D4')),
 ('ROW_004', rpad('', 5, 'F1'), rpad('', 13, 'F2'), null, rpad('', 24, 'F4')),
 ('ROW_005', rpad('', 5, 'C1'), rpad('', 13, 'C2'), null, rpad('', 35, 'C4')),
 ('ROW_006', rpad('', 5, 'G1'), rpad('', 13, 'G2'), null, rpad('', 26, 'G4')),
 ('ROW_008', rpad('', 5, 'H1'), rpad('', 13, 'H2'), 
      rpad('', 28, 'H3'), rpad('', 28, 'H4'));
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（1） 💬（1）<div>在每个段开始时，先用 32个碎片页来存放数据，在使用完这些碎片页之后才去申请 64个连续页，这样对于一些小表，可在开始时申请较少的空间，节省磁盘开销

mysql&gt; system ls -lh &#47;data&#47;mysql&#47;mysql3306&#47;data&#47;test&#47;t1.ibd
-rw-r----- 1 mysql mysql 112K Oct 20 23:20 &#47;data&#47;mysql&#47;mysql3306&#47;data&#47;test&#47;t1.ibd

mysql&gt; INSERT into t1 SELECT NULL,REPEAT(&#39;a&#39;,7000);
...

mysql&gt; system ls -lh &#47;data&#47;mysql&#47;mysql3306&#47;data&#47;test&#47;t1.ibd
-rw-r----- 1 mysql mysql 608K Oct 20 23:18 &#47;data&#47;mysql&#47;mysql3306&#47;data&#47;test&#47;t1.ibd

mysql&gt; INSERT into t1 SELECT NULL,REPEAT(&#39;a&#39;,7000);
mysql&gt; system ls -lh &#47;data&#47;mysql&#47;mysql3306&#47;data&#47;test&#47;t1.ibd
-rw-r----- 1 mysql mysql 2.0M Oct 20 23:18 &#47;data&#47;mysql&#47;mysql3306&#47;data&#47;test&#47;t1.ibd</div>2024-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（1） 💬（1）<div>老师，后面可以单独来个每章最后的问题解答吗？</div>2024-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/4a/fe/7b6bd101.jpg" width="30px"><span>笙 鸢</span> 👍（0） 💬（1）<div>对于我们使用的默认的 16K 的页面大小，任意一个页面在文件中的偏移量是 16K 的整数倍，任意一个字节在页面内的偏移量在 0x00 - 0x03FF 之间。这个一个字节在页面的偏移量有点看不懂，是不是0x00-0x3FFF啊。。。</div>2024-12-10</li><br/>
</ul>