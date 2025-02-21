你好，我是徐昊。今天我们继续使用TDD的方式实现RESTful Web Services。

## 回顾架构愿景与任务列表

目前我们已经实现了ResourceRouter，整体的架构愿景如下：

![](https://static001.geekbang.org/resource/image/59/24/59ee2d534a4ae87623a736157e848924.jpg?wh=2284x1285)  
![](https://static001.geekbang.org/resource/image/2e/a4/2ef7e84ba450b36d1df67cfce9e61da4.jpg?wh=2284x1285)

## 细化任务列表

沿着调用栈的顺序，就要进入RootResource/Resource/ResourceMethod的开发中。未经细化的任务列表如下：

- Resource/RootResource/ResourceMethod
  
  - 在处理请求派分时，可以支持多级子资源（Sub-Resource）
  - 在处理请求派分时，可以根据客户端提供的超媒体类型，选择对应的资源方法（Resource Method）
  - 在处理请求派分时，可以根据客户端提供的Http方法，选择对应的资源方法
  - 资源方法可以返回Java对象，由Runtime自行推断正确的返回状态
  - 资源方法可以不明确指定返回的超媒体类型，由Runtime自行推断，比如，资源方法标注了Produces标注，那么就使用标注提供的超媒体类型等
  - 资源方法可按找期望的类型，访问Http请求的内容
  - 资源对象和资源方法可接受环境组件的注入

而在当前架构愿景下，RootResource/Resource/ResourceMethod都需要使用UriTemplate、UriInfoBuilder作为支撑。其中，UriInfoBuilder还没有具体的接口设计，那么我们可以先实现UriTemplate。视频演示如下：
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/0d/fe/4e5ba578.jpg" width="30px"><span>Jason</span> 👍（0） 💬（0）<div>正则表达式真是神奇😅</div>2022-08-11</li><br/>
</ul>