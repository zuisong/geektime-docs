你好，我是傅健。

今天，我们来学习 Spring 的异常处理机制。Spring 提供了一套健全的异常处理框架，以便我们在开发应用的时候对异常进行处理。但是，我们也会在使用的时候遇到一些麻烦，接下来我将通过两个典型的错误案例，带着你结合源码进行深入了解。

## 案例 1：小心过滤器异常

为了方便讲解，我们还是沿用之前在事务处理中用到的学生注册的案例，来讨论异常处理的问题：

```
@Controller
@Slf4j
public class StudentController {
    public StudentController(){
        System.out.println("construct");
    }


    @PostMapping("/regStudent/{name}")
    @ResponseBody
    public String saveUser(String name) throws Exception {
        System.out.println("......用户注册成功");
        return "success";
    }
}
```

​为了保证安全，这里需要给请求加一个保护，通过验证 Token 的方式来验证请求的合法性。这个 Token 需要在每次发送请求的时候带在请求的 header 中，header 的 key 是 Token。

为了校验这个 Token，我们引入了一个 Filter 来处理这个校验工作，这里我使用了一个最简单的 Token：111111。

当 Token 校验失败时，就会抛出一个自定义的 NotAllowException，交由 Spring 处理：

```
@WebFilter
@Component
public class PermissionFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpServletRequest = (HttpServletRequest) request;
        String token = httpServletRequest.getHeader("token");


        if (!"111111".equals(token)) {
            System.out.println("throw NotAllowException");
            throw new NotAllowException();
        }
        chain.doFilter(request, response);
    }


    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }


    @Override
    public void destroy() {
    }
```

NotAllowException 就是一个简单的 RuntimeException 的子类：

```
public class NotAllowException extends RuntimeException {
    public NotAllowException() {
        super();
    }
}
```

同时，新增了一个 RestControllerAdvice 来处理这个异常，处理方式也很简单，就是返回一个 403 的 resultCode：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/11/c8/889846a7.jpg" width="30px"><span>黑白颠倒</span> 👍（4） 💬（0）<div>学习这章之前需要先了解一下Spring处理异常的几种方式，这里推荐一篇文章。https:&#47;&#47;blog.csdn.net&#47;qq_24598601&#47;article&#47;details&#47;89243914?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-0.control&amp;spm=1001.2101.3001.4242</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/11/c8/889846a7.jpg" width="30px"><span>黑白颠倒</span> 👍（1） 💬（0）<div>第一个没怎么看得懂。。。</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/09/2c/cb8dd9ef.jpg" width="30px"><span>阿波罗</span> 👍（0） 💬（0）<div>
@ExceptionHandler(NoHandlerFoundException.class)这个按照老师的说明404不生效的直接原因找到了，因为服务的启动类加了@EnableAdminServer，去掉这个注解就可以了，加上就不好使了，</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>收货很多，原理，流程</div>2021-11-08</li><br/>
</ul>