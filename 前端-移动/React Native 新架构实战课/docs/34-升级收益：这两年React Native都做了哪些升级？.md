你好，我是蒋宏伟。这节课我们来聊聊 React Native 的近况。

经常有朋友问我，现阶段 React Native 的发展如何？新架构是否真的可用？我是否应该对我的业务进行升级？

今天，我们就来迅速了解下，在过去的两年中 React Native 都做了哪些改进。

## 新架构

众所周知，React Native团队在2018年时提出了新架构的设想，2022年开始发布新架构的预览版。又一年过去了，我们先来看看新架构的进展如何。

去年，新架构的预览版刚推出时，社区发布了 4 篇帖子，比较了新架构和旧架构的性能。一些人测试了ScrollView组件的渲染性能，有些人则测试了View、Text组件，还有人对比了 FlatList 和 ScrollView 场景下的渲染性能。得出的结论是：**虽然新架构在某些场景下有优势，但在更多的场景中新架构的性能却下降了。**

例如，一位社区成员在他的帖子中测试了FlatList（Virtualized）和ScrollView（Non Virtualized）组件，以及渲染导航组件和View组件的性能。

在ScrollView场景下，所有的组件都会被渲染出来，此时新架构的性能明显不如旧架构。而在FlatList 场景下，只有可视区附近的组件会被渲染出来，这时新架构的导航组件渲染性能优于旧架构，但View组件的渲染性能却弱于旧架构。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_accfac</span> 👍（0） 💬（0）<div>您好，请问58同城的APP现在使用是0.72版本吗？还是旧版本没有开启hermes呢</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3c/55/74844d08.jpg" width="30px"><span>大大小小</span> 👍（0） 💬（2）<div>请问目前最新的0.71.8的性能也有问题吗？需要更新到0.72 RC版本，性能才会提升？
</div>2023-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3c/55/74844d08.jpg" width="30px"><span>大大小小</span> 👍（0） 💬（2）<div>关于Hermes的使用，Android和iOS如何使用可以展开详细说下吗？
有几个疑问？iOS不使用Hermes，是整个项目不使用Hermes吗？那我如果是用最新的0.71.8版本的工程，如何关闭Hermes引擎？另外关于iOS的热更新，所谓的与Hermes字节码不兼容是什么意思，expo的热更新不是使用Hermes吗？</div>2023-06-05</li><br/>
</ul>