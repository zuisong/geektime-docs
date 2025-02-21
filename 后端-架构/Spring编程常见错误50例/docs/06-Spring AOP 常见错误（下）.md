你好，我是傅健。

上一节课，我们介绍了 Spring AOP 常遇到的几个问题，通过具体的源码解析，相信你对 Spring AOP 的基本原理已经有所了解了。不过，AOP 毕竟是 Spring 的核心功能之一，不可能规避那零散的两三个问题就一劳永逸了。所以这节课，我们继续聊聊 Spring AOP 中还会有哪些易错点。实际上，当一个系统采用的切面越来越多时，因为执行顺序而导致的问题便会逐步暴露出来，下面我们就重点看一下。

## 案例1：错乱混合不同类型的增强

还是沿用上节课的宿舍管理系统开发场景。

这里我们先回顾下，你就不用去翻代码了。这个宿舍管理系统保护了一个电费充值模块，它包含了一个负责电费充值的类 ElectricService，还有一个充电方法 charge()：

```
@Service
public class ElectricService {
    public void charge() throws Exception {
        System.out.println("Electric charging ...");
    }
}
```

为了在执行 charge() 之前，鉴定下调用者的权限，我们增加了针对于 Electric 的切面类 AopConfig，其中包含一个 @Before 增强。这里的增强没有做任何事情，仅仅是打印了一行日志，然后模拟执行权限校验功能（占用 1 秒钟）。

```
//省略 imports
@Aspect
@Service
@Slf4j
public class AspectService {
  @Before("execution(* com.spring.puzzle.class6.example1.ElectricService.charge()) ")
  public void checkAuthority(JoinPoint pjp) throws Throwable {
      System.out.println("validating user authority");
      Thread.sleep(1000);
  }
}
```

执行后，我们得到以下 log，接着一切按照预期继续执行：

```
validating user authority
Electric charging ...
```

一段时间后，由于业务发展，ElectricService 中的 charge() 逻辑变得更加复杂了，我们需要仅仅针对 ElectricService 的 charge() 做性能统计。为了不影响原有的业务逻辑，我们在 AopConfig 中添加了另一个增强，代码更改后如下：
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（13） 💬（0）<div>拆分成两个切面，用@Order或Ordered接口控制顺序。个人觉得Spring在排序设计上比较混乱，各种排序规则不统一</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/27/4fbf8f6a.jpg" width="30px"><span>luke Y</span> 👍（8） 💬（4）<div>老师你好，请教个问题，案例一的问题修正doCharge() 方法在charge()中调用，这个代理应该不会走到doCharge()的切面吧</div>2021-05-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errHypG6kuO0QPzlibWLetJqTKy9JzxYbDYEjfjZMuIvdvDTeIJJlETLJicIeETVTLYoc19ohQiaXRkA/132" width="30px"><span>大斌啊啊啊</span> 👍（7） 💬（4）<div>&quot;如果两个方法名长度相同，则依次比较每一个字母的 ASCII 码，ASCII 码越小，排序越靠前；若长度不同，且短的方法名字符串是长的子集时，短的排序靠前。&quot; 这里的描述好像有点问题，短的方法名字符串是长的子集时，短的排序不一定靠前。因为子集不能保证起始值相同，比如说”bc“是”abc“的子集，但是abc会排前面吧</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（4） 💬（5）<div>这段代码调用doCharge()会失效的。这不是上节课的坑吗？就躺进去了

@Service
public class ElectricService {
 
    public void charge() {
        doCharge();
    }
    public void doCharge() {
        System.out.println(&quot;Electric charging ...&quot;);
    }
}</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/66/c6/d779dfb6.jpg" width="30px"><span>松松</span> 👍（3） 💬（1）<div>直觉上@Around和@Before是各干各的，容易把优先级理解成“先用@Around包一圈然后把@Before挂前头”，实际上同一个切面配置类里是捆在一起然后判断执行顺序的。
若干切面配置类之间的Order则是优先级高（数字小）的越外层（@Around和@Before先执行），优先级低的在内层。
怎么说呢，有点儿反直觉，特别是后者，圆环套圆环直觉上来说优先级越高越靠近本体来着。
把@Around、@Before、@After拆到三个优先级从高到低的配置类中，那么会变成@Around-&gt;@Before-&gt;proceed()-&gt;@After-&gt;@Around的顺序，和放在同一个配置类中的@Around-&gt;@Before-&gt;proceed()-&gt;@Around()-&gt;@After是不一样的。</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/06/10/77f6ccea.jpg" width="30px"><span>尘灬</span> 👍（2） 💬（0）<div>spring5.3.x版本之前的顺序是上面这样的 
之后的顺序是
around前置，before 目标方法 afterreturning&#47;afterthrowing  after  around后置</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（2） 💬（1）<div>思考题：切面实现Order接口或者增加@Ordered注解
AspectJAwareAdvisorAutoProxyCreator#sortAdvisors  --&gt;  
AnnotationAwareOrderComparator.sort(advisors)    AnnotationAwareOrderComparator

另外有个小问题：PartialOrder.sort(partiallyComparableAdvisors) 这段代码是在干啥，没看明白。
</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（1） 💬（0）<div>师傅领进门，修行在个人。
专栏有瑕疵不要紧，知识学到手才是重要的啊同学们。
共勉。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/c6/5d186c6f.jpg" width="30px"><span>李米</span> 👍（0） 💬（0）<div>请问下案例和示例代码在哪里下载？</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d7/b7/a78a3d45.jpg" width="30px"><span>中国杰</span> 👍（0） 💬（0）<div>在手机上听了好几节课了，总听音频里说是有附件，电脑上打开文稿看了下，哦，是傅健！</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/26/fe/6c0f9ac7.jpg" width="30px"><span>lava</span> 👍（0） 💬（0）<div>应该可以用order注解把，值越小越先执行</div>2022-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/49/4e/f97abc5b.jpg" width="30px"><span>行者</span> 👍（0） 💬（0）<div>笔记：
在同一个切面配置中，如果存在多个不同类型的增强，那么其执行优先级是按照增强类型的特定顺序排列，依次的增强类型为 Around.class,Before.class,After.class,AfterReturning.class,AfterThrowing.class;
在同一个切面配置中，如果存在多个相同类型的增强，那么其执行优先级是按照该增强的方法名排序，排序放松依次为比较方法名的每一个字母，直到发现第一个不相同且ASCII码较小的字母</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（0） 💬（0）<div>这里的 字符l 是不是写错了， 应该是字符 v？

我们可以将原来的 validateAuthority() 改为 checkAuthority()，这种情况下，对增强（Advisor）的排序，其实最后就是在比较字符 l 和 字符 c。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/f1/16545faf.jpg" width="30px"><span>学习</span> 👍（0） 💬（0）<div>关于doChange()问题，好似后面都重新发文章了，现在是自己注入了自己，看得我一脸懵逼</div>2021-10-27</li><br/>
</ul>