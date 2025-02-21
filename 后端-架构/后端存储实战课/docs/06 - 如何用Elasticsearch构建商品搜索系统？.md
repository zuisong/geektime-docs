你好，我是李玥。

搜索这个特性可以说是无处不在，现在很少有网站或者系统不提供搜索功能了，所以，即使你不是一个专业做搜索的程序员，也难免会遇到一些搜索相关的需求。搜索这个东西，表面上看功能很简单，就是一个搜索框，输入关键字，然后搜出来想要的内容就好了。

搜索背后的实现，可以非常简单，简单到什么程度呢？我们就用一个SQL，LIKE一下就能实现；也可以很复杂，复杂到什么程度呢？不说百度谷歌这种专业做搜索的公司，其他非专业做搜索的互联网大厂，搜索团队大多是千人规模，这里面不仅有程序员，还有算法工程师、业务专家等等。二者的区别也仅仅是，搜索速度的快慢以及搜出来的内容好坏而已。

今天这节课，我们就以电商中的商品搜索作为例子，来讲一下，如何用ES(Elasticsearch)来快速、低成本地构建一个体验还不错的搜索系统。

## 理解倒排索引机制

刚刚我们说了，既然我们的数据大多都是存在数据库里，用SQL的LIKE也能实现匹配，也能搜出结果，为什么还要专门做一套搜索系统呢？我先来和你分析一下，为什么数据库不适合做搜索。

搜索的核心需求是全文匹配，对于全文匹配，数据库的索引是根本派不上用场的，那只能全表扫描。全表扫描已经非常慢了，这还不算，还需要在每条记录上做全文匹配，也就是一个字一个字的比对，这个速度就更慢了。所以，使用数据来做搜索，性能上完全没法满足要求。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e7/76/79c1f23a.jpg" width="30px"><span>李玥</span> 👍（57） 💬（3）<div>Hi，我是李玥。

还是在这里回顾一下上节课的思考题：

2PC也有一些改进版本，比如3PC、TCC这些，它们大体的思想和2PC是差不多的，解决了2PC的一些问题，但是也会带来新的问题，实现起来也更复杂，限于篇幅我们没法每个都详细地去讲解。在理解了2PC的基础上，课后请你自行去学习一下3PC和TCC，然后对比一下，2PC、3PC和TCC分别适用于什么样的业务场景？

谈一下我的理解：

3PC相比于2PC做了两个改进，一是事务执行器也增加了超时机制，避免我们课程中提到的因为协调者宕机，导致执行器长时间卡死的问题，另外，3PC在2PC之前增加一个询问阶段，这个阶段事务执行器可以去尝试锁定资源（但不等待），这样避免像2PC那样直接去锁定资源，而资源不可用的情况下，一直等待资源而卡住事务的情况。

TCC可以理解为业务层面的2PC（也有观点主张TCC和2PC是完全不同的，我个人建议没必要在这些概念上较真，理解并正确使用才是关键），TCC同样分为Try和Confirm&#47;Cancel 两个阶段，在Try阶段锁定资源，但不执行任何更新操作，Confirm阶段来执行所有更新操作并提交，如果失败进入Cancel阶段。Cancel阶段就是收拾烂摊子，把Confirm阶段做的数据更新都改回去，把Try阶段锁定的资源都释放。相比于2PC，TCC可以不依赖于本地事务，但是Cancel阶段的业务逻辑比较难实现。</div>2020-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIdsbpIiaryKso4qcjFfuWoMebCNM7jvC0N5GdOqks4waTiaZdgKwbwmyv5xiaVeHVKJzaOYXTZoL0OQ/132" width="30px"><span>Geek_c76e2d</span> 👍（191） 💬（6）<div>因为用户每输入一个字都可能会发请求查询搜索框中的搜索推荐。所以搜索推荐的请求量远高于搜索框中的搜索。es针对这种情况提供了suggestion api，并提供的专门的数据结构应对搜索推荐，性能高于match，但它应用起来也有局限性，就是只能做前缀匹配。再结合pinyin分词器可以做到输入拼音字母就提示中文。如果想做非前缀匹配，可以考虑Ngram。不过Ngram有些复杂，需要开发者自定义分析器。比如有个网址www.geekbang.com，用户可能记不清具体网址了，只记得网址中有2个e，此时用户输入ee两个字母也是可以在搜索框提示出这个网址的。以上是我在工作中针对前缀搜索推荐和非前缀搜索推荐的实现方案。</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（31） 💬（4）<div>老师，我刚刚问的那个问题，我这边找到了一个方案，但不知道是否是业界用的方案，还请老师指点一下
全文检索要把 title 的 type 设置为 text
前缀推荐要把 title 的 type 设置为 completion
想同时支持全文检索和前缀匹配推荐如何做？
用 fields 

mapping 文件如下
PUT sku
{
  &quot;mappings&quot;: {
    &quot;properties&quot;: {
      &quot;sku_id&quot;:{
        &quot;type&quot;: &quot;long&quot;
      },
      &quot;title&quot;:{
        &quot;type&quot;: &quot;text&quot;,
        &quot;analyzer&quot;: &quot;ik_max_word&quot;,
        &quot;search_analyzer&quot;: &quot;ik_max_word&quot;,
        &quot;fields&quot;: {
          &quot;title_suggest&quot;:{
            &quot;type&quot;:&quot;completion&quot;
          }
        }
      }
    }
  }
}

支持全文检索
GET sku&#47;_search?pretty
{
  &quot;query&quot;: {
    &quot;match&quot;: {
      &quot;title&quot;: &quot;苹果手机&quot;
    }
  }
}

支持前缀匹配
POST sku&#47;_search?pretty
{
  &quot;size&quot;:0,
  &quot;suggest&quot;: {
    &quot;suggester&quot;: {
      &quot;prefix&quot;: &quot;烟台&quot;,
      &quot;completion&quot;: {
        &quot;field&quot;: &quot;title.title_suggest&quot;
      }
    }
  }
}</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/af/d9/b1fc248c.jpg" width="30px"><span>黄平</span> 👍（10） 💬（4）<div>老师，es除了做搜索，还有哪些业务场景可以使用呢？能简单列举下吗？</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/da/79/9b093890.jpg" width="30px"><span>大秦皇朝</span> 👍（8） 💬（1）<div>李sir我还想再问下，根据我们不同的业务，选分词插件有啥讲究没？虽有点跑题，但是能不能简单说下，感谢~</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/ae/7b310c2d.jpg" width="30px"><span>呦呦鹿鸣</span> 👍（4） 💬（3）<div>李老师好，请问下ES在做深度分页查询时的场景下有什么好的方案么</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/67/59e81206.jpg" width="30px"><span>王超</span> 👍（4） 💬（2）<div>老师，针对订单中心的表数据，业务库用mysql，同步到es做查询时，比如一个订单主表，关联5个子表，在es存的时候是以嵌套的形式存一个index，还是mysql一张表，对应es的一个index，然后维护父子关系？或者有更好的方案</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/77/f9f1b47d.jpg" width="30px"><span>Jax</span> 👍（4） 💬（2）<div>老师您好，是否可以做一些电商这种海量数据下，后台管理系统存储方面的最佳实践。还有对于不同系统之间的数据同步，也希望得到一些比较好的实践方案或者工具。

以下是比较具体的点：

我在上家公司也是做电商系统的，不过我负责的是后台商品数据的维护系统。前台可以用各种缓存来提速，但是对于后台系统，该如何让系统变得比较快？尤其是后台管理系统往往会涉及大批量商品的价格，库存之类的更新，并且更新后业务团队希望能实时看到他们更新成功了，而且有不少更新的操作对丢数据的容忍度比较低，这种情况下缓存也很难做，所以想得到一些对于这种大批量数据后台管理系统的实践经验。

对于数据同步，主要是有的原始数据存储在传统数据库，而为了速度，会存储到一些no sql产品做缓存，但是我们在实践中，经常会有一些丢数据，或者未能及时同步的情况发生，希望能得到这方面的一些经验分享。</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（4） 💬（2）<div>老师 您说的二次查找是指在第一次的查找结果中继续查找吗</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（3） 💬（2）<div>老师 面试中经常会有问到几千万条数据列表的查询如何实现 ，本质就是考避免使用数据库而选择这种es来搜索是么 。 那几千万条数据在es中查询 “苹果” 是不是也会有性能之类的问题</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/00/12149f4e.jpg" width="30px"><span>郭刚</span> 👍（2） 💬（1）<div>用ES有两个问题，1.它不适合多索引关联，就像关系数据库的多表关联，那关系数据库多表关联查询的情况是不是建一张中间表，把中间表的数据导入到es   2.要做到准实时的要求，有没有好的方式</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（2）<div>老师，请教个问题，比如一个商品搜索系统，给一些商品打标签，然后支持根据商品信息和标签搜索商品，有啥方案吗？</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ed/e0/c63d6a80.jpg" width="30px"><span>1</span> 👍（0） 💬（1）<div>比如商品搜索跟每个用户签了某些商品的价格，每个客户看到签的价格不一样，用es查询给每个用户都建一个index，还是有什么更好的方法？想让它可以按价格排序</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/a1/b08f3ee7.jpg" width="30px"><span>何妨</span> 👍（0） 💬（1）<div>那一般什么时候来更新索引呢？是建立一个定时任务来更新么</div>2020-03-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（52） 💬（2）<div>老师，能否来一篇加餐，讲讲ES、MySQL、MongoDB、RocketMQ&#47;Kafka、newSQL这些存储的对比，底层是基于什么原理擅长干哪些事，不擅长干哪些事？</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/52/014accaf.jpg" width="30px"><span>划过天空阿忠</span> 👍（11） 💬（0）<div>es这个结构化mapping感觉好麻烦，另外老师三俩句就把倒排索引给我讲清楚了，厉害！</div>2020-03-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ydFhHonicUQibGlAfsAYBibNOfSxpCG5cJNp9oRibTJm3TrxM7Hj4WPPCRE3vluZJb0TGQqpKCaBWLdmra5Su1KF5Q/132" width="30px"><span>yudidi</span> 👍（2） 💬（2）<div>注意type这个概念在es6之后被逐渐移除了。
https:&#47;&#47;www.elastic.co&#47;guide&#47;en&#47;elasticsearch&#47;reference&#47;6.3&#47;getting-started-concepts.html#_type</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c4/cf/9ab85d9b.jpg" width="30px"><span>啥也不懂爱乱说</span> 👍（2） 💬（0）<div>对于分布式事务部分还是没太能理解，老师可否加个餐，展示一波代码看一下2pc和tcc具体的代码实战</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（0）<div>思考题需要把要支持前缀推荐的 field 的类型设置为  completion，现在只支持前缀匹配</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（1）<div>老师，有个问题请教一下，如果用 ES 做全文检索，需要把 title 的类型设置为 text，支持分词，这样就可以像老师在专栏中介绍的一样，用 “苹果手机”进行全文检索了。
但是如果要实现思考题这种前缀推荐，需要 title 的类型为 completion。
要想实现 title 既支持前缀推荐，又支持全文检索，但一个 field 只能设置一种类型，这种该怎么实现呢？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/da/79/9b093890.jpg" width="30px"><span>大秦皇朝</span> 👍（1） 💬（1）<div>windows下测试避坑：
分词插件icu支持路径中带空格或者说是可以es放在Program Files下；如果用ik的话，建议路径不要带空格，网上很多说权限之类的，我把权限调整了也不行，路径不带空格立马OK。</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/c0/106d98e7.jpg" width="30px"><span>Sam_Deep_Thinking</span> 👍（0） 💬（0）<div>这篇算是写的言简意赅，但是又能学到东西，厉害哈。</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/cf/0d/8a595ab0.jpg" width="30px"><span>Sun</span> 👍（0） 💬（1）<div>在电商中有一个常见的场景就是根据商品销量倒叙展示问题，销量试试变动，我现在是查询出来商品id再到数据库中查找库存排序，但是如果有分页客户体验特别差，没库存的或者缺货的会排在前面几页，老师请问有没有什么好的思路</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/92/b7/fc482ba9.jpg" width="30px"><span>爱喝可乐的派大星星</span> 👍（0） 💬（1）<div>es不适合更新字段，那假如我需要修改内容，我是更新好还是删除后新增好。</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e4/e7/31944ee7.jpg" width="30px"><span>千军万马万马@</span> 👍（0） 💬（0）<div>咋没人点赞啊</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cf/78/72c1545a.jpg" width="30px"><span>JiaLong</span> 👍（0） 💬（1）<div>老师，能不能再解释一下什么是倒排？，苹果的倒排是果苹，烟台，台烟？</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/dd/82d8eff2.jpg" width="30px"><span>Mine</span> 👍（0） 💬（1）<div>就没有人说说多数据源异构同步至一个index如何处理吗😭😭😭。数据如何保证不丢失，如何保证同步的顺序选。</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/16/ed/2db68084.jpg" width="30px"><span>刘瓜瓜</span> 👍（0） 💬（0）<div>为什么不用B+树，而要用B树呢，B+树搜索不是更好吗</div>2021-03-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIG2aw6bmrrxPkrwIyStmZsfaYVHzYbP05A8V9LCa8ZnKl7yYb4zHTyicN5grp03nnpRqgQicpsaTxg/132" width="30px"><span>STOREFEE</span> 👍（0） 💬（2）<div>发现即使用了中文分词，查询也没有mysql那么准确呢？这个是怎么彻底解决呢？</div>2020-10-14</li><br/>
</ul>