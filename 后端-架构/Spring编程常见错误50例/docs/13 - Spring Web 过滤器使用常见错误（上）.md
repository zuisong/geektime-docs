你好，我是傅健。

我们都知道，过滤器是 Servlet 的重要标准之一，其在请求和响应的统一处理、访问日志记录、请求权限审核等方面都有着不可替代的作用。在 Spring 编程中，我们主要就是配合使用 @ServletComponentScan 和 @WebFilter 这两个注解来构建过滤器。

说起来比较简单，好像只是标记下这两个注解就一劳永逸了。但是我们还是会遇到各式各样的问题，例如工作不起来、顺序不对、执行多次等等都是常见的问题。这些问题的出现大多都是使用简单致使我们掉以轻心，只要你加强意识，大概率就可以规避了。

那么接下来我们就来学习两个典型的案例，并通过分析，带你进一步理解过滤器执行的流程和原理。

## 案例 1：@WebFilter 过滤器无法被自动注入

假设我们要基于 Spring Boot 去开发一个学籍管理系统。为了统计接口耗时，可以实现一个过滤器如下：

```
@WebFilter
@Slf4j
public class TimeCostFilter implements Filter {
    public TimeCostFilter(){
        System.out.println("construct");
    }
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        log.info("开始计算接口耗时");
        long start = System.currentTimeMillis();
        chain.doFilter(request, response);
        long end = System.currentTimeMillis();
        long time = end - start;
        System.out.println("执行时间(ms)：" + time);
    }
}
```

这个过滤器标记了@WebFilter。所以在启动程序中，我们需要加上扫描注解（即@ServletComponentScan）让其生效，启动程序如下：

```
@SpringBootApplication
@ServletComponentScan
@Slf4j
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
        log.info("启动成功");
    }
}
```

然后，我们提供了一个 StudentController 接口来供学生注册：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（16） 💬（1）<div>@Qualifier(&quot;com.spring.puzzle.filter.TimeCostFilter&quot;) ​FilterRegistrationBean timeCostFilter;
往controller层注入filter的意义是什么？有什么应用场景么？ 估计CodeReview会被打吧</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/f1/16545faf.jpg" width="30px"><span>学习</span> 👍（7） 💬（0）<div>其实对第二个案例有疑问，在catch中做业务逻辑，是因为需要业务补偿，怎么说都是在try里面未执行chain.doFilter才会补偿，但在try…catch外面再做一个chain.doFilter怎么看都不符合是碳基生物写的。假设catch到exception一定要抛出去然后处理异常信息，那后面doFilter永远不可能执行，毕竟是存在这种业务情况的。当然也存在catch到异常后还希望正常往下走。所以不是很理解在try…catch外后面执行的case</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/80/c8/ac09f52c.jpg" width="30px"><span>码畜</span> 👍（5） 💬（0）<div>Q:一次也没有调
A:结果是接口无法正常响应，程序不会回调执行，最后无返回</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（3） 💬（0）<div>为什么不能直接将Filter直接注册成bean呢而是要封装在FilterRegistrationBean中
思考题:自定义的filte中不调用chain.doFilter(),由于还在if (pos &lt; n) {}作用域中,又没有继续调用下一个filter,就会直接return,无法执行核心业务代码servlet.service(request, response);</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（1） 💬（0）<div>积累知识点就好了，别抬杠啊。。。</div>2022-03-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqxCNYbtwpaicsJxjU8f8htibTjpdQYOhyUoaCgJ2nVicdEF3Vwu9dxCtMtOjSupJUzuvtebSPvxNwOg/132" width="30px"><span>高新刚</span> 👍（0） 💬（0）<div>遇到有问题排查的思路可能比知识点更重要，找源码，看堆栈，梳理流程等等类似的思考问题的方法值得我们学习</div>2023-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/28/040f6f01.jpg" width="30px"><span>Y</span> 👍（0） 💬（1）<div>在案例 2 中，我们提到一定要避免在过滤器中调用多次 FilterChain#doFilter()。那么假设一个过滤器因为疏忽，在某种情况下，这个方法一次也没有调用，会出现什么情况呢？
----测试了一下，没有任何返回</div>2022-04-25</li><br/>
</ul>