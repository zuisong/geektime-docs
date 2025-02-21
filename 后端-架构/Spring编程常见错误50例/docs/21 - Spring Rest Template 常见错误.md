你好，我是傅健。

前面几节课，我们介绍了一个 Spring 微服务使用数据库过程中可能遇到的常见错误。而实际上，除了直接使用数据库外，使用其他微服务来完成功能也是一个常见的应用场景。

一般而言，微服务之间的通信大多都是使用 HTTP 方式进行的，这自然少不了使用 HttpClient。在不使用 Spring 之前，我们一般都是直接使用 Apache HttpClient 和 Ok HttpClient 等，而一旦你引入 Spring，你就有了一个更好的选择，这就是我们这一讲的主角 RestTemplate。那么在使用它的过程中，会遇到哪些错误呢？接下来我们就来总结下。

## 案例 1：参数类型是 MultiValueMap

首先，我们先来完成一个 API 接口，代码示例如下：

```
@RestController
public class HelloWorldController {
    @RequestMapping(path = "hi", method = RequestMethod.POST)
    public String hi(@RequestParam("para1") String para1, @RequestParam("para2") String para2){
        return "helloworld:" + para1 + "," + para2;
    };
}
```

这里我们想完成的功能是接受一个 Form 表单请求，读取表单定义的两个参数 para1 和 para2，然后作为响应返回给客户端。

定义完这个接口后，我们使用 RestTemplate 来发送一个这样的表单请求，代码示例如下：

```
RestTemplate template = new RestTemplate();
Map<String, Object> paramMap = new HashMap<String, Object>();
paramMap.put("para1", "001");
paramMap.put("para2", "002");

String url = "http://localhost:8080/hi";
String result = template.postForObject(url, paramMap, String.class);
System.out.println(result);
```

上述代码定义了一个 Map，包含了 2 个表单参数，然后使用 RestTemplate 的 postForObject 提交这个表单。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（6） 💬（0）<div>传参数的时候，还遇到过Integer cannot cast to String.不好好看官方文档，仅仅依靠片面的互联网资料，就会踩坑。感谢老师！</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/ac/6128225f.jpg" width="30px"><span>jjn0703</span> 👍（3） 💬（0）<div>抓包排查问题 很关键的了~</div>2021-12-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1xMrjxEolCQLIK5ejjTap84U6gRT5TicFDwaxeUTAJLNzWuHrwEfHOzTWU02xc07wMcNvufqqL5DoCcqjQJ8Htg/132" width="30px"><span>chenlx</span> 👍（2） 💬（0）<div>不同版本的 SpringBoot UriComponentsBuilder#fromHttpUrl 和 UriComponentsBuilder#fromUriString 对 fragment 逻辑是不一致的，SpringBoot 2.7.6 UriComponentsBuilder#fromHttpUrl 得到结果是 helloworld:1 而不是 helloworld:1#2</div>2022-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f4/d8/1442fa54.jpg" width="30px"><span>刘增泽</span> 👍（0） 💬（0）<div>spring-boot 2.3.7.RELEASE UriComponentsBuilder的fromHttpUrl方法也添加了对fragment的解析</div>2023-12-24</li><br/>
</ul>