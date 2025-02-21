上一节课中，我们学习了Spring框架背后蕴藏的一些经典设计思想，比如约定优于配置、低侵入松耦合、模块化轻量级等等。我们可以将这些设计思想借鉴到其他框架开发中，在大的设计层面提高框架的代码质量。这也是我们在专栏中讲解这部分内容的原因。

除了上一节课中讲到的设计思想，实际上，可扩展也是大部分框架应该具备的一个重要特性。所谓的框架可扩展，我们之前也提到过，意思就是，框架使用者在不修改框架源码的情况下，基于扩展点定制扩展新的功能。

前面在理论部分，我们也讲到，常用来实现扩展特性的设计模式有：观察者模式、模板模式、职责链模式、策略模式等。今天，我们再剖析Spring框架为了支持可扩展特性用的2种设计模式：观察者模式和模板模式。

话不多说，让我们正式开始今天的学习吧！

## 观察者模式在Spring中的应用

在前面我们讲到，Java、Google Guava都提供了观察者模式的实现框架。Java提供的框架比较简单，只包含java.util.Observable和java.util.Observer两个类。Google Guava提供的框架功能比较完善和强大：通过EventBus事件总线来实现观察者模式。实际上，Spring也提供了观察者模式的实现框架。今天，我们就再来讲一讲它。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/d2/fb5306c4.jpg" width="30px"><span>zz</span> 👍（36） 💬（7）<div>看到源码中有这么多的if else，瞬间给了自己一些信心。</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/21/3fa228e6.jpg" width="30px"><span>悟光</span> 👍（11） 💬（0）<div>支持按照消息类型匹配观察者，最终调用 SimpleApplicationEventMulticaster 类的multicastEvent方法通过反射匹配类型。根据配置采用异步还是同步的监听方式。
	public void multicastEvent(final ApplicationEvent event, @Nullable ResolvableType eventType) {
		ResolvableType type = (eventType != null ? eventType : resolveDefaultEventType(event));
		Executor executor = getTaskExecutor();
		for (ApplicationListener&lt;?&gt; listener : getApplicationListeners(event, type)) {
			if (executor != null) {
				executor.execute(() -&gt; invokeListener(listener, event));
			}
			else {
				invokeListener(listener, event);
			}
		}
	}
</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（10） 💬（1）<div>看了下源码,其流程可以从
图片: https:&#47;&#47;uploader.shimo.im&#47;f&#47;fZuIVWFIlWQnnRFq.png
推送Event时候,去发送Event开始走
主要就是这个
在此方法中,会调用getApplicationListeners(event,eventType)函数
图片: https:&#47;&#47;uploader.shimo.im&#47;f&#47;3mZZvSBhmc8CXLnx.png
在这个方法中,会获取到对应的所有监听者,如何获取到的,会先通过一个锁来从一个名为retrieverCache的map中尝试获取到对应的监听者
如果拿不到,会进入到retrieveApplicationListeners()这个函数之中
图片: https:&#47;&#47;uploader.shimo.im&#47;f&#47;GFvS2QEKGlMctZrc.png
在这个方法中,会在add返回的结果的时候,会调用一个方法supportsEvent(),
这才是真正进行匹配的方法
图片: https:&#47;&#47;uploader.shimo.im&#47;f&#47;102Ia9ToqIw5ZOyq.png
匹配事件和源类型是否一致,一致才算做可以发送</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（8） 💬（0）<div>用反射获取的type</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（7） 💬（1）<div>定义了一个bean同时实现了InitializingBean, BeanPostProcessor, DisposableBean，发现方法跟老师最后一张图的不一致：
1、顺序是构造器、afterPropertiesSet、postProcessBeforeInitialization、postProcessAfterInitialization、destroy
2、postProcessBeforeInitialization、postProcessAfterInitialization这两个方法交替执行了N次</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/ed/f9347e5e.jpg" width="30px"><span>松小鼠</span> 👍（6） 💬（3）<div>昨天刚好在隔壁小马哥那里看到了，两个课一起听，侧重点不同，都很重要啊</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/86/52/b92dc111.jpg" width="30px"><span>Tobias</span> 👍（3） 💬（0）<div>Spring 提供的观察者模式是支持按照消息类型匹配观察者。getApplicationListeners(event, type) 方法会根据eventtype 找到对应的的listeners. getApplicationListeners(event, type) 通过反射找到 event 以及event的子类 对应的listeners.</div>2020-07-27</li><br/><li><img src="" width="30px"><span>tonyli</span> 👍（2） 💬（0）<div>使用模板模式定义了一系列步骤的骨架，是各类框架的根本设计模式。</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/e4/e6faf686.jpg" width="30px"><span>握了个大蚂蚱</span> 👍（2） 💬（0）<div>1.实现InitializingBean的初始化方法，也是约定优于配置的一个体现，只不过不是覆盖默认值而是实现init-method的一个前置方法afterPropertiesSet。
2.实现InitializingBean的初始化方法和自己指定init-method相比，侵入性更高，所以不太推荐。可以用注解版的@Bean(initMethod = &quot;xx&quot;)来指定初始化方法，或者使用JSR250中的@PostConstruct标注在初始化方法上来让程序回调。</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（2） 💬（1）<div>spring中的refresh是一个模板方法：
大致有：注册beanFactoryPostProcessor，beanPostProcessor，读取bean definition，创建并初始化bean,等</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/f2/3865fe28.jpg" width="30px"><span>李金鹏</span> 👍（0） 💬（0）<div>自定义注解加AOP可以实现支持按照消息类型匹配观察者</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/81/c457def1.jpg" width="30px"><span>鹤涵</span> 👍（0） 💬（1）<div>策论模式 缓存对象类型和处理器的关系</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f4/8c/0866b228.jpg" width="30px"><span>子房</span> 👍（0） 💬（0）<div>spring 中通过 simple 实现类发送事件，并维护了事件和监听者的映射关系，当需要发送一个事件时会把该事件对应的监听者取出，并执行。</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/18/293cd24d.jpg" width="30px"><span>o0oi1i</span> 👍（0） 💬（0）<div>打卡85</div>2020-11-02</li><br/>
</ul>