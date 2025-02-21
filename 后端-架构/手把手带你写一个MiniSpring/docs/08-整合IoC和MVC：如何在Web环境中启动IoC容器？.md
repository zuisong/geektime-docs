你好，我是郭屹。

通过上节课的工作，我们就初步实现了一个原始的MVC框架，并引入了@RequestMapping注解，还通过对指定的包进行全局扫描来简化XML文件配置。但是这个MVC框架是独立运行的，它跟我们之前实现的IoC容器还没有什么关系。

那么这节课，我们就把前面实现的IoC容器与MVC结合在一起，使MVC的Controller可以引用容器中的Bean，这样整合成一个大的容器。

## Servlet服务器启动过程

IoC容器是一个自我实现的服务器，MVC是要符合Web规范的，不能自己想怎么来就怎么来。为了融合二者，我们有必要了解一下Web规范的内容。在Servlet规范中，服务器启动的时候，会根据web.xml文件来配置。下面我们花点时间详细介绍一下这个配置文件。

这个web.xml文件是Java的Servlet规范中规定的，它里面声明了一个Web应用全部的配置信息。按照规定，每个Java Web应用都必须包含一个web.xml文件，且必须放在WEB-INF路径下。它的顶层根是web-app，指定命名空间和schema规定。通常，我们会在web.xml中配置context-param、Listener、Filter和Servlet等元素。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（10） 💬（1）<div>思考题：Spring中有父子容器的概念。子容器：MVC容器，父容器：Spring容器。子可以访问父，反过来不行，这是由Spring的体系结构决定的，子容器继承父容器，所以子容器是知道父容器的，所以也就能得到父容器的引用，进而得到父容器中的bean。但是父容器是无法知道子容器的，所以也就无法直接获取子容器中的bean，但是可以通过getBeanFactory来得到子容器，从而获取到子容器中的bean，但java的三层模型，controller---&gt;service---&gt;dao，controller注入service对象是正常的，service注入controller有点奇怪，一般不这么干。不知道以上理解的对不对</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/70/79/bb591140.jpg" width="30px"><span>睿智的仓鼠</span> 👍（7） 💬（1）<div>文中代码实现了webApplicationContext的注入，但排版缺少了很重要的 populateBean()方法，没有使用到初始化好的ioc容器，github中相关的完整的代码是：
```java
DispatcherServlet：

protected void initController() {
        this.controllerNames = scanPackages(this.packageNames);
        for (String controllerName : this.controllerNames) {
            Object obj = null;
            Class&lt;?&gt; clz = null;
            try {
                clz = Class.forName(controllerName);
                obj = clz.newInstance();
            } catch (Exception e) {
                e.printStackTrace();
            }
            this.controllerClasses.put(controllerName, clz);

            populateBean(obj);
            this.controllerObjs.put(controllerName, obj);
        }
    }

    &#47;&#47; 处理controller中的@Autowired注解
    private void populateBean(Object bean) {
        Class&lt;?&gt; clz = bean.getClass();
        Field[] fields = clz.getDeclaredFields();
        for (Field field : fields) {
            boolean isAutowired = field.isAnnotationPresent(Autowired.class);
            if (isAutowired) {
                String fieldName = field.getName();
                Object autowiredBean = this.webApplicationContext.getBean(fieldName);
                field.setAccessible(true);
                try {
                    field.set(bean, autowiredBean);
                } catch (IllegalAccessException e) {
                    throw new RuntimeException(e);
                }
            }
        }
    }
```</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/5c/0d/9ec703ab.jpg" width="30px"><span>不是早晨，就是黄昏</span> 👍（2） 💬（1）<div>最后，在 com.minis.test.HelloworldBean 内的测试方法上
但是你项目代码里有新建了一个test目录，且是和minis同级，而minisMVC-servlet.xml里配置的也是com.test，文章给的代码也是com.test里的，感觉写的有点过于随意了。。。。</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/03/10/82c56b87.jpg" width="30px"><span>Cooler</span> 👍（0） 💬（1）<div>老师，目前wac.setServletContext(servletContext); 这一块相关代码是不是没有用在这一章讲的内容</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（1）<div>课后题，通过WebApplicationContext 可以访问到DispatcherServlet里面的bean吗？
我觉得是分成两种情况来讲的？
根据Servlet的时序来讲的话，那么当初始化好WebApplicationContext的时候，DispatcherServlet还没有进行初始化，所以是空的无法访问的；
但是Servlet初始化完成后呢那应该是可以的？但是怎么访问？用一个方法？
这个方法怎么表明他是IOC的bean的？有点乱了</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（1）<div>黑夜模式，代码里面的标签全没了，作者可以跟后台反馈一下吗 改一下颜色啥的</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ac/ff/791d0f5e.jpg" width="30px"><span>Geek_b71d2c</span> 👍（0） 💬（1）<div>老师，请问一下servletContext.getInitParameter(CONFIG_LOCATION_PARAM)一直获取到的是空，这是什么原因呀</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/45/adf079ae.jpg" width="30px"><span>杨松</span> 👍（0） 💬（1）<div>老师，在代码分支geek_mvc2中，ContextLoaderListener加载了资源文件applicationContext.xml中的bean对象，然后DispatcherServlet会加载&#47;WEB-INF&#47;minisMVC-servlet.xml并扫描包com.test，那么这个包下的对象即被ioc容器加载了，又被DispatcherServlet(mvc容器)加载了，是不是后续的分支会解决这个问题</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（4）<div>请教老师几个问题：
Q1：我用idea2019创建的后端项目并没有web.xml，为什么？
我创建的是springboot项目，maven项目，src目录下面是main和test，main下面是java和resource，并没有WebContent目录，也没有WEB_INF目录，更没有web.xml文件。这个现象怎么解释？另外，不同的项目有不同的目录结构，目录结构的定义在哪里有官方说明？
Q2：用idea创建的项目缺省是基于tomcat吗？
Q3：spring必须基于tomcat，不能独立工作吗？
按文中的说法，servlet必须要用tomcat这个容器，这样的话，spring并不能独立使用，必须依赖于tomcat。</div>2023-03-31</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（0） 💬（1）<div>课后习题：目前Dispatcher可以 访问到WebApplicationContext中的bean，Dispatcher中的bean目前也存在对象的属性中了，但是Dispatcher没有被WebApplicationContext引用所以不能被访问。请问老师spring在管理controller产生的bean的时候是将这些bean统一注册到WebApplicationContext吗？</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6e/61/b1273106.jpg" width="30px"><span>Shark</span> 👍（0） 💬（1）<div>在tomcat启动的过程中，是先初始化IoC容器，再初始化DispatcherServlet，在初始化DispatcherServlet的过程中记录URI与负责执行的方法和方法的对象关系映射，所以这些URI对应的对象此时是由DispatcherServlet管理的，而非IoC容器，而DispatcherServlet也不是IoC容器管理的，后续是不是会统一到IoC容器中？</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/9a/cf/791d0f5e.jpg" width="30px"><span>7up</span> 👍（1） 💬（0）<div>看代码这里将controller放到Dispatcher容器中，其他bean放到webApplicationContext容器中，在Dispatcher初始化时将两者关联起来，第7节课则是没有区分。统一放到了MVC容器中，没有关联IOC容器。</div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/6a/7f858f1f.jpg" width="30px"><span>白不吃</span> 👍（0） 💬（0）<div>看完之后，感觉清晰了很多，不像以前 tomcat 和 spring 对于我来说，就是两个黑盒</div>2025-01-20</li><br/>
</ul>