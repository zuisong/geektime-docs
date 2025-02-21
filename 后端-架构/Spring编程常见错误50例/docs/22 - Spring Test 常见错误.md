你好，我是傅健。

前面我们介绍了许多 Spring 常用知识点上的常见应用错误。当然或许这些所谓的常用，你仍然没有使用，例如对于 Spring Data 的使用，有的项目确实用不到。那么这一讲，我们聊聊 Spring Test，相信你肯定绕不开对它的使用，除非你不使用 Spring 来开发程序，或者你使用了 Spring 但是你不写测试。但话说回来，后者的情况就算你想如此，你的老板也不会同意吧。

那么在 Spring Test 的应用上，有哪些常见错误呢？这里我给你梳理了两个典型，闲话少叙，我们直接进入这一讲的学习。

## 案例 1：资源文件扫描不到

首先，我们来写一个 HelloWorld 版的 Spring Boot 程序以做测试备用。

先来定义一个 Controller：

```
@RestController
public class HelloController {

    @Autowired
    HelloWorldService helloWorldService;

    @RequestMapping(path = "hi", method = RequestMethod.GET)
    public String hi() throws Exception{
        return  helloWorldService.toString() ;
    };

}
```

当访问 [http://localhost:8080/hi](http://localhost:8080/hi) 时，上述接口会打印自动注入的HelloWorldService类型的 Bean。而对于这个 Bean 的定义，我们这里使用配置文件的方式进行。

1. 定义 HelloWorldService，具体到 HelloWorldService 的实现并非本讲的重点，所以我们可以简单实现如下：

```
public class HelloWorldService {
}
```

2. 定义一个 spring.xml，在这个 XML 中定义 HelloWorldService 的Bean，并把这个 spring.xml 文件放置在/src/main/resources 中：
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（0）<div>把依赖 Mock 的 Bean 声明在一个统一的地方，这种方式也太不方便了</div>2023-01-03</li><br/>
</ul>