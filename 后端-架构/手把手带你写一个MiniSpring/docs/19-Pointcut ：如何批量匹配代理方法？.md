你好，我是郭屹。今天我们继续手写MiniSpring。

到目前为止，我们已经初步实现了简单的AOP，做到了封装JDK的动态代理，并且定义了Advice，实现了调用前、调用时、调用后三个不同位置对代理对象进行增强的效果，而这些切面的定义也是配置在外部文件中的。我们现在在这个基础之上继续前进，引入Pointcut这个概念，批量匹配需要代理的方法。

## 引入Pointcut

我们再回头看一下代码，前面所有的代理方法，都是同一个名字——doAction。我们用以下代码将该方法名写死了，也就是说我们只认定这一个方法名为代理方法，而且名字是不能改的。

```java
if (method.getName().equals("doAction")) {
}
```

如果我们需要增加代理方法，或者就算不增加，只是觉得这个方法名不好想换一个，怎么办呢？当前这种方法自然不能满足我们的需求了。而这种对多个方法的代理需求又特别重要，因为业务上有可能会想对某一类方法进行增强，统一加上监控日志什么的，这种情况下，如果要逐个指定方法名就太麻烦了。

进一步考虑，即便我们这里可以支持多个方法名，但是匹配条件仍然是equals，也就是说，规则仅仅是按照方法名精确匹配的，这样做太不灵活了。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/5c/0d/9ec703ab.jpg" width="30px"><span>不是早晨，就是黄昏</span> 👍（3） 💬（1）<div>能不能说明以下Advice接口和Advisor接口之间的关系，更进一步的是设计上的关系。</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/5b/2a342424.jpg" width="30px"><span>青莲</span> 👍（1） 💬（1）<div>每个匹配模式都可以实现PointcutAdvisor接口，尊循单一职责，如果要同时支持几种能力，可以考虑拐出一个管理类组合几种接口使用</div>2023-05-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/SGicbDM2syIuJKTOkQqboZGD5E0UzhZpbbwOceWg4ZJwS6sR1Uyapo1L0wBZqf9cYiaFrniaSQ4bhAq1QLQDzPvTQ/132" width="30px"><span>欧阳利</span> 👍（0） 💬（1）<div>为什么Interceptor需要实现Advice接口</div>2023-04-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8HibfYTXFWaeXsujL7j1ZEulbibhiaMrTxkm3PticiaP9q3fGv8vkp1XHo9zsVE7Bh9HzkNicOnicd9QHFR73cefiaR7Qg/132" width="30px"><span>Ben Guo</span> 👍（1） 💬（0）<div>1. NameMatchMethodPointcut的getMethodMatcher()应该返回 this，而不是null；
2. JdkDynamicAopProxy的invoke方法，如果方法名不是mappedName匹配，应该要执行method.invoke()。 示例及源码中均返回null，导致该方法没有被执行。</div>2023-08-17</li><br/>
</ul>