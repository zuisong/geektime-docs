你好，我是郭屹。从这节课开始，我们开启一个新的部分：MVC。

前面一章，我们实现了一个简单的IoC。麻雀虽小，五脏俱全，相比原生Spring框架而言，我们写的MiniSpring功能简单，但其核心功能已具备。我们会在这个基础上进一步扩展我们的框架。

这一章我们来实现Spring MVC。MVC，全名对应Model（模型）、View（视图）、Controller（控制器）。它的基本流程是：前端发送请求到控制器，控制器寻找对应模型，找到模型后返回结果，渲染视图返回给前端生成页面。这是标准的前端请求数据的模型。实现了MVC之后，我们会把MVC和之前我们已经实现的IoC结合起来，这是我们这一章的整体思路。

![图片](https://static001.geekbang.org/resource/image/a7/41/a79dc2ca9b96c2f4904c2f389926fb41.png?wh=1660x916)

这节课我们就开启Spring MVC的第一步，先实现一个原始的MVC。目标是通过一个Controller来拦截用户请求，找到相应的处理类进行逻辑处理，然后将处理的结果发送给客户端。

## 调整目录

按照惯例，我们还是参照Spring的目录结构来调整。MVC是Web模型，所以我们先调整一下目前的项目结构，采用Web的项目结构。同时，我们还要引入Tomcat服务器以及Tomcat的jar包。

你可以看一下项目目录结构，主要是新增一个和src目录同级的WebContent目录，在这个目录里存储部分前端页面需要的静态资源，还有各项XML配置文件。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（2） 💬（3）<div>    private List&lt;String&gt; scanPackage(String packageName) {
    	List&lt;String&gt; tempControllerNames = new ArrayList&lt;&gt;();
        URL url  =this.getClass().getClassLoader().getResource(&quot;&#47;&quot;+packageName.replaceAll(&quot;\\.&quot;, &quot;&#47;&quot;));
        File dir = new File(url.getFile());
        for (File file : dir.listFiles()) {
            if(file.isDirectory()){
            	scanPackage(packageName+&quot;.&quot;+file.getName());
            }else{
                String controllerName = packageName +&quot;.&quot; +file.getName().replace(&quot;.class&quot;, &quot;&quot;);
                tempControllerNames.add(controllerName);
            }
        }
        return tempControllerNames;
    }
这个方法写的没问题么？照理说应该是递归把所有的类文件都加载进去，应该是tempControllerNames.addAll(scanPackage(packageName+&quot;.&quot;+file.getName()))
是我理解有问题么？</div>2024-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（2） 💬（4）<div>思考题。我理解：MVC中的bean是为了标识这是一个controller，用来接收处理web层请求，而Spring中的bean感觉是一种服务能力，哪个地方需要这种能力，注入后就可以使用。不知道理解的对不对。
另外，跟代码的过程中，发现一个问题，如果包下有接口，Class.newInstance就会报错的。老师，将controller实例化处的代码是不是应该加个Class.isInstance()的判断呢？</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c0/0c/f726d4d0.jpg" width="30px"><span>KernelStone</span> 👍（1） 💬（1）<div>搞了半天这节内容对我这种工程小白而言，难是难在从IDEA中进行项目部署。终于跑通了，参考链接如下：
1、https:&#47;&#47;blog.csdn.net&#47;Wxy971122&#47;article&#47;details&#47;123508532
2、https:&#47;&#47;blog.csdn.net&#47;fannyoona&#47;article&#47;details&#47;113933113
3、另外有需要可以搜一下Tomcat控制台乱码问题

还有感谢评论区的帮助！</div>2023-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a1/0a/b1f68315.jpg" width="30px"><span>零零后糖豆豆</span> 👍（1） 💬（1）<div>response设置contentType避免返回中文乱码
response.setContentType(&quot;text&#47;html; charset=UTF-8&quot;);</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（1） 💬（1）<div>老师 文中的代码和下载的代码分支geek-mvc1 对应不上</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/df/43a260d1.jpg" width="30px"><span>x-arts</span> 👍（1） 💬（2）<div>源码给的过于随意了。。。。</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/70/79/bb591140.jpg" width="30px"><span>睿智的仓鼠</span> 👍（1） 💬（1）<div>加入注解后改造的initMapping()方法中
Class&lt;?&gt; clazz = this.controllerClasses.get(controllerName);下面缺少了一行：
Object obj = this.controllerObjs.get(controllerName);</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/cd/2c3808ce.jpg" width="30px"><span>Yangjing</span> 👍（0） 💬（2）<div>老师，扩展MVC前，启动 Tomcat，是要怎么配置 Tomcat、MiniS 配合启动的呢</div>2023-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/70/79/bb591140.jpg" width="30px"><span>睿智的仓鼠</span> 👍（0） 💬（1）<div>请问郭老师，最后DispatcherServlet中的controllerObjs和mappingObjs这两个map，存储的都是请求地址和处理请求的bean的映射关系，这里为什么要维护两份？我能理解它们的思想不同，但也想不出维护两份后期会有什么扩展。后期会体现出这样做的好处吗？</div>2023-03-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8HibfYTXFWaeXsujL7j1ZEulbibhiaMrTxkm3PticiaP9q3fGv8vkp1XHo9zsVE7Bh9HzkNicOnicd9QHFR73cefiaR7Qg/132" width="30px"><span>Ben Guo</span> 👍（5） 💬（1）<div>关于启动Tomcat，可以加入 embeded tomcat的依赖，然后用下面的代码 跑起来

public class App 
{
    public static void main( String[] args ) throws LifecycleException {
        System.out.println( &quot;Hello World!&quot; );
        Tomcat tomcat = new Tomcat();
        String webappDirLocation = &quot;WebContent&quot;;
        StandardContext context = (StandardContext) tomcat.addWebapp(&quot;&#47;&quot;, new File(webappDirLocation).getAbsolutePath());
        Connector connector = new Connector();
        connector.setPort(8080);
        tomcat.setConnector(connector);
        tomcat.start();
        tomcat.getServer().await();
    }
}</div>2023-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/96/079a158d.jpg" width="30px"><span>adelyn</span> 👍（2） 💬（0）<div>感谢老师，之前没注意过requestMapping为什么是mapping，今天恍然大悟，原来是用url做key维护了一个mapping，</div>2023-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/96/079a158d.jpg" width="30px"><span>adelyn</span> 👍（1） 💬（0）<div>上条写错了，维护了三个mapping，三个mapping正好提供了反射的三个条件，看源码太爽了</div>2023-04-09</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（1） 💬（0）<div>思考题：mvc中的bean只是项目中的一种bean，而ioc管理的是整个项目的bean。可以说mvc中的bean是整个ioc bean的子集</div>2023-03-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0NDY4UtG3BYWVKicTqFPRMGpFyuE6NFPSibz2kxBwC0a8KTyvEmembjQfZnx6DTTSTukm1ibicTDSj9PTTSbhV4dA/132" width="30px"><span>撇目双人聿</span> 👍（0） 💬（0）<div>Mac OS 上 Tomcat的启动参考：https:&#47;&#47;medium.com&#47;@raju6508&#47;a-beginners-guide-installing-apache-tomcat-on-your-mac-11fa0995f3c7 (一步
一步照着做就可以正常启动，特别要注意的是去官网下载 tomcat 的 tar 文件不要下载错了!)
</div>2024-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/ff/d2/c1f5334d.jpg" width="30px"><span>dirtychill</span> 👍（0） 💬（0）<div>MVC的bean指的是controller，是一种特殊的bean</div>2024-05-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BBaAkryVSFImaoWL5QcRbSpB8IfUbUZGfzGH4xUz0qicJGU1vREvcFedgWAXJlYX9ibkzG3BlnJEQDzejZ5ibLCGA/132" width="30px"><span>Geek_28bb47</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;ykexc&#47;minispring每节课对应一个分支，使用嵌入式tomcat,无需IDEA配置。每节课代码都可以运行欢迎大家来参考补充。</div>2024-04-10</li><br/><li><img src="" width="30px"><span>Geek_08c860</span> 👍（0） 💬（0）<div>idea项目设置-工件-修复-设置右下方的路径为 WebContent，默认的 web 是不存在的。然后启动 tomcat，即可解决 404 问题</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/f0/5b/791d0f5e.jpg" width="30px"><span>云从</span> 👍（0） 💬（0）<div>omcat:HTTP状态 404 - 未找到解决方法:
https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;493657861?utm_id=0</div>2023-06-09</li><br/>
</ul>