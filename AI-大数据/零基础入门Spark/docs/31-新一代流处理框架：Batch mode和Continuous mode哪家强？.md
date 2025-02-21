你好，我是吴磊。

在上一讲，我们通过“流动的Word Count”示例，初步结识了Structured Streaming，并学习了流处理开发三要素，也就是Source、流处理引擎与Sink。

![图片](https://static001.geekbang.org/resource/image/35/5a/35cd34dfa43a3a9c52f538e002e5905a.jpg?wh=1920x562)

今天这一讲，让我们把目光集中到Structured Streaming，也就是流处理引擎本身。Structured Streaming与Spark MLlib并列，是Spark重要的子框架之一。值得一提的是，Structured Streaming天然能够享受Spark SQL提供的处理能力与执行性能，同时也能与其他子框架无缝衔接。因此，基于Structured Streaming这个新一代框架开发的流处理应用，天然具备优良的执行性能与良好的扩展性。

知己知彼，百战百胜。想要灵活应对不同的实时计算需求，我们就要先了解Structured Streaming的计算模型长啥样，搞清楚它如何应对容错、保持数据一致性。我们先从计算模型说起。

## 计算模型

当数据像水流一样，源源不断地流进Structured Streaming引擎的时候，引擎并不会自动地依次消费并处理这些数据，它需要一种叫做Trigger的机制，来触发数据在引擎中的计算。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/32/62/d39a638c.jpg" width="30px"><span>刘启涛</span> 👍（5） 💬（1）<div>课后习题: 
我觉得先消费再记录的方式是可以实现，但是如果记录的时候出现异常(hdfs写数据网络抖动)，可能会导致数据重复消费，这种方式“Exactly Once”的准确性没有先记录、再消费数据高。
老师，我这里还有一个问题，Continuous mode是处理完数据异步记录日志，感觉很难保证“刚好一次”</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/92/201da8a7.jpg" width="30px"><span>六月的余晖</span> 👍（2） 💬（1）<div>老师，可以比较一下Continuous mode和Flink 吗</div>2021-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（0） 💬（1）<div>老师，后面课程没有spark streaming内容的讲解吗</div>2021-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（0） 💬（1）<div>老师，虽然kafka幂等性不能保证跨分区的原子写入，但是kafka还支持事务呀</div>2021-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（0） 💬（2）<div>老师，0.11版本后的kafka，引入了幂等性机制呀，文中问什么说kafka不是幂等的呢</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9a/63dc81a2.jpg" width="30px"><span>Geek1185</span> 👍（0） 💬（1）<div>为什么batch mode的WAL不做成异步的形式呢？</div>2023-02-06</li><br/>
</ul>