你好，我是尹会生。

在我为运营工作提供技术咨询的时候，遇到过这样一个场景：这场运营活动，需要在电脑和手机端的多个不同应用程序，同时推送产品宣传图片和视频。这些大量的图片需要有不同的格式和尺寸，视频也需要根据不同的App截取不同的时长。

如果这类需要大量计算的多个任务成为你的日常工作，会花费你不少的时间和精力。不过别担心，我们可以通过程序并行计算，来提升任务效率。

不过你可能会说，用Python自动化执行，也可以提高计算效率啊，那为什么还要学习并行计算呢？

要知道，Python默认的自动化只能利用CPU的一个逻辑核心，如果采用并行计算，那就能够最大化地利用CPU资源，从而成倍提升大量计算的任务效率。接下来我就详细分析一下并行计算的高效之处。

## 为什么要进行并行计算

还是我在开头提出的运营工作的场景。如果你从这类任务消耗计算机主要资源的角度去考虑，会发现这类需求有两个共同的特点。

第一，它们都需要进行大量的计算，而计算主要是通过CPU来实现的。CPU的硬件指标上有两个和计算效率最相关的概念，分别是主频和多核。

主频决定CPU处理任务的快慢，多核决定处理的时候是否可以并行运行。这和生活中超市的收银一样，收银员的工作效率和超市开放了多少个收银台的通道，都决定了你能否以最快的速度购买到你想要买的商品。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/4c/b1/c8fc2efa.jpg" width="30px"><span>聂小倩</span> 👍（7） 💬（1）<div>老师，请问为什么说“在多进程的程序中，不能采用标准数据类型来传递数据”呢？</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/94/a3/9cfea58e.jpg" width="30px"><span>十一哈哈</span> 👍（6） 💬（2）<div>windows下使用multiprocessing，要将进程池相关代码应该放在if __name__ == &#39;__main__&#39;下面，要不然运行会报错....</div>2021-03-08</li><br/><li><img src="" width="30px"><span>Geek_a345af</span> 👍（1） 💬（1）<div>把您的代码复制到我电脑上试了下，
1、发现100以内的求平方，我这边的结果并没有启用多进程，一个进程就做完了这些。改成求1000的内的平方，才创建了两个进程。(电脑cpu是8)
2、queue.put(os.getpid())向队列里添加进程的id，在后面向set里存这些id的时候，发现queue是空的，不太明白是为什么。
</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/0c/c438c5df.jpg" width="30px"><span>天国之影</span> 👍（1） 💬（1）<div>老师，我运行出来的时间统计结果如下：

并行计算时间统计: 0.1607363224029541
串行计算时间统计: 0.0009999275207519531

为什么并行计算比串行计算耗时还长？</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/c1/be/dcce5f5a.jpg" width="30px"><span>Bill</span> 👍（0） 💬（1）<div>打卡</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（0） 💬（1）<div>老师，请问如果在代码运行过程中出现“UnicodeEncodeError: &#39;ascii&#39; codec can&#39;t encode characters in position 18-19: ordinal not in range(128)” 这样的报错，应该如何解决呢？</div>2021-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/0c/c438c5df.jpg" width="30px"><span>天国之影</span> 👍（1） 💬（0）<div>如果在Jupyter Notebook下，可使用以下方法：
通过临时文件方式，读取并使用并行计算

from multiprocessing import Pool
from functools import partial
import inspect
 
def parallal_task(func, iterable, cpu_count = 4):
 
    with open(f&#39;.&#47;tmp_func.py&#39;, &#39;w&#39;) as file:
        file.write(inspect.getsource(func).replace(func.__name__, &quot;task&quot;))
 
    from tmp_func import task
 
    if __name__ == &#39;__main__&#39;:
        func = partial(task)
        pool = Pool(cpu_count * 2)
        res = pool.map(func, iterable)
        pool.close()
        return res
    else:
        raise &quot;Not in Jupyter Notebook&quot;

# 计算平方
def def_f(x):
    return x * x

for res in parallal_task(def_f, range(1, 101)):
    print(f&#39;计算平方的结果是:{res}&#39;)</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/21/aa/3b1dbca7.jpg" width="30px"><span>坚果</span> 👍（0） 💬（0）<div>这一章有没有windows并行计算参考资料，我一个程序都没有调试成功，一运行就堵塞</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/21/aa/3b1dbca7.jpg" width="30px"><span>坚果</span> 👍（0） 💬（0）<div>
通过临时文件方式，读取并使用并行计算，为什么要通过临时文件使用并行计算？</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/2f/d08a1363.jpg" width="30px"><span>聪少 Jeff</span> 👍（0） 💬（0）<div>为了初步本次课程的小伙伴想我遇到相同的问题（即是：进程池相关代码应放在if__name__ == &#39;main&quot;的报错）解决方法参考，这个问题已经在十一哈哈学员的提醒下发现的，为了直观一些提供以下代码参考一下。

[示例代码]
from multiprocessing import Pool
# 1-100平方模拟程序


def f(x):
    # 计算平方
    return x * x


def test():
    with Pool(8) as p:
        res = p.map(f, range(1, 101))
        print(f&#39;计算平方的结果是:{res}&#39;)


if __name__ == &#39;__main__&#39;:
    test()
</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f5/9f/1509d389.jpg" width="30px"><span>栾~龟虽寿！</span> 👍（0） 💬（0）<div>打卡学习了</div>2021-05-07</li><br/>
</ul>