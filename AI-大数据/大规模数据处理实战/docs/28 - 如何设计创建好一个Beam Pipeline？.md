你好，我是蔡元楠。

今天我要与你分享的主题是“如何设计创建好一个Beam Pipeline”。

这一讲我们会用到[第7讲](https://time.geekbang.org/column/article/92928)中介绍过的四种常见设计模式——复制模式、过滤模式、分离模式和合并模式。这些设计模式就像是武功的基本套路一样，在实战中无处不在。今天，我们就一起来看看我们怎么用Beam的Pipeline来实现这些设计模式。

## 设计Pipeline的基本考虑因素

在设计Pipeline时，你需要注意4条基本的考虑因素。

### 1.输入数据存储在哪里？

输入数据是存储在云存储文件系统，还是存储在一个关系型数据库里？有多大的数据量？这些都会影响你的pipeline设计是如何读入数据的。上一讲已经讲到过，Pipeline的数据读入是使用Read这个特殊的Transform。而数据读入往往是一个Pipeline的第一个数据操作。

### 2.输入数据是什么格式？

输入数据是纯文本文件？还是读取自关系型数据库的行？还是结构化好的特殊数据结构？这些都会影响你对于PCollection的选择。比如，如果输入数据是自带key/value的结构，那你用Beam的key/value为元素的PCollection能更好的表示数据。

### 3.这个pipeline你打算对数据进行哪些操作？
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（4） 💬（2）<div>Beam Pipeline的合并模式是否支持keyed join，inner&#47;left outer&#47;right outer&#47;full outer都支持吗? 看上面的代码示例虽然是叫Joiner Pattern，实际效果却是Union。分离模式倒是跟flink的split&#47;select算子组合很类似。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/99/cc30e2ca.jpg" width="30px"><span>人唯优</span> 👍（3） 💬（1）<div>平台的自然语言理解（NLP）的数据处理模块可以分析视频数据，自动生成视频字幕。
感觉这里不是很严谨，字幕这块应该是OCR+ASR为主吧</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/21/eb/bb2e7a3b.jpg" width="30px"><span>Ming</span> 👍（2） 💬（2）<div>我也有个小问题：在实践中一个集群往往同一时间只能执行一个pipeline吗？假如一个产品需要用到文中的全部四个例子，两个流处理两个批处理，实践中往往是有四个集群，还是一个集群？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（1） 💬（3）<div>老师你好，我问一个大数据相关的问题呢，在大数据处理场景中有没有什么好的CDC方案额。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f9/20/3dc898af.jpg" width="30px"><span>闫少伟</span> 👍（1） 💬（0）<div>PCollection userCollection = ...;
PCollection diamondUserCollection = userCollection.apply(&quot;filterDiamondUserTransform&quot;, ParDo.of(new DoFn(){ @ProcessElement public void processElement(ProcessContext c) { if (isDiamondUser(c.element()) { c.output(c.element()); } }}));
PCollection notifiedUserCollection = userCollection.apply(&quot;notifyUserTransform&quot;, ParDo.of(new DoFn(){ @ProcessElement public void processElement(ProcessContext c) { if (notifyUser(c.element()) { c.output(c.element()); } }}));
这里notifiedUserCollection ，是不是要用diamondUserCollection.apply呀？</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/9c/abb7bfe3.jpg" width="30px"><span>abc-web</span> 👍（1） 💬（0）<div>老师，你的课程是否有实际的实例代码，这样学习效果会更好些；</div>2019-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（1） 💬（0）<div>老师，有几个问题不解。在复制或者分离模式下，每个处理和输出是不同步的吧，如果业务上对不同输出有同步要求时，怎么办？复制或者分离模式和组合模式进行组合时，上一步的输出不同步或者延迟较大会加大后续组合时数据业务时间乱序问题（特别是流处理）这时有解决办法吗或者其它思路</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f1/25/6908f80a.jpg" width="30px"><span>juan</span> 👍（0） 💬（0）<div>
          @ProcessElement
          public void processElement(ProcessContext c) {
            if (isFiveStartMember(c.element())) {
              c.output(c.element());  &#47;&#47; 忘了 starmemember ???c.output(fiveStartMemberTag,c.element());
            } else if (isGoldenMember(c.element())) {
              c.output(goldenMembershipTag, c.element());
            } else if (isDiamondMember(c.element())) {
	  c.output(diamondMembershipTag, c.element());
	}
          }
        })


</div>2019-07-03</li><br/>
</ul>