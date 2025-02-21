你好，我是傅健。

上一章节我们讲解了各式各样的错误案例，这些案例都是围绕 Spring 的核心功能展开的，例如依赖注入、AOP 等诸多方面。然而，从现实情况来看，在使用上，我们更多地是使用 Spring 来构建一个 Web 服务，所以从这节课开始，我们会重点解析在 Spring Web 开发中经常遇到的一些错误，帮助你规避这些问题。

不言而喻，这里说的 Web 服务就是指使用 HTTP 协议的服务。而对于 HTTP 请求，首先要处理的就是 URL，所以今天我们就先来介绍下，在 URL 的处理上，Spring 都有哪些经典的案例。闲话少叙，下面我们直接开始演示吧。

## 案例 1：当@PathVariable 遇到 /

在解析一个 URL 时，我们经常会使用 @PathVariable 这个注解。例如我们会经常见到如下风格的代码：

```
@RestController
@Slf4j
public class HelloWorldController {
    @RequestMapping(path = "/hi1/{name}", method = RequestMethod.GET)
    public String hello1(@PathVariable("name") String name){
        return name;
        
    };  
}
```

当我们使用 [http://localhost:8080/hi1/xiaoming](http://localhost:8080/hi1/xiaoming) 访问这个服务时，会返回"xiaoming"，即 Spring 会把 name 设置为 URL 中对应的值。

看起来顺风顺水，但是假设这个 name 中含有特殊字符/时（例如[http://localhost:8080/hi1/xiao/ming](http://localhost:8080/hi1/xiaoming) ），会如何？如果我们不假思索，或许答案是"xiao/ming"？然而稍微敏锐点的程序员都会判定这个访问是会报错的，具体错误参考：
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/98/89/ca8fa978.jpg" width="30px"><span>GTian</span> 👍（11） 💬（2）<div>我运行思考题结果是：xiaoming,hanmeimei
看源码是两个同名请求参数name被放到Stiring[]中，Spring转换器转换String[]-&gt;String时，用“，”分隔符拼接后返回。
看别人运行结果不一样，很疑惑。
期待正确答案。</div>2021-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（6） 💬（1）<div>思考题：结果是  xiaoming,hanmeimei 
原因：分析源码， 目标类-String，源类型-String[]。
代码在GenericConversionService#convert，再深入最后选择的是CollectionToStringConverter#convert. 然而此方法的实现是取出数组中所有元素并用”,“进行连缀。
源码如下：

public Object convert(Object source, TypeDescriptor sourceType, TypeDescriptor targetType) {
		if (source == null) {
			return null;
		}
		Collection&lt;?&gt; sourceCollection = (Collection&lt;?&gt;) source;
		if (sourceCollection.isEmpty()) {
			return &quot;&quot;;
		}
		StringBuilder sb = new StringBuilder();
		int i = 0;
		for (Object sourceElement : sourceCollection) {
			if (i &gt; 0) {
				sb.append(DELIMITER);
			}
			Object targetElement = this.conversionService.convert(
					sourceElement, sourceType.elementTypeDescriptor(sourceElement), targetType);
			sb.append(targetElement);
			i++;
		}
		return sb.toString();
	}</div>2021-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/poo31O8Gibev15vZoDCgQlWM47nhhe6rBmJtAPeib2La7iadhKP09QQ3XKia7DkIt4rwOiaq3fkD0lBv4ibphvSqwfIw/132" width="30px"><span>Geek_21673e</span> 👍（4） 💬（0）<div>@DateTimeFormat 只会在GET请求中生效,对于请求体中的转换无能为力,这个时候需要@JsonFormat</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/57/27de274f.jpg" width="30px"><span>萧</span> 👍（3） 💬（1）<div>虽然熟悉，但看下来收获很大</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（1） 💬（0）<div>我 debug 了下代码.发现这个是tomcat 处理得到的String[],然后 Spring 再处理成&quot;,&quot;分割的 String,见org.apache.catalina.connector.Request#getParameterValues方法</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（1） 💬（0）<div>运行程序后，结果是xiaoming,hanmeimei
两个同名请求参数name被放到Stiring[]中，Spring转换器转换String[]-&gt;String时，用“，”分隔符拼接后返回。</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>
@RequestMapping(path = &quot;&#47;hi6&quot;, method = RequestMethod.GET)
public String hi6(@RequestParam(&quot;Date&quot;) Date date){
    return &quot;date is &quot; + date ;
};

http:&#47;&#47;localhost:8080&#47;hi6?date=2021-5-1 20:26:53

代码是参数是”Date“，URL中是&quot;date&quot;大小对不上。。。
</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ee/e5/b2a9a746.jpg" width="30px"><span>望舒</span> 👍（1） 💬（2）<div>结果居然跟我想象中的不一样，程序没有识别后面的参数。</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（1） 💬（0）<div>思考题：应该是xiaoming
RequestParamMapMethodArgumentResolver#resolveArgument  134行，相同参数只会取第一个参数

有个问题，@RequestBody和@RequestParam区别是不是可以加餐一下？刚学习的时候走了点弯路</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/84/8f/a305cc1e.jpg" width="30px"><span>otakuhuang</span> 👍（0） 💬（0）<div>Spring Boot 2.5.15:

在 AbstractNamedValueMethodArgumentResolver#resolveArgument 中，通过 resolveName 方法，在Tomcat 的 Parameters#getParameterValues，通过 name 取 paramHashValues 中对应的 value 值，取到的是一个 ArrayList&lt;String&gt; 集合，该方法返回时，将 ArrayList 集合转为了 String[] 数组。

回到 AbstractNamedValueMethodArgumentResolver#resolveArgument，在 125 行寻找类型转换器，最后走到了 CollectionToStringConverter#convert 将 String[] 数组 join 了。</div>2024-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rD5lVpIsATSD07rcH7s2NY7442S9hM2ia3QusazbUXKhbCiahnJNibA1Nz16LNlESeKRTicy3bianBQiatnSz5V4FYyg/132" width="30px"><span>Geek_d5ed3d</span> 👍（0） 💬（0）<div>课程中的SpringBoot是哪个版本呢，用新的sprigboot，源码不一样</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7f/eb/c26be6c2.jpg" width="30px"><span>🇳 江⃮⃯⃗</span> 👍（0） 💬（0）<div>xiaoming,hanmeimei:
StringJoiner sj = new StringJoiner(&quot;,&quot;);
                Iterator var6 = sourceCollection.iterator();

                while(var6.hasNext()) {
                    Object sourceElement = var6.next();
                    Object targetElement = this.conversionService.convert(sourceElement, sourceType.elementTypeDescriptor(sourceElement), targetType);
                    sj.add(String.valueOf(targetElement));
                }

                return sj.toString();</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（0） 💬（0）<div>看到request.getParameterValues(name)，我仿佛回到了十几年前，刚毕业那会</div>2021-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/74/578b169d.jpg" width="30px"><span>Yuuuuu</span> 👍（0） 💬（1）<div>对于RequestParam和RequestBody的使用也有一些疑惑，哪些参数可以被RequestParam获取，哪些可以被RequestBody获取?</div>2021-05-12</li><br/>
</ul>