你好，我是傅健。

通过上节课的两个案例，我们了解了容器运行时过滤器的工作原理，那么这节课我们还是通过两个错误案例，来学习下容器启动时过滤器初始化以及排序注册等相关逻辑。了解了它们，你会对如何使用好过滤器更有信心。下面，我们具体来看一下。

## 案例1：@WebFilter过滤器使用@Order无效

假设我们还是基于Spring Boot去开发上节课的学籍管理系统，这里我们简单复习下上节课用到的代码。

首先，创建启动程序的代码如下：

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

实现的Controller代码如下：

```
@Controller
@Slf4j
public class StudentController {
    @PostMapping("/regStudent/{name)}")
    @ResponseBody
    public String saveUser(String name) throws Exception {
        System.out.println("......用户注册成功");
        return "success";
    }
}
```

上述代码提供了一个 Restful 接口 "/regStudent"。该接口只有一个参数 name，注册成功会返回"success"。

现在，我们来实现两个新的过滤器，代码如下：

AuthFilter：例如，限制特定IP地址段（例如校园网内）的用户方可注册为新用户，当然这里我们仅仅Sleep 1秒来模拟这个过程。

```
@WebFilter
@Slf4j
@Order(2)
public class AuthFilter implements Filter {
    @SneakyThrows
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
        if(isPassAuth()){
            System.out.println("通过授权");
            chain.doFilter(request, response);
        }else{
            System.out.println("未通过授权");
            ((HttpServletResponse)response).sendError(401);
        }
    }
    private boolean isPassAuth() throws InterruptedException {
        System.out.println("执行检查权限");
        Thread.sleep(1000);
        return true;
    }
}
```

TimeCostFilter：计算注册学生的执行耗时，需要包括授权过程。

```
@WebFilter
@Slf4j
@Order(1)
public class TimeCostFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        System.out.println("#开始计算接口耗时");
        long start = System.currentTimeMillis();
        chain.doFilter(request, response);
        long end = System.currentTimeMillis();
        long time = end - start;
        System.out.println("#执行时间(ms)：" + time);
    }
}
```

在上述代码中，我们使用了@Order，期望TimeCostFilter先被执行，因为TimeCostFilter设计的初衷是统计这个接口的性能，所以是需要统计AuthFilter执行的授权过程的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/80/c8/ac09f52c.jpg" width="30px"><span>码畜</span> 👍（30） 💬（6）<div>过滤器这两章给我一个启发，能不用@WebFilter就不用，没啥大用还出一堆问题</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（0）<div>秀啊</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/8e/1d68db9a.jpg" width="30px"><span>Geek1591</span> 👍（1） 💬（2）<div>不知道你是哪个版本的Spring。
对于你说@WebFilter + @Order不生效的问题，亲测是生效的。
spring-boot-1.5.1.RELEASE.jar的
org.springframework.boot.web.servlet.ServletContextInitializerBeans#getOrderedBeansOfType(org.springframework.beans.factory.ListableBeanFactory, java.lang.Class&lt;T&gt;, java.util.Set&lt;?&gt;)
此版本的这个方法的返回内容，已经是根据指定的order排序后的BeanList，并且设置了order属性的值，以便后续（多种类型Filter的大范围）再次排序。</div>2021-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（0） 💬（0）<div>@WebFilterbu最终实际没设置order是spring的bug吗？</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/11/c8/889846a7.jpg" width="30px"><span>黑白颠倒</span> 👍（0） 💬（0）<div>@WebFilter问题真多</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b6/15/e2cfd10d.jpg" width="30px"><span>ImYours°</span> 👍（0） 💬（0）<div>实现order接口的话是有效的吗？</div>2021-07-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIcBRhqN1lpk5Kk9OJuM6XL6epbJXGMZOL1no1RyBjwycEzJU4L1TIUAoRUSoNG4pDsnN9wLrRqbg/132" width="30px"><span>xiaomifeng1010</span> 👍（0） 💬（2）<div>使用@Component注解替换@WebFilter，是不是启动类上的@ServletComponentScan注解也要去掉呢？</div>2021-07-13</li><br/>
</ul>