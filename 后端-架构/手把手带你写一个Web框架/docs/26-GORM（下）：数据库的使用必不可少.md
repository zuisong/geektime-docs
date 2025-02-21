你好，我是轩脉刃。

上一节课，我们梳理了Gorm的核心逻辑，也通过思维导图，详细分析了Gorm的源码搞清楚它是如何封装database/sql的。这节课我们就要思考和操作，如何将Gorm融合进入hade框架了。

Gorm的使用分为两个部分，数据库的连接和数据库的操作。

对于数据库操作接口的封装，Gorm已经做的非常好了，它在gorm.DB中定义了非常多的对数据库的操作接口，这些接口已经是非常易用了，而且每个操作接口在[官方文档](https://gorm.io/docs/)中都有对应的说明和使用教程。比如在DB的操作接口列表中，我们可以看到常用的增删改查的逻辑：

```go
func (db *DB) Create(value interface{}) (tx *DB)

func (db *DB) Delete(value interface{}, conds ...interface{}) (tx *DB)

func (db *DB) Get(key string) (interface{}, bool)

func (db *DB) Update(column string, value interface{}) (tx *DB)
```

同时，[官方首页](https://gorm.io/docs/)的例子也把获取到DB后的增删改查操作显示很清楚了，建议你在浏览器收藏这个Gorm的说明文档，因为在具体的应用开发中，你会经常参考使用它的。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（2）<div>我都是直接靠Raw直接写sql语句的。因为有时候不太好定义模型</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/24/3d/0682fdb9.jpg" width="30px"><span>宁建峰</span> 👍（2） 💬（0）<div>api_orm.go中，以下代码gin1.8.1已经过过限制了，999&lt;code&gt;100，所以这里使用50001，会发生panic：invalid WriteHeader code 50001
if err != nil { 
   logger.Error(c, err.Error(), nil) 
   c.AbortWithError(50001, err) 
   return 
}
gin v1.8.1 源码如下：
func checkWriteHeaderCode(code int) {
	&#47;&#47; Issue 22880: require valid WriteHeader status codes.
	&#47;&#47; For now we only enforce that it&#39;s three digits.
	&#47;&#47; In the future we might block things over 599 (600 and above aren&#39;t defined
	&#47;&#47; at https:&#47;&#47;httpwg.org&#47;specs&#47;rfc7231.html#status.codes)
	&#47;&#47; and we might block under 200 (once we have more mature 1xx support).
	&#47;&#47; But for now any three digits.
	&#47;&#47;
	&#47;&#47; We used to send &quot;HTTP&#47;1.1 000 0&quot; on the wire in responses but there&#39;s
	&#47;&#47; no equivalent bogus thing we can realistically send in HTTP&#47;2,
	&#47;&#47; so we&#39;ll consistently panic instead and help people find their bugs
	&#47;&#47; early. (We can&#39;t return an error from WriteHeader even if we wanted to.)
	if code &lt; 100 || code &gt; 999 {
		panic(fmt.Sprintf(&quot;invalid WriteHeader code %v&quot;, code))
	}
}</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/72/85/c337e9a1.jpg" width="30px"><span>老兵</span> 👍（0） 💬（0）<div>不知道是不是我理解不对，感觉目前gorm在数据库字段的迁移的方案还是不行。比如数据库表加一个字段，删除一个字段，用auto-migrate还是无法做到精准像active_record那样的方便吧？
不知道叶老师是否有一些golang下orm+migration的经验？
</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/50/1f5154fe.jpg" width="30px"><span>无笔秀才</span> 👍（0） 💬（1）<div>我觉得除了orm 还应该支持直接sql,毕竟很多人不喜欢用orm</div>2022-01-11</li><br/>
</ul>