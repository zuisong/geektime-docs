你好，我是蒋宏伟。

从今天开始，我们将进入 React Native 基础设施建设篇的学习。我也特地邀请了多年以来和我一起做 58RN 基建的两位老搭档：58RN Android 负责人况众文和58RN iOS 负责人朴惠姝一起来讲解。

在基础设施建设篇中，众文老师、惠姝老师会和我一起为你详细介绍怎么搭建 React Native 混合应用、怎么创建新架构的自定义组件，以及怎么自研热更新平台，又怎么进行性能优化。

无论你是 FE、Android 还是 iOS，相信基建篇的内容都能让你大有收获，甚至帮助你在公司中晋级。好了，下面我们正式开启基建篇的学习。

* * *

你好，我是况众文，是 58RN 负责Android 端的同学。接下来基础设施建设篇中移动端相关的几讲，将由我和我的同事，负责iOS 端的同学朴惠姝一起来讲解。

这几讲是《混合应用：如何从零开始集成 React Native？》、《自定义组件：如何满足业务的个性化需求？》，以及《客户端优化：如何把性能提升到极致？》。在这三讲中，我们将结合自己在 React Native 开发的实际经验，以及真实的业务案例，和你一起循序渐进地走入混合开发的世界。

而且，我们这几讲将使用 React Native 最新框架来讲解，你也可以借此了解 Fabric、TurboModules、CodeGen、JSI、Hermes 等新概念。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/c7/26485903.jpg" width="30px"><span>Yolo七夜</span> 👍（1） 💬（2）<div>RN 可以与 flutter直接混编吗？</div>2022-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/9b/d7/13d8bf91.jpg" width="30px"><span>飘逸跑酷</span> 👍（11） 💬（0）<div>来波源码，参照一下</div>2022-05-26</li><br/><li><img src="https://thirdqq.qlogo.cn/qqapp/101423631/0FD57A9C0C5BFBDA3DA69AE26B3514FB/100" width="30px"><span>下一刻。</span> 👍（6） 💬（0）<div>iOS 期望可以讲解一下，类似Android arr的混合模式。把iOS RN部分打包成framework。</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/bd/50d98f9e.jpg" width="30px"><span>黑马有点白986</span> 👍（3） 💬（0）<div>Android 端动态加载 bundle 就讲完了,按照你的文档来，根本跑不通呀，能不能给个demo</div>2023-02-13</li><br/><li><img src="" width="30px"><span>Geek_585b44</span> 👍（3） 💬（0）<div>没看懂iOS是怎么集成RN的，没有demo吗</div>2022-11-18</li><br/><li><img src="https://thirdqq.qlogo.cn/qqapp/101423631/0FD57A9C0C5BFBDA3DA69AE26B3514FB/100" width="30px"><span>下一刻。</span> 👍（2） 💬（1）<div>安卓使用arr混合模式后，可以抛弃node_modules，那么如果项目中使用到一些原生第三方库，应该如何处理呢？</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f2/6e/6f621806.jpg" width="30px"><span>Print JQK°</span> 👍（1） 💬（0）<div>来波源码，参考一下</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（1） 💬（0）<div>podspec 参考哪啊，大哥，不能就直接给个 github 项目首页的地址吧</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/16/4d/a2f34fe1.jpg" width="30px"><span>王小东</span> 👍（1） 💬（0）<div>新手小白提问，这种搭建的是线上运行环境吧 如何搭建方便调试的开发环境呢</div>2023-02-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTISicpsLbj7rPDKW5HpUVExAT3ljKKVHvMSgFm3hWzZBSFiaHNteUuuicEdySFopjL0U4FQJb7PxkBicQ/132" width="30px"><span>Geek_4a10b1</span> 👍（1） 💬（1）<div>关于混合开发的环境集成这块儿有个问题咨询下，如果Android项目集成新版本架构，我看官网介绍需要依赖nodemodule里的react-native-gradle-plugin，nodemodule都被删了的话，这一步你们是怎么处理呢？另外如果要用TuboModule和Fabric，需要生成各种c++文件使用NDK进行编译，采用混合开发这种集成方式的话这一步又要怎么处理呢？</div>2022-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/1d/c59e0b59.jpg" width="30px"><span>Sunny</span> 👍（1） 💬（1）<div>请问下，纯RN的客户端如何配置热更新？如果能具体些，非常感谢！期望是搭配23章CDN方案实现</div>2022-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIdLUtkvdNcLalw2PUxJaXY7Giacj4ZnGSPPTJkauHpoSG1jurGxxFXXf5zV52r1oRLzOuEBdmdGEA/132" width="30px"><span>小怪兽</span> 👍（1） 💬（1）<div>不用添加react.gradle脚本吗</div>2022-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div>我用 swift 集成了一下，开发阶段热更新也没有问题，但是如果有报错，iOS 就崩溃了，这是怎么回事？
&#39;-[hybridnative.AppDelegate window]: unrecognized selector sent to instance</div>2023-04-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLib4GiaK4KB3UvnnzIkMAD4QzKBAkOzdntPwsb8RX1xjHYgr2w0GLWhmoPdwy3iby3zOHbeTBR2DgRQ/132" width="30px"><span>songyq</span> 👍（0） 💬（0）<div> RCTSetFatalHandler(^(NSError *error) {
    dispatch_async(dispatch_get_main_queue(), ^{
        RNViewController *rnVC = nil;
        RCTBridge *bridge = (RCTBridge *)error.userInfo[@&quot;ErrorBridgeTag&quot;];
        if (bridge) {
           carrierVC = (RNViewController *)bridge.delegate;
        }
        NSString *descriptions = error.localizedDescription;
        NSLog(@&quot;error --- %@ --- %@&quot;, rnVC.rnModel.bundleID, descriptions);
    }
}
指出一处错误
carrierVC 名称错误了，应该是rnVC</div>2022-08-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLib4GiaK4KB3UvnnzIkMAD4QzKBAkOzdntPwsb8RX1xjHYgr2w0GLWhmoPdwy3iby3zOHbeTBR2DgRQ/132" width="30px"><span>songyq</span> 👍（0） 💬（0）<div>RNViewController *rnVC = nil; RCTBridge *bridge = (RCTBridge *)error.userInfo[@&quot;ErrorBridgeTag&quot;]; if (bridge) { carrierVC = (RNViewController *)bridge.delegate; } NSString *des</div>2022-08-19</li><br/><li><img src="" width="30px"><span>Geek_444dfb</span> 👍（0） 💬（0）<div>大佬，有没有精简的demo呢，希望能来一份😁</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/45/788e2e12.jpg" width="30px"><span>赱叉月月鳥</span> 👍（0） 💬（0）<div>这里没看懂：然后你将这三个部分作为 React Native 功能模块，直接参考官方提供的 podspec</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/df/a64b3146.jpg" width="30px"><span>长林啊</span> 👍（0） 💬（0）<div>老师，如何使用 RN 构建一个多路由视图的RN SDK呢？
</div>2022-06-14</li><br/>
</ul>