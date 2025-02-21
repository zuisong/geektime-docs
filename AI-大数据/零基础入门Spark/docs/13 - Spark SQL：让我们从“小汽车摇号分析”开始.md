你好，我是吴磊。

在开篇词我们提出“入门Spark需要三步走”，到目前为止，我们携手并肩跨越了前面两步，首先恭喜你学到这里！熟练掌握了Spark常用算子与核心原理以后，你已经可以轻松应对大部分数据处理需求了。

不过，数据处理毕竟是比较基础的数据应用场景，就像赛车有着不同的驾驶场景，想成为Spark的资深赛车手，我们还要走出第三步——学习Spark计算子框架。只有完成这一步，我们才能掌握Spark SQL，Structured Streaming和Spark MLlib的常规开发方法，游刃有余地应对不同的数据应用场景，如数据分析、流计算和机器学习，等等。

![图片](https://static001.geekbang.org/resource/image/6a/a3/6a56c520ab7666d1bb9dd1f0683346a3.jpg?wh=1920x915 "还差第三步")

那这么多子框架，从哪里入手比较好呢？在所有的子框架中，Spark SQL是代码量最多、Spark社区投入最大、应用范围最广、影响力最深远的那个。就子框架的学习来说，我们自然要从Spark SQL开始。

今天我们从一个例子入手，在实战中带你熟悉数据分析开发的思路和实现步骤。有了对Spark SQL的直观体验，我们后面几讲还会深入探讨Spark SQL的用法、特性与优势，让你逐步掌握Spark SQL的全貌。

## 业务需求

今天我们要讲的小例子，来自于北京市小汽车摇号。我们知道，为了限制机动车保有量，从2011年开始，北京市政府推出了小汽车摇号政策。随着摇号进程的推进，在2016年，为了照顾那些长时间没有摇中号码牌的“准司机”，摇号政策又推出了“倍率”制度。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（16） 💬（3）<div>spark无关。讨论下摇号。

评论区有匿名读者质疑文中的结论。这里尝试换个角度代入具体的数字分析下。

简单起见，假设每轮摇号有1000人中签，并且倍率和轮次一致，即第一轮大家都是1倍，第一轮没中的人在第二轮变为2倍，第二轮又没中的人到了第三轮就变成3倍，依次类推。

先看第一轮的1000个中签者，显然他们的倍率都是1，没有其他倍率的中签者，记为:

[1000, 0, 0, ...]

再看第二轮的1000个中签者。由于新加入的申请者倍率为1，第一轮未中的人倍率为2。按照倍率摇号的话，期望的结果就是，倍率为2的中签人数是倍率为1的中签人数的2倍，记为：

[333, 667, 0, 0, ...]

以此类推，第三轮就是：

[167, 333, 500, 0, 0, ...]

尝试摇个10轮，可以得到下表：

[1000, 0, 0, ...]
[333, 667, 0, 0, ...]
[167, 333, 500, 0, 0, ...]
[100, 200, 300, 400, 0, 0, ...]
[67, 133, 200, 267, 333, 0, 0, ...]
[48, 95, 143, 190, 238, 286, 0, 0, ...]
[36, 71, 107, 143, 179, 214, 250, 0, 0, ...]
[28, 56, 83, 111, 139, 167, 194, 222, 0, 0, ...]
[22, 44, 67, 89, 111, 133, 156, 178, 200, 0, 0, ...]
[18, 36, 55, 73, 91, 109, 127, 145, 164, 182, 0, 0, ...]

可以看到在每一轮的中签者中，确实是倍率越高中签的人数越多。

而文中的统计方法，相当于把这张表按列求和：

[1819, 1635, 1455, 1273, 1091, 909, 727, 545, 364, 182, 0, 0, ...]

可以看到这是一条单调递减的曲线。然而却不能像文中一样得出“中签率没有随着倍率增加”的结论。高倍率的中签人数比低倍率的人数少，是因为能达到高倍率的人本身就少。比如上面例子中，10轮过后10倍率的中签者只有182人，是因为前9轮没有人能达到10倍率。相比之下，在第一轮就有1000个1倍率的人中签。

至于文中配图为什么会是一条类似钟型的曲线，猜测可能第一次引入倍率摇号的时候，就已经给不同的人分配不同的倍率了，而不是大家一开始都是1倍率。在上面的例子中，如果只对后5轮求和，可以得到：

[152, 302, 455, 606, 758, 909, 727, 545, 364, 182]

这样就和文中的配图比较接近了。

所以结论就是要验证中签率和倍率的关系，不能按照倍率去累加中签人数，而是要看单次摇号中不同倍率的中签者的分布。</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/ec/c60b29f5.jpg" width="30px"><span>Alvin-L</span> 👍（6） 💬（2）<div>```
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import first, collect_list, mean, count, max
import matplotlib.pyplot as plt

def plot(res):
    x = [x[&quot;multiplier&quot;] for x in res]
    y = [y[&quot;cnt&quot;] for y in res]
    plt.figure(figsize=(8, 5), dpi=100)
    plt.xlabel(&#39;倍率&#39;)
    plt.ylabel(&#39;人数&#39;)
    plt.rcParams[&#39;font.sans-serif&#39;]=[&#39;SimHei&#39;] 
    plt.rcParams[&#39;axes.unicode_minus&#39;]=False
    plt.bar(x, y, width=0.5)
    plt.xticks(x)
    plt.show()

# py文件就在项目的根目录下
rootPath = os.path.split(os.path.realpath(__file__))[0]

conf = SparkConf()
conf.set(&#39;spark.executor.memory&#39;, &#39;4g&#39;)
conf.set(&#39;spark.driver.memory&#39;, &#39;8g&#39;)
conf.set(&quot;spark.executor.cores&quot;, &#39;4&#39;)
conf.set(&#39;spark.cores.max&#39;, 16)
conf.set(&#39;spark.local.dir&#39;, rootPath)
spark = SparkSession(SparkContext(conf=conf))
# 申请者数据
# Windows环境
# 注意点1：增加 option(&quot;basePath&quot;, rootPath) 选项
# 注意点2：路径 hdfs_path_apply 需要追加 &#47;*&#47;*.parquet
hdfs_path_apply = rootPath + &quot;&#47;apply&quot;
applyNumbersDF = spark.read.option(&quot;basePath&quot;, rootPath).parquet(
    hdfs_path_apply + &quot;&#47;*&#47;*.parquet&quot;
)
# 中签者数据
hdfs_path_lucky = rootPath + &quot;&#47;lucky&quot;
luckyDogsDF = spark.read.option(&quot;basePath&quot;, rootPath).parquet(
    hdfs_path_lucky + &quot;&#47;*&#47;*.parquet&quot;
)
# 过滤2016年以后的中签数据，且仅抽取中签号码carNum字段
filteredLuckyDogs = (
    luckyDogsDF
    .filter(luckyDogsDF[&quot;batchNum&quot;] &gt;= &quot;201601&quot;)
    .select(&quot;carNum&quot;)
)
# 摇号数据与中签数据做内关联，Join Key为中签号码carNum
jointDF = applyNumbersDF.join(filteredLuckyDogs, &quot;carNum&quot;, &quot;inner&quot;)
# 以batchNum、carNum做分组，统计倍率系数
multipliers = (
    jointDF
    .groupBy([&quot;batchNum&quot;, &quot;carNum&quot;])
    .agg(count(&quot;batchNum&quot;).alias(&quot;multiplier&quot;))
)
# 以carNum做分组，保留最大的倍率系数
uniqueMultipliers = (
    multipliers
    .groupBy(&quot;carNum&quot;)
    .agg(max(&quot;multiplier&quot;).alias(&quot;multiplier&quot;))
)
# 以multiplier倍率做分组，统计人数
result = (
    uniqueMultipliers
    .groupBy(&quot;multiplier&quot;)
    .agg(count(&quot;carNum&quot;).alias(&quot;cnt&quot;))
    .orderBy(&quot;multiplier&quot;)
)
result.show(40)
res = result.collect()
# 画图
plot(res)
```</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ba/c6/10448065.jpg" width="30px"><span>东围居士</span> 👍（2） 💬（2）<div>补一个完整的 spark 代码（windows环境）：

package spark.basic

import org.apache.spark.sql.functions.{col,count, lit, max}
import org.apache.spark.sql.{DataFrame, SparkSession}

object Chapter13 {
    def main(args: Array[String]): Unit = {

        val spark: SparkSession = SparkSession.builder().master(&quot;local[*]&quot;).appName(&quot;Chapter13&quot;).getOrCreate()
        import spark.implicits._

        val rootPath: String = &quot;E:\\temp\\yaohao_home\\yaohao&quot;
        &#47;&#47; 申请者数据
        val hdfs_path_apply: String = s&quot;${rootPath}&#47;apply&quot;
        &#47;&#47; spark是spark-shell中默认的SparkSession实例
        &#47;&#47; 通过read API读取源文件
        val applyNumbersDF: DataFrame = spark.read.option(&quot;basePath&quot;, rootPath).parquet(hdfs_path_apply + &quot;&#47;*&#47;*.parquet&quot;)

        &#47;&#47; 中签者数据
        val hdfs_path_lucky: String = s&quot;${rootPath}&#47;lucky&quot;
        &#47;&#47; 通过read API读取源文件
        val luckyDogsDF: DataFrame = spark.read.option(&quot;basePath&quot;, rootPath).parquet(hdfs_path_lucky + &quot;&#47;*&#47;*.parquet&quot;)

        &#47;&#47; 过滤2016年以后的中签数据，且仅抽取中签号码carNum字段
        val filteredLuckyDogs: DataFrame = luckyDogsDF.filter(col(&quot;batchNum&quot;) &gt;= &quot;201601&quot;).select(&quot;carNum&quot;)

        &#47;&#47; 摇号数据与中签数据做内关联，Join Key为中签号码carNum
        val jointDF: DataFrame = applyNumbersDF.join(filteredLuckyDogs, Seq(&quot;carNum&quot;), &quot;inner&quot;)

        &#47;&#47; 以batchNum、carNum做分组，统计倍率系数
        val multipliers: DataFrame = jointDF.groupBy(col(&quot;batchNum&quot;),col(&quot;carNum&quot;))
            .agg(count(lit(1)).alias(&quot;multiplier&quot;))

        &#47;&#47; 以carNum做分组，保留最大的倍率系数
        val uniqueMultipliers: DataFrame = multipliers.groupBy(&quot;carNum&quot;)
            .agg(max(&quot;multiplier&quot;).alias(&quot;multiplier&quot;))

        &#47;&#47; 以multiplier倍率做分组，统计人数
        val result: DataFrame = uniqueMultipliers.groupBy(&quot;multiplier&quot;)
            .agg(count(lit(1)).alias(&quot;cnt&quot;))
            .orderBy(&quot;multiplier&quot;)

        result.collect
        result.show()
    }
}
</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/83/74e3fabd.jpg" width="30px"><span>火炎焱燚</span> 👍（2） 💬（2）<div>对应的python代码为：

# 在notebook上运行时，加上下面的配置
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession

sc_conf = SparkConf() # spark参数配置
# sc_conf.setMaster()
# sc_conf.setAppName(&#39;my-app&#39;)
sc_conf.set(&#39;spark.executor.memory&#39;, &#39;2g&#39;) 
sc_conf.set(&#39;spark.driver.memory&#39;, &#39;4g&#39;) 
sc_conf.set(&quot;spark.executor.cores&quot;, &#39;2&#39;) 
sc_conf.set(&#39;spark.cores.max&#39;, 20)    
sc = SparkContext(conf=sc_conf)

# 加载数据，转换成dataframe
rootPath=&#39;~~&#47;RawData&#39;
hdfs_path_apply=rootPath+&#39;&#47;apply&#39;
spark = SparkSession(sc)
applyNumbersDF=spark.read.parquet(hdfs_path_apply)
# applyNumbersDF.show() # 打印出前几行数据，查看数据结构

hdfs_path_lucky=rootPath+&#39;&#47;lucky&#39;
luckyDogsDF=spark.read.parquet(hdfs_path_lucky)
# luckyDogsDF.show()

filteredLuckyDogs=luckyDogsDF.filter(luckyDogsDF[&#39;batchNum&#39;]&gt;=&#39;201601&#39;).select(&#39;carNum&#39;)
jointDF=applyNumbersDF.join(filteredLuckyDogs,&#39;carNum&#39;,&#39;inner&#39;)
# join函数消耗内存较大，容易出现OOM错误，如果出错，要将spark.driver.memory调大
# jointDF.show() # 打印出join之后的df部分数据

# 进行多种groupBy操作
from pyspark.sql import functions as f
multipliers=jointDF.groupBy([&#39;batchNum&#39;,&#39;carNum&#39;]).agg(f.count(&#39;batchNum&#39;).alias(&quot;multiplier&quot;))
# multipliers.show()

uniqueMultipliers=multipliers.groupBy(&#39;carNum&#39;).agg(f.max(&#39;multiplier&#39;).alias(&#39;multiplier&#39;))
# uniqueMultipliers.show()

result=uniqueMultipliers.groupBy(&#39;multiplier&#39;).agg(f.count(&#39;carNum&#39;).alias(&#39;cnt&#39;)).orderBy(&#39;multiplier&#39;)
result2=result.collect()

# 绘图
import matplotlib.pyplot as plt
x=[i[&#39;multiplier&#39;] for i in result2]
y=[i[&#39;cnt&#39;] for i in result2]
plt.bar(x,y)</div>2021-10-23</li><br/><li><img src="" width="30px"><span>Geek_d447af</span> 👍（1） 💬（2）<div>文章里的代码需要在 Hadoop 环境才能跑起来，spark 本身不支持解析 parquet 文件</div>2021-10-09</li><br/><li><img src="" width="30px"><span>lightning_女巫</span> 👍（0） 💬（1）<div>我在本地跑这个代码碰到了如下错误，请问如何解决？
22&#47;01&#47;28 15:13:22 ERROR BypassMergeSortShuffleWriter: Error while deleting file &#47;private&#47;var&#47;folders&#47;hk&#47;7j9sqdtn55j3cq_gv5qvp5pm39d49n&#47;T&#47;blockmgr-88ef94e9-943a-4971-a3a8-33d25949886f&#47;1a&#47;temp_shuffle_e0e163fb-852c-4298-b08e-dc4989277ab3
22&#47;01&#47;28 15:13:22 ERROR DiskBlockObjectWriter: Uncaught exception while reverting partial writes to file &#47;private&#47;var&#47;folders&#47;hk&#47;7j9sqdtn55j3cq_gv5qvp5pm39d49n&#47;T&#47;blockmgr-88ef94e9-943a-4971-a3a8-33d25949886f&#47;08&#47;temp_shuffle_6c160c23-3395-445f-be03-b29a375e1139
java.io.FileNotFoundException: &#47;private&#47;var&#47;folders&#47;hk&#47;7j9sqdtn55j3cq_gv5qvp5pm39d49n&#47;T&#47;blockmgr-88ef94e9-943a-4971-a3a8-33d25949886f&#47;08&#47;temp_shuffle_6c160c23-3395-445f-be03-b29a375e1139 (No such file or directory)
	at java.io.FileOutputStream.open0(Native Method)
	at java.io.FileOutputStream.open(FileOutputStream.java:270)
	at java.io.FileOutputStream.&lt;init&gt;(FileOutputStream.java:213)
	at org.apache.spark.storage.DiskBlockObjectWriter$$anonfun$revertPartialWritesAndClose$2.apply$mcV$sp(DiskBlockObjectWriter.scala:217)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:1369)
	at org.apache.spark.storage.DiskBlockObjectWriter.revertPartialWritesAndClose(DiskBlockObjectWriter.scala:214)
	at org.apache.spark.shuffle.sort.BypassMergeSortShuffleWriter.stop(BypassMergeSortShuffleWriter.java:237)
	at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:105)
	at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:55)
	at org.apache.spark.scheduler.Task.run(Task.scala:123)
	at org.apache.spark.executor.Executor$TaskRunner$$anonfun$10.apply(Executor.scala:408)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:1360)
	at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:414)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ba/c6/10448065.jpg" width="30px"><span>东围居士</span> 👍（0） 💬（3）<div>老师，数据文件方便存一份到别的地方吗，比如马云家的网盘，或者做个种子下载什么的，百度网盘那速度真的是，我下到下午下班过周末都下不完</div>2021-10-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（0） 💬（2）<div>用scala实现，lit(1)是什么意思呀</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（1）<div>result具体数值：
scala&gt; result.collect
res7: Array[org.apache.spark.sql.Row] = Array([1,8967], [2,19174], [3,26952], [4,29755], [5,32988], [6,34119], [7,29707], [8,26123], [9,19476], [10,9616], [11,3930], [12,1212])</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5e/b2/aceb3e41.jpg" width="30px"><span>Neo-dqy</span> 👍（0） 💬（1）<div>【.agg(count(lit(1)).alias(&quot;cnt&quot;))】问下老师，这里count中的lit(1)是什么意思啊？
对于汽车摇号的倍率制度，如果为了优先让倍率高的人摇到号，可以把每一期的资格分多次抽取。就是说，先构建一个所有人都在里面的样本，抽部分人；再将倍率高于某个阈值的人都取出来，构建一个新的样本，再抽取部分人。（具体划分成几个样本可以按倍率的人数分布来划分）当然这样又会对新来的人不公平，所以大家还是挤地铁吧~~</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（2） 💬（0）<div>Java实现
https:&#47;&#47;github.com&#47;Spoon94&#47;spark-practice&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;spoon&#47;spark&#47;sql&#47;CarNumAnalyseJob.java</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（1） 💬（0）<div>大概看了下评论，发现一次摇号一个号码会出现多次，是为了增加n次参与的人被摇到的概率。相当于在一个封闭的箱子里摇球，一个号码的球多放了几个，摇箱子后个数多的号码被抽到的概率更高（n&#47;N，N为箱子内球的总数）</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/d2/f12dd0ac.jpg" width="30px"><span>翡翠小南瓜</span> 👍（1） 💬（2）<div>不懂北京的摇号规则，也没写清楚，所以是一个批次号里面，一个申请号可以有多次？？？？</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/9f/d7/e393d0ec.jpg" width="30px"><span>Each</span> 👍（0） 💬（0）<div>老師您好, 無法下載 dataset, 可以提供海外載點嗎? 謝謝.</div>2024-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/a3/80/02f4da95.jpg" width="30px"><span>风一样</span> 👍（0） 💬（1）<div>上面的结论感觉不太正确，偏离了每个每个倍率下的基数，倍率越高中签概率肯定越大啊，对个人而言，如果我们每次参与抽签的人数大基数不变的情况下(基数1000)，倍率越大，相当于往里面添加了多个样本（8倍率），本来是1&#47;1000的概率变为了8&#47;1000。但是考虑到每次倍率越大没中签的用户重复的次数越多，基数也会跟着变大，相对于新加入的人来说其实是有优势的，但是新增的人其实远小于已经参与过抽签的人，所以才导致了感觉上变化不大</div>2022-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/6f/3a97712e.jpg" width="30px"><span>林Curry</span> 👍（0） 💬（0）<div>val multipliers: DataFrame = jointDF.groupBy(col(&quot;batchNum&quot;),col(&quot;carNum&quot;)).agg(count(lit(1)).alias(&quot;multiplier&quot;))

老师，有点没有看懂倍率的计算方式，以batchNum和carNum两个字段groupby的话，计算的不就是申请号在各个批次中出现的次数么？ 难道一个申请号还会在同个批次中出现多次吗</div>2022-07-16</li><br/><li><img src="" width="30px"><span>杨帅</span> 👍（0） 💬（0）<div>老师，本地报错 类似Caused by: java.io.IOException: Failed to connect to &#47;192.168.1.3:50561，这个一般是什么问题？</div>2022-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/36/1c/adfeb6c4.jpg" width="30px"><span>爱学习的王呱呱</span> 👍（0） 💬（0）<div>join的时候一直提示：【No offset index for column carNum is available; Unable to do filtering】网上没搜到，求大佬们帮忙看看原因

sc = SparkContext()
spark = SparkSession(sc)
root_path = &quot;&#47;Users&#47;admin&#47;Documents&#47;2011-2019小汽车摇号数据&quot;

hdfs_path_apply = root_path + &quot;&#47;apply&quot;
applyDF = spark.read.parquet(hdfs_path_apply).select(&quot;carNum&quot;)
# applyDF.show()

hdfs_path_lucky = root_path + &quot;&#47;lucky&quot;
lucyDF = spark.read.parquet(hdfs_path_lucky)
# lucyDF.show()


lucy_car_num = lucyDF.filter(lucyDF[&#39;batchNum&#39;] &gt;= &#39;201601&#39;).select(&#39;carNum&#39;)
all_car_num = applyDF.join(lucy_car_num, &quot;carNum&quot;, &quot;inner&quot;)
all_car_num.show()</div>2022-04-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIfxu4yQEXdQ3icro8QEb0W3Rk014YXqibgw28kAcezVGy0DJzkERd1gXh5uEKL42VnnwomelvgPMDA/132" width="30px"><span>Geek_9d1801</span> 👍（0） 💬（0）<div>apply&#47;batchNum=201905&#47;part-00001-f8bb8e7b-904f-42a7-a616-a413406f06fb.c000.snappy.parquet is not a Parquet file. expected magic number at tail [80, 65, 82, 49] but found [14, 14, 14, 14]
没有人报这个错误吗？是什么问题？</div>2022-04-07</li><br/>
</ul>