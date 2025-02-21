在Hadoop问世之前，其实已经有了分布式计算，只是那个时候的分布式计算都是专用的系统，只能专门处理某一类计算，比如进行大规模数据的排序。很显然，这样的系统无法复用到其他的大数据计算场景，每一种应用都需要开发与维护专门的系统。而Hadoop MapReduce的出现，使得大数据计算通用编程成为可能。我们只要遵循MapReduce编程模型编写业务处理逻辑代码，就可以运行在Hadoop分布式集群上，无需关心分布式计算是如何完成的。也就是说，我们只需要关心业务逻辑，不用关心系统调用与运行环境，这和我们目前的主流开发方式是一致的。

请你先回忆一下，在前面[专栏第4期](http://time.geekbang.org/column/article/65106)我们讨论过，大数据计算的核心思路是移动计算比移动数据更划算。既然计算方法跟传统计算方法不一样，移动计算而不是移动数据，那么用传统的编程模型进行大数据计算就会遇到很多困难，因此Hadoop大数据计算使用了一种叫作MapReduce的编程模型。

其实MapReduce编程模型并不是Hadoop原创，甚至也不是Google原创，但是Google和Hadoop创造性地将MapReduce编程模型用到大数据计算上，立刻产生了神奇的效果，看似复杂的各种各样的机器学习、数据挖掘、SQL处理等大数据计算变得简单清晰起来。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/b0/30007f3c.jpg" width="30px"><span>大数据技术与数仓</span> 👍（35） 💬（2）<div>package com.company.sparkcore

import org.apache.log4j.{Level, Logger}
import org.apache.spark.{SparkConf, SparkContext}

object CountPVByGroup {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName(CountPVByGroup.getClass.getSimpleName)
      .setMaster(&quot;local&quot;)
    Logger.getLogger(&quot;org.apache.spark&quot;).setLevel(Level.OFF)
    Logger.getLogger(&quot;org.apache.hadoop&quot;).setLevel(Level.OFF)
    val sc = new SparkContext(conf)
    val lines = sc.textFile(&quot;file:&#47;&#47;&#47;e:&#47;pv_users.txt&quot;)
    &#47;&#47;拼接成（1_25,1）的形式
    val newKeyValue =  lines.map(_.split(&quot;,&quot;)).map(pvdata =&gt; ((pvdata(0)+ &quot;_&quot; + pvdata(1)),1))
   &#47;&#47;对上述KV进行统计
    val pvcount = newKeyValue.reduceByKey(_ + _)
    &#47;&#47;将拼接符号去掉，组合成形如(1,25,1)的形式
    val pvid_age_count = pvcount.map(newkv =&gt; (newkv._1.split(&quot;_&quot;)(0),newkv._1.split(&quot;_&quot;)(1),newkv._2))
    &#47;&#47;结果输出
&#47;&#47;    (1,25,1)
&#47;&#47;    (2,25,2)
&#47;&#47;    (1,32,1)
    pvid_age_count.collect().foreach(println)
  }

}</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/cf/7bec93d8.jpg" width="30px"><span>朱国伟</span> 👍（29） 💬（1）<div>单机安装伪hadoop集群
见：https:&#47;&#47;hadoop.apache.org&#47;docs&#47;stable&#47;hadoop-project-dist&#47;hadoop-common&#47;SingleCluster.html
注：在Mac中安装遇到了一些问题 但是google一下就能解决 恕不一一道来

思考题解答步骤
cat pv_users
1,25
2,25
1,32
2,25

# 导入该文件到dfs中
bin&#47;hdfs dfs -put pv_users pv_users

# 因为每一行只有pageid, age并且中间没有空格 可以直接利用hadoop自带的wordcount程序
# 读取dfs中的pv_user文件 进行统计 然后将结果输出到pv_users_count中
bin&#47;yarn jar share&#47;hadoop&#47;mapreduce&#47;hadoop-mapreduce-examples-2.9.1.jar wordcount pv_users pv_users_count
# 读取统计结果
bin&#47;hdfs dfs -cat pv_users_count&#47;part-r-00000
1,25	1
1,32	1
2,25	2
</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/01/997432f3.jpg" width="30px"><span>喜笑延开</span> 👍（21） 💬（1）<div>不能光想，必须动手实践：
## Mapper
public class PageMapper extends Mapper&lt;LongWritable,Text,Text,IntWritable&gt; {
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String data = value.toString();
        String[] words = data.split(&quot;\n&quot;);
        for (String word : words) {
            context.write(new Text(word), new IntWritable(1));
        }
    }
}
## Reducer
public class PageReducer extends Reducer&lt;Text,IntWritable,Text,IntWritable&gt; {
    @Override
    protected void reduce(Text key, Iterable&lt;IntWritable&gt; values, Context context) throws IOException, InterruptedException {
        int total=0;
        for (IntWritable value : values) {
            total=total+value.get();
        }
        context.write(key, new IntWritable(total));
    }
}
##  Main
public class PageMain {
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        Job job = Job.getInstance();
        job.setJarByClass(PageMain.class);

        job.setMapperClass(PageMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        job.setReducerClass(PageReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.setInputPaths(job,new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.waitForCompletion(true);


    }
}

## 命令行
hadoop jar page-1.0-SNAPSHOT.jar PageMain &#47;input&#47;page  &#47;output5
ps：第一次运行报错了~~（不练不知道）
错误：Initialization of all the collectors failed. Error in last collector was :interface javax.xml.soap.
原因：编写Main的时候，Text的引用import错了，习惯了弹出提示直接确定~应该导入`import org.apache.hadoop.io.Text;`</div>2018-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（18） 💬（3）<div>我想问一下那个计算过程的示意图里map输入部分，上面的是0，12，下面是0，13，是啥意思？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/27/1d/1cb36854.jpg" width="30px"><span>小辉辉</span> 👍（13） 💬（1）<div>java8中的流式框架也用的MapReduce，之前一直没理解用MapReduce的意义何在，今天突然顿悟。
软件中很多思想和设计都是通用的，今天接触一种新东西，明天说不定在其它地方又能碰到，又能加深一遍印象。所以说学得多了，很多时间就可以融会贯通了。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bf/d7/9e2c8648.jpg" width="30px"><span>呆猫</span> 👍（7） 💬（1）<div>文章真的是看的赏心悦目，尤其是那段描述抽象的文字😃</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/b2/1e8b5616.jpg" width="30px"><span>老男孩</span> 👍（5） 💬（1）<div>老师关于抽象是洞察事物本质的总结很精辟。关于思考题，我的思路是把pageid+age作为map函数计算key值，value分别是1。然后reduce再根据key对value的集合进行sum。就可以得出sql的结果。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/18/4b02510f.jpg" width="30px"><span>明天更美好</span> 👍（4） 💬（1）<div>对于大数据来说是盲区，如果应用直接往hbase中写可以吗？2.5万的并发。hbase可以满足我们的查询需求吗？还有日志分析</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/72/5c801d71.jpg" width="30px"><span>牛油果</span> 👍（3） 💬（1）<div>后面一段话，一看就是好人，好老师。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/4f/92118333.jpg" width="30px"><span>Geek_0yda1p</span> 👍（3） 💬（1）<div>为什么相同key的合并是形成&lt;key, value集合&gt;而不是直接形成一个&lt;key,  value reduce后的结果&gt;呢？后者不是效率更高吗？</div>2018-11-14</li><br/><li><img src="" width="30px"><span>极客人</span> 👍（2） 💬（1）<div>老师，文章中的代码是Java语言写的吗，因为我是0基础的，看不懂上面的代码，是否需要去补充基本的语言编程基础？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/a5/df917d18.jpg" width="30px"><span>ward-wolf</span> 👍（2） 💬（1）<div>我的思路和前面几个同学的类似，就是把文本直接当做key，value使用数字统计，最后就是通过reduce统计出现次数了</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/8c/7363897a.jpg" width="30px"><span>万东海</span> 👍（1） 💬（1）<div>思考题的答案就是老师文中的吗? 
把 
1,25
2,25
1,32
2,25
直接当成单词理解</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（1） 💬（1）<div>感觉大数据处理和需要汇总处理结果的多线程有点类似，任务分发到多个线程，并行处理，等到所有线程处理完毕汇总结果再统一处理返回，不知道理解的对不对</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/a3/68/e913d823.jpg" width="30px"><span>*其</span> 👍（0） 💬（1）<div>安装Hadoop的各种组件对硬件配置要求很高吧</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（0） 💬（1）<div>老师，大数据python,java都可以，有没有说哪个语言会更具备优势？</div>2018-11-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJF2gTFBleTUHJtpV4KeyMGdiaycVkrX1JgZJITFfmUa4xWyiapicRF7h0Ur4YI5IdDJ9N43Q6ey8vyA/132" width="30px"><span>亭亭亭</span> 👍（0） 💬（1）<div>如果是non additive的结果，map reduce 怎么计算呢</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/e6/a69cff76.jpg" width="30px"><span>lyshrine</span> 👍（0） 💬（1）<div>老师，看您用的python举例，请问mapduce的编程语言是什么呢，各种语言都行吗？</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/9d/be04b331.jpg" width="30px"><span>落叶飞逝的恋</span> 👍（86） 💬（10）<div>老师，我是个大数据的初学者，因为这个专栏是从零入门的，但是目前的我还不知道如何在自己机器上安装哪些软件？如何操作？因为这些问题没解决，所以没办法真切的体会到文中的处理单词统计大数据的魅力。所以希望老师能讲下必备软件的安装的内容，及操作环节。谢谢</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/89/09/d660509d.jpg" width="30px"><span>intuition</span> 👍（52） 💬（0）<div>李老师的文章已经不仅仅局限于技术本身 更多的是对人生的的思考 如何去成为一个思考者才是我们所追求的目标</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（20） 💬（0）<div>把pageID和age当做key计算出现的次数并做汇总，然后对key排序，输出排序后的key和其对应的总次数</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/c1/d4e6147e.jpg" width="30px"><span>一箭中的</span> 👍（13） 💬（0）<div>将pageid和 age拼接成字符串当做一个key，然后通过Map和Reduce计算即可得出对应的count</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/e1/ee5705a2.jpg" width="30px"><span>Zend</span> 👍（11） 💬（0）<div>--Map输入--
1,25
2,25
1,32
2,25
--Map计算后的结果为Map输出--
&lt;&lt;1,25&gt;,1&gt;
&lt;&lt;2,25&gt;,1&gt;
&lt;&lt;1,32&gt;,1&gt;
&lt;&lt;2,25&gt;,1&gt;
--MapReduce计算框架处理后的结果为Reduce输入--
&lt;&lt;1,25&gt;,&lt;1&gt;&gt;
&lt;&lt;2,25&gt;,&lt;1,1&gt;&gt;
&lt;&lt;1,32&gt;,&lt;1&gt;&gt;
--Reduce计算后的结果为Reduce输出--
&lt;&lt;1,25&gt;,1&gt;
&lt;&lt;2,25&gt;,2&gt;
&lt;&lt;1,32&gt;,1&gt;</div>2019-11-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/vhOPEib27xAuTycN0eQekLzsCe9zwcTTcrOb98cIfpgibgcweZBDN38tIicABibuZBwah9jnGVr02H2Zjuue1fLfEQ/132" width="30px"><span>Ahikaka</span> 👍（10） 💬（1）<div>老师能不能推荐些学大数据的书籍，博客，网站 。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/31/c1ce2abc.jpg" width="30px"><span>糊糊</span> 👍（8） 💬（0）<div>mapreduce核心思想就跟传统的SQL中的group by一样</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（6） 💬（0）<div>看到这个问题，我在想我在怎么想？</div>2018-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eobHCkMA1WJgZZYRfHqXDeIwybVwSxNGFAWWSunYVNLiaKia6q3rVkG7P8tl4ZcNRI7iaxdZhVckroVA/132" width="30px"><span>Lambda</span> 👍（4） 💬（0）<div>好像中间拉下了 shuffle </div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/99/ff/046495bb.jpg" width="30px"><span>小成</span> 👍（3） 💬（0）<div>老师，我是大数据初学者，除了编程语言本身的，可以推荐一些书籍或者资料辅助这个专栏的学习吗，像hadoop相关类的，这期的代码看不懂了。</div>2019-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/9d/bdfd9e58.jpg" width="30px"><span>无处不在</span> 👍（3） 💬（0）<div>这个如果在复杂或者高级一点，就需要用mapreduce的序列化对象作为key的功能去实现了，最近也在学习大数据，学的时候感觉找到了sql的本质，记得公司前年的项目就是手写了一堆js函数，实现了mongodb的类似sql的分组聚合操作。
后续可以开设视频的专栏就更好了</div>2018-11-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eov38ZkwCyNoBdr5drgX0cp2eOGCv7ibkhUIqCvcnFk8FyUIS6K4gHXIXh0fu7TB67jaictdDlic4OwQ/132" width="30px"><span>珠闪闪</span> 👍（2） 💬（0）<div>为智慧老师的文字而激动。让我对工作 学习和生活有了更多的思考。

关注模型，遇见问题努力去抽象。

遇见事情停下来思考一下。这个问题为什么会出现，背后的规律是什么，如何解决这个问题。

当每件事情停下来想一下，就会让自己察觉到以前不曾注意的一些情况，进而发现事物深层的规律，这就是洞察力

</div>2020-09-03</li><br/>
</ul>