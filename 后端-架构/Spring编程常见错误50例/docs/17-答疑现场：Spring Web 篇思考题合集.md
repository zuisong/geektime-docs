你好，我是傅健。

欢迎来到第二次答疑现场，恭喜你，已经完成了三分之二的课程。到今天为止，我们已经解决了 38 个线上问题，不知道你在工作中有所应用了吗？老话说得好，“纸上得来终觉浅，绝知此事要躬行”。希望你能用行动把知识从“我的”变成“你的”。

闲话少叙，接下来我就开始逐一解答第二章的课后思考题了，有任何想法欢迎到留言区补充。

## [**第9课**](https://time.geekbang.org/column/article/373215)

关于 URL 解析，其实还有许多让我们惊讶的地方，例如案例 2 的部分代码：

```
@RequestMapping(path = "/hi2", method = RequestMethod.GET)
public String hi2(@RequestParam("name") String name){
    return name;
};
```

在上述代码的应用中，我们可以使用 [http://localhost:8080/hi2?name=xiaoming&amp;name=hanmeimei](http://localhost:8080/hi2?name=xiaoming&name=hanmeimei) 来测试下，结果会返回什么呢？你猜会是 [xiaoming&amp;name=hanmeimei](http://localhost:8080/hi2?name=xiaoming&name=hanmeimei) 么？

针对这个测试，返回的结果其实是"xiaoming,hanmeimei"。这里我们可以追溯到请求参数的解析代码，参考 org.apache.tomcat.util.http.Parameters#addParameter：

```
public void addParameter( String key, String value )
        throws IllegalStateException {
    //省略其他非关键代码
    ArrayList<String> values = paramHashValues.get(key);
    if (values == null) {
        values = new ArrayList<>(1);
        paramHashValues.put(key, values);
    }
    values.add(value);
}
```

可以看出当使用 [name=xiaoming&amp;name=hanmeimei](http://localhost:8080/hi2?name=xiaoming&name=hanmeimei) 这种形式访问时，name 解析出的参数值是一个 ArrayList 集合，它包含了所有的值（此处为xiaoming和hanmeimei）。但是这个数组在最终是需要转化给我们的 String 类型的。转化执行可参考其对应转化器 ArrayToStringConverter 所做的转化，关键代码如下：
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/a4/8d/5347f90a.jpg" width="30px"><span>Keke</span> 👍（0） 💬（0）<div>老师你好，请问有什么办法可以在项目运行过程中注册过滤器吗？</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/3e/cdc36608.jpg" width="30px"><span>子夜枯灯</span> 👍（0） 💬（0）<div>打卡完成17节课的学习</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>收货满满</div>2021-11-08</li><br/>
</ul>