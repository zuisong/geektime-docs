Word这种文本编辑器你平时应该经常用吧，那你有没有留意过它的拼写检查功能呢？一旦我们在Word里输入一个错误的英文单词，它就会用标红的方式提示“拼写错误”。**Word的这个单词拼写检查功能，虽然很小但却非常实用。你有没有想过，这个功能是如何实现的呢？**

其实啊，一点儿都不难。只要你学完今天的内容，**散列表**（Hash Table）。你就能像微软Office的工程师一样，轻松实现这个功能。

## 散列思想

散列表的英文叫“Hash Table”，我们平时也叫它“哈希表”或者“Hash表”，你一定也经常听过它，我在前面的文章里，也不止一次提到过，但是你是不是真的理解这种数据结构呢？

**散列表用的是数组支持按照下标随机访问数据的特性，所以散列表其实就是数组的一种扩展，由数组演化而来。可以说，如果没有数组，就没有散列表。**

我用一个例子来解释一下。假如我们有89名选手参加学校运动会。为了方便记录成绩，每个选手胸前都会贴上自己的参赛号码。这89名选手的编号依次是1到89。现在我们希望编程实现这样一个功能，通过编号快速找到对应的选手信息。你会怎么做呢？

我们可以把这89名选手的信息放在数组里。编号为1的选手，我们放到数组中下标为1的位置；编号为2的选手，我们放到数组中下标为2的位置。以此类推，编号为k的选手放到数组中下标为k的位置。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（1689） 💬（118）<div>
1. 假设我们有 10 万条 URL 访问日志，如何按照访问次数给 URL 排序？

遍历 10 万条数据，以 URL 为 key，访问次数为 value，存入散列表，同时记录下访问次数的最大值 K，时间复杂度 O(N)。

如果 K 不是很大，可以使用桶排序，时间复杂度 O(N)。如果 K 非常大（比如大于 10 万），就使用快速排序，复杂度 O(NlogN)。

2. 有两个字符串数组，每个数组大约有 10 万条字符串，如何快速找出两个数组中相同的字符串？

以第一个字符串数组构建散列表，key 为字符串，value 为出现次数。再遍历第二个字符串数组，以字符串为 key 在散列表中查找，如果 value 大于零，说明存在相同字符串。时间复杂度 O(N)。</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/b7/e59c22f0.jpg" width="30px"><span>黄金的太阳</span> 👍（43） 💬（13）<div>请教老师，当我在查找元素时候，在相同散列值的链表中遍历如何区分哪个是我要找的元素？毕竟查找时查询条件只包含KEY的信息吧</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/0c/b9eafe83.jpg" width="30px"><span>王荣慧</span> 👍（35） 💬（4）<div>有个疑问，如果在冲突的位置的下一个空闲位置存储数据，文中提到，根据key算出的位置存储的值和要查询的数据进行对比，确定是否是要查询的数据，如果我已经知道了要查询的数据，应该就不用查询了吧，这个地方不大理解。</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/6b/f31d4538.jpg" width="30px"><span>这么写的闫</span> 👍（32） 💬（3）<div>当散列冲突，表中存储了多个相同散列值时，查询数据怎么确定查询到的是我想要的那个？
这一点很疑惑，求指点</div>2018-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/71/cc94469a.jpg" width="30px"><span>吴彪</span> 👍（12） 💬（2）<div>为什么数组的存储空间有限，也会加大散列冲突的概率呢？hash函数得出来的散列值相同的概率应该是很低的，比如git hash-object，几乎不可能有碰撞，为啥在散列表里碰撞的可能性就这么大</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/a7/6a837523.jpg" width="30px"><span>之城</span> 👍（11） 💬（1）<div>既然说散列表使用了数组的随机访问的优势，那么它如何保证hash函数计算后的hash值集中地位于内存中的一块连续区域，而不是七零八落散落在内存各处呢？对，我问的就是散列函数是怎么回事。😄</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/89/32e3f682.jpg" width="30px"><span>肖小强</span> 👍（9） 💬（2）<div>老师，关于置顶的那个回答有些疑问。
比如第一题的解答说到“url为key，出现次数为value”
我的疑问是，hash(key)=VALUE，这个VALUE经过处理后不应该是一个随机的数组的下标吗？然后把出现次数value存入到这个位置中并不断更新。我对上面那句话的理解是hash(url)=value，所以为什么可以把出现次数作为value，value不应该是一个随机值吗？还是这个value本来就不是那个VALUE？</div>2018-11-04</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIaOAxRlZjFkGfRBn420LuAcyWkMrpq5iafGdqthX5icJPjql0ibZOAdafaqbfvw4ZpVzDmsaYglVXDw/132" width="30px"><span>唐朝农民</span> 👍（9） 💬（1）<div>Word 单词验证 是不是用 Trie 树更好，大神讲讲这个数据结构，尤其是编码这块</div>2018-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（7） 💬（2）<div>没有理解为什么散列冲突产生的具体原因是什么，所以后面讲到为何空闲位置减少发生散列冲突的几率就增加了，这块有点疑惑。</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/52/677d9d1a.jpg" width="30px"><span>Gavin黄炯鹏</span> 👍（3） 💬（1）<div>开放寻址法查找那里，我希望通过key得到y的值，我都不知道y是多少，只有key，所以与y比较的究竟是什么？</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（3） 💬（2）<div>老师   二次探测      步长增长的太快了  遍历的时候岂不是会经常的漏掉要查找的元素？</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/cb/94/eedbace3.jpg" width="30px"><span>ILoveKindness</span> 👍（2） 💬（1）<div>老师您好，我不是很理解如何对散列表进行排序，如果散列表中的顺序发生改变，不就无法根据key找到相应的数据了嘛，请求老师解答</div>2019-06-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FiaxAZEdIq4SJNBSYXWeo4sKVTDSdFY81xvLtrzldzcFuaZenzD0lVuVHQWBwfp9kQPMaaAz3k1UkDqCyb8tqgg/132" width="30px"><span>pefami</span> 👍（2） 💬（1）<div>“我们通过散列函数求出要查找元素的键值对应的散列值，然后比较数组中下标为散列值的元素和要查找的元素是否相等，若相等，则说明就是我们要查找的元素”
你好，这里是怎么去判断两个元素是相等的呢，查找一般我们是通过Key去找值，如果Key1!=Key2,而Hash(Key1)=Hash(Key2),是不是需要在散列值的位置同时保存Key和Value呢，不能只存储Value值
</div>2019-04-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJicwphCoQ0S1DaibWNarUJq3DrGOeADY02AreVbKCLkm0PWJmZR0f1rMrrXDRzOwLCmIQbqeibQ4uHQ/132" width="30px"><span>樱桃子77</span> 👍（2） 💬（1）<div>请教第一个问题：如果用访问次数为key， URＬ为value 并记下最大访问次数K 然后遍历哈希表就行了。这样行吗？</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/01/cc4d66ea.jpg" width="30px"><span>马小平</span> 👍（2） 💬（2）<div>请教老师，当我在查找元素时候，在相同散列值的链表中遍历如何区分哪个是我要找的元素？毕竟查找时查询条件只包含KEY的信息吧

这个问题我看您回答过了今天，但是我还是没懂怎么对比Key </div>2018-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/7e/b5b59ae4.jpg" width="30px"><span>上善若水（德水）</span> 👍（2） 💬（1）<div>word估计不太会用这种存储来检查，因为他还要给建议autosuggestion?

散列冲突后，这种存储后，查找的时候如何知道要查找的位置就一定是我要找的那个？</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/05/88/0a1f1b1d.jpg" width="30px"><span>linus</span> 👍（1） 💬（5）<div>能详细讲解下为什么要有deleted标识吗？删都删了，加个deleted标识，这个坑以后就不用了吗？文中的表述方式实在没看懂</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/aa/f53a6800.jpg" width="30px"><span>Dong</span> 👍（1） 💬（1）<div>采用链地址法的哈希表的平均时间复杂度是O(1)吗？如果是，那是怎么算的呀。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ef/3c/83859355.jpg" width="30px"><span>悦仙子的小跟班</span> 👍（1） 💬（2）<div>有个地方有个疑问，原文描述是：我们通过散列函数求出要查找元素的键值对应的散列值，然后比较数组中下标为散列值的元素和要查找的元素是否相等，若相等，则说明就是我们要查找的元素；否则，就顺序往后依次查找。如果遍历到数组的空闲位置还未找到，就说明要查找的元素并没有在散列表中。
其中 比较数组中下标为散列值的元素和要查找的元素是否相等，这个是怎么做到的呢？我不就是要找这个值吗？我怎么会知道这个值的呢？</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（1） 💬（1）<div>老师您好，有个问题，就是关于散列冲突里面，讲到删除元素，则标记为deleted，那么这个删除的空间是否一直没空出来？这样不就导致，整个数组的本来要删除的数据，没有真正让出空间，导致有效数据很小，垃圾数据很多，这样怎么解决？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1e/c5/4e640126.jpg" width="30px"><span>momo</span> 👍（0） 💬（1）<div>那啥，写n的幂次，不妨加个尖角符号，看的更清楚</div>2019-10-28</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/jqDSNBHmPbPGayjtXrm9iciccSKbfg6g8oMgXc147jib4HjoUK1RINorZYfBuiaQBibqJIrQRVG77PKGS0dW5PVAAicw/132" width="30px"><span>huangzehao</span> 👍（0） 💬（1）<div>老师，你好，有个问题想请教一下你：

双重散列可以通过多个散列函数hash1(key)，hash2(key)，hash3(key)……可以获取到空闲的存储位置并插入数据，但是查找数据要如何查找呢？如何判断是通过哪个hash函数找到目标数据是否存在呢？假设我是通过hash3函数插入数据的，但是我查找的时候是依据hash1(key)，hash2(key)，hash3(key)…… 里面的哪个函数为准呢？
</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（3）<div>开放地址法在删除元素的时候标记deleted，如果一直不释放这个deleted空间是不是很浪费内存啊
</div>2019-08-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（0） 💬（1）<div>散列函数中的数组下标和散列值有啥区别呢</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（2）<div>老师，二次探测和双重探测由于可能由于散列冲突的原因，在经过多次探测才找到了空闲位置插入数据，那么想删除刚才这个数据，要怎么根据二次探测和双重探测来确定位置呢？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>同问:
1. 关于开放空间的散列冲突：既然存在散列冲突问题，插入时可以通过分配新的 key 来插入存在散列冲突的元素，那么在访问时又是如何解决散列冲突的呢？比如有两个键值对 {key1: val1}, {key2: val2} 它们的 key 在生成时是冲突的，key2 经过重新分配，现在访问 {key2: val2} 时应该如何通过hash函数得到正确的 key2 呢？假如删除 {key1: val1}，现在要访问 {key2: val2} ，那么执行 hash(string) 后得到的 key1 并不存在，应该怎么实现对 {key2: val2} 的正确访问呢？</div>2019-06-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDY9bVLK3oyLmF6X2OnUZAzwSNVpS7XPxOQg84XJdvhr6SfvPe5uhYvzSf8ycIokfiapAJ8lvPxHA/132" width="30px"><span>goodxwp</span> 👍（0） 💬（1）<div>请教下老师，文中的英文单词例子，原理都比较简单，但是请问这个例子的hash函数怎么设计呢？你在文中计算内存的时候，默认是hash函数计算出来的数组下标是连续的，求教怎么做到连续</div>2019-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRyUPicEMqGsbsMicHPuvwM8nibfgK8Yt0AibAGUmnic7rLF4zUZ4dBj4ialYz54fOD6sURKwuJIWBNjhg/132" width="30px"><span>咸鱼与果汁</span> 👍（0） 💬（1）<div>请问如果二次探测也冲突了，但是当前装载因子还没超过设定值会怎么做，会扩容吗？</div>2019-05-26</li><br/><li><img src="" width="30px"><span>请叫我红领巾</span> 👍（0） 💬（1）<div>假如十万条不能同时在内存中处理，能有什么好办法吗？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（0） 💬（1）<div>对于置顶的方案，有个小问题： 对hashmap的value做排序，完成后，怎么对应得到排序的Key？

1. 假设我们有 10 万条 URL 访问日志，如何按照访问次数给 URL 排序？

遍历 10 万条数据，以 URL 为 key，访问次数为 value，存入散列表，同时记录下访问次数的最大值 K，时间复杂度 O(N)。

如果 K 不是很大，可以使用桶排序，时间复杂度 O(N)。如果 K 非常大（比如大于 10 万），就使用快速排序，复杂度 O(NlogN)。
</div>2019-05-09</li><br/>
</ul>