你好，我是傅健。

从导读中我们已知，Spring 的核心是围绕 Bean 进行的。不管是 Spring Boot 还是 Spring Cloud，只要名称中带有Spring关键字的技术都脱离不了 Bean，而要使用一个 Bean 少不了要先定义出来，所以**定义一个Bean 就变得格外重要了**。

当然，对于这么重要的工作，Spring 自然给我们提供了很多简单易用的方式。然而，这种简单易用得益于 Spring 的“**约定大于配置**”，但我们往往不见得会对所有的约定都了然于胸，所以仍然会在 Bean 的定义上犯一些经典的错误。

接下来我们就来了解下那些经典错误以及它们背后的原理，你也可以对照着去看看自己是否也曾犯过，后来又是如何解决的。

## 案例 1：隐式扫描不到 Bean 的定义

在构建 Web 服务时，我们常使用 Spring Boot 来快速构建。例如，使用下面的包结构和相关代码来完成一个简易的 Web 版 HelloWorld：

![](https://static001.geekbang.org/resource/image/63/48/63f7d08fb89653e12b9946c4dca31c48.png?wh=375%2A93)

其中，负责启动程序的 Application 类定义如下：

```
package com.spring.puzzle.class1.example1.application
//省略 import
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

提供接口的 HelloWorldController 代码如下：

```
package com.spring.puzzle.class1.example1.application
//省略 import
@RestController
public class HelloWorldController {
    @RequestMapping(path = "hi", method = RequestMethod.GET)
    public String hi(){
         return "helloworld";
    };
}
```

上述代码即可实现一个简单的功能：访问[http://localhost:8080/hi](http://localhost:8080/hi) 返回helloworld。两个关键类位于同一个包（即 application）中。其中 HelloWorldController 因为添加了@RestController，最终被识别成一个 Controller 的 Bean。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/a0/b4/5173f1af.jpg" width="30px"><span>小不点</span> 👍（1） 💬（2）<div>先马后看，从Netty过来的，Netty篇章反复看了好久才算整明白，希望这次也一样</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/8c/8e95e21e.jpg" width="30px"><span>许金亮</span> 👍（51） 💬（5）<div>案例 3：原型 Bean 被固定
service可以使用scope注解的proxyMode，设置成target_class，这样注入到controller的bean就是代理对象了，每次都会从beanfactory里面重新拿过
@Scope(value = &quot;prototype&quot;, proxyMode = ScopedProxyMode.TARGET_CLASS)</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/72/25/2471fd9f.jpg" width="30px"><span>点点</span> 👍（27） 💬（1）<div>@Scope(value=ConfigurableBeanFactory.SCOPE_PROTOTYPE)这个是说在每次注入的时候回自动创建一个新的bean实例

@Scope(value=ConfigurableBeanFactory.SCOPE_SINGLETON)单例模式，在整个应用中只能创建一个实例

@Scope(value=WebApplicationContext.SCOPE_GLOBAL_SESSION)全局session中的一般不常用

@Scope(value=WebApplicationContext.SCOPE_APPLICATION)在一个web应用中只创建一个实例

@Scope(value=WebApplicationContext.SCOPE_REQUEST)在一个请求中创建一个实例

@Scope(value=WebApplicationContext.SCOPE_SESSION)每次创建一个会话中创建一个实例

里面还有个属性

proxyMode=ScopedProxyMode.INTERFACES创建一个JDK代理模式

proxyMode=ScopedProxyMode.TARGET_CLASS基于类的代理模式

proxyMode=ScopedProxyMode.NO（默认）不进行代理</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（13） 💬（1）<div>亲测：
1、@ComponentScan可以多个同时使用，且都生效。效果等同于@ComponentScans
2、@ComponentScans不能与@ComponentScan一起使用</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/dd/c6035349.jpg" width="30px"><span>Bumblebee</span> 👍（9） 💬（0）<div>今日收获
①  Spring默认扫描包是application类（@SpringBootApplication）所在的包，通过@ComponentScans或@ComponentScan直接可以指定需要扫码的包；


②  Bean的定义缺少隐式依赖；

@Service
public class ServiceImpl {
    
    private String serviceName；
    public ServiceImpl(String serviceName){
        this.serviceName = serviceName;
    }

}
      1）上述代码中的serviceName如果不是Spring容器的Bean创建ServiceIml  Bean时会报错，因为Spring创建Bean时会调用AbstractAutowireCapableBeanFactory#createBeanInstance，他主要是通过反射获取构造器，通过构造器创建Bean，此时获取到的构造器是一个携带参数的构造，为了获取此构造器的参数serviceName，会从Spring容器中去获取，获取不到则报错；
      2）需要Spring管理的类不能有多个构造函数，因为Spring在创建Bean时无法确定该调用那个构造函数，会报错；

③  原型Bean被固定；
      1）被@Autowired修饰的成员变量会在所属Bean被创建后，执行BeanPostProcessor给属性注入值，只注入一次，因为对于被@Autowired修饰的原型Bean，每次想获取到一个全新的Bean，是不能达到目的的；
       2）对于原型Bean每次想获取到一个全新的Bean可以从AppliactionContext获取，或者通过@LookUp注解获取，示例代码如下；
    @Lookup
    public ServiceImpl getServiceImpl(){
        return null;
    }  
被@LookUp注解修饰的方法本身实现不重要


</div>2022-05-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PQxKfm8F19icfBichibEoTJvLCZtatEZyytCWrCKhia5zBgFNO57nYHUzpp51CPByic6VeEE8nCiaW8YUWxwr8do14Vw/132" width="30px"><span>Geek_ca230e</span> 👍（9） 💬（1）<div>案例1 也可以用这样的方式显示指定扫描包：@SpringBootApplication(scanBasePackages = {&quot;com.xxx.xxxxx&quot;,&quot;com.xxx.xxx&quot;})</div>2021-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/d4/15a5c91f.jpg" width="30px"><span>Sway</span> 👍（5） 💬（4）<div>想咨询一下，是怎么通过 ComponentScan 注解，找到 ComponentScanAnnotationParser 这个类的？在看其他的项目时，看到很多注解，但是想了解它具体做了什么工作，却无从下手。 （ 很可能项目并不能跑起来去 DEBUG ）</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/a4/1d/81e93f87.jpg" width="30px"><span>jzhongchen</span> 👍（4） 💬（3）<div>案例 3：原型 Bean 被固定
设置scope为prototype的bean是每次调用的时候会产生一个新的bean，案例中由于controller没有设置scope，默认为singleton。每次请求的时候controller是同一个对象，当然service不会变。如果把controller的scope设置为prototype的话，就能够实现每次请求的时候service是一个新对象。
lookup注解以前没有听说过，还是第一次看到。</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（4） 💬（1）<div>对于案例3: 最近项目中，我使用构造器模式，构造器scop指定的为prototype；通过autowired去注入构造器；我感觉我自己就踩坑了...在测试过程中由于没有多线程去使用构造器，数据看不出来，待会去增加一个日志看下，是否返回都是同一个对象。</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（4） 💬（1）<div>问题：
1、关于用@ComponentScan修正那段代码，是不是少写了ComponentScan
2、JDK 1.8已经支持Repeatable注解，那是不是就不需要用@ComponentScans注解了，直接添加多个@ComponentScan注解就行
思考题：可以给构造器的参数添加@Autowired(required = false)就不会报错了</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/37/96/9f4f4658.jpg" width="30px"><span>Oishi上好佳。</span> 👍（2） 💬（0）<div>用的SpringBoot2.6.7版本，第二个案例，按照老师的写法，会报循环依赖，重新提供个类，专门用来注册这个 serviceName 即可。</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（2） 💬（0）<div>@Service
public class TestService {
    private String serviceName;
    &#47;&#47; spring创建bean时,如果存在多个构造,会选无参构造。
    public TestService() {
    }

    public TestService(String serviceName) {
        this.serviceName = serviceName;
    }

    public String doSomething() {
        return serviceName;
    }
}</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（1） 💬（0）<div>老师，你是根据这个@ComponentScan 注解的 basePackages() 就定位到 ComponentScanAnnotationParser#parse 这个方法的呢</div>2022-08-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGtG01ksyBtjxfvS0A93enaCumrnrgZILWnHkIg2x80CqoXcibLWSdVIDkplictKCNmJBZl8dONyibw/132" width="30px"><span>Geek_13168b</span> 👍（1） 💬（1）<div>新版本的spring，对于案例二已经不能运行了，在项目运行之前就会报错</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（1） 💬（0）<div>短短一篇专栏，补齐了5个知识点。太值了。</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f4/8c/0866b228.jpg" width="30px"><span>子房</span> 👍（1） 💬（0）<div>不错解决了我之前的一个疑问</div>2021-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/29/06/791d0f5e.jpg" width="30px"><span>Geek_ieee754</span> 👍（0） 💬（0）<div>总结：约定和配置
1. 没有配置时，遵守约定；有配置时，遵守配置
2. 配置失效时（多个配置，优先级相同），遵守约定；约定失效，报错
3. 对于一些标准的解决方案（多例bean的依赖注入），强行遵循约定，而不用理会配置</div>2024-08-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RKo5N6Y7Hgcr3YicsHul0XuDACAYzIpiaiazOc7LkkOoDlAHTTmX1dlIrhBZ6gP1QFXermLrP8Algg/132" width="30px"><span>小林桑</span> 👍（0） 💬（0）<div>课后总结一下：
1.文件路径问题导致bean没有注入Spring容器，指定bean扫描路径即可（默认bean扫描路径为启动类所在的包路径）
2.自定义多个构造方法导致Spring容器在初始化bean的时候不知道应该使用哪个那个构造函数，使用autowired注解属性或者注解构造函数。或者只定义一个构造函数即可
3.被注入的bean使用autowried注解表示该属性已经被固定，但是被注入的bean使用socp使用了prototype注解属性（prototype表示每次使用bean时都需要新创建bean实例），但是该bean又被autowried注解固定，导致Spring程序在使用bean时报错。可以用lookup注解一个方法每次使用该bean时调用方法或者每次使用bean时从Spring容器获取。</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/af/b8/458866d3.jpg" width="30px"><span>Bo</span> 👍（0） 💬（0）<div>案例3层层递进，写得太好了！</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/74/63/96f3adb1.jpg" width="30px"><span>骗子</span> 👍（0） 💬（0）<div>关于思考题，应该不会报错，spring创建bean分为两步，先创建引用，然后实例化。由于找不到构造函数，只是不会实例化，相当于定义了一个 A a，不调用的话是不会报错的（仅个人理解）</div>2023-01-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mQddXC7nRiaKHTwdficicTB3bH0q5ic5UoSab51Omic7eyLBz0SNcvbLpQnNib7zP1yJFm7xxx4ia81iahfibRVnbTwHmhw/132" width="30px"><span>浮石沉木</span> 👍（0） 💬（1）<div>老师我项目启动类也没加@ComponentScan，但是可以识别非启动类目录下的对象</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/62/d3/791d0f5e.jpg" width="30px"><span>胡同学</span> 👍（0） 💬（0）<div>@lookup是不是也可以用来获取当前类被代理的实例，从而解决自身应用的问题？</div>2022-05-13</li><br/><li><img src="" width="30px"><span>Geek_f19eb2</span> 👍（0） 💬（0）<div>lookup注解学到了</div>2022-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5e/c6/24198c51.jpg" width="30px"><span>hackjavaer</span> 👍（0） 💬（0）<div>回答下文章最后的问题，我尝试了下，如果构造参数是数组或者List ,Map的集合类型，那么也会自动构造一个对应类型的数组或者List，Map出来</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（0）<div>感谢讲师，手敲案例代码已上传GitHub。地址是：git@github.com:ziyekudeng&#47;geekbang_springDemo.git</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/b6/abdebdeb.jpg" width="30px"><span>Michael</span> 👍（0） 💬（0）<div>老师讲课的这思路确实很好啊！从问题描述到源码剖析。但是我这边有两个问题还是想请教老师：
1. Spring源码很多，所以即便很多时候我想去debug看源码也是有心无力，那我觉得对于新手来说比较棘手的问题就是我怎么知道哪个类是重要的类？
2. 接上面的问题，我怎么知道这个类的哪个方法是我期望能帮我解决问题的方法？
希望老师能讲一下您是怎么从0到1阅读源码的。</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>那个bean隐式依赖的例子看不太懂</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/6b/f5f94a6f.jpg" width="30px"><span>唐国强</span> 👍（0） 💬（0）<div>案例二 对象有状态 实际大部分情况下没有状态</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/6b/f5f94a6f.jpg" width="30px"><span>唐国强</span> 👍（0） 💬（0）<div>案例一 很常见</div>2021-10-27</li><br/><li><img src="" width="30px"><span>恒星</span> 👍（0） 💬（0）<div>回答问题，如果spring容器中已经存在构造器中需要的bean，就不会报注入bean的时候缺失参数依赖的错误</div>2021-10-10</li><br/>
</ul>