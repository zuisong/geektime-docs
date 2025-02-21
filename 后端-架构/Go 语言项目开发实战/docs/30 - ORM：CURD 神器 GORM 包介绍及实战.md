你好，我是孔令飞。

在用Go开发项目时，我们免不了要和数据库打交道。每种语言都有优秀的ORM可供选择，在Go中也不例外，比如[gorm](https://github.com/go-gorm/gorm)、[xorm](https://github.com/go-xorm/xorm)、[gorose](https://github.com/gohouse/gorose)等。目前，GitHub上 star数最多的是GORM，它也是当前Go项目中使用最多的ORM。

IAM项目也使用了GORM。这一讲，我就来详细讲解下GORM的基础知识，并介绍iam-apiserver是如何使用GORM，对数据进行CURD操作的。

## GORM基础知识介绍

GORM是Go语言的ORM包，功能强大，调用方便。像腾讯、华为、阿里这样的大厂，都在使用GORM来构建企业级的应用。GORM有很多特性，开发中常用的核心特性如下：

- 功能全。使用ORM操作数据库的接口，GORM都有，可以满足我们开发中对数据库调用的各类需求。
- 支持钩子方法。这些钩子方法可以应用在Create、Save、Update、Delete、Find方法中。
- 开发者友好，调用方便。
- 支持Auto Migration。
- 支持关联查询。
- 支持多种关系数据库，例如MySQL、Postgres、SQLite、SQLServer等。

GORM有两个版本，[V1](https://github.com/jinzhu/gorm)和[V2](https://github.com/go-gorm/gorm)。遵循用新不用旧的原则，IAM项目使用了最新的V2版本。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（6） 💬（1）<div>go语言中，orm使用gorm包。
gorm功能全，操作界面符合直觉，不需要额外的理解负担。</div>2021-08-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83equY82MMjfvGtzlo8fhT9fdKO5LjWoy0P8pfCmiaFJS0v8Z4ibzrmwHjib9CnmgMiaYMhPyja7qS6KqiaQ/132" width="30px"><span>Geek_004fb2</span> 👍（3） 💬（1）<div>老师,企业级的应用往往需要在业务层处理&quot;事物&quot;,这个模式应该如何设计比较优雅?我看了iam项目暂时没发现相关处理</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（3） 💬（1）<div>测试发现项目中的软删除功能不起作用, 需要将源码
https:&#47;&#47;github.com&#47;marmotedu&#47;component-base&#47;blob&#47;master&#47;pkg&#47;meta&#47;v1&#47;types.go 中的
DeletedAt *time.Time `json:&quot;-&quot; gorm:&quot;column:deletedAt;index:idx_deletedAt&quot;` 
改为: 	
DeletedAt gorm.DeletedAt `json:&quot;-&quot; gorm:&quot;index;column:deletedAt&quot;`

</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/5b/a1656a72.jpg" width="30px"><span>潘达</span> 👍（3） 💬（1）<div>gorm下是否有从表中直接生成struct的工具呢，xorm下的反向生成工具还是挺实用的</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/8f/61/cf0d0a95.jpg" width="30px"><span>huining</span> 👍（2） 💬（1）<div>如果按照这样写，那用不了事务啊，比如老师的代码里删除用户时，是先调用polices.delete(),然后再delete用户，那假如中途出错，也无法回滚。我的做法是再加一个*DB参数，但是感觉写起来很丑，方法里要判断之前是否启动了事务。所以如果想要添加对事务的支持应该怎么做呢？</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（2） 💬（1）<div>总结：
1. 首先定义一个 GORM 模型（Models），GORM模型就是一个普普通通的golang struct。使用结构体名的 snake_cases 作为表名，使用字段名的 snake_case 作为列名。
2. gorm.Model 为表增加了 ID、CreatedAt、UpdatedAt、DeletedAt 等字段。如果是资源表，建议统一资源的元数据。参见第29章节。
3. 在结构体中，通过 tag，指定数据库中字段的名称。
4. gorm 支持表CRUD操作，每种操作也会有各种变形，与 数据库操作相对应。
</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/e2/e6d3d9bf.jpg" width="30px"><span>XI</span> 👍（2） 💬（1）<div>go的连接池网上教程有点少，go 连接redis,monggodb 应该都需要连接池，gorm官方文档连接池的讲解也是寥寥数语，老师能不能详细补充点连接池相关的，如何使用，如果能再加上redis ，mongdb 的连接池一类的就更好了</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（1） 💬（1）<div>孔大，ent咋样 有没有ent的讲解呢 👀</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/b4/ff82483d.jpg" width="30px"><span>邵俊达</span> 👍（1） 💬（2）<div>请问 gorm 如何处理操作多张表的事务？比如类似
```
begin
 User.save
 Book.update
 Account.update
commit
```

用 gorm 的 transaction 就要用他的 tx 来操作数据，那封装好的 dao 是不是就没法用了？</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/1e/18/9d1f1439.jpg" width="30px"><span>liaomars</span> 👍（1） 💬（1）<div>老师：
sqlDB.SetMaxIdleConns(10)              &#47;&#47; 设置MySQL的最大空闲连接数（推荐100）
这个最大空闲连接数是10还是100？代码写的是10，注释写的是100</div>2021-12-03</li><br/><li><img src="" width="30px"><span>刘世杰</span> 👍（1） 💬（1）<div>老师您好，
我在使用 github.com&#47;go-xorm&#47;xorm 这个包连接 mycat 的时候
当我执行带 ? 号的 sql 语句时出现 {&quot;Number&quot;:1047,&quot;Message&quot;:&quot;Prepare unsupported!&quot;} 报错
我应该怎么配置连接信息呢？
以下是我的数据库连接信息
user:pass@tcp(127.0.0.1:3306)&#47;db?charset=utf8&amp;interpolateparams=true
以下是我执行的代码
engine := model.Get()
uid := 1
var list []model.User
res1 := engine.SQL(&quot;select * from tr_user where id = ?&quot;, uid).Find(&amp;list)
res := engine.SQL(&quot;select * from tr_user where id = 1&quot;).Find(&amp;list)
data := map[string]interface{}{
	&quot;userid&quot;: con.Uid,
	&quot;res&quot;: res,
	&quot;res1&quot;: res1,
	&quot;list&quot;: list,
}
以上 res1 打印的信息是 &quot;res1&quot;:{&quot;Number&quot;:1047,&quot;Message&quot;:&quot;Prepare unsupported!&quot;}
res 运行的 sql 能够正常运行
直连数据库的时候，本地连接数据库，以上代码均正常
使用 mycat 时，无法正常执行 sql
网上看了一些文档，说是 interpolateparams 这个参数的问题，但是我试了都没有用</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（1） 💬（2）<div>生产环境不应该使用AutoMigrate，除非有靠谱的code review流程，否则随着协作的人数越多，越容易失控</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>看了下iam启动过程的源码，发现依赖的mysql实例获取不到也不会退出程序，个人感觉这样设计是否更好：写两个函数，一个用来初始化mysql单例，一个用来获取mysql单例，在server的Preparerun函数中来初始化，初始化失败则退出程序提示用户，在router中来获取已经初始化过的mysql单例，这样感觉更清晰一些～</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/67/4e381da5.jpg" width="30px"><span>Derek</span> 👍（1） 💬（1）<div>老师，拿要是连接多个数据库，不同的struct使用不同的库要怎么搞，是不是要初始化好几个连接，然后指定一下struct用的库？</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/91/b1/fb117c21.jpg" width="30px"><span>先听</span> 👍（1） 💬（1）<div>请问 事务的嵌套，有没有什么好的解决方案呢</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（1） 💬（1）<div>“如果没有指定表名，则 GORM 使用结构体名的蛇形复数作为表名。例如：结构体名为 DockerInstance ，则表名为 dockerInstances 。”，蛇形不是下划线连接吗</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a5/5b/164dc7d2.jpg" width="30px"><span>二三闲语</span> 👍（1） 💬（3）<div>怎么配置主从，多库</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>请问老师，在链接数据库New方法里，是否要调用下sqlDB.ping来确定链接是否成功呢？</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（3）<div>GORM 支持 AutoMigrate 功能，思考下，你的生产环境是否可以使用 AutoMigrate 功能，为什么？

肯定不能啊，生产环境严格的要死，提交的SQL都要一圈的审核，怎么能直接偏移，爆炸了年奖全都没了</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/9a/6f/c4490cf2.jpg" width="30px"><span>czy</span> 👍（0） 💬（2）<div>
&#47;&#47; DELETE from users where id = 10 AND name = &quot;jinzhu&quot;;
db.Where(&quot;name = ?&quot;, &quot;jinzhu&quot;).Delete(&amp;user)
这段代码是不是有问题？没有添加id过滤条件呀？</div>2022-10-26</li><br/><li><img src="" width="30px"><span>Geek_c2083d</span> 👍（0） 💬（1）<div>java用惯了mybatis-plus 感觉这个好难用呀，sql写在代码里面不是很难维护码，</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（0） 💬（1）<div>“接着，在PrepareRun函数中，调用GetMySQLFactoryOr函数，初始化并获取仓库层的实例mysqlFactory” 
PrepareRun 函数中调用 GetMySQLFactoryOr 获取的仓库层实例是为了在优雅关停时关闭数据库，初始化仓库层实例步骤是在这个方法里完成的：func (c *completedExtraConfig) New() (*grpcAPIServer, error)</div>2022-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8e/62/5cb377fd.jpg" width="30px"><span>yangchnet</span> 👍（0） 💬（1）<div>问题：
1. 请问老师了解sqlc这个包吗
2. 数据库版本迁移老师有没有靠谱好用的工具推荐</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（1） 💬（0）<div>目前用过几款orm。有beego自带的  gorm ent</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/02/e4/700e5bcd.jpg" width="30px"><span>Harris Han</span> 👍（0） 💬（1）<div>十分想了解老师的事务实现方式，现在就只能传db *gorm.DB 来在service层开启事务了。</div>2023-02-15</li><br/><li><img src="" width="30px"><span>geek_geek</span> 👍（0） 💬（0）<div>老是请问事物怎么启动？</div>2021-12-23</li><br/>
</ul>