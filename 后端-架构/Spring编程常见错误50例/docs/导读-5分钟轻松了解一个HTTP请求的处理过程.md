你好，我是傅健。

上一章节我们学习了自动注入、AOP 等 Spring 核心知识运用上的常见错误案例。然而，我们**使用 Spring 大多还是为了开发一个 Web 应用程序**，所以从这节课开始，我们将学习Spring Web 的常见错误案例。

在这之前，我想有必要先给你简单介绍一下 Spring Web 最核心的流程，这可以让我们后面的学习进展更加顺利一些。

那什么是 Spring Web 最核心的流程呢？无非就是一个 HTTP 请求的处理过程。这里我以 Spring Boot 的使用为例，以尽量简单的方式带你梳理下。

首先，回顾下我们是怎么添加一个 HTTP 接口的，示例如下：

```
@RestController
public class HelloWorldController {
    @RequestMapping(path = "hi", method = RequestMethod.GET)
    public String hi(){
         return "helloworld";
    };
}
```

这是我们最喜闻乐见的一个程序，但是对于很多程序员而言，其实完全不知道为什么这样就工作起来了。毕竟，不知道原理，它也能工作起来。

但是，假设你是一个严谨且有追求的人，你大概率是有好奇心去了解它的。而且相信我，这个问题面试也可能会问到。我们一起来看看它背后的故事。

其实仔细看这段程序，你会发现一些**关键的“元素”**：

1. 请求的 Path: hi
2. 请求的方法：Get
3. 对应方法的执行：hi()

那么，假设让你自己去实现 HTTP 的请求处理，你可能会写出这样一段伪代码：

```
public class HttpRequestHandler{
    
    Map<RequestKey, Method> mapper = new HashMap<>();
    
    public Object handle(HttpRequest httpRequest){
         RequestKey requestKey = getRequestKey(httpRequest);         
         Method method = this.mapper.getValue(requestKey);
         Object[] args = resolveArgsAccordingToMethod(httpRequest, method);
         return method.invoke(controllerObject, args);
    };
}
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/57/27de274f.jpg" width="30px"><span>萧</span> 👍（13） 💬（0）<div>清晰易懂，感觉可以基于此篇文章再自己研究源码写一篇源码解析，哈哈</div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（5） 💬（0）<div>spring web前端控制器的执行流程是常被问到的面试题</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（4） 💬（0）<div>Springboot1.5.31.RELEASE版本
EmbeddedTomcat是在EmbeddedServletContainerAutoConfiguration类中定义的</div>2021-06-24</li><br/>
</ul>