上一篇文章中，我们讲到了如何在Excel中使用SQL进行查询。在Web应用中，即使不通过后端语言与数据库进行操作，在Web前端中也可以使用WebSQL。WebSQL是一种操作本地数据库的网页API接口，通过它，我们就可以操作客户端的本地存储。

今天的课程主要包括以下几方面的内容：

1. 本地存储都有哪些，什么是WebSQL？
2. 使用WebSQL的三个核心方法是什么？
3. 如何使用WebSQL在本地浏览器中创建一个王者荣耀英雄数据库，并对它进行查询和页面的呈现？

## 本地存储都有哪些？什么是WebSQL？

我刚才讲到了WebSQL实际上是本地存储。其实本地存储是个更大的概念，你现在可以打开Chrome浏览器，看下本地存储都包括了哪些。

Cookies是最早的本地存储，是浏览器提供的功能，并且对服务器和JS开放，这意味着我们可以通过服务器端和客户端保存Cookies。不过可以存储的数据总量大小只有4KB，如果超过了这个限制就会忽略，没法进行保存。

Local Storage与Session Storage都属于Web Storage。Web Storage和Cookies类似，区别在于它有更大容量的存储。其中Local Storage是持久化的本地存储，除非我们主动删除数据，否则会一直存储在本地。Session Storage只存在于Session会话中，也就是说只有在同一个Session的页面才能使用，当Session会话结束后，数据也会自动释放掉。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/8f/4b0ab5db.jpg" width="30px"><span>Middleware</span> 👍（11） 💬（2）<div>```php
&lt;body&gt;
    &lt;div class=&quot;content&quot;&gt;
        &lt;label for=&quot;name&quot;&gt;&lt;&#47;label&gt;
        &lt;input id=&quot;name&quot; type=&quot;text&quot; name=&quot;name&quot;&gt; 
        &lt;input type=&quot;button&quot; value=&quot;查询&quot; onclick=&quot;query()&quot;&gt;
    &lt;&#47;div&gt;
    &lt;script type=&quot;text&#47;javascript&quot;&gt;
        if(!window.openDatabase)
        {
            alert(&#39;您的浏览器不支持 WebSQL&#39;);
        }
        var db = openDatabase(&#39;wucai&#39;, &#39;1.0&#39;, &#39;王者荣耀数据库&#39;, 1024 * 1024);

        db.transaction(function (tx) {
            tx.executeSql(&#39;CREATE TABLE IF NOT EXISTS heros (id unique, name, hp_max, mp_max, role_main)&#39;);
            tx.executeSql(&#39;INSERT INTO heros (id, name, hp_max, mp_max, role_main) VALUES (10000, &quot;夏侯惇&quot;, 7350, 1746, &quot; 坦克 &quot;)&#39;);
            tx.executeSql(&#39;INSERT INTO heros (id, name, hp_max, mp_max, role_main) VALUES (10001, &quot;钟无艳&quot;, 7000, 1760, &quot; 战士 &quot;)&#39;);
            tx.executeSql(&#39;INSERT INTO heros (id, name, hp_max, mp_max, role_main) VALUES (10002, &quot;张飞&quot;, 8341, 100, &quot; 坦克 &quot;)&#39;);
            tx.executeSql(&#39;INSERT INTO heros (id, name, hp_max, mp_max, role_main) VALUES (10003, &quot;牛魔&quot;, 8476, 1926, &quot; 坦克 &quot;)&#39;);
            tx.executeSql(&#39;INSERT INTO heros (id, name, hp_max, mp_max, role_main) VALUES (10004, &quot;吕布&quot;, 7344, 0, &quot; 战士 &quot;)&#39;);
            msg = &#39; 数据表创建成功，一共插入 5 条数据&#39;;
            
            console.log(msg);
         });

         function query(){
            var name = document.getElementById(&#39;name&#39;).value;
            
            var sql = &#39;SELECT * FROM heros where name like ?&#39;;
             &#47;&#47; 查询数据
            db.transaction(function (tx) {
                tx.executeSql(sql, [&#39;%&#39;+name+&#39;%&#39;], function (tx, data) {
                var len = data.rows.length;
                console.log(&#39;查找到：&#39; +len +&#39;条记录&#39;);
                console.log(data.rows);
                });

            });
         }
    &lt;&#47;script&gt;
&lt;&#47;body&gt;
```</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（6） 💬（2）<div>localForage这个库可以兼容处理IndexDB,localStorage,webSQL等</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/8f/4b0ab5db.jpg" width="30px"><span>Middleware</span> 👍（6） 💬（1）<div>WebSQL 这项标准已经废弃了吧

https:&#47;&#47;dev.w3.org&#47;html5&#47;webdatabase&#47;</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（4） 💬（1）<div>WebSQL的功能确实很强大，但是在目前的项目中还没有用到过。</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/65/cce8eb34.jpg" width="30px"><span>nimil</span> 👍（3） 💬（2）<div>这个功能厉害了</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（1） 💬（2）<div>这两个都是长期有效，只能用户手动删除才可以的吗？</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/65/68bd8177.jpg" width="30px"><span>雪飞鸿</span> 👍（0） 💬（3）<div>看了下文档IndexedDB虽然是NoSql，但也是基于事务来处理数据的。</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/cf/d5382404.jpg" width="30px"><span>RRR</span> 👍（2） 💬（0）<div>webSQL 已经被规范废弃，现在只支持 IndexDB。</div>2020-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（2） 💬（0）<div>了解了浏览器端的五种存储方式：Cookie,Local storage,Session storage,WebSQL,IndexedDB</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/f0/a73607b3.jpg" width="30px"><span>victor666</span> 👍（2） 💬（0）<div>挺有意思的。可以拿来做SQL语句测试</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（1） 💬（1）<div>session是什么概念呢？http请求不是无状态的么，难道一次http请求就是一个session吗</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>长见识了</div>2024-08-26</li><br/>
</ul>