你好，我是傅健，这节课我们来聊聊 Spring Web 开发中的参数检验（Validation）。

参数检验是我们在Web编程时经常使用的技术之一，它帮助我们完成请求的合法性校验，可以有效拦截无效请求，从而达到节省系统资源、保护系统的目的。

相比较其他 Spring 技术，Spring提供的参数检验功能具有独立性强、使用难度不高的特点。但是在实践中，我们仍然会犯一些常见的错误，这些错误虽然不会导致致命的后果，但是会影响我们的使用体验，例如非法操作要在业务处理时才被拒绝且返回的响应码不够清晰友好。而且这些错误不经测试很难发现，接下来我们就具体分析下这些常见错误案例及背后的原理。

## 案例1：对象参数校验失效

在构建Web服务时，我们一般都会对一个HTTP请求的 Body 内容进行校验，例如我们来看这样一个案例及对应代码。

当开发一个学籍管理系统时，我们会提供了一个 API 接口去添加学生的相关信息，其对象定义参考下面的代码：

```
import lombok.Data;
import javax.validation.constraints.Size;
@Data
public class Student {
    @Size(max = 10)
    private String name;
    private short age;
}
```

这里我们使用了@Size(max = 10)给学生的姓名做了约束（最大为 10 字节），以拦截姓名过长、不符合“常情”的学生信息的添加。

定义完对象后，我们再定义一个 Controller 去使用它，使用方法如下：
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（7） 💬（0）<div>案例一有个天坑。
引入 spring-boot-starter-validation ， 没毛病。
但是如果同时引入了 javax.validation - validation-api 。
校验会失效。</div>2022-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkeOAC8k7aPMfQZ4ickiavpfR9mTQs1wGhGtIicotzAoszE5qkLfFTabkDU2E39ovSgoibJ1IiaLXtGicg/132" width="30px"><span>bigben</span> 👍（3） 💬（1）<div>如果是List&lt;Phone&gt;怎么加@Valid</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（3） 💬（2）<div>思考题：解析器是ServletRequestMethodArgumentResolver，验证后发现校验并没有生效。因为里面没有相关的校验方法，需要在类上面增加@Validated才能做一个增强

另外问一个小问题：老师怎么通过注解找到相关的实现类的，非常好奇。@Size 找到 SizeValidatorForCharSequence#isValid

</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（2） 💬（0）<div>今天讲的两个案例亲身经历过，特别是级联检验时，因为没有加注解导致未检验。面向百度开发去了，汗颜 没有去面向源码深入研究为什么需要加注解才能级联检验</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/21/f692bdb0.jpg" width="30px"><span>路在哪</span> 👍（1） 💬（0）<div>思考题：负责解析Id的参数解析器是：PathVariableMethodArgumentResolver，然后校验参数的解析器是：ServletRequestMethodArgumentResolver，该解析器在DispatcherServlet#processDispatchResult方法中得到并校验参数</div>2022-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/6b/f5f94a6f.jpg" width="30px"><span>唐国强</span> 👍（1） 💬（0）<div>很多问题真的是没有仔细学习文档挖的坑，反而浪费了时间</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（1）<div>思考题：解析器为 org.springframework.web.servlet.mvc.method.annotation.PathVariableMethodArgumentResolver，触发debug了半天没找着。</div>2021-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKEDxLO0wLibic5WkVl1x7TIL0fsxX1zl2GbRjutYQ89fGRrv2VKJtNmmJb32iarbcHROlmW8SOQsHag/132" width="30px"><span>X</span> 👍（0） 💬（0）<div>org.springframework.web.servlet.mvc.method.annotation.PathVariableMethodArgumentResolver

cglib代理校验
org.springframework.validation.beanvalidation.MethodValidationInterceptor</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/21/f692bdb0.jpg" width="30px"><span>路在哪</span> 👍（0） 💬（0）<div>负责解析ID值的参数解析器是：PathVariableMethodArgumentResolver  负责校验ID的解析器是：ServletRequestMethodArgumentResolver</div>2022-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（0）<div>打卡，完成本节课程</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/89/34f2cbcc.jpg" width="30px"><span>杨宇</span> 👍（0） 💬（0）<div>@Validated 支持分组 groups，使用起来更加灵活。</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（0） 💬（2）<div>老师：案例一的问题修正并没有解决问题，虽然进入了校验判断，但是遍历Validator时getValidators()集合为空，校验操作并未执行
protected void validateIfApplicable(WebDataBinder binder, MethodParameter parameter) {
   Annotation[] annotations = parameter.getParameterAnnotations();
   for (Annotation ann : annotations) {
      Validated validatedAnn = AnnotationUtils.getAnnotation(ann, Validated.class);
      &#47;&#47;判断是否需要校验
      if (validatedAnn != null || ann.annotationType().getSimpleName().startsWith(&quot;Valid&quot;)) {
         Object hints = (validatedAnn != null ? validatedAnn.value() : AnnotationUtils.getValue(ann));
         Object[] validationHints = (hints instanceof Object[] ? (Object[]) hints : new Object[] {hints});
         &#47;&#47;执行校验
         binder.validate(validationHints);
         break;
      }
   }
}

public void validate(Object... validationHints) {
		Object target = getTarget();
		Assert.state(target != null, &quot;No target to validate&quot;);
		BindingResult bindingResult = getBindingResult();
		&#47;&#47; Call each validator with the same binding result
		for (Validator validator : getValidators()) {
			if (!ObjectUtils.isEmpty(validationHints) &amp;&amp; validator instanceof SmartValidator) {
				((SmartValidator) validator).validate(target, bindingResult, validationHints);
			}
			else if (validator != null) {
				validator.validate(target, bindingResult);
			}
		}
}</div>2021-05-19</li><br/>
</ul>