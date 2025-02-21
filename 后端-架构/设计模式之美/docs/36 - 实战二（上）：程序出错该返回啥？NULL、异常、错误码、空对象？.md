我们可以把函数的运行结果分为两类。一类是预期的结果，也就是函数在正常情况下输出的结果。一类是非预期的结果，也就是函数在异常（或叫出错）情况下输出的结果。比如，在上一节课中，获取本机名的函数，在正常情况下，函数返回字符串格式的本机名；在异常情况下，获取本机名失败，函数返回UnknownHostException异常对象。

在正常情况下，函数返回数据的类型非常明确，但是，在异常情况下，函数返回的数据类型却非常灵活，有多种选择。除了刚刚提到的类似UnknownHostException这样的异常对象之外，函数在异常情况下还可以返回错误码、NULL值、特殊值（比如-1）、空对象（比如空字符串、空集合）等。

每一种异常返回数据类型，都有各自的特点和适用场景。但有的时候，在异常情况下，函数到底该返回什么样的数据类型，并不那么容易判断。比如，上节课中，在本机名获取失败的时候，ID生成器的generate()函数应该返回什么呢？是异常？空字符？还是NULL值？又或者是其他特殊值（比如null-15293834874-fd3A9KBn，null表示本机名未获取到）呢？

函数是代码的一个非常重要的编写单元，而函数的异常处理，又是我们在编写函数的时候，时刻都要考虑的。所以，今天我们就聊一聊，如何设计函数在异常情况下的返回数据类型。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/62/b8/bb9657c6.jpg" width="30px"><span>Promise°</span> 👍（9） 💬（2）<div>大家好,第一次发言。有个疑问:各位在Service层返回的是对象还是Result接口</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/17/d3/936f4599.jpg" width="30px"><span>sunnywhy</span> 👍（6） 💬（4）<div>第二种返回Null的情况，可以使用Optional吗</div>2020-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（4） 💬（1）<div>这句话不太理解，即便是可恢复的异常依然是向上抛更合理，比如提现金额大于余额就应该告知用户啊。实在想不明白受检查异常的用武之地在哪？


对于代码 bug（比如数组越界）以及不可恢复异常（比如数据库连接失败），即便我们捕获了，也做不了太多事情，所以，我们倾向于使用非受检异常。对于可恢复异常、业务异常，比如提现金额大于余额的异常，我们更倾向于使用受检异常，明确告知调用者需要捕获处理。</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（3） 💬（1）<div>Happy new year！
鼠年大吉🎊🎈🎉🍾️🎆🧧</div>2020-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8f/1c/1c728388.jpg" width="30px"><span>皮卡皮卡</span> 👍（0） 💬（1）<div>返回空对象章节中，return Collectiosn.emptyList();出现拼写错误，应该是Collections.emptyList();</div>2020-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（111） 💬（0）<div>回答问题
1.抛出异常，因为服务器获取不到host是一种异常情况，并且打印的异常日志不能是warm,而是err，因为该异常不会自动回复。

2.往上抛，原封不动。应该在api统一出口处处理异常，这样异常代码会比较聚合（个人习惯）。该异常描述已经很准确，且处理异常依旧在genId接口中，所以上层函数可以认识该异常，所以原封不动。（而统一出口函数，则可以抛自定义异常，以收敛api使用方的考虑范围）。

3.抛出异常，null值裁剪名称是一种异常情况。或则说，对于裁剪名称这个函数，入参不能为null。

4.返回空字符串。小于等于0说明不需要带随机后缀，这也是一个正常的业务场景。返回空字符串是为了方便调用方不用做null判断。


分歧：
1.get,find,select等dao层操作，返回null是正常业务情况，表示数据不存在。但在其应用层，数据不存在可能意味着有脏数据，数据缺失等情况，属于异常情况，需要抛出异常。所以同样是get方法，持久层返回null，业务层返回可能是异常。

2.异常流开销大，在对响应时间要求很严格的场景。放弃合理的异常处理，采用不合理的特殊返回值的方式也是合理的。所以合理的运用异常流在java也是一个选择项。在可读和性能我们需要权衡，而这两玩意经常是相驳的。

最后：
祝栏主和同学们新年快乐！</div>2020-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（24） 💬（1）<div>1、不抛。返回null-123123784378-aldjf780。从功能上讲，函数是生成logtraceid，用于给记录加id，便于查找日志。返回null不影响定位问题，同时程序不会蹦。
2、上抛，到generate中处理。
3、返回空串
4、返回空串</div>2020-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（21） 💬（0）<div>Go语言函数返回的时候分正确值、错误值，比较简单</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（10） 💬（0）<div>对于今天课堂留的作业，我采用了统一的思路—能用异常解决的都用异常解决。

1.对于 generate() 函数，如果本机名获取失败，函数返回什么？这样的返回值是否合理？
答：抛出异常，这是一个无法恢复的情况，打断正常的处理流程并进入异常逻辑处理模块

2. 对于 getLastFiledOfHostName() 函数，是否应该将 UnknownHostException 异常在函数内部吞掉（try-catch 并打印日志）？还是应该将异常继续往上抛出？如果往上抛出的话，是直接把 UnknownHostException 异常原封不动地抛出，还是封装成新的异常抛出？
答：不应该内部吞掉，应该抛出到上层做统一的异常处理，这里是个单一的模块，不需要再封装

3. 对于 getLastSubstrSplittedByDot(String hostName) 函数，如果 hostName 为 NULL 或者是空字符串，这个函数应该返回什么？
答：抛出异常，异常消息是—hostName为NULL或空字符串

4. 对于 generateRandomAlphameric(int length) 函数，如果 length 小于 0 或者等于 0，这个函数应该返回什么？
答：抛出异常，异常消息是—参数不合法</div>2020-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cc/d9/20d4f7c2.jpg" width="30px"><span>大雁小鱼</span> 👍（5） 💬（4）<div>我的领导告诉我，代码稳定是第一位的，如果线上代码没有出错，即便代码写得很烂，都是不允许去修改的，一个标点一个符号都不能修改，更别说小步重构了。所以可以理解为什么有的公司代码永远都是4、5年前的样子，不去动它了。</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/33/c33c0e8a.jpg" width="30px"><span>exception</span> 👍（4） 💬（0）<div>关于函数返回值的问题，之前写代码也纠结过，思考过，目前我在项目中使用如下：
定义返回值Result(success, value, errCode, errMessage)和异常同时使用。
正常的业务逻辑，都使用Result进行返回，业务逻辑中出现失败的情况，通过错误码进行定义。像文中提到的查询成功但是没有数据的情况，那就是Result的success为true，但是value为空。
异常适用于处理非业务逻辑情况，如远程RPC调用失败，网络超时，空指针，等情况才使用异常往外抛。
对于受检异常和非受检异常，各自各有优劣吧，不能说谁完全就能代替谁，只要用的得当，都有他的价值，没必要太极端。</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/4d/b0228a1a.jpg" width="30px"><span>平风造雨</span> 👍（4） 💬（0）<div>不能恢复的异常应该抛出，能处理能恢复的可以吞掉，但是吞掉的异常要有办法在日志或者其它办法看到异常的原因，便于后续排查问题。异常是否要重新定义异常并抛出，不能一概而论，某些情况下，异常的值和类型本身就是接口约定中的一部分，特别是unchecked异常。</div>2020-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/5b/ff28088f.jpg" width="30px"><span>郑大钱</span> 👍（3） 💬（1）<div>异常，这对我来说是一个多么陌生的概念。
OC中的try catch不能捕获UncaughtException，而内存溢出、野指针等大部分异常都是UncaughtException，而可以捕获的异常基本都是我们可以预防的，所以OC中的异常处理很鸡肋，也因此异常处理对我来说是真空的。异常信息依赖于**Error指针参数。
转写dart代码后，发现异常处理居然是一种流程控制语句，抛出异常会影响后续代码的执行。异常流程是一个很优雅的错误处理方案，用上了就停不下来。</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（2） 💬（0）<div>对于 generate() 函数，如果本机名获取失败，函数返回什么？这样的返回值是否合理？
返回null-时间戳-8位随机数字字母符号的字符串.
这样返回合理.因为业务允许一定概率的id重复,并且时间戳-8位随机的数字字母重叠的概率本身就很低,所以代码可以满足业务继续执行,至于最终要不要继续执行可以由上层业务程序控制.

对于 getLastFiledOfHostName() 函数，是否应该将 UnknownHostException 异常在函数内部吞掉（try-catch 并打印日志）？还是应该将异常继续往上抛出？如果往上抛出的话，是直接把 UnknownHostException 异常原封不动地抛出，还是封装成新的异常抛出？
不应该内部吞掉异常,应该直接把异常原封不动地抛出.因为当前是非业务工具类,异常处理该要交由业务程序来处理.

对于 getLastSubstrSplittedByDot(String hostName) 函数，如果 hostName 为 NULL 或者是空字符串，这个函数应该返回什么？
hostName为NULL会抛出空指针异常,这时该要抛出异常由业务程序来处理;hostName为空字符串属于正常业务可以返回空字符串.

对于 generateRandomAlphameric(int length) 函数，如果 length 小于 0 或者等于 0，这个函数应该返回什么？
length小于0时会抛出异常,这时也该要抛出异常由业务程序处理;length等于0时也是正常业务可以返回空字符串.</div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（2） 💬（0）<div>从团队的实践来看，异常统一只靠人为约定是比较难实行的，团队成员理解不一样，实际写代码时候各种原因不按约定来。通过插件，或者IDE自动监测的手段会比较好，比如sonar。</div>2020-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（1） 💬（0）<div>设计模式_36:
# 作业
  1. 返回了null，不合理
  2. 直接re-throw
  3. 应该返回NULL值
  4. 抛出一个自定义的异常

# 感想
  异常这种机制的设计，是为了更好地处理真实的异常情况，要合理地使用，不要为了怕麻烦就乱用，制造出一个个排查问题的灾难。</div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>看业务需求吧，如果是唯一性可以返回一个特殊值。如果后续需要通过id获取主机编号等，就要抛异常</div>2020-02-03</li><br/><li><img src="" width="30px"><span>阳光</span> 👍（1） 💬（0）<div>打卡</div>2020-01-24</li><br/><li><img src="" width="30px"><span>Geek_44ce9a</span> 👍（0） 💬（0）<div>typo：getLastFiledOfHostName()</div>2025-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2c/c6/416bd86e.jpg" width="30px"><span>阿杰</span> 👍（0） 💬（0）<div>1、函数返回null-时间戳-随机码，我认为是对于日志打印的场景来说，是合理的。对于日志标识的场景，调用者关注的重点是标识唯一，而不是标识的格式。
2、获取hostname的最后一位是否异常，调用者并不关心，try catch后打印日志即可。
​3、应该返回空值。
​4、应该抛出异常。</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fd/86/3610ac9c.jpg" width="30px"><span>BKA</span> 👍（0） 💬（0）<div>问题2如果抛出了异常，2和3问题基本能避免，问题1应该返回空字符串或者特殊值</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ed/12/fd8155f5.jpg" width="30px"><span>MasterNeverDown</span> 👍（0） 💬（0）<div>错误码
null
空值 例如 空串 0 空集合
异常 受检异常，非受检异常
</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fc/55/e03bb6db.jpg" width="30px"><span>i-neojos</span> 👍（0） 💬（0）<div>代码风格统一最重要</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（0） 💬（0）<div>返回null 不太影响 目前没有更好的策略替换 空hostname  如果随意替换其他东西会造成迷惑
捕获住，打印error 日志 然后往上返回一个空字符串
空字符
空字符</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6f/c8/4183a146.jpg" width="30px"><span>大头</span> 👍（0） 💬（0）<div>学习了</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/bb/3b/6e020a32.jpg" width="30px"><span>多学多看多记</span> 👍（0） 💬（0）<div>回答问题：
2. getLastFiledOfHostName函数是最底层的函数，出现错误应该返回对应error，由上层函数决定是否处理。
3. getLastSubstrSplittedByDot函数相当于中间函数，要做好对入参异常值的处理，当hostName为null时返回空字符串
4. generateRandomAlphameric等同于getLastSubstrSplittedByDot函数，返回空字符串
1. generate最为最顶层的函数，同时又是非业务代码，不需要关心底层逻辑，开箱即用，有错误也不要上抛，返回默认的错误值即可。内部打好日志，方便以后debug
</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8d/5b/383a49e4.jpg" width="30px"><span>charmsongo</span> 👍（0） 💬（0）<div>1、返回错误码
2、返回 NULL 值。但是需要每次对NULL做处理
3、返回空对象。可以避免每次都做空处理
4、抛出异常对象
	上游方法直接吞掉。异常可以恢复，且不关心，可以直接吞掉
	上游直接向上抛。可以理解，且业务有相关性，可以 继续向上抛
	上游包装成新的异常抛出。异常太底层，缺乏背景理解且业务不相关，包装后向上抛</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（0） 💬（0）<div>还是没理解受检异常，如何识别出受检异常? 在函数定义后面加了 throw xxxException 的就是受检异常吗？</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/88/64/39501fbe.jpg" width="30px"><span>Ricky Gu</span> 👍（0） 💬（0）<div>最终异常要么吞掉，要么程序崩掉</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1c/a4/202dde43.jpg" width="30px"><span>猴精鸭</span> 👍（0） 💬（1）<div>我觉得go的思路就很好，统一使用错误处理，结合多返回值得特性，比较好用。如果是可恢复的错误就选择内部处理或者返回错误，错误中可带有错误码，错误信息和堆栈信息，如果认为这样的错误是不可恢复的直接panic，让程序退出</div>2021-02-06</li><br/>
</ul>