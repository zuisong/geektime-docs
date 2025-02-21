你好，我是陈航。

在前两篇文章中，我首先与你一起学习了Dart程序的基本结构和语法，认识了Dart语言世界的基本构成要素，也就是类型系统，以及它们是怎么表示信息的。然后，我带你学习了Dart面向对象设计的基本思路，知道了函数、类与运算符这些其他编程语言中常见的概念，在Dart中的差异及典型用法，理解了Dart是怎么处理信息的。

可以看到，Dart吸纳了其他编程语言的优点，在关于如何表达以及处理信息上，既简单又简洁，而且又不失强大。俗话说，纸上得来终觉浅，绝知此事要躬行。那么今天，我就用一个综合案例，把前面学习的关于Dart的零散知识串起来，希望你可以动手试验一下这个案例，借此掌握如何用Dart编程。

有了前面学习的知识点，再加上今天的综合案例练习，我认为你已经掌握了Dart最常用的80%的特性，可以在基本没有语言障碍的情况下去使用Flutter了。至于剩下的那20%的特性，因为使用较少，所以我不会在本专栏做重点讲解。如果你对这部分内容感兴趣的话，可以访问[官方文档](https://dart.dev/tutorials)去做进一步了解。

此外，关于Dart中的异步和并发，我会在后面的第23篇文章“单线程模型怎么保证UI运行流畅？”中进行深入介绍。

## 案例介绍
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/08/fd/3f3dca30.jpg" width="30px"><span>relax</span> 👍（4） 💬（3）<div>能不能所有的示例代码放到一个git下面</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/77/ff/4ce0aa51.jpg" width="30px"><span>Ω</span> 👍（36） 💬（3）<div>Item operator+(Item item) =&gt; I...
double get price =&gt; bookings...

这个改造+号的代码还是无法看懂
</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/07/380666e3.jpg" width="30px"><span>bytecode</span> 👍（13） 💬（1）<div>double get price() {
  double sum = 0.0;
  for(var i in bookings) {
    sum += i.price;
  }
  return sum;
} 

文中这里的price()是多了括号()，要去掉()</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a9/09/fd67d691.jpg" width="30px"><span>jia58960</span> 👍（10） 💬（2）<div>大概能看懂并实现代码，但构造函数中的属性什么时候用this.属性，什么时候不用this，希望老师能回答下。</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/80/ccf2f428.jpg" width="30px"><span>灰灰</span> 👍（5） 💬（2）<div>abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

class Meta {
  double price;
  String name;
  Meta(this.name, this.price);
}

&#47;&#47; 定义商品Item类
class Item extends Meta {
  int count;
  Item(name, price, this.count): super(name, price);
  Item operator+(Item item) =&gt; Item(name + item.name, price * count + (item.price * item.count), 1);
}

&#47;&#47;定义购物车类
class ShoppingCart extends Meta with PrintHelper {
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;

  double get price =&gt; bookings.reduce((value, element) =&gt; (value + element)).price;
&#47;&#47;  ShoppingCart(name, this.code): date = DateTime.now(), super(name,0);
  ShoppingCart({name}): this.withCode(name: name, code: null);
  ShoppingCart.withCode({name, this.code}): date = DateTime.now(), super(name, 0);
  getInfo () =&gt; &#39;&#39;&#39;
     购物车信息:
     
     ----------------
     商品名    单价    数量    总价
     ----------------
     ${bookings.map((item) =&gt; &#39;${item.name}  ${item.price}  ${item.count}  ${item.price * item.count}&#39;).join(&#39;\n     &#39;)}
     
     ================
     用户名： $name
     优惠码： ${code ?? &quot;没有&quot;}
     总价： $price
     日期： $date
  &#39;&#39;&#39;;
}

void main() {
  ShoppingCart.withCode(name: &#39;张三&#39;, code: &#39;123456&#39;)
  ..bookings = [Item(&#39;苹果&#39;, 10.0, 3), Item(&#39;鸭梨&#39;, 20.0, 1)]
  ..printInfo();

  ShoppingCart(name: &#39;李四&#39;)
  ..bookings = [Item(&#39;香蕉&#39;, 2.4, 2), Item(&#39;芒果&#39;, 6.8, 4)]
  ..printInfo();
}</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/3b/b8c00291.jpg" width="30px"><span>Uncle.Wang</span> 👍（3） 💬（1）<div>class Meta {
  double price;
  String name;
  &#47;&#47; 成员变量初始化语法糖
  Meta(this.name, this.price);
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

class Item extends Meta with PrintHelper {
  int count;
  Item(name, price, {int count = 1}): super(name, price) {
    this.count = count;
  }
  &#47;&#47; 重载 + 运算符，将商品对象合并为套餐商品
  Item operator+(Item item) =&gt; Item(name + item.name, price + item.price); 
    @override
  getInfo() =&gt; &#39;&#39;&#39;
    商品名: $name
    单价: $price
    数量: $count
    ---------------
&#39;&#39;&#39;;
}

&#47;&#47;with 表示以非继承的方式复用了另一个类的成员变量及函数
class ShoppingCart extends Meta with PrintHelper{
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;
  &#47;&#47; 以归纳合并方式求和
  double get price =&gt; bookings.reduce((value, element) =&gt; value + element).price;
  &#47;&#47; 默认初始化函数，转发至 withCode 函数
  ShoppingCart({name}) : this.withCode(name:name, code:null);
  &#47;&#47;withCode 初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code}) : date = DateTime.now(), super(name,0);

  getBookingInfo() {
    String str = &quot;&quot;;
    for (Item item in bookings) {
      str += item.getInfo();
    }
    return str;
  }

  &#47;&#47;?? 运算符表示为 code 不为 null，则用原值，否则使用默认值 &quot; 没有 &quot;
  @override
  getInfo() =&gt; &#39;&#39;&#39;
购物车信息:
-----------------------------
  用户名: $name
  优惠码: ${code??&quot; 没有 &quot;}
  总价: $price
  Date: $date
  商品列表：
    ---------------
${ getBookingInfo() }
-----------------------------
&#39;&#39;&#39;;
}

void main() {
  ShoppingCart.withCode(name:&#39;张三&#39;, code:&#39;123456&#39;)
  ..bookings = [Item(&#39;苹果&#39;,10.0, count: 10), Item(&#39;鸭梨&#39;,20.0, count: 5)]
  ..printInfo();

  ShoppingCart(name:&#39;李四&#39;)
  ..bookings = [Item(&#39;香蕉&#39;,15.0), Item(&#39;西瓜&#39;,40.0)]
  ..printInfo();
}
</div>2019-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epxMjZcn8LFy6PIT7uGzUOHTCZosTwh39jBKlyW3Ffzyscm14PQGh3QZ1GrEGF4UWxwKZrAib8AXCA/132" width="30px"><span>江宁彭于晏</span> 👍（3） 💬（1）<div>class Meta {
  double price;
  String name;
  &#47;&#47; 成员变量初始化语法糖
  Meta(this.name, this.price);
}

class Item extends Meta{
  Item(name, price) : super(name, price);
  &#47;&#47; 重载 + 运算符，将商品对象合并为套餐商品
  Item operator+(Item item) =&gt; Item(name + item.name, price + item.price); 
}

class Items {
  Item item;
  double num;
  Items(this.item, this.num);
  double get totalPrice =&gt; item.price * num; 
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

&#47;&#47;with 表示以非继承的方式复用了另一个类的成员变量及函数
class ShoppingCart extends Meta with PrintHelper{
  DateTime date;
  String code;
  List&lt;Items&gt; bookings;
  &#47;&#47; 以归纳合并方式求和
  double get shopPrice {
     double result = 0.0;
     bookings.forEach((element) =&gt; result+=element.totalPrice);
     return result;
  }

  &#47;&#47; 默认初始化函数，转发至 withCode 函数
  ShoppingCart({name}) : this.withCode(name:name, code:null);
  &#47;&#47;withCode 初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code}) : date = DateTime.now(), super(name,0);

  &#47;&#47;?? 运算符表示为 code 不为 null，则用原值，否则使用默认值 &quot; 没有 &quot;
  @override
  String getInfo() {
  String bookingsResult = &#39;商品明细: \n&#39;;
  bookings.forEach((item) =&gt; bookingsResult += &#39;  商品名称：${item.item.name}  单价：${item.item.price} 数量 ：${item.num}  总价：${item.totalPrice}\n&#39;);

  return &#39;&#39;&#39;
购物车信息:
-----------------------------
  用户名: $name
  优惠码: ${code??&quot; 没有 &quot;}
  $bookingsResult
  总价: $shopPrice
  Date: $date
-----------------------------
&#39;&#39;&#39;;
  }
}

void main() {
  ShoppingCart.withCode(name:&#39;张三&#39;, code:&#39;123456&#39;)
  ..bookings = [Items(Item(&#39;苹果&#39;,10.0),5.0), Items(Item(&#39;鸭梨&#39;,20.0),10.0)]
  ..printInfo();

  ShoppingCart(name:&#39;李四&#39;)
  ..bookings = [Items(Item(&#39;香蕉&#39;,15.0),10.0), Items(Item(&#39;西瓜&#39;,40.0),1.0)]
  ..printInfo();
}
</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/55/48de9a24.jpg" width="30px"><span>Carlo</span> 👍（1） 💬（1）<div>看到一段代码：
firebaseService.login().then(
                        (value) {
                          print(value.toJson());
                        },
                        onError: (err) {
                          print(err);
                        },
                      );

请问这个onError是怎么回事啊。为什么会被执行呢？  这是dart特有的语法么？
我所知道的一般sync function的语法是

thisFunction()
    .catch(console.error)
    .then(() =&gt; console.log(&#39;We do cleanup here&#39;));</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（1） 💬（1）<div>老师您的第二个题目，我理解是要做每一种商品的分类，但是我还是用了以前语言的思路来做了。麻烦老师，看看是否正确。

关键代码如下：
&#47;&#47;定义购物车类
class ShoppingCar extends Meta with PrintHelper {
  DateTime date; &#47;&#47;购物日期
  String code; &#47;&#47;优惠券
  List&lt;Item&gt; _bookings; &#47;&#47;定义私有属性
  num count; &#47;&#47;商品数量

  &#47;&#47;求出总价
  double get price =&gt;
      books.reduce((value, element) =&gt; value + element).price;

  List&lt;Item&gt; get books =&gt; _bookings;

  &#47;&#47;给bookings定义set方法
  set book(List&lt;Item&gt; bookings) {
    this._bookings = bookings;
    this.count = bookings.length;
  }

  &#47;&#47;获取分类产品信息
  String getGoodsInfo() {
    StringBuffer temp = new StringBuffer();
    Map map = new Map&lt;String, List&lt;Item&gt;&gt;();
    books.forEach((item) {
      if (!map.containsKey(item.name)) {
        List list = new List&lt;Item&gt;();
        list.add(item);
        map[item.name] = list;
      } else {
        (map[item.name] as List&lt;Item&gt;).add(item);
      }
    });
    map.forEach((k, v) {
      temp.write(&quot;商品名称：$k,该种商品数量：${(v as List).length},该种商品单价：${(v as List&lt;Item&gt;)[0].price}元\n&quot;);
      print(&quot;$k,$v&quot;);
    });
    return temp.toString();
  }

  &#47;&#47;这种表达式赋值还是挺方便的
  ShoppingCar.withCode({name, this.code}): this.date = DateTime.now(),super(name, 0.0);

  ShoppingCar({name}) : this.withCode(name: name, code: null);

  @override
  getInfo() {
    return &#39;&#39;&#39;
      购物车信息：
      ----------------------
      用户名：$name
      优惠码：${code ?? &quot;没有优惠券啊&quot;}
      商品总量：$count
      总价：$price  
      日期：$date
      ${getGoodsInfo()}
      ----------------------
  &#39;&#39;&#39;;
  }
}

运行后信息如下：购物车信息：
      ----------------------
      用户名：小李
      优惠码：没有优惠券啊
      商品总量：3
      总价：29.0  
      日期：2019-08-14 22:01:24.437085
      商品名称：苹果,该种商品数量：2,该种商品单价：10.0元
      商品名称：梨,该种商品数量：1,该种商品单价：9.0元
      ----------------------</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/36/8e7aec6c.jpg" width="30px"><span>刘荣清</span> 👍（1） 💬（1）<div>在vs code已经安装dart、code runner插件，本地也安装完dart SDK，然后通过vs code运行dart 提示：dart : 无法将“dart”项识别为 cmdlet、函数...
但在cmd 控制板中就可以正常运行，这是为咋啊，vs code需要额外配置咋吗</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/e8/f726c635.jpg" width="30px"><span>加温后的啤酒</span> 👍（0） 💬（1）<div>直接通过mixin关键字定义PrintHelper也比较简单：
mixin  PrintHelper {
  void printInfo() =&gt; print(getInfo());
  String getInfo();
}

</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/55/75/7045c225.jpg" width="30px"><span>庆</span> 👍（0） 💬（1）<div>
class Meta {
  double price;
  String name;
  &#47;&#47;成员变量初始化语法糖
  Meta(this.name, this.price);
}

class Item extends Meta{
  Item(name, price) : super(name, price);
  &#47;&#47;重载+运算符，将商品对象合并为套餐商品
  Item operator+(Item item) =&gt; Item(name + item.name, price + item.price); 
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

&#47;&#47;with表示以非继承的方式复用了另一个类的成员变量及函数
class ShoppingCart extends Meta with PrintHelper{
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;
  &#47;&#47;以归纳合并方式求和
  double get price =&gt; bookings.reduce((value, element) =&gt; value + element).price;
  &#47;&#47;默认初始化函数，转发至withCode函数
  ShoppingCart({name}) : this.withCode(name:name, code:null);
  &#47;&#47;withCode初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code}) : date = DateTime.now(), super(name,0);

  &#47;&#47;??运算符表示为code不为null，则用原值，否则使用默认值&quot;没有&quot;
  @override
  getInfo() =&gt; &#39;&#39;&#39;
购物车信息:
-----------------------------
  用户名: $name
  优惠码: ${code??&quot;没有&quot;}
  总价: $price
  Date: $date
  物品数量: ${bookings.length}
&#39;&#39;&#39;;

printDetails(){
   bookings.forEach((item){
     print(&quot;物品 &quot;+item.name + &quot; 价格 ${item.price}&quot;);
   });

   print(&quot;-----------------------------&quot;);

}

}

void main() {
  ShoppingCart.withCode(name:&#39;张三&#39;, code:&#39;123456&#39;)
  ..bookings = [Item(&#39;苹果&#39;,10.0), Item(&#39;鸭梨&#39;,20.0)]
  ..printInfo()
  ..printDetails();

  ShoppingCart(name:&#39;李四&#39;)
  ..bookings = [Item(&#39;香蕉&#39;,15.0), Item(&#39;西瓜&#39;,40.0)]
  ..printInfo()
  ..printDetails();
}</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/5b/6980ae63.jpg" width="30px"><span>DERUWE</span> 👍（0） 💬（1）<div>使用了这个Item operator+(Item item) =&gt; Item(name + item.name, price + item.price);最后的bookings就变为长度为1的吗</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/3c/9ef80bfe.jpg" width="30px"><span>icer</span> 👍（0） 💬（1）<div>class Meta {
  double price;
  String name;
  Meta(this.name,this.price);
}

class Item2 extends Meta {
  int num;
  Item2(String name, double price,{this.num=1}) :super(name, price);
  Item2 operator + (Item2 item) =&gt; Item2(name + item.name,price * num + item.price * item.num);
}

abstract class printHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

class ShoppingCart2 extends Meta with printHelper {
  DateTime date;
  String code;
  List&lt;Item2&gt; bookings;

  ShoppingCart2({name}) : this.withCode(name:name,code:null);
  ShoppingCart2.withCode({name,this.code}) : date = DateTime.now(),super(name, 0);

  double get price =&gt; bookings.reduce((value,element) =&gt; value + element).price;

  String get cardInfo {
    String str = &quot;&quot;;
    bookings.forEach((v) =&gt;
    str +=&#39;${v.name} ----- ${v.num}\n&#39;);
    return str;
  }

  getInfo() {
    return
          &quot;&quot;&quot;
        购物车信息:
        -----------------------------
        用户名: $name
        优惠码: ${code??&quot;没有&quot;}
        $cardInfo
        总价:   $price
        日期:   $date
        -----------------------------
        &quot;&quot;&quot;;
  }
</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/61/32/e9046955.jpg" width="30px"><span>入夜、渐微凉</span> 👍（0） 💬（1）<div>在一个道友的回答上稍加改动，加了一个商品总数和购物车为空的情况，老师帮忙看看有没有可以优化的地方。
class Meta {
  double price;
  String name;
  String info;
  &#47;&#47;成员变量初始化语法糖
  Meta(this.name, this.price);
}
class Item extends Meta {
  int count;
  Item(name, price, {int count = 1}) : super(name, price) {
    this.count = count;
    this.info = &#39;&#39;&#39;
 商品名: $name
   单价: $price
   数量: $count
   ---------------
  &#39;&#39;&#39;;
  }
  
  Item operator +(Item item) =&gt;
      Item(name + item.name, price + item.price, count: count + item.count);
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

&#47;&#47;with表示以非继承的方式复用了另一个类的成员变量及函数
class ShoppingCart extends Meta with PrintHelper {
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;
  &#47;&#47;以归纳合并方式求和
  double get price =&gt;bookings != null ?
      bookings.reduce((value, element) =&gt; value + element).price : 0.00;
  int get count =&gt; bookings != null ? bookings.reduce((value, element) =&gt; value + element).count : 0;
  &#47;&#47;默认初始化函数，转发至withCode函数
  ShoppingCart({name, List&lt;Item&gt; bookings})
      : this.withCode(name: name, code: null, bookings: bookings);
  &#47;&#47;withCode初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code, this.bookings})
      : date = DateTime.now(),
        super(name, 0) {
        if (bookings != null) {
            String str = &quot;&quot;;
            for (Item item in bookings) {
              str += item.info;
            }
            info = str;
        }
  }

  &#47;&#47;??运算符表示为code不为null，则用原值，否则使用默认值&quot;没有&quot;
  @override
  getInfo() =&gt; &#39;&#39;&#39;
购物车信息:
-----------------------------
  用户名: $name
  优惠码: ${code ?? &quot;没有&quot;}
  商品总数: $count
  总价: $price
  Date: $date
  商品列表: 
  ${info ?? &quot;购物车为空&quot;}
-----------------------------
&#39;&#39;&#39;;
}

void main() {
  ShoppingCart.withCode(
      name: &#39;张三&#39;,
      code: &#39;123456&#39;,
      bookings: [Item(&#39;苹果&#39;, 10.0, count: 1), Item(&#39;鸭梨&#39;, 20.0, count: 2)])
    ..printInfo();

  ShoppingCart(
      name: &#39;李四&#39;, bookings: [Item(&#39;香蕉&#39;, 15.0), Item(&#39;西瓜&#39;, 40.0, count: 4)])
    ..printInfo();

  ShoppingCart(name: &#39;王五&#39;)..printInfo();
}</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/93/7b/97d45363.jpg" width="30px"><span>狗子不要喝奶茶</span> 👍（0） 💬（1）<div>如果方便的话 能否附上课后问题的 解法。方便对一下~自己的思路</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/97/80740db0.jpg" width="30px"><span>JW</span> 👍（0） 💬（1）<div>老师好！我运行代码出现这个错误，是环境的问题吗？

Unhandled exception:
NoSuchMethodError: No static method &#39;withCode&#39; declared in class &#39;ShoppingCart&#39;.
Receiver: ShoppingCart
Tried calling: withCode(name: &quot;张三&quot;, code: &quot;123456&quot;)
#0      NoSuchMethodError._throwNew (dart:core-patch&#47;dart:core&#47;errors_patch.dart:203)
#1      main (file:&#47;&#47;&#47;Users&#47;jw&#47;flutter_app&#47;lib&#47;dart_sample.dart:55:16)
#2      _startIsolate.&lt;anonymous closure&gt; (dart:isolate-patch&#47;dart:isolate&#47;isolate_patch.dart:279)
#3      _RawReceivePortImpl._handleMessage (dart:isolate-patch&#47;dart:isolate&#47;isolate_patch.dart:165)</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/08/f7/2c3238bd.jpg" width="30px"><span>Lihyper</span> 👍（0） 💬（1）<div>交作业了,老师

main() {
  ShopCart.withCode(&quot;张三&quot;, &quot;123456&quot;)
    ..bookings = [Item(&quot;苹果&quot;, 10.0, 3), Item(&quot;樱桃&quot;, 100.0, 1)]
    ..printInfo();
}

class Meta {
  double price;
  String name;
  int count;

  Meta(this.name, this.price, this.count);
}

class Item extends Meta {
  Item(name, price, count) : super(name, price, count);

  Item operator +(Item other) =&gt; Item(name + other.name,
      price * count + other.price * other.count, count + other.count);
}

class ShopCart extends Meta with PrintHelper {
  String code;
  List&lt;Item&gt; bookings;
  DateTime date;

  &#47;&#47; 没有重载,所以出现了可选参数
  &#47;&#47;ShopCart(String name) : this.withCode(name,null);

  ShopCart(String name, String code) : this.withCode(name, code);

  ShopCart.withCode(String name, this.code)
      : date = DateTime.now(),
        super(name, 0, 0);

  get price {
    &#47;&#47;a??b运算符a!=null ? a:b;
    if (bookings == null || bookings.isEmpty) {
      return 0;
    }
    return bookings.reduce((value, element) =&gt; value + element).price;
  }

  get count {
    if (bookings == null || bookings.isEmpty) {
      return 0;
    }
    return bookings.reduce((value, element) =&gt; value + element).count;
  }

  getListInfo() {
    String bookInfo = &quot;&quot;;
    if (bookings == null || bookings.isEmpty) {
      return bookInfo;
    }
    bookings.forEach((item) =&gt;
        bookInfo += &quot;商品名称:${item.name} 单价:${item.price} 数量:${item.count}\n&quot;);
    return bookInfo;
  }

  getInfo() =&gt; &#39;&#39;&#39;
  购物车信息:
  ---------------------
  用户名: $name 
  优惠码: ${code ?? &quot;没有&quot;}
  商品明细:\n ${getListInfo()}
  总价: $price
  总数量: $count
  Date: $date
  ---------------------
  
  &#39;&#39;&#39;;
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());

  getInfo();
}</div>2019-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK95MP7iatc1WcDdusl6mWibiaGXQebI2WFbfTjANfH2eaQX07u7nTnQ6JGOaYKibXYOjPwXDT2FBhUXg/132" width="30px"><span>Geek_614299</span> 👍（0） 💬（1）<div>ShoppingCart类中的 double get price {...}看不懂，意思是重写Meta类中price属性？一定要带get（或者get的意思）？来自js开发者的二连问号
</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/83/b2/e83dd93c.jpg" width="30px"><span>🌙</span> 👍（0） 💬（1）<div>double get price =&gt; bookings.reduce((value, element) =&gt; value + element).price;这个name也会拼接起来？</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/59/a6/4e185fcb.jpg" width="30px"><span>曹昆</span> 👍（0） 💬（1）<div>老师，double get price {...}这个语法是什么意思啊？还有dart方法不用写返回值得吗？</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/98/60d13550.jpg" width="30px"><span>Bryan</span> 👍（0） 💬（2）<div>get price 利用 reduce 的方法那里，每次 reduce 都会调用重载的 + 造成一个新类的实例化，这样不会影响性能吗？</div>2019-08-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/pYVcoj11tKBribn2L05X16icJ4hkMg7fh0iaAnZjGfiawunst0a7mRQiaI5unFy3PUZdY9a1u1IXicOw4muedQGrubibQ/132" width="30px"><span>Todd</span> 👍（0） 💬（2）<div>abstract class printHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

class Meta {
  double price;
  String name;
  &#47;&#47; 1.商品数量属性；
  int quantity;
  Meta(this.name, this.price, this.quantity);
}

&#47;&#47; 定义商品 Item 类
class Item extends Meta {
  Item(name, price, quantity) : super(name, price, quantity);
  &#47;&#47; 重载了 + 运算符，合并商品为套餐商品
  Item operator +(Item item) =&gt; Item(name + item.name,
      price * quantity + item.price * item.quantity, quantity + item.quantity);

  @override
  String toString() {
    &#47;&#47; 2.购物车信息增加商品列表信息（包括商品名称，数量及单价）输出，实现小票的基本功能。
    return &#39;${name}, ${price}, ${quantity}&#39;;
  }
}

&#47;&#47; 定义购物车类
class ShoppingCart extends Meta with printHelper {
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;

  double get price =&gt; bookings.reduce((v, e) =&gt; v + e).price;
  int get quantity =&gt; bookings.reduce((v, e) =&gt; v + e).quantity;

  &#47;&#47; 默认初始化方法，转发到 withCode 里
  ShoppingCart({name}) : this.withCode(name: name, code: null);
  &#47;&#47;withCode 初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code})
      : date = DateTime.now(),
        super(name, 0, 0);
  &#47;&#47;?? 运算符表示为 code 不为 null，则用原值，否则使用默认值 &quot; 没有 &quot;
  getInfo() =&gt; &#39;&#39;&#39;
购物车信息:
-----------------------------
用户名: $name
优惠码: ${code ?? &quot; 没有 &quot;}
总价格: $price
总件数: $quantity
Date: $date
-----------------------------
商品列表信息：
名称, 价格, 数量
${bookings.join(&#39;\n&#39;)}
-----------------------------
  &#39;&#39;&#39;;
}

void main() {
  ShoppingCart.withCode(name: &#39;张三&#39;, code: &#39;123&#39;)
    ..bookings = [Item(&#39;苹果&#39;, 10.0, 3), Item(&#39;鸭梨&#39;, 20.0, 5)]
    ..printInfo();

  ShoppingCart.withCode(name: &#39;张q&#39;)
    ..bookings = [Item(&#39;苹果&#39;, 10.0, 7), Item(&#39;鸭梨&#39;, 20.0, 4)]
    ..printInfo();
}
</div>2019-08-10</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/qoEev6CRRTKAlHibxGcfbFIBaUbLS6XUQ5cRylZI6hYV66m4PSOMQo5vmv1GUiaicLUn9oouQb74tJ26JI88oSq5g/132" width="30px"><span>jimzqw</span> 👍（0） 💬（1）<div>class Meta {
  double price;
  String name;
  &#47;&#47; 成员变量初始化语法糖
  Meta(this.name, this.price);
}

class Item extends Meta{
int count;
  Item(name, price, this.count) : super(name, price);
  &#47;&#47; 重载 + 运算符，将商品对象合并为套餐商品
  Item operator+(Item item) =&gt; Item(name + item.name, price*count + item.price*item.count, count + item.count); 
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

&#47;&#47;with 表示以非继承的方式复用了另一个类的成员变量及函数
class ShoppingCart extends Meta with PrintHelper{
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;
  &#47;&#47; 以归纳合并方式求和
  double get price =&gt; bookings.reduce((value, element) =&gt; value + element).price;

  int get count =&gt; bookings.reduce((value, element) =&gt; value + element).count;
  &#47;&#47; 默认初始化函数，转发至 withCode 函数
  ShoppingCart({name}) : this.withCode(name:name, code:null);
  &#47;&#47;withCode 初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code}) : date = DateTime.now(), super(name,0);

  &#47;&#47;?? 运算符表示为 code 不为 null，则用原值，否则使用默认值 &quot; 没有 &quot;
  @override
  getInfo() =&gt; &#39;&#39;&#39;
购物车信息:
-----------------------------
  用户名: $name
  优惠码: ${code??&quot; 没有 &quot;}
  总价: $price
  数量： $count
  Date: $date
-----------------------------
&#39;&#39;&#39;;
}

void main() {
  ShoppingCart.withCode(name:&#39;张三&#39;, code:&#39;123456&#39;)
  ..bookings = [Item(&#39;苹果&#39;,10.0, 2), Item(&#39;鸭梨&#39;,20.0, 1)]
  ..printInfo();

  ShoppingCart(name:&#39;李四&#39;)
  ..bookings = [Item(&#39;香蕉&#39;,15.0, 2), Item(&#39;西瓜&#39;,40.0, 1)]
  ..printInfo();
}
</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7a/90/dc3537e7.jpg" width="30px"><span>神经蛙</span> 👍（0） 💬（1）<div>class Meta {
  double price;
  String name;
  Meta(this.name, this.price);
}

abstract class PrintHelper{
  printInfo()=&gt;print(getInfo());
  getInfo();
}

class Item extends Meta {
  &#47;&#47; 商品数量
  int total;
  &#47;&#47; total可选，默认1
  Item(name, price, {this.total=1}):super(name,price) ;
  Item operator+(Item item) =&gt; Item(name + item.name, price + item.price*item.total);
}

class ShoppingCart extends Meta with PrintHelper{
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;

  double get price =&gt; bookings.reduce((value, element) =&gt; value + element).price;
  &#47;&#47; 获取购物车列表
  String get _info =&gt; bookings.fold(&#39;商品\t数量\t单价&#39;,(value, element) =&gt; 
                                    &#39;$value\n    ${element.name}\t${element.total}\t${element.price}&#39;);
  ShoppingCart({name}): this.withCode(name: name, code: null);
  ShoppingCart.withCode({name, this.code}): date=DateTime.now(), super(name, 0);
  
  @override
  getInfo() {
    return &#39;&#39;&#39;
    购物车信息:
    用户名: $name
    优惠码: ${code??&quot;无&quot;}
    -----------------------------
    $_info
    -----------------------------
    总价: $price
    日期: ${date.toString()}
    &#39;&#39;&#39;;
  }
}

void main() {
  ShoppingCart(name:&#39;张三&#39;)
    ..bookings = [Item(&#39;苹果&#39;, 10.0), Item(&#39;草莓&#39;,16.0, total: 3),  Item(&#39;鸭梨&#39;, 20.0, total: 2)]
    ..printInfo();
}</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/56/b7/4258025c.jpg" width="30px"><span>top_founder</span> 👍（0） 💬（1）<div>withcode中的name，前面是不是少写了this. ？如果不加，输出的name无值</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/dc/88c34436.jpg" width="30px"><span>keep</span> 👍（0） 💬（1）<div>老师，为什么dart不可以直接调用其他语言的动态库？是dart没提供这个功能？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/88/4dfad2fd.jpg" width="30px"><span>徐西文</span> 👍（0） 💬（1）<div>&#47;&#47; 思考题
class Meta {
  String name;
  double price;
  double count;
  &#47;&#47; 成员变量初始化语法糖
  Meta(this.name, this.price, this count);
}

class Item extends Meta{
  Item(name, price, count) : super(name, price, count);
  &#47;&#47; 重载 + 运算符，将商品对象合并为套餐商品
  Item operator+(Item item) =&gt; Item(name + item.name, count + item.count, price * count + item.price * item.count); 
}

abstract class PrintHelper {
  printInfo() =&gt; print(getInfo());
  getInfo();
}

&#47;&#47;with 表示以非继承的方式复用了另一个类的成员变量及函数
class ShoppingCart extends Meta with PrintHelper{
  DateTime date;
  String code;
  List&lt;Item&gt; bookings;
  &#47;&#47; 以归纳合并方式求和
  double get price =&gt; bookings.reduce((value, element) =&gt; value + element).price;
  double get countNum =&gt; bookings.reduce((value, element) =&gt; value + element).count;
  &#47;&#47; 默认初始化函数，转发至 withCode 函数
  ShoppingCart({name}) : this.withCode(name:name, code:null);
  &#47;&#47;withCode 初始化方法，使用语法糖和初始化列表进行赋值，并调用父类初始化方法
  ShoppingCart.withCode({name, this.code}) : date = DateTime.now(), super(name,0);

  &#47;&#47;?? 运算符表示为 code 不为 null，则用原值，否则使用默认值 &quot; 没有 &quot;
  @override
  getInfo() =&gt; &#39;&#39;&#39;
购物车信息:
-----------------------------
  用户名: $name
  优惠码: ${code??&quot; 没有 &quot;}
  总价: $price
  总数量: $countNum
  Date: $date
-----------------------------
&#39;&#39;&#39;;
}

void main() {
  ShoppingCart.withCode(name:&#39;张三&#39;, code:&#39;123456&#39;)
  ..bookings = [Item(&#39;苹果&#39;,10.0,3), Item(&#39;鸭梨&#39;,20.0,2)]
  ..printInfo();

  ShoppingCart(name:&#39;李四&#39;)
  ..bookings = [Item(&#39;香蕉&#39;,15.0, 1), Item(&#39;西瓜&#39;,40.0, 4)]
  ..printInfo();
}
</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/55/50/09c6ce64.jpg" width="30px"><span>大神留条命</span> 👍（0） 💬（1）<div>我想用泛型来取后台 data 中的数据。我知道限制继承了某个类的是可以的。我想传入的类限制为实现了fromJsonMap这个工厂方法的可以吗。</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/9f/9f9f02c3.jpg" width="30px"><span>allen</span> 👍（0） 💬（1）<div>ShoppingCart.withCode这个withCode方法是自己定义的么，还是系统自带的，我没见到这个方法，还是说直接能类名加方法名定义的</div>2019-07-17</li><br/>
</ul>