你好，我是陈航。

在专栏的第2篇预习文章“[Dart语言概览](https://time.geekbang.org/column/article/104071)”中，我们简单地认识了Dart这门优秀的程序语言。那么，Dart与其他语言究竟有什么不同呢？在已有其他编程语言经验的基础上，我又如何快速上手呢？

今天，我们就从编程语言中最重要的组成部分，也就是基础语法与类型变量出发，一起来学习Dart吧。

## Dart初体验

为了简单地体验一下Dart，我们打开浏览器，直接在[repl.it](https://repl.it/languages/dart) 新建一个main.dart文件就可以了（当然，你也可以在电脑安装Dart SDK，体验最新的语法）。

下面是一个基本的hello world示例，我声明了一个带int参数的函数，并通过字符串内嵌表达式的方式把这个参数打印出来：

```
printInteger(int a) {
  print('Hello world, this is $a.'); 
}

main() {
  var number = 2019; 
  printInteger(number); 
}
```

然后，在编辑器中点击“run”按钮，命令行就会输出：

```
Hello world, this is 2019. 
```

和绝大多数编译型语言一样，Dart要求以main函数作为执行的入口。

在知道了如何简单地运行Dart代码后，我们再来看一下Dart的基本变量类型。

## Dart的变量与类型

在Dart中，我们可以用var或者具体的类型来声明一个变量。当使用var定义变量时，表示类型是交由编译器推断决定的，当然你也可以用静态类型去定义变量，更清楚地跟编译器表达你的意图，这样编辑器和编译器就能使用这些静态类型，向你提供代码补全或编译警告的提示了。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/83/e8/f726c635.jpg" width="30px"><span>加温后的啤酒</span> 👍（48） 💬（2）<div>老师，能详细解释下final和const吗。你说“const，表示变量在编译期间即能确定的值； final 则可以在运行时确定值”。
那是否能理解为：在编译期间能确定的值 用const或者用final修饰都可以，但是在运行时确定的值，只能用final修饰？？
</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/e4/abb7bfe3.jpg" width="30px"><span>TerryGoForIt</span> 👍（27） 💬（2）<div>思考题：
Dart 是支持泛型的，所以可以使用形如 List&lt;dynamic&gt; 和 Map&lt;String, dynamic&gt; 为集合添加不同类型的元素，遍历时判断类型用 is 关键字。</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/18/7cbc34eb.jpg" width="30px"><span>davidzhou</span> 👍（14） 💬（1）<div>所有皆为对象，就可以通过反射机制获取对象的类型，不过，list和map不做类型约束的话，在读取里面数据会有很多坑，代码也不够健壮</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/49/b8/cfebebf8.jpg" width="30px"><span>七分呗轻唱</span> 👍（7） 💬（1）<div>runtimeType 判断</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/56/03fb63d9.jpg" width="30px"><span>于留月</span> 👍（4） 💬（1）<div>可以使用List&lt;dynamic&gt; 和 Map&lt;dynamic&gt;支持多种类型内部元素，遍历集合时，可以根据泛型确认数据类型</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/1f/cd1cbdb1.jpg" width="30px"><span>晓冰</span> 👍（3） 💬（1）<div>对于Map和List  我在写swift时也是需要指定确定类型的，同一个字典或者数组类型一般都要一样，如果不一样处理起来麻烦，自己的程序就不要给自己挖坑了 哈哈。 只有在一种情况下我才会使用Any 就是提交服务器数据的时候，由于配置的数据类型不可能完全一样。</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/a3/af469d27.jpg" width="30px"><span>Qilin Lou</span> 👍（3） 💬（2）<div>抛砖引玉哈，直接拿各个item的runtimeType属性，简单代码如下

main() {
  var arr = [1,2,&#39;s&#39;];
  arr.forEach(
    (v) =&gt; print(&#39;The value is ${v}, and the type is ${v.runtimeType}&#39;)
  );
}</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/e0/39432f9b.jpg" width="30px"><span>薛敬飞</span> 👍（1） 💬（1）<div>帮忙解释一下评论区中Dynamic？为啥不建议用这个？</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/c5/2f359dc3.jpg" width="30px"><span>Young</span> 👍（1） 💬（1）<div>类，方法参数，返回值都可以指定泛型，判断单个元素的类型可以使用is</div>2019-07-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLEIsgI4ub1VOKWtVOfouAzSqx8Yt8ibQEsAnwNJsJHmuJzzpQqG79HullvYwpic8hgiclgON2GwXSjw/132" width="30px"><span>cv0cv0</span> 👍（0） 💬（1）<div>Dart 支持扩展函数吗？</div>2019-12-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WIpLWqkJ8fRQEKqjkWE8ytr302DiaxNnUoiaK4MrmVoc2nibOcK13cDzAvnoiblMKYE5pyIoIia6sQJdBvHeoT60hxQ/132" width="30px"><span>moran</span> 👍（0） 💬（1）<div>老师好，const和final可不可以理解为赋值后，值就不可更改？</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/8c/ffc4215e.jpg" width="30px"><span>sixgod</span> 👍（0） 💬（2）<div>用dynamic类型和object有什么区别吗</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/a0/ddde3c31.jpg" width="30px"><span>陶先森来了</span> 👍（0） 💬（1）<div>我用Android Studio安装了Dart的安装包，版本是2.2.1的，但是我的项目是2.2.2以上的，请问如何升级Dart呢？还有就是能否单独安装Dart SDK?</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/3f/3ed9119b.jpg" width="30px"><span>Eagle~</span> 👍（0） 💬（1）<div>文中的“实际上，你打开官方文档或查看源码，就会发现这些常见的运算符也是继承自 num：”不是很理解，为什么运算符能继承呢？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/93/00/afeeb6ed.jpg" width="30px"><span>lf</span> 👍（0） 💬（1）<div>老师，flutter源码中构造函数都是用const，为什么呢</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/54/ff/7c878439.jpg" width="30px"><span>呼呼</span> 👍（0） 💬（2）<div>升级到最新的flutter 版本，打包生成ipa，app打开是空白的，请教一下，这个是什么原因呢？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/b4/0808999d.jpg" width="30px"><span>白马</span> 👍（2） 💬（2）<div>老师，有两个问题，1.可以直接print(v)吗？2.什么叫做类型安全？能麻烦您详细解释一下吗？</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（1） 💬（1）<div>【day003】
1. 集合类型 List 和 Map，如何让其内部元素支持多种类型（比如，int、double）？
    使用var 关键字 或 不指定子项类型 或 显示地指定为 dynamic 类型，如 List&lt;dynamic&gt;.of([1, &#39;test&#39;, true])
2. 如何在遍历集合时，判断究竟是何种类型呢？
    通过 is 操作符， xx is String</div>2021-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEK5icO2A4K7HYTYfQoagTz7VbtgxfS2ibBqLnKVWwQZgsePibZWFvFJEhPT8BtpQSaFx9IEodyp6c0dw/132" width="30px"><span>Geek_jg3r26</span> 👍（1） 💬（1）<div>老师，int x = 20 和 var x = 20 是等同的吧， int x 比var x 表达上更好一些事吗</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/22/812f754a.jpg" width="30px"><span>春阳</span> 👍（1） 💬（0）<div>List 指定 length 后，默认数值都为null ，这是由于未初始化的变量都是 null
特性，并且这时候可以在安全下标内进行赋值，但是不指定 length 的 List 则无法指定下标赋值，因为超出了下标边界。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/c9/833d5060.jpg" width="30px"><span>玉皇大亮</span> 👍（0） 💬（0）<div> multiTypeArray.add(true);
  multiTypeArray.add(&#39;test&#39;);
  multiTypeArray.add(5);
  multiTypeArray.add(new List.of([1, 2, 3]));
  multiTypeArray.add({&quot;a&quot;: 1, &quot;b&quot;: true});
 
  multiTypeArray.forEach((v) =&gt; 
   print(&#39;v is ${v}, type = ${v.runtimeType}&#39;)
  );

==================输出结果===============
v is true, type = bool
v is test, type = String
v is 5, type = int
v is [1, 2, 3], type = JSArray&lt;int&gt;
v is {a: 1, b: true}, type = JsLinkedHashMap&lt;String, Object&gt;
&#47;&#47; 有点意思，通过runtimeType 判断， 数组类型是 JSArray，集合类型是JsLinkedHashMap
</div>2024-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/c9/833d5060.jpg" width="30px"><span>玉皇大亮</span> 👍（0） 💬（0）<div>void main() {
  var multiTypeArray = new List&lt;Object&gt;.of([]);
  
  multiTypeArray.add(true);
  multiTypeArray.add(&#39;test&#39;);
  multiTypeArray.add(5);
  multiTypeArray.add(new List.of([1, 2, 3]));
  multiTypeArray.add({&quot;a&quot;: 1, &quot;b&quot;: true});
  
  multiTypeArray.forEach((v) =&gt; {
   if (v is String) {
     print(&#39;v is ${v}, type = String&#39;)
   } else if (v is int) {
     print(&#39;v is ${v}, type = Int&#39;)
   } else if (v is bool) {
     print(&#39;v is ${v}, type = Bool&#39;)
   } else if (v is Map&lt;String, Object&gt;) {
     print(&#39;v is ${v}, type = Map&#39;)
   } else if (v is List&lt;Object&gt;) {
     print(&quot;v is ${v}, type = List&quot;)
   }
  });
}</div>2024-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b0/2d/dd070a55.jpg" width="30px"><span>sello</span> 👍（0） 💬（0）<div>打卡</div>2023-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/85/a9cf7c2a.jpg" width="30px"><span>吖金女的闻先生</span> 👍（0） 💬（0）<div>实际上，你打开官方文档或查看源码，就会发现这些常见的运算符也是继承自 num：
这些操作符，不是继承num吧，应该是在num中运算符重载</div>2021-08-18</li><br/><li><img src="" width="30px"><span>Geek_763c44</span> 👍（0） 💬（0）<div>List&lt;String&gt;这个跟java的泛型一样吗？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/0f/7a/385e4816.jpg" width="30px"><span>tao.ai.dev</span> 👍（0） 💬（0）<div>今日打卡</div>2020-01-18</li><br/>
</ul>