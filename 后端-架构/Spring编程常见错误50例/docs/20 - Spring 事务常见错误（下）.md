你好，我是傅健。

通过上一节课的学习，我们了解了 Spring 事务的原理，并解决了几个常见的问题。这节课我们将继续讨论事务中的另外两个问题，一个是关于事务的传播机制，另一个是关于多数据源的切换问题，通过这两个问题，你可以更加深入地了解 Spring 事务的核心机制。

## 案例 1：嵌套事务回滚错误

上一节课我们完成了学生注册功能，假设我们需要对这个功能继续进行扩展，当学生注册完成后，需要给这个学生登记一门英语必修课，并更新这门课的登记学生数。为此，我添加了两个表。

1. 课程表 course，记录课程名称和注册的学生数。

```
CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(64) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

2. 学生选课表 student\_course，记录学生表 student 和课程表 course 之间的多对多关联。

```
CREATE TABLE `student_course` (
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

同时我为课程表初始化了一条课程信息，id = 1，course\_name = "英语"，number = 0。

接下来我们完成用户的相关操作，主要包括两部分。

1. 新增学生选课记录

```
@Mapper
public interface StudentCourseMapper {
    @Insert("INSERT INTO `student_course`(`student_id`, `course_id`) VALUES (#{studentId}, #{courseId})")
    void saveStudentCourse(@Param("studentId") Integer studentId, @Param("courseId") Integer courseId);
}
```

2. 课程登记学生数 + 1

```
@Mapper
public interface CourseMapper {
    @Update("update `course` set number = number + 1 where id = #{id}")
    void addCourseNumber(int courseId);
}
```

我们增加了一个新的业务类 CourseService，用于实现相关业务逻辑。分别调用了上述两个方法来保存学生与课程的关联关系，并给课程注册人数+1。最后，别忘了给这个方法加上事务注解。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/81/0e/ec667c01.jpg" width="30px"><span>Wallace Pang</span> 👍（5） 💬（0）<div>spring boot多数据源更简单</div>2021-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/81/cc/07257bc8.jpg" width="30px"><span>Yarin</span> 👍（2） 💬（0）<div>内外部事务都使用注解，希望两者同步回滚。但是内部事务抛出特定异常回滚，外部事务接收到的是回滚异常，如何把这个异常传给外部事务呢？我们目前做的是内部事务手动开启事务，在抛出指定异常后手动回滚，再往外抛出指定异常。欢迎交流，有没有更好的方法。</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/fc/379387a4.jpg" width="30px"><span>ly</span> 👍（2） 💬（2）<div>第1个案例个人觉得有个小问题: 
内层事务是给学员存储要学的学科，如果用的新事务require_new，那么假设内层事务程序改为不抛异常了，内层事务就会正常先入库。 
而此时外层事务还未提交，一旦出现程序问题，导致异常，那么学员就不能保存成功，但是结果呢，学员所学的学科已经成功入库了。感觉就产生垃圾数据了。  我不知道分析对没</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/89/34f2cbcc.jpg" width="30px"><span>杨宇</span> 👍（2） 💬（0）<div>对于高频访问数据库的场景，DriverManagerDatasource效率低下，应改用HikariDatasource</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/57/27de274f.jpg" width="30px"><span>萧</span> 👍（1） 💬（0）<div>干货满满</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/33/a9/791d0f5e.jpg" width="30px"><span>你是否清醒</span> 👍（0） 💬（0）<div>这种两个数据源一般就用分布式事务的了</div>2024-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/7d/774e07f9.jpg" width="30px"><span>study的程序员</span> 👍（0） 💬（0）<div>直接指定两个TransactionManager  ,两个DataSource ,@Transactional指定manager 更方便吧</div>2022-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/7d/774e07f9.jpg" width="30px"><span>study的程序员</span> 👍（0） 💬（0）<div>point.proceed(); 
MyDataSource.clearDataSource();
要加上try finally</div>2022-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/99/c3/e4f408d4.jpg" width="30px"><span>陌兮</span> 👍（0） 💬（0）<div>虽然多数据源事务的操作让人眼前一亮，但是涉及到的问题也非常多。感觉实用性并不大啊</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/39/c5/868a626c.jpg" width="30px"><span>palladio</span> 👍（0） 💬（0）<div>不行。每个事务都是和对应数据源绑定的，在默认事务声明的情况下，外层和内层的事务是同一个，也就意味着两个事务绑定的数据源是同一个。所以外层和内层事务回滚的都是同一个数据源，card 库回滚不了</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/07/70/cc0e0288.jpg" width="30px"><span>S | c</span> 👍（0） 💬（0）<div>案例二没太理解，多个数据源的场景为什么不声明多个transactionManager bean实例？各管各的dataSource。。。

@Transactional可以指定对应的transactionManager bean吧，反正你内部的发卡service也是在card库上开一个新事务来跑。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学到很多技巧</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/62/47/7c83cebe.jpg" width="30px"><span>梦尘</span> 👍（0） 💬（0）<div>如果用默认的传播属性，切换应该会失败，会一直使用前一个数据源。
AbstractPlatformTransactionManager.getTransaction()下的isExistingTransaction应该是true，所以DataSourceTransactionManager.doBegin()不会再次进入了。</div>2021-06-22</li><br/>
</ul>