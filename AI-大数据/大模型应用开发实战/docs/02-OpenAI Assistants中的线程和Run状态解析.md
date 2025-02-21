你好，我是黄佳，欢迎来到启程篇的第二节课。

在上节课中，我们介绍了如何使用OpenAI的Playground创建一个Assistant，并通过Python程序检索并调用它完成一个简单的订单总价计算任务。今天，我们将继续深入探讨OpenAI Assistant中两个重要的概念：Thread（线程）和Run（运行），以及它们的生命周期和各种状态。

OpenAI Assistants的技术架构中总共有4个值得一提的对象，分别是：Assistant、Thread、Run和Message，其基本操作步骤如下：

![](https://static001.geekbang.org/resource/image/28/bf/2801d4e3c087093fe6da67a0b12ba3bf.jpg?wh=1417x927)

这些对象中，Assisant和Message不言自明，无须解释。那么，如何理解Thread和Run呢？

## 究竟什么是 Thread 和 Run?

在OpenAI Assistant的设计中，Thread代表了Assistant和用户之间的一次完整对话会话。它存储了Assistant和用户之间来回的Messages（消息），并自动处理上下文截断，以适应模型的上下文长度限制。

其实这就像是你在网页上和ChatGPT等任何语言模型的一个**聊天页面**，这个会话过程中，背后的Thread帮你记住之前的聊天上下文，并且在你输入的信息过长时会提醒你。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/09/1e/fc5144ff.jpg" width="30px"><span>王轲</span> 👍（1） 💬（2）<div>我觉得Thread此处不应该翻译成线程，线程这个词容易让人和操作系统的线程产生错误联想。应该取这个解释:[countable] (computing计算机) a series of connected messages on email, social media, etc. that have been sent by different people（互联网留言板上帖子的）系列相关信息，链式消息</div>2024-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/f0/d8/c344594a.jpg" width="30px"><span>🇾.🇨.</span> 👍（1） 💬（6）<div>感觉最近两节课收获很小啊，我有OpenAI，但是是Azure上的，根本用不了Assistant。兄弟们国内还是走虚拟卡服务商订阅openai吗？</div>2024-05-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VR5VwSsY8uGQKkeibUy5rGbvChLMh936xYDNCUGAszqulibIy94PVGpL9jqEtZI61thGceeLibr1ev7yUlGmOFD7Q/132" width="30px"><span>Geek_a15a44</span> 👍（0） 💬（1）<div>大佬你好，请问assistant可以根据用户query连续调用两个函数吗，是否会连续两次出现requires_action状态呢？</div>2024-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>u1s1, assistants还在beta, 一直在变化, 所以课程内容可能需要持续更新. 比如课上提到的thread列表, 前一阵出了个project页面, 可以分不同的project管理thread. 另外不活跃的thread也不是说不会扣费, 因为前一阵出了vector store, 可以attach到thread上用于rag什么的. 就算thread里没有新token产生, vector store还是会默认扣费7天.</div>2024-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（1） 💬（0）<div>1. 相同：都是通过循环轮询当前run的状态 不同：终止轮询条件和轮询间隔
2. 根据run的created_at和expires_at字段得知run的生命周期默认时600s，即10分钟
3. # 定义一个轮询run状态的函数
def poll_run_status(thread_id, run_id: str, interval=3):
    while True:
        run = client.beta.threads.runs.retrieve(
            run_id=run_id,
            thread_id=thread_id,
        )
        print(f&#39;Run的状态: {run.status}&#39;)
        print(f&#39;Run的轮询信息: \n{run}\n&#39;)
        if run.status in [&#39;require_action&#39;, &#39;completed&#39;, &#39;cancelled&#39;]:
            return run
        if run.status == &#39;in_progress&#39;:
            client.beta.threads.runs.cancel(run_id=run_id, thread_id=thread_id)
        time.sleep(interval)</div>2024-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/ec/406130f3.jpg" width="30px"><span>coderlee</span> 👍（0） 💬（0）<div>Q1: 
1）create_and_poll相当于先cerate，再执行poll_run_status
2）poll_run_status中，判断跳出循环的run.status是requires_action和completed；create_and_poll中跳出循环的run.status增加了cancelled, failed,expired,incomplete的判断。
3）个人理解，课程中使用自定义函数poll_run_status，一个是让大家理解api（手戳create_and_poll），一个是更方便的去展示run的生命周期
Q2：
1）生命周期应该是从Thread被run开始，从queued状态，直到completed&#47;failed&#47;expired&#47;cancelled的一整个过程。
2）当run执行过程中超出时间未响应就会过期。（个人理解类似于http请求的超时时间）
Q3：
有手就行</div>2024-11-15</li><br/>
</ul>