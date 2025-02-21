你好，我是陈航。

在上一篇文章中，我与你分享了调试Flutter代码的3种基本方式，即输出日志、断点调试与布局调试。

通过可定制打印行为的debugPrint函数，我们可以实现生产环境与开发环境不同的日志输出行为，从而保证在开发期打印的调试信息不会被发布至线上；借助于IDE（Android Studio）所提供的断点调试选项，我们可以不断调整代码执行步长和代码暂停条件，收敛问题发生范围，直至找到问题根源；而如果我们想找出代码中的布局渲染类Bug，则可以通过Debug Painting和Flutter Inspector提供的辅助线和视图可视化信息，来更为精准地定位视觉问题。

除了代码逻辑Bug和视觉异常这些功能层面的问题之外，移动应用另一类常见的问题是性能问题，比如滑动操作不流畅、页面出现卡顿丢帧现象等。这些问题虽然不至于让移动应用完全不可用，但也很容易引起用户反感，从而对应用质量产生质疑，甚至失去耐心。

那么，如果应用渲染并不流畅，出现了性能问题，我们该如何检测，又该从哪里着手处理呢？

在Flutter中，性能问题可以分为GPU线程问题和UI线程（CPU）问题两类。这些问题的确认都需要先通过性能图层进行初步分析，而一旦确认问题存在，接下来就需要利用Flutter提供的各类分析工具来定位问题了。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/0b/73/4f1c9676.jpg" width="30px"><span>舒大飞</span> 👍（2） 💬（4）<div>

想请教下，看了dart的单线程执行异步任务，像future这种执行网络请求的话，直接把任务放进event queue同步执行，那么then的任务如何处理，等网络请求返回再放进event queue?整个过程是怎样的，谢谢

</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/d4/5a0a2f8d.jpg" width="30px"><span>火腿</span> 👍（0） 💬（1）<div>dart是单线程模型，但Isolate是类似Unix的进程，所以可以这样理解吧： dart是多进程(每个进程只有单线程）的模型？ </div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>感谢老师分享。</div>2019-09-21</li><br/>
</ul>