你好，我是宫文学。现在，就到了我们编译之旅的最后一站了，我们一起来探索一下MySQL编译器。

数据库系统能够接受SQL语句，并返回数据查询的结果，或者对数据库中的数据进行修改，可以说几乎每个程序员都使用过它。

而MySQL又是目前使用最广泛的数据库。所以，解析一下MySQL编译并执行SQL语句的过程，一方面能帮助你加深对数据库领域的编译技术的理解；另一方面，由于SQL是一种最成功的DSL（特定领域语言），所以理解了MySQL编译器的内部运作机制，也能加深你对所有使用数据操作类DSL的理解，比如文档数据库的查询语言。另外，解读SQL与它的运行时的关系，也有助于你在自己的领域成功地使用DSL技术。

**那么，数据库系统是如何使用编译技术的呢？**接下来，我就会花两讲的时间，带你进入到MySQL的内部，做一次全面的探秘。

今天这一讲，我先带你了解一下如何跟踪MySQL的运行，了解它处理一个SQL语句的过程，以及MySQL在词法分析和语法分析方面的实现机制。

好，让我们开始吧！

## 编译并调试MySQL

按照惯例，你要下载[MySQL的源代码](https://github.com/mysql/mysql-server)。我下载的是8.0版本的分支。

源代码里的主要目录及其作用如下，我们需要分析的代码基本都在sql目录下，它包含了编译器和服务端的核心组件。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（2） 💬（2）<div>宫老师，按照这篇文章https:&#47;&#47;www.codeleading.com&#47;article&#47;90351944418&#47; 用xcode build mysqld这个项目时，报下面的错误。请问老师知道是哪里出现了问题。
dyld: Symbol not found: __ZN20wireless_diagnostics6google8protobuf2io16CodedInputStream24default_recursion_limit_E
  Referenced from: &#47;System&#47;Library&#47;PrivateFrameworks&#47;WirelessDiagnostics.framework&#47;Versions&#47;A&#47;Libraries&#47;libAWDSupport.dylib。

  Expected in: &#47;Users&#47;xxx&#47;Documents&#47;mysql-server&#47;bld_debug&#47;library_output_directory&#47;Debug&#47;libprotobuf-lite.dylib
 in &#47;System&#47;Library&#47;PrivateFrameworks&#47;WirelessDiagnostics.framework&#47;Versions&#47;A&#47;Libraries&#47;libAWDSupport.dylib

</div>2020-08-20</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（2） 💬（2）<div>没有自己开发过dsl，但是经常会用json作为配置文件，通过json格式的结构来描述一个类似于AST的结构，然后写一个解释器按照自己定义的规则去执行操作。
相当于人肉做了前端工作吧，等有时间了，可以自己去试着写一个前端部分，自己编写一套语法规则</div>2020-07-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cabLXAUXiavXnEckAgo971o4l1CxP4L9wOV2eUGTyKBUicTib6gJyKV9iatM4GG1scz5Ym17GOzXWQEGzhE31tXUtQ/132" width="30px"><span>日就月将</span> 👍（0） 💬（1）<div>老师 mysql root用户缺省的密码 在哪里查看</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d4/54/7263deb2.jpg" width="30px"><span>吃饭</span> 👍（0） 💬（0）<div>老师，尝试可很久去debug mysql,还是不知道怎么搞，c++&#47;c之类的的确不怎么熟，能详细描述一下吗？</div>2021-07-25</li><br/>
</ul>