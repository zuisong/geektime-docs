你好，我是朱晔。今天，我要和你分享的主题是，空值处理：分不清楚的null和恼人的空指针。

有一天我收到一条短信，内容是“尊敬的null你好，XXX”。当时我就笑了，这是程序员都能Get的笑点，程序没有获取到我的姓名，然后把空格式化为了null。很明显，这是没处理好null。哪怕把null替换为贵宾、顾客，也不会引发这样的笑话。

程序中的变量是null，就意味着它没有引用指向或者说没有指针。这时，我们对这个变量进行任何操作，都必然会引发空指针异常，在Java中就是NullPointerException。那么，空指针异常容易在哪些情况下出现，又应该如何修复呢？

空指针异常虽然恼人但好在容易定位，更麻烦的是要弄清楚null的含义。比如，客户端给服务端的一个数据是null，那么其意图到底是给一个空值，还是没提供值呢？再比如，数据库中字段的NULL值，是否有特殊的含义呢，针对数据库中的NULL值，写SQL需要特别注意什么呢？

今天，就让我们带着这些问题开始null的踩坑之旅吧。

## 修复和定位恼人的空指针问题

**NullPointerException是Java代码中最常见的异常，我将其最可能出现的场景归为以下5种**：
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（75） 💬（11）<div>补充下：在MySQL的使用中，对于索引列，建议都设置为not null，因为如果有null的话，MySQL需要单独专门处理null值，会额外耗费性能。
回答下问题：
第一个问题：
从ConcurrentHashMap他自己的作者（Doug Lea）：

http:&#47;&#47;cs.oswego.edu&#47;pipermail&#47;concurrency-interest&#47;2006-May&#47;002485.html

The main reason that nulls aren&#39;t allowed in ConcurrentMaps
(ConcurrentHashMaps, ConcurrentSkipListMaps) is that
ambiguities that may be just barely tolerable in non-concurrent
maps can&#39;t be accommodated. The main one is that if
map.get(key) returns null, you can&#39;t detect whether the
key explicitly maps to null vs the key isn&#39;t mapped.
In a non-concurrent map, you can check this via map.contains(key),
but in a concurrent one, the map might have changed between calls.

ConcurrentMaps（ConcurrentHashMaps，ConcurrentSkipListMaps）不允许使用null的主要原因是，无法容纳在非并行映射中几乎无法容忍的歧义。最主要的是，如果map.get(key)return null，则无法检测到该键是否显式映射到null该键。在非并行映射中，您可以通过进行检查 map.contains(key)，但在并行映射中，两次调用之间的映射可能已更改。

hashtable也是线程安全的，所以也是key和value也是不可以null的
treeMap 线程不安全，但是因为需要排序，进行key的compareTo方法，所以key是不能null中，value是可以的

第二个问题：
MyBatis @Column注解的updateIfNull属性，可以控制，当对应的列value为null时，updateIfNull的true和false可以控制</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/69/af/ceb4450c.jpg" width="30px"><span>Asha</span> 👍（17） 💬（2）<div>老师，麻烦问下
UserDto 中只保留 id、name 和 age 三个属性，且 name 和 age 使用 Optional 来包装，以区分客户端不传数据还是故意传 null， 这个我不太明白是怎么区分出来的呢？
还有下面的这句话，他能走到orElse上吗？
if (user.getName() != null) { userEntity.setName(user.getName().orElse(&quot;&quot;)); }</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/aa/32fc0d54.jpg" width="30px"><span>失火的夏天</span> 👍（12） 💬（2）<div>ConcurrentHashMap 的 Key 和 Value 都不能为 null，而 HashMap 却可以。

ConcurrentHashMap这个老爷子只说了value如果是空，会有二义性。就是在线程安全情况下，他到底是设置了一个null还是根本就没这玩意，key他老人家没说。。。老师可以说下理解吗？

TreeMap的Key不能为空，因为TreeMap是基于compare的，空值不能compare。value可以为空，TreeMap并不线程安全。Hashtable 的 Key 和 Value也不能空，我想原理应该和ConcurrentHashMap一样。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/6f/42494dcf.jpg" width="30px"><span>Jerry Wu</span> 👍（8） 💬（16）<div>这是我个人的一些工作经历。

以前尝试过Optional，但其他人反馈看不懂，最后还是换回了if-else。

得出结论，技术要考虑团队的接受程度。

新技术、新特性虽好，但团队每个人的能力不同，而决定技术走向的，是团队最弱的那个人。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（7） 💬（5）<div>有个规范我记得是说，不要在字段，方法参数，集合中使用Optional</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3f/57/a014199a.jpg" width="30px"><span>书林</span> 👍（3） 💬（1）<div>关于SQL 判断空有一点想提出来讨论，=NULL 不是赋值确实是判断，只是NULL和任何值的直接比较都为NULL，比如NULL&lt;&gt;NULL, NULL=NULL, NULL=1结果都为NULL。对 NULL 进行判断只能使用 IS NULL 或者 IS NOT NULL，或者ISNULL()。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/d5/1f5c5ab6.jpg" width="30px"><span>大大大熊myeh</span> 👍（3） 💬（1）<div>原文：“归根结底，这是如下 5 个方面的问题：明确 DTO 种 null 的含义”或许是“明确 DTO各种 null 的含义”吧.

MySQL中
count(1)选取每一行并赋值为1，进行统计
count(*)选取每一行进行统计
count(字段)选取每一行中的该字段，选择不为null的行进行统计

我认为Optional可以代替原来的if-else赋值，使代码看上去稍许简洁。但需要注意如Optional.ofNullable(number).orElse(0)，当number为null时，返回的0不会赋值给number，它返回的是一个新地址（对象）。

思考题1，楼上Darren老兄说的很对。更加白话的说明“非并行映射中几乎无法容忍的歧义”就是——如果map.get(key)返回了null，无法明确是因为map中没有找到该key返回的null，还是因为该key包含的value就是null。

思考题2，xml配置文件中的if标签&lt;if test=&quot;id!=null and id !=&#39;&#39;&quot;&gt;&lt;&#47;if&gt;需要注意if标签中的字段id如果是Date类型的话，不要写id!=&#39;&#39;，这是由于Data类型与字符串类型进行比较的报错，此时只需写null的判断即可。

以前不知道@Column注解的updateIfNull属性，学到了。
</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/6e/6c5f5734.jpg" width="30px"><span>终结者999号</span> 👍（3） 💬（1）<div>在平常的开发中，对于DTO的值验证性校验也可以使用Hibernate Validator，也可以杜绝用户不按接口文档中所定义的格式输入，感觉也可以使用</div>2020-04-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dgox0m94vr6w2Vxk0N6651pyL5wKWicqgwIxU9iahlIn5LKeFfQJDjzUoQKM8WNibS7Yuxyulmic1Xxfia5ibFc6ia0Hw/132" width="30px"><span>Geek_fe5e8a</span> 👍（1） 💬（1）<div>老师讲的真的好  满分</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（1） 💬（1）<div>问题大家都答的很好，我就直接问问题吧。
老师，Hashtable的put会对value做null判断，key是在调用hashcode方法时报空指针，而ConcurrentHashMap是直接对key和value做null判断，是不是Hashtable的设计有问题？</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（29） 💬（0）<div>今天最大的惊喜就是arthas，以前听说过，但是从来没使用过，真心神器，感谢，感谢！！！</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（11） 💬（0）<div>第二个问题，mybatis 可以使用 if 标签来判断属性是否为 null 从而动态生成不含该属性的 sql。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（8） 💬（4）<div>谢谢老师。小伙伴们，我们这边UserDto都要求写成UserDTO，你们是哪种呢</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（5） 💬（0）<div>1、以前遇到过好几次null异常，都是通过打日志搞定的，十分低效，arthas是个好工具，收藏了。
2、Optional很少用，确实是个好东东。
3、map我觉得都不应该支持Null，非线程安全map get返回Null时，到底是没有key，还是value为Null有二义性（但可以通过探测破解二义，这可能是支持了Null的原因），线程安全map 探测结果本身就不可靠（可能被并发修改），所以作者选则不支持，列如：
B put key null   B往线程安全map中插入值为null的数据
A contain key   A探测key存在
B remove key   B移除key
A get key         A获取key得到null，A认为key的值为null，实际返回的null并非key的值</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（3） 💬（0）<div>解决方案里，我觉得既然先查了一次实体，就没必要使用 @DynamicUpdate 部分更新字段了呀？这时全字段更新也没有问题的</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/05/f154d134.jpg" width="30px"><span>刘楠</span> 👍（3） 💬（0）<div>ConcurrentHashMap
 final V putVal(K key, V value, boolean onlyIfAbsent) {
        if (key == null || value == null) throw new NullPointerException();
因为直接对key进行了hashCode,要进行比较

put方法对key和value做了判断的，

HashMap
key，只能有一个key为null,value没限制，


TreeMap 

key也是不能为能为null的,put方法中要调用comparator方法去比较key
value可以为null

Hashtable
key,value都不能为null
因为直接对key进行了hashCode,同时对value做了判断为null直接抛出异常了</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（2） 💬（0）<div>学习了，optional还可以这么用，SpringMVC数据绑定也会支持吗？</div>2020-04-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/L8EpqHoAnmvkzCIsdOkv5QvhIzu5tMaF2FDusXShqukv5ZBkS8DbicWaErjnYydibiaqBrs70wQ8P6axvC2FbWpbQ/132" width="30px"><span>Geek_d3928c</span> 👍（1） 💬（0）<div>线上机器也不允许使用arthas呀</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/46/7d65ae37.jpg" width="30px"><span>木几丶</span> 👍（1） 💬（0）<div>ConcurrentHashMap，Hashtable等线程安全的集合key value不能为null，因为会有二义性：get时返回null到底是没有还是就是null？为什么hashmap可以呢，因为对于单线程的集合可以用containsKey辅助判断，而多线程下用containsKey判断会有线程安全问题（get和containsKey之间插入了put）</div>2021-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/VGh9ULc7y9ZzVp5aHQLb4J9qmQOAE4ibYHfeia1F8s08PwvhH9kKZ1wr91gTfTEnj0LtybegsFibPcceyTIkHJTcw/132" width="30px"><span>Geek_Gary</span> 👍（1） 💬（0）<div>Optional还有这种用法，谨受教������</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/45/d719f7df.jpg" width="30px"><span>李和桃</span> 👍（1） 💬（0）<div>1、ConcurrentHashMap不能为null的原因主要是因为考虑到多线程并发的情况。在多线程并发处理下，如果key = null or value = null，很难判断是设置key=null还是key根本不存在。HashMap本身建议是在单线程任务执行时使用，所以可以设置为null。
TreeMap的key是不可以为null的，value可以是null。为了保证有序，treemap中的key还需要实现comparator的compare方法。
HashTable的key和value都不可以为null，这个原因个人猜测，继承了字典类，字典里面有null不合适。HashMap对null的处理是专门给了一个0的槽，而且这个槽只会有一个entry.
2、采用if-test标签的方式，对字段进行是否为null的判断。</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/2c/b73b9dfe.jpg" width="30px"><span>2019</span> 👍（1） 💬（0）<div>打个卡卡。那个说写Java8新特效被喷的，你同事那是属于不想进步。让他待在舒适区好了。</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/db/ddfe411f.jpg" width="30px"><span>yanghao</span> 👍（1） 💬（0）<div>原来一直在坑里，最近项目里就是各种判空</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4c/7e/4771d8a4.jpg" width="30px"><span>彭发红</span> 👍（1） 💬（0）<div>个人习惯对于数据的验证都会在控制层通过@Validated来实现第一道业务数据验证，然后再通过Optional</div>2020-04-17</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（1） 💬（0）<div>及时发现及时处理日志空指针异常</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/df/04/791d0f5e.jpg" width="30px"><span>笨手笨脚の</span> 👍（0） 💬（0）<div>实际开发中，在使用stream流进行 GroupBy 的时候，如果 GroupBy 的对象为 null，会出现空指针错误</div>2025-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/55/ad/791d0f5e.jpg" width="30px"><span>joyboy</span> 👍（0） 💬（0）<div>学习本篇文章的收获：
1.要结合业务思考字段为null的含义才能正确处理。
2.数据库null值的坑</div>2024-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>高版本的jdk对于npe的支持与提示已经很友好了，其实主要还是对于代码书写健壮性与合理性的考虑。大部分开发人员其实还是没有意识到对于null的处理，只是遇到了npe然后在进行补充。</div>2022-04-19</li><br/>
</ul>