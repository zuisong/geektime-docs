你好，我是蒋德钧。这节课，我们继续从底层数据结构的视角出发，来聊聊Redis中的Stream数据类型是如何保存消息的。

Redis从5.0版本开始支持提供Stream数据类型，它可以用来保存消息数据，进而能帮助我们实现一个带有消息读写基本功能的消息队列，并用于日常的分布式程序通信当中。我在讲[如何使用Redis实现消息队列](https://time.geekbang.org/column/article/284291)的时候，曾介绍过Stream。当时，有不少同学就说想学习了解下Stream的实现，以便掌握Stream内部结构的操作特点，但自己对Stream类型不太熟悉，不知道Stream底层是采用怎样的数据结构来保存消息数据的。

其实，为了节省内存空间，在Stream数据类型的底层数据结构中，采用了**Radix Tree和listpack**两种数据结构来保存消息。我在[第6讲](https://time.geekbang.org/column/article/405387)已经给你介绍过了listpack，它是一个紧凑型列表，在保存数据时会非常节省内存。

所以今天这节课，我就来给你介绍下Stream用到的另一个数据结构Radix Tree。这个数据结构的**最大特点是适合保存具有相同前缀的数据**，从而实现节省内存空间的目标，以及支持范围查询。

同时，和常见的B树或B+树类似，Radix Tree也是一种重要的树型结构，在操作系统内核和数据库中也有应用。所以，了解Radix Tree的设计与实现，既可以帮助我们掌握Stream的实现思路，还可以让我们把Radix Tree应用到需要节省内存的有序树型索引场景中，进一步解决具有公共前缀的大量数据保存时的内存开销问题。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（25） 💬（3）<div>作为有序索引，Radix Tree 也能提供范围查询，和我们日常使用的 B+ 树，以及第5讲中介绍的跳表相比，你觉得 Radix Tree 有什么优势和不足么？

1、Radix Tree 优势

- 本质上是前缀树，所以存储有「公共前缀」的数据时，比 B+ 树、跳表节省内存
- 没有公共前缀的数据项，压缩存储，value 用 listpack 存储，也可以节省内存
- 查询复杂度是 O(K)，只与「目标长度」有关，与总数据量无关
- 这种数据结构也经常用在搜索引擎提示、文字自动补全等场景

Stream 在存消息时，推荐使用默认自动生成的「时间戳+序号」作为消息 ID，不建议自己指定消息 ID，这样才能发挥 Radix Tree 公共前缀的优势。

2、Radix Tree 不足

- 如果数据集公共前缀较少，会导致内存占用多
- 增删节点需要处理其它节点的「分裂、合并」，跳表只需调整前后指针即可
- B+ 树、跳表范围查询友好，直接遍历链表即可，Radix Tree 需遍历树结构
- 实现难度高比 B+ 树、跳表复杂

每种数据结构都是在面对不同问题场景下，才被设计出来的，结合各自场景中的数据特点，使用优势最大的数据结构才是正解。</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（9） 💬（3）<div>在阅读的时候其实已经有想到Radix Tree，B+树 和跳表之间的区别，没想到老师文章最后刚好提到这个问题，那我就站在我个人理解的角度回到一下我的想法，问题是：【Radix Tree，B+ 和跳跃表之间的区别】

【我分为以下几个问题自问自答带出我的想法和思考的角度】

问题一：B+树和跳跃表有什么关联？
	答： 
		1、B+树和跳跃表这两种数据结构在本身设计上是有亲缘关系的，其实如果把B+树拉直来看不难发现其结构和跳跃表很相似，甚至B+树的父亲结点其实类似跳跃表的level层级。
		2、在当前计算机硬件存储设计上，B+树能比跳表存储更大量级的数据，因为跳表需要通过增加层高来提高索引效率，而B+树只需要增加树的深度。此外B+树同一叶子的连续性更加符合当代计算机的存储结构。然而跳表的层高具有随机性，当层高较大的时候磁盘插入会带来一定的开销，且不利于分块。

问题二：那么为什么Redis不使用B+树呢而选择跳表呢？
	答：因为数据有序性的实现B+树不如跳表，跳表的时间性能是优于B+树的（B+树不是二叉树，二分的效率是比较高的）。此外跳表最低层就是一条链表，对于需要实现范围查询的功能是比较有利的，而且Redis是基于内存设计的，无需考虑海量数据的场景。

问题三：Radix Tree优势在哪？
	答：
		1、当存储大量key字符串很长的时候跳表不如前缀树，甚至不利于实现这种场景，因为跳表层高有最大限制，此外跳表不能很好的标识key的字符串顺序，不像前缀树可以从根目录下路就是字符顺序。
		2、在内存环境下，前缀树是二叉树，而B+树不是，这样一来当对于key的索引效果来说，前缀树会比B+树索引效果更好（类比：新华字典目录越丰富，通过目录快速定位到目标字的概率更高）。

问题四：Radix Tree劣势在哪？
	答：
		1、Radix Tree能保证在索引key的前缀顺序，但是在保证数据顺序且连续性上不如跳表。
		2、查询性能上存在欠缺，虽然是二叉树但是当访问一个key的时候每次都需要依次访问前缀字符，不如hash表对整个key的直接索引。
		3、不适合存储像UUID等，非对称结构的key（而且使用时候建议让Redis自动生成）。</div>2021-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（3） 💬（4）<div>最后一个图有点懵。listpack那里不应该画listpack内存结构么？然后listpack的master entry放key，后面的entry放value。我怎么感觉又是一个raxNode。</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（2） 💬（0）<div>一方面，Radix Tree 非叶子节点，要不然是压缩节点，只指向单个子节点，要不然是非压缩节点，指向多个子节点，但每个子节点只表示一个字符。所以，非叶子节点无法同时指向表示单个字符的子节点和表示合并字符串的子节点。
这句话如何得到的结论，看了几遍没看明白因果关系。</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fa/51/5da91010.jpg" width="30px"><span>Miroticwillbeforever</span> 👍（1） 💬（1）<div>这一篇文章讲的很透彻！！！
第一次看就被惊艳到了。。好东西！</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8a/7e/bfe37c46.jpg" width="30px"><span>飞鱼</span> 👍（0） 💬（0）<div>
“它们本身就已经包含了子节点代表的字符或合并字符串。而对于它们的子节点来说，也都属于非压缩或压缩节点，所以，子节点本身又会保存，子节点的子节点所代表的字符或合并字符串。 ” 这句有点绕，我想知道的是，压缩节点d ,那幅图片里面，本身的d字符串是存储在那里？是在HDR 中所谓的合并字符串里面吗 ？相当于d不单独存储，而是在合并字符串里面 ？</div>2024-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/0a/9b2126ac.jpg" width="30px"><span>anqi</span> 👍（0） 💬（0）<div>stream value中存的是 dict, 类似于field1:value1  field2:value2
因为field基本都一样,所以可以开启压缩:  分别存储field和value

存field:   id1:field1  id2: field2 id3:field3
存value:    id2:value2, 利用id去简化field的存储. (一个int类型肯定比字符串的field要小很多,这个int值不大,还在listpack中压缩存储,占用空间很小)
甚至如果开启 认为所有消息的field一样, 那么存value的时候,还可以省略id, 按照类似于数组的方式存value.其index即为field的id.
https:&#47;&#47;github.com&#47;zpoint&#47;Redis-Internals&#47;blob&#47;5.0&#47;Object&#47;streams&#47;streams.md</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（0） 💬（0）<div>可以维持插入有序 因为我最近在搞内存数据库 再用两个指针维护所有的key 这样就是插入有序了</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/52/b96c272d.jpg" width="30px"><span>🤐</span> 👍（0） 💬（1）<div>看到最后发现不能排序 有点失望 </div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/46/42/eaa0cc92.jpg" width="30px"><span>无风</span> 👍（0） 💬（4）<div>为什么每个raxNode要存子节点的字符呢？为什么不能自己存自己？</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（3）<div>这个课的内容之前不太了解，得多看几遍才能理解，我太菜了。。。</div>2021-08-10</li><br/>
</ul>