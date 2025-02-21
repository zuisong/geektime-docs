你好，我是傅健。

前面，我们介绍了50个各式各样的问题，在正式结束课程之前，我觉得有必要带着你去梳理下或者说复盘下问题出现的原因。错误的表现千万种，但是如果追根溯源的话，其实根源不会太多。

当然可能有的同学会把所有的问题都简单粗暴地归结为“学艺不精”，但是除了这个明显的原因外，我想你还是应该深入思考下，最起码，假设是Spring本身就很容易让人犯的错误，你至少是有意识的。那么接下来，我们就来梳理下关于Spring使用中常见的一些错误根源。

## 隐式规则的存在

要想使用好 Spring，你就一**定要了解它的一些潜规则**，例如默认扫描Bean的范围、自动装配构造器等等。如果我们不了解这些规则，大多情况下虽然也能工作，但是稍微变化，则可能完全失效，例如在[第1课](https://time.geekbang.org/column/article/364761)的案例1中，我们使用 Spring Boot 来快速构建了一个简易的 Web 版 HelloWorld：

![](https://static001.geekbang.org/resource/image/ca/a0/ca8e3fd8b3e39833d29c7041cfa47ea0.png?wh=345x87)

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

但是，假设有一天，当我们需要添加多个类似的 Controller，同时又希望用更清晰的包层次结构来管理时，我们可能会去单独建立一个独立于 application 包之外的 Controller 包，并调整类的位置。调整后结构示意如下：
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（1） 💬（1）<div>完结撒花！70分，二刷二刷</div>2021-06-18</li><br/>
</ul>