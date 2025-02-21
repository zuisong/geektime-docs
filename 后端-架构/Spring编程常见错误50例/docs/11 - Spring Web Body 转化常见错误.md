你好，我是傅健。前面几节课我们学习了 Spring Web 开发中绕不开的 URL 和 Header 处理。这一节课，我们接着讲 Body 的处理。

实际上，在 Spring 中，对于 Body 的处理很多是借助第三方编解码器来完成的。例如常见的 JSON 解析，Spring 都是借助于 Jackson、Gson 等常见工具来完成。所以在 Body 处理中，我们遇到的很多错误都是第三方工具使用中的一些问题。

真正对于 Spring 而言，错误并不多，特别是 Spring Boot 的自动包装以及对常见问题的不断完善，让我们能犯的错误已经很少了。不过，毕竟不是每个项目都是直接基于 Spring Boot 的，所以还是会存在一些问题，接下来我们就一起梳理下。

## 案例 1：No converter found for return value of type

在直接用 Spring MVC 而非 Spring Boot 来编写 Web 程序时，我们基本都会遇到 “No converter found for return value of type” 这种错误。实际上，我们编写的代码都非常简单，例如下面这段代码：

```
//定义的数据对象
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Student {
    private String name;
    private Integer age;
}
//定义的 API 借口
@RestController
public class HelloController {
 
    @GetMapping("/hi1")
    public Student hi1() {
        return new Student("xiaoming", Integer.valueOf(12));
    }    
}
```

然后，我们的 pom.xml 文件也都是最基本的必备项，关键配置如下：

```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.2.3.RELEASE</version>
</dependency>
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7h5GibZwWfgYNeiahJwoYPIa7PjM30smlpsg9Jdz7uqFUyBBPFwXHphtf9ziaKEiceezp7ibaR1Owjt3qWVK4aIYOZA/132" width="30px"><span>Geek_tod-f2e</span> 👍（17） 💬（1）<div>springboot的starter自动引入了jackson依赖包</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（4） 💬（2）<div>源码果然还是不那么容易啃,看着看着就走神了;铁子们有啥好办法吗
</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/11/c8/889846a7.jpg" width="30px"><span>黑白颠倒</span> 👍（3） 💬（0）<div>源码很不容易看，所以可以先做笔记，记下结论，有空再深入源码分析。</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（1） 💬（1）<div>思考题：springboot自动装配了WebMvcAutoConfiguration
</div>2021-05-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VQniaFZTiagBQPZpH6sZY0pcXPq6lib8E3vqrO2OibnVWnV8s9RIcuRIvt3Ir4sSiaKXCM7Tsq9iaXRSQmNU3DqYrbPQ/132" width="30px"><span>温度</span> 👍（0） 💬（0）<div>老师好，案例3定义PrintRequestBodyAdviceAdapter的方式，似乎有问题。在源码里，如果message.hasBody()为true，才会走到afterBodyRead；但由于自定义过滤器已经读取了一遍，所以hasBody其实是false，所以并不会走到自定义的aferBodyRead。这也是在IDEA里debug源码所得现象。
PS：我是阅读后感觉案例3有问题所以实践了一下，并没有实践案例1和2。请帮忙解惑，谢谢</div>2024-09-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKEDxLO0wLibic5WkVl1x7TIL0fsxX1zl2GbRjutYQ89fGRrv2VKJtNmmJb32iarbcHROlmW8SOQsHag/132" width="30px"><span>X</span> 👍（0） 💬（0）<div>HttpMessageConvertersAutoConfiguration</div>2023-07-18</li><br/>
</ul>