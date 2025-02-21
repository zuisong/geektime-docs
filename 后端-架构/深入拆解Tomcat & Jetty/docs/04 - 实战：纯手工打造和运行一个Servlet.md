作为Java程序员，我们可能已经习惯了使用IDE和Web框架进行开发，IDE帮我们做了编译、打包的工作，而Spring框架在背后帮我们实现了Servlet接口，并把Servlet注册到了Web容器，这样我们可能很少有机会接触到一些底层本质的东西，比如怎么开发一个Servlet？如何编译Servlet？如何在Web容器中跑起来？

今天我们就抛弃IDE、拒绝框架，自己纯手工编写一个Servlet，并在Tomcat中运行起来。一方面进一步加深对Servlet的理解；另一方面，还可以熟悉一下Tomcat的基本功能使用。

主要的步骤有：

1.下载并安装Tomcat。  
2.编写一个继承HttpServlet的Java类。  
3.将Java类文件编译成Class文件。  
4.建立Web应用的目录结构，并配置`web.xml`。  
5.部署Web应用。  
6.启动Tomcat。  
7.浏览器访问验证结果。  
8.查看Tomcat日志。

下面你可以跟我一起一步步操作来完成整个过程。Servlet 3.0规范支持用注解的方式来部署Servlet，不需要在`web.xml`里配置，最后我会演示怎么用注解的方式来部署Servlet。

**1. 下载并安装Tomcat**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/93/5d/91f1d849.jpg" width="30px"><span>darren</span> 👍（62） 💬（1）<div>发现xml与注解不能同时起作用，那在用xml方式的老项目中就没办法使用注解的方式了吗？</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（33） 💬（2）<div>老师，实践中发现个问题：虽然response.setContentType(&quot;text&#47;html;charset=utf-8&quot;)，但是out.println中有输出中文还是乱码的</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（18） 💬（2）<div>1、postman 
2、curl 命令发送post
3、用HttpClient发送

周六早上坚持打卡，本章节绝大多数知识以前有接触过，只有@WebServlet注解是新知识，现在业务开发一般都是写SpringMVC容器中的Controller来代替类似文中的Servlet类。

问题：基于Spring+SpringMVC+Mybais的框架搭建的项目，平常开发的都是写Controller与Service、DAO。
1、请问Servlet容器只管理DispatchServlet这一个Servlet吗？
2、有什么可视化工具可以直接查看各种容器中管理的对象吗？

谢谢！</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（11） 💬（1）<div>课后思考：
访问doPost()方法有两种方式
1. 使用postMan等工具发起post请求
2. 在代码中doGet()方法去调用doPost()

疑问：
doGet和doPost其实在网络层没有任何区别，通过浏览器地址栏中发起的是get请求，get请求其实也能携带像post请求一样的请求体参数，具体区别其实是不同浏览器和服务器实现方式的区别。
常见的面试题很喜欢考post和get的区别，之所以区分get和post是为了http协议更加解耦吗？就像业务拆分一样专职专工</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e1/d2/42ad2c87.jpg" width="30px"><span>今夜秋风和</span> 👍（9） 💬（1）<div>老师，验证的时候默认增加了 super.doGet(req, resp);在http1.1写一下不能工作，查看httpServlet 源码里面   对协议做了限制，http 1.1 协议默认不支持。这个为什么是这样设计的呢？
源代码:
        String protocol = req.getProtocol();
        String msg = lStrings.getString(&quot;http.method_get_not_supported&quot;);
        if (protocol.endsWith(&quot;1.1&quot;)) {
            resp.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, msg);
        } else {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, msg);
        }
第二个是如果是那个注解访问的，可以不用删除web.xml，把web.xml里面的url-pattern 改成注解同样的路由，也可以支持；如果web.xml 路由自定义一个的话，测试发现自定义的会有404，是不是注解的路由优先级会更高呢？
3.如果把web.xml删除，servlet容器启动的时候是不是会自动扫描注解类，将它注册到容器中?</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/98/6e17646a.jpg" width="30px"><span>桔子</span> 👍（6） 💬（1）<div>李老师，doGet方法的request和response的初始化代码在哪里呢，只知道是servlet容器创建的，但是去哪里可以看到容器初始化response的源码呢。</div>2019-05-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRiaKX0ulEibbbwM4xhjyMeza0Pyp7KO1mqvfJceiaM6ZNtGpXJibI6P2qHGwBP9GKwOt9LgHicHflBXw/132" width="30px"><span>Geek_ebda96</span> 👍（6） 💬（1）<div>李老师，请教一个问题，你这里所说的servlet和spring mvc里面的controller是什么关系，servlet里面可以直接接收请求，处理请求业务，controller只是通过dispatch servlet再接入进来的？</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/87/be/7466bf26.jpg" width="30px"><span>清风</span> 👍（5） 💬（1）<div>注解是高版本的Servlet才支持的吧，好像是2.5以上</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/4d/7ba09ff0.jpg" width="30px"><span>郑童文</span> 👍（5） 💬（1）<div>请问老师： 我们在servlet的实现类中import的是javax.servlet.http.HttpServlet 请问为什么需要Tomcat的servlet-api.jar呢？难道javax.servlet.http.HttpServlet这个类不是jdk中的吗？谢谢！</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/9f/8dbd9558.jpg" width="30px"><span>逆流的鱼</span> 👍（2） 💬（1）<div>用Tomcat实现servlet，总感觉哪里不对</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（2） 💬（1）<div>请问一下老师我这边在logs的文件夹下没有看到catalina.out， 是哪里没配置吗？</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/16/6c/26fc96c4.jpg" width="30px"><span>cloud</span> 👍（2） 💬（1）<div>是怎么找到有写的注解类？遍历加载所有jar包中的类吗</div>2019-05-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWOyzdmdY17rpT3NicFQ9xy7siaCGqG4ibq5LGAANjvmMO6aKmR81TRhpWWm0Xo665qwCQYMtIo4Wbg/132" width="30px"><span>Geek_1eaf13</span> 👍（1） 💬（1）<div>javac -cp .&#47;servlet-api.jar MyServlet.java
这个不是很理解老师</div>2019-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epgKOrnIOAjzXJgb0f0ljTZLeqrMXYaHic1MKQnPbAzxSKgYxd7K2DlqRW8SibTkwV2MAUZ4OlgRnNw/132" width="30px"><span>小羊</span> 👍（1） 💬（1）<div>可以介绍一些 有哪些 不继承 HTTPServlet 的 GenericServlet 实现类。
和直接实现 Servlet 的实现类吗？以及这样做的原因</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/85/081804f7.jpg" width="30px"><span>逍遥</span> 👍（0） 💬（2）<div>老师，我按您说的步骤操作一遍后，最后浏览器访问http:&#47;&#47;localhost:8080&#47;MyWebApp&#47;myservlet，是一片空白，啥都没有。。。。这是为啥，代码啥的跟您的都一模一样，只不过我用的jdk8和tomcat8，tomcat已经启动成功了</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（0） 💬（1）<div>老师，我在windows启动Tomcat，点击bin下的startup.bat，一个命令行黑框一闪而过，一直无法成功启动。求助</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/25/27/5aef841d.jpg" width="30px"><span>feitian</span> 👍（197） 💬（20）<div>既然是纯手工，就应该把servlet那套完整的写出来，不应该再用tomcat容器而应该手写实现tomcat的核心代码。最核心的应该是类似HttpServlet功能的实现，把这个从最初的servlet接口实现了才算讲透，不然还是有点和稀泥的感觉。我觉得应该按照这种思路讲会更好，请参考我写的mytomcat，https:&#47;&#47;github.com&#47;feifa168&#47;mytomcat</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/e8/bc84c47d.jpg" width="30px"><span>熊斌</span> 👍（27） 💬（10）<div>按老师的步骤操作，结果一致，开心！
整个过程遇到以下几个问题，记录一下，如果有遇到同样问题的小伙伴可以借鉴下解决问题的思路(大神可以略过)：

首先说明一下我的运行环境：
操作系统：win10
Tomcat版本：apache-tomcat-9.0.27（免安装版本）
JDK版本：jdk-13.0.1（免安装版）

问题1：javac失败
原因&amp;解决方案：未配置系统环境变量，在系统环境变量path中，加入E:\xxx\jdk-13.0.1\bin,问题解决；

问题2：脱离IDE，新建MyServlet.java，执行文章中的javac命令失败
原因&amp;解决方案：按文章中的命令原封不动执行的话，java源文件需要建到tomcat的lib目录下，否则会导包失败。然后在lib目录下，shift+右键（在此处打开命令窗口）打开cmd窗口，执行成功，生成了MyServlet.class

问题3：tomcat startup.bat执行一闪而过（如果一闪而过，说明没启动成功，拿文中的http:&#47;&#47;localhost:8080&#47;MyWebApp&#47;myservlet 访问的话什么都没有）
原因&amp;解决方案：按照https:&#47;&#47;blog.csdn.net&#47;scau_lth&#47;article&#47;details&#47;83218335 文章中，第二点方案得以解决。

问题4：访问http:&#47;&#47;localhost:8080&#47; 成功跳转tomcat主页，访问http:&#47;&#47;localhost:8080&#47;MyWebApp&#47;myservlet  404（这种情况一般就是容器启动加载你的应用失败，需要根据日志具体分析是哪块的问题）

原因&amp;解决方案：查看apache-tomcat-9.0.27\logs 目录下的日志发现，17-Nov-2019 22:19:40.620 信息 [main] org.apache.catalina.startup.HostConfig.deployDirectory 把web 应用程序部署到目录 [F:\workspace\apache-tomcat-9.0.27\webapps\MyWebApp]
17-Nov-2019 22:19:40.674 严重 [main] org.apache.tomcat.util.digester.Digester.fatalError Parse fatal error at line [2] column [6]
	org.xml.sax.SAXParseException; systemId: file:&#47;F:&#47;workspace&#47;apache-tomcat-9.0.27&#47;webapps&#47;MyWebApp&#47;WEB-INF&#47;web.xml; lineNumber: 2; columnNumber: 6; 不允许有匹配 &quot;[xX][mM][lL]&quot; 的处理指令目标。

Context [&#47;MyWebApp] startup failed due to previous errors
我的web.xml是直接从文章中拷贝的，复制粘贴时多了空格，修改后启动成功

修改后保存，容器会重新加载，看日志你会发现Context with name [&#47;MyWebApp] is completed
再次使用http:&#47;&#47;localhost:8080&#47;MyWebApp&#47;myservlet 浏览器访问时会看到结果 MyServlet
</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/01/63/193c7ecf.jpg" width="30px"><span>翼</span> 👍（21） 💬（0）<div>@Amanda 不知道怎么直接回复你，我跟你一样也是遇到乱码的问题。我也设置了response.setCharacterEncoding(utf8)，在getWriter之前，但依然是一样的乱码。
原因在与javac编译生成的class文件是用的gbk的编码。换句话说，你生成的class源文件就已经是中文乱码了。
所以在javac的时候加上 -encoding UTF-8就好了。
ps:我是Windows的环境。</div>2019-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（17） 💬（3）<div>IDE和框架诞生之初是为了让程序员从繁琐的底层配置中抽离出来专注于业务开发，然而大多数人在享受IDE和框架带来的便捷时，也成了温水里的青蛙，对于实现原理认识模糊，渐渐沦落为一个CRUD，这不是一件好事，啊～幡然醒悟</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/bd/a51ae4b2.jpg" width="30px"><span>吃饭饭</span> 👍（11） 💬（0）<div>分享一个编译源码的帖子：https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;wp1LZcdK2eLRZU3HlubW9w</div>2019-09-26</li><br/><li><img src="" width="30px"><span>Geek_0db340</span> 👍（8） 💬（0）<div>表单提交method=post 就可以啦</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/a7/440aff07.jpg" width="30px"><span>风翱</span> 👍（6） 💬（0）<div>可以利用工具，例如postman。 也可以编写代码，利用http的post方法去调用。 或者像楼上所说的不管通过get还是post都通知转发到doPost中。</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/77/61/adf1c799.jpg" width="30px"><span>KL3</span> 👍（4） 💬（0）<div>把业务逻辑写在dopost里，然后doget方法调用dopost方法</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/12/e8/c42ad60d.jpg" width="30px"><span>大白</span> 👍（2） 💬（0）<div>实践过程遇到几个问题，解决方法如下，供参考：
1、	编译MyServlet.java时报错：Desktop\MyServlet.java:13: 错误: 编码 GBK 的不可映射字符 (0x80)。
原因：系统字符集不匹配。
   解决办法：编译时添加“-encoding utf-8”参数即可解决。
2、	tomcat官网下载windows版，免安装tomcat，启动报错。
原因：startup.bat文件中的CATALINA_HOME参数未设置。
解决办法：在startup.bat文件中添加SET CATALINA_HOME=”tomcat安装路径”即可。
3、	启动tomcat后，项目启动报错。
原因：web.xml文件格式编写错误，web.xml文件第一行为空行。
解决办法：删除空行及空格，顶格写。
</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（2） 💬（0）<div>curl -X POST http:&#47;&#47;127.0.0.1:8080&#47;MyWebApp&#47;myAnnotationServlet</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（2） 💬（0）<div>“javac -cp .&#47;servlet-api.jar MyServlet.java”执行报错:
&quot;MyServlet.java:16: 错误: 编码GBK的不可映射字符
        System.out.println(&quot;MyServlet 鍦ㄥ鐞? get锛堬級璇锋眰...&quot;);&quot;
换成：“javac -encoding UTF-8  -cp .&#47;servlet-api.jar MyServlet.java”解决。百度搬运工。。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/f3/008d74f7.jpg" width="30px"><span>kmmshmily</span> 👍（2） 💬（0）<div>这个demo  大学期间一直这样写啊  最后才用Spring的</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/2b/c8acb384.jpg" width="30px"><span>Howard</span> 👍（2） 💬（1）<div>代码放在github上需要注意开源协议，像apache这种协议明确说明受美国出口管制的</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/dd/e136dbe9.jpg" width="30px"><span>Geek_bde3dc</span> 👍（2） 💬（0）<div>最简单的办法就是在doGet里调用doPost😁</div>2019-05-18</li><br/>
</ul>