你好，我是俊达。

从前两讲中，我们知道了InnoDB表和索引的物理存储格式。执行Select语句的时候，最终会从ibd文件中获取数据，执行Insert/Update/Delete语句的时候，最终会将数据写入到ibd文件。读取或修改ibd文件中的数据时，都需要先将数据页缓存到InnoDB Buffer Pool中。这主要是因为访问内存的响应时间比访问磁盘要低几个数量级，将数据页缓存在Buffer Pool中再操作，可以减少磁盘的访问次数，提升性能。

那么数据页是怎么加载到Buffer Pool中，又是怎么写回到ibd文件中的，缓存页在Buffer Pool中是怎么组织的？这就是这一讲中我们要学习的内容。

另外，Buffer Pool中还有一些用来提升性能和保证数据一致性的结构，包括Change Buffer、自适应Hash索引、Double Write Buffer，对这些结构我们也会做一些介绍。

## InnoDB Buffer Pool

InnoDB将数据存储在表空间中，读取或写入数据时，需要先将数据从文件加载到内存中。InnoDB分配了专门的内存来缓存表空间中的数据（包括表、索引以及回滚段等），这一块内存称为Buffer Pool。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM59PTNiaDASVicbVaeWBU1WKmOgyHcqVtl85nDwAqDicib1EUKE2RRoU0x0vZctZO4kbPDUTTke8qKfAw/132" width="30px"><span>binzhang</span> 👍（0） 💬（1）<div>思考题： 对于drop的表和索引没有必要同步刷脏页和清理非脏页。mysql 可以在内存里或者文件头记录该space ID是否被drop了。可以采用异步的方式 刷脏页线程遇见drop table&#47;index的脏页直接抛弃。新创建一个线程专门异步处理lru中的非脏页。 这样drop 超级大的表也可以很快结束。</div>2024-10-23</li><br/>
</ul>