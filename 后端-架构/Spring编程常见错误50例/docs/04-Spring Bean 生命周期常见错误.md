你好，我是傅健，这节课我们来聊一聊 Spring Bean 的初始化过程及销毁过程中的一些问题。

虽然说 Spring 容器上手简单，可以仅仅通过学习一些有限的注解，即可达到快速使用的目的。但在工程实践中，我们依然会从中发现一些常见的错误。尤其当你对 Spring 的生命周期还没有深入了解时，类初始化及销毁过程中潜在的约定就不会很清楚。

这会导致这样一些状况发生：有些错误，我们可以在 Spring 的异常提示下快速解决，但却不理解背后的原理；而另一些错误，并不容易在开发环境下被发现，从而在产线上造成较为严重的后果。

接下来我们就具体解析下这些常见案例及其背后的原理。

## 案例 1：构造器内抛空指针异常

先看个例子。在构建宿舍管理系统时，有 LightMgrService 来管理 LightService，从而控制宿舍灯的开启和关闭。我们希望在 LightMgrService 初始化时能够自动调用 LightService 的 check 方法来检查所有宿舍灯的电路是否正常，代码如下：

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
@Component
public class LightMgrService {
  @Autowired
  private LightService lightService;
  public LightMgrService() {
    lightService.check();
  }
}
```

我们在 LightMgrService 的默认构造器中调用了通过 @Autoware 注入的成员变量 LightService 的 check 方法：
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/0a/0c/333ecdfe.jpg" width="30px"><span>NobugNomiss</span> 👍（33） 💬（1）<div>接口方法 close() 也会在 Spring 容器被销毁的时候自动执行么？
会，原因：requiresDestruction方法中，有两个逻辑短路或判断，第一个是destroyMethodName不为空，另一个是destroyMethodName为空且bean属于AutoCloseable类型，而Closeable接口是AutoCloseable的子类，所以可以满足条件执行close方法。</div>2021-05-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erb3HxekfsIdQumoyJVicmOuvibm0DqIiaCNHeESJdic3t1eIXAplplMicOnmLzibI19uiagdXm8qgZftHbw/132" width="30px"><span>Geek_45e28f</span> 👍（5） 💬（1）<div>“LightService 的 shutdown() 方法能被自动调用；最终打印出 check all ligh”

调用的是LightService.check()吧？</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（2） 💬（0）<div>DefaultListableBeanFactory 类是 Spring Bean 的灵魂。dubug了看了DefaultListableBeanFactory#doCreateBean源码，也debug了下。bean的创建过程总结得不错</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（2） 💬（1）<div>思考题:会的。为啥@Bean要有销毁方法这个默认值？</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/e0/294f6de8.jpg" width="30px"><span>kycool</span> 👍（1） 💬（0）<div>原文中：

我们在 LightMgrService 的默认构造器中调用了通过 @Autoware 注入的成员变量 LightService 的 check 方法：

中的 Autoware 应为 Autowired</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/8a/4afd2896.jpg" width="30px"><span>Swaven</span> 👍（1） 💬（0）<div>会的，在hasDestroyMethod方法中判断bean是否DisposableBean或者AutoCloseable实例，Close-able继承自AutoCloseable，所以会在销毁时执行。</div>2021-06-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7RKo5N6Y7Hgcr3YicsHul0XuDACAYzIpiaiazOc7LkkOoDlAHTTmX1dlIrhBZ6gP1QFXermLrP8Algg/132" width="30px"><span>小林桑</span> 👍（0） 💬（0）<div>简单总结一下吧：
1.无参构造方法内调用被注入对象的方法会报空指针异常
因为：Spring容器调用无参构造方法时，只是简单调用，并未对被注入的bean实例化，所以调用bean的方法会报空指针。如果使用有参构造方法，Spring会在执行构造方法时实例化bean，此时执行bean的方法就不会报错。
2.close、shutdown方法：使用@Bean注解的对象，Spring容器会在容器销毁时自动执行close和shutdown方法（close和shutdown必须是pulic且无参数的方法）。
3.如果想实现容器销毁时调用制定的方法还可以：@Bean(destroyMethod=&quot;methodName&quot;）指定销毁方法。或者使用其他注解注入（Component 或者 Service等），并且被注入的属性类型必须实现AutoCloseable接口的close方法。</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1e/58/2bfb3da0.jpg" width="30px"><span>故作</span> 👍（0） 💬（0）<div>在第 02 课的案例 2 中，我们就提到了构造器参数的隐式注入。
纠正一下，是第01课的案例2</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/c8/f1c4378a.jpg" width="30px"><span>哇</span> 👍（0） 💬（0）<div>傅老师你好，很羡慕你对源码的熟悉，你是如何做到的？我阅读调试了数次spring源码，还只是粗略了解，感觉很费力费神。</div>2022-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7f/eb/c26be6c2.jpg" width="30px"><span>🇳 江⃮⃯⃗</span> 👍（0） 💬（0）<div>会被执行
if (bean instanceof DisposableBean || bean instanceof AutoCloseable) {return true;}</div>2022-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（0） 💬（0）<div>傅哥，这两句话中，都提到了 “注册到 Spring 容器”，看起来处理的都是 “后置处理器类”， 如何理解呢？
第一部分，将一些必要的系统类，比如 Bean 的后置处理器类，注册到 Spring 容器，其中就包括我们这节课关注的 CommonAnnotationBeanPostProcessor 类；
第二部分，将这些后置处理器实例化，并注册到 Spring 的容器中；</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（0）<div>思考题:
会的，原因：requiresDestruction方法中，有两个逻辑短路或判断，第一个是destroyMethodName不为空，另一个是destroyMethodName为空且bean属于AutoCloseable类型，而Closeable接口是AutoCloseable的子类，所以可以满足条件执行close方法。</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/26/f21afb83.jpg" width="30px"><span>暖色浮余生</span> 👍（0） 💬（0）<div> 会的。 在 DisposableBeanAdapter 的 inferDestroyMethodIfNecessary 方法中。 会判断如果没有设置销毁方法的话。会继续判断当前 bean 是否属于 AutoCloseable 接口的实现。</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/36/d677e741.jpg" width="30px"><span>黑山老妖</span> 👍（0） 💬（0）<div>接口方法 close() 也会在 Spring 容器被销毁的时候自动执行么？
会的。</div>2021-04-29</li><br/>
</ul>