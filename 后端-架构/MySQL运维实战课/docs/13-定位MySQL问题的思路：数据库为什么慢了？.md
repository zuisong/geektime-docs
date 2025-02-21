你好，我是俊达。

作为一名DBA，在使用和运维MySQL的十多年里，我遇到过很多各种各样的问题，比如：

- 平时执行很正常的一些SQL，不知道什么原因，突然都变慢了。
- 数据库变得很慢，就是连接到数据库这么简单的操作都需要好几秒，有时甚至会超时。
- 应用系统发布了新的版本，SQL好像也没有做大的调整，但是数据库负载就是上涨了很多。
- 执行某个SQL为什么需要花这么长的时间，总选不到更好的执行计划。

这些都是比较常见的情况，你平时在使用MySQL时，是否也遇到过类似的问题呢？在这一讲中，我们将提供一些比较通用的方法，用来分析和定位MySQL的各种性能问题。

## 通用问题分析框架

把大象放入冰箱只需要几个简单的步骤：一是打开冰箱门，二是将大象放入冰箱，三是关上冰箱门。在分析MySQL相关问题时，我们也采取类似的步骤，首先，了解问题，然后分析MySQL运行环境的问题，再分析MySQL数据库，最后分析访问数据库的客户端的问题。

### 了解问题本身

在正式开始解决问题之前，你需要先了解问题本身。

- 问题是不是正在发生？是当前有问题，还是过去某些时间出现了问题？
- 收集问题的详细信息。问题的现象是什么，问题出现的时间有什么规律吗？
- 如果有报错，记录详细的报错信息，特别是跟数据库相关的报错信息，如错误编号、错误文本。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/8d/4d/992070e8.jpg" width="30px"><span>叶明</span> 👍（1） 💬（1）<div>会话 1842782 的 state 字段的完整信息是不是 Waiting for table flush？

从 id 和 time 字段来分析这个过程执行的顺序：
首先，会话 1657130 中的语句被执行，Time 达到 184551 秒，查询语句是聚合语句，说明这是一个大查询，在查询执行期间，语句中涉及到的表会被打开，且持有 MDL 读锁。
其次，可能执行了一个类似 flush tables 的命令，导致有刷新表的操作，该操作要关闭并重新打开表，因为会话 1842782 在执行大查询，表处于打开状态，因此发生冲突，从而进入等待状态
最后，会话 1842782 对该表中记录进行变更，从 state 来看，该会话处于等待状态，看来是被执行 flush tables 的会话 1044 所阻塞


会话 1044 中的 flush table 操作与大查询冲突，导致后续涉及到该表的读写操作的会话都陷入阻塞。</div>2024-09-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM59PTNiaDASVicbVaeWBU1WKmOgyHcqVtl85nDwAqDicib1EUKE2RRoU0x0vZctZO4kbPDUTTke8qKfAw/132" width="30px"><span>binzhang</span> 👍（1） 💬（1）<div>思考题里面1044这个thread值得怀疑 系统用户 没有显示具体是哪个db 在connect阶段 做flush tables操作。先杀这个试试。不知道为啥一个connect命令会触发flush table</div>2024-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/77/16/96ef147f.jpg" width="30px"><span>王欢</span> 👍（0） 💬（1）<div>mysql 大事务，多条update 和 多条delete 语句， 事务执行时间长有什么好的优化办法吗</div>2024-09-24</li><br/>
</ul>