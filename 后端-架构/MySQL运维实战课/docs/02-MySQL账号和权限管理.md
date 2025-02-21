你好，我是俊达。

在上一讲中，我们学习了安装MySQL的几种方法。MySQL安装好之后，系统默认建好了root@localhost用户，这个用户只能在MySQL服务器上登录本地的数据库。root账号拥有数据库所有的权限，可以执行任何操作，因此我建议应用程序不要使用root账号访问数据库，这存在很大的安全隐患。

我们需要根据各个业务方的访问需求，分别创建数据库用户，并授予合理的权限。在这一讲中，我们来学习如何创建和管理数据库用户，以及如何给用户授权。

## 用户管理

我们使用create user命令创建用户，你可以看一下命令的基本格式。

```plain
create user 'username'@'host' identified by 'complex_password';
```

在MySQL中，一个用户由两部分组成，username是用户名，host是允许登录数据库的客户端的主机名或IP。host中可以使用通配符，使用百分号 `"%"` 匹配任意字符串，使用下划线 `"_"` 匹配一个字符。比如我们下面创建的这个用户，可以在任何地方登录数据库。

```plain
create user 'u01'@'%' identified by 'somepassword';
```

创建账号时，也可以使用IP地址段来指定客户端IP范围，比如下面创建的u02用户可以在172.16这个网段内访问数据库。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3c/4e/44/49b29792.jpg" width="30px"><span>Geek_0126</span> 👍（3） 💬（1）<div>1.网络防火墙做好端口放行策略。
2.使用单独的账号，并给予最小权限
3.传输加密</div>2024-08-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM59PTNiaDASVicbVaeWBU1WKmOgyHcqVtl85nDwAqDicib1EUKE2RRoU0x0vZctZO4kbPDUTTke8qKfAw/132" width="30px"><span>binzhang</span> 👍（1） 💬（1）<div>This class not only talk about mysql knowledge ,but it also mention lots of best practices in production daily operation job. It&#39;s fantastic. </div>2024-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a1/d8/42252c48.jpg" width="30px"><span>123</span> 👍（1） 💬（1）<div>老师，权限赋值哪一块是否和用户登录的逻辑是一致（为什么会出现这样的问题呢？大概是因为 MySQL 只使用了库名为 &#39;db\_1&#39; 的这条授权记录。），具备一定的优先级，若存在指定表就不会去匹配通配符？
+-------------------------------------------------------------------------------------------+
| Grants for u03@%                                                                          |
+-------------------------------------------------------------------------------------------+
| GRANT PROCESS ON *.* TO `u03`@`%`                                                         |
| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON `db01`.* TO `u03`@`%` |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `db\_1`.* TO `u03`@`%`                            |
| GRANT CREATE, DROP, INDEX, ALTER ON `db__`.* TO `u03`@`%`                                 |
+-------------------------------------------------------------------------------------------+

对u03赋权DDL：grant create,alter,index,drop on `db\_1`.* to &#39;u03&#39;@&#39;%&#39;;
+--------------------------------------------------------------------------------------------+
| Grants for u03@%                                                                           |
+--------------------------------------------------------------------------------------------+
| GRANT PROCESS ON *.* TO `u03`@`%`                                                          |
| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON `db01`.* TO `u03`@`%`  |
| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON `db\_1`.* TO `u03`@`%` |
| GRANT CREATE, DROP, INDEX, ALTER ON `db__`.* TO `u03`@`%`                                  |
+--------------------------------------------------------------------------------------------+

因为对于同一个表，DDL和DML是在同一行，匹配到对应表的数据项后就直接返回了</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（1） 💬（1）<div>非专业回答：
风险一：任意来源访问，数据库被爆破登录
规避方案：授权尽量不使用 %，越精确越好
风险二：数据传输过程中被拦截捕获
规范方案：SSL 加密传输</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（0） 💬（1）<div>老师，请问在配置文件中配置bind-address = 0.0.0.0是必须的吧，否则就无法远程登录数据库？关于权限的控制，要在账号层面以及网络防火墙层面？</div>2024-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（0） 💬（2）<div>另外加的这个-e &#39;select current_user()&#39;是由什么特殊意义吗？</div>2024-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/93/f0247cf8.jpg" width="30px"><span>一本书</span> 👍（0） 💬（1）<div>[root@172-16-121-236 ~]# mysql -u u03 -pwrongpassword -h172.16.121.234ERROR 1045 (28000): Access denied for user &#39;u03&#39;@&#39;mysql02&#39; (using password: YES)$ mysql -u u03 -pwrongpassword -h172.16.121.234 -e &#39;select current_user()&#39;ERROR 1045 (28000): Access denied for user &#39;u03&#39;@&#39;192.168.113.13&#39; (using password: YES)
请问老师这两段SQL的对比是什么意思啊,意思是如果在服务器上存在172.16.121.236 mysql02的映射关系，返回报错信息里面的客户端IP会修改为主机名，当客户端IP是192.168.113.13时，由于映射关系不存在，所以报错信息里面返回客户端IP？</div>2024-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/24/36/0829cbdc.jpg" width="30px"><span>TheOne</span> 👍（0） 💬（2）<div>俊达老师你好，我有几个问题想请教一下
1. 我自己想搭建一个mysql的实验环境，我是用dokcer的方式来启动好，还是像您这章讲的一样自己去手把手安装一个好？如果未来我想搭建mysql的主从集群，配置读写分离这样的实验环境，用哪个会更方便一点呢？对于学习和实践来说，您更推荐哪种呢。
2. 还有就是现在云数据库很流行了，自己本地部署的库和云数据库除了硬件上，其他方面的差别大概有哪些呢？我的理解是云数据库会把 redolog binlog 各种 buff 的以及其他配置设置的更合理，让客户专注于自己的业务逻辑，除此之外，还有那些其他优势呢？</div>2024-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（0） 💬（1）<div>在公网容易被攻击。还有其他风险吗？</div>2024-08-21</li><br/>
</ul>