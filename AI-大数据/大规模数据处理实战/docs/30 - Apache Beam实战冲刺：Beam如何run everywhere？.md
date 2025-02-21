你好，我是蔡元楠。

今天我要与你分享的主题是“Apache Beam实战冲刺：Beam如何run everywhere”。

你可能已经注意到，自第26讲到第29讲，从Pipeline的输入输出，到Pipeline的设计，再到Pipeline的测试，Beam Pipeline的概念一直贯穿着文章脉络。那么这一讲，我们一起来看看一个完整的Beam Pipeline究竟是如何编写的。

## Beam Pipeline

一个Pipeline，或者说是一个数据处理任务，基本上都会包含以下三个步骤：

1. 读取输入数据到PCollection。
2. 对读进来的PCollection做某些操作（也就是Transform），得到另一个PCollection。
3. 输出你的结果PCollection。

这么说，看起来很简单，但你可能会有些迷惑：这些步骤具体该怎么做呢？其实这些步骤具体到Pipeline的实际编程中，就会包含以下这些代码模块：

Java

```
// Start by defining the options for the pipeline.
PipelineOptions options = PipelineOptionsFactory.create();

// Then create the pipeline.
Pipeline pipeline = Pipeline.create(options);

PCollection<String> lines = pipeline.apply(
  "ReadLines", TextIO.read().from("gs://some/inputData.txt"));

PCollection<String> filteredLines = lines.apply(new FilterLines());

filteredLines.apply("WriteMyFile", TextIO.write().to("gs://some/outputData.txt"));

pipeline.run().waitUntilFinish();
```

从上面的代码例子中你可以看到，第一行和第二行代码是创建Pipeline实例。任何一个Beam程序都需要先创建一个Pipeline的实例。Pipeline实例就是用来表达Pipeline类型的对象。这里你需要注意，一个二进制程序可以动态包含多个Pipeline实例。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDhZkQGEnzjnu3dibxbRiblWIUjXXrXic0MStUS2ApKt5WiaoxV3IVhAtSXkknODA9oibick3NHic4Frzfw/0" width="30px"><span>suncar</span> 👍（11） 💬（1）<div>请问一下老师，可不可提供几个获取大量测试数据的网止。谢谢</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（5） 💬（6）<div>想问下读者中多少人用beam在生产环境…</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8a/1b/1af2abcf.jpg" width="30px"><span>hugo</span> 👍（1） 💬（0）<div>runner是如何在多平台，多语言间实现兼容的？像flink，go runner会在本地调用java runner吗</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/07/7f821042.jpg" width="30px"><span>David</span> 👍（1） 💬（0）<div>请教一下，GCP上同时有Composer&#47;Airflow和Dataflow&#47;Beam两种可以用来完成ETL工作的产品。
是否可以讲一下两者的比较，和在技术上如何进行选型？
谢谢！</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/3c/47d70fdc.jpg" width="30px"><span>ditiki</span> 👍（0） 💬（0）<div>请教两个production遇到的问题.

In a beam pipeline (dataflow), one step is to send http request to schema registry to validate event schema. A groupby event type before this step and static cache are used to reduce calls to schema registry. How does beam (or the underline runner) optimise IO ? Is it a good practice to use a thread pool for asynchronous http calls ? 

The event object has a Json (json4s library) payload, each time we try to update the Dataflow pipeline, we get the error says that the Kryo coder generated for the JSON has changed, such that the current pipeline can’t be updated in place. We did a work a round by serialise the Json payload to string in a custom coder, which should be very inefficient. Have you ever seen this before ? Does Kryo generate a different coder at each compile time ? 

多谢啦！</div>2019-07-03</li><br/>
</ul>