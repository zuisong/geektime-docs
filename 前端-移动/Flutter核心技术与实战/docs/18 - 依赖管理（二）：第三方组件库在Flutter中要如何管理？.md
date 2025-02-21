你好，我是陈航。

在上一篇文章中，我与你介绍了Flutter工程的资源管理机制。在Flutter中，资源采用先声明后使用的机制，在pubspec.yaml显式地声明资源路径后，才可以使用。

对于图片，Flutter基于像素密度，设立不同分辨率的目录分开管理，但只需要在pubspec.yaml声明一次；而字体则基于样式支持，除了正常字体，还可以支持粗体、斜体等样式。最后，由于Flutter需要原生运行环境，因此对于在其启动之前所需的启动图和图标这两类特殊资源，我们还需要分别去原生工程中进行相应的设置。

其实，除了管理这些资源外，pubspec.yaml更为重要的作用是管理Flutter工程代码的依赖，比如第三方库、Dart运行环境、Flutter SDK版本都可以通过它来进行统一管理。所以，pubspec.yaml与iOS中的Podfile、Android中的build.gradle、前端的package.json在功能上是类似的。

那么，今天这篇文章，我就主要与你分享，在Flutter中如何通过配置文件来管理工程代码依赖。

## Pub

Dart提供了包管理工具Pub，用来管理代码和资源。从本质上说，包（package）实际上就是一个包含了pubspec.yaml文件的目录，其内部可以包含代码、资源、脚本、测试和文档等文件。包中包含了需要被外部依赖的功能抽象，也可以依赖其他包。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（45） 💬（1）<div>pubspec.yaml、.packages 与 pubspec.lock 这三个文件，在包管理中的具体作用是什么？
pubspec.yaml是声明依赖哪些包的配置文件
.packages是表示包在本地目录缓存的地址
pubspec.lock是把依赖锁死的文件
只有pubspec.yaml需要自己编写 其它两个文件会自动生成。

.packages 与 pubspec.lock 是否需要做代码版本管理呢？为什么？
pubspec.lock需要做版本管理，因为lock文件把版本锁定，统一工程环境
.packages不需要版本管理，因为跟本地环境有关，无法做到统一</div>2019-08-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erUjTyQGvvFoLkHoLqmXUqgC7ZtQx4Zyjdg3dLOKeCzH5InYYeibf7Q02dR1iaQvttib4HTIqSu1d22g/132" width="30px"><span>哗啦啦</span> 👍（12） 💬（2）<div>想问下老师 。我在ROW 中有3个widget ,想实现 3个widget 的高度填充整个ROW （即3个子widget 中高度最大的那个的高度 ）  ，请问有什么好办法能实现 ，我更换了交叉轴对齐方式为 CrossAxisAlignment.stretch 也不行 。感谢 卡了很久这个问题 </div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（6） 💬（3）<div>老师请问下，^0.1.2 这个版本号中的 ^ 是什么意思呢？</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（5） 💬（1）<div>1、pubspec.yaml 算是对 flutter 项目配置的管理，类似于 Android 中的 gradle，这些配置包括：项目名称(但是如果桌面的应用名称还得去具体平台的项目里面修改)、项目描述 、各种资源(资源包括图片、文件、字体等)，图片文件等资源需要在 yaml 文件中的 assets 标签下配置，字体需要在 fonts 标签下配置；

当然也有项目依赖 dart sdk 的版本配置，项目所依赖的第三方库的配置，而这些第三方库可以是远程 pub 仓库(类似于 jcenter&#47;maven)，也可以是 git 仓库，还可以是 本地的依赖库。

.packages 文件里面配置了远程依赖库下载到本地的路径，是一种映射关系。

pubspec.lock 文件里面则是配置了远程依赖库的具体信息，包括依赖库名称、版本号以及依赖地址。里面也有 dart sdk 的版本号。

2、.packages 是不需要版本管理，也不需要提交至远程仓库，应当对它添加忽略，因为它是与本地的映射，每个人的本地目录是不同的；pubspec.lock 则是需要版本管理的，因为他里面记录了具体的依赖信息。</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/29/a85c2853.jpg" width="30px"><span>汪帅</span> 👍（3） 💬（3）<div>我一直比较关心的还是关于第三方官方库支持情况，例如地图，即时通讯，音视频等等！安卓我倒是可以解决就是iOS我不会还是需要纯flutter的</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/18/7cbc34eb.jpg" width="30px"><span>davidzhou</span> 👍（2） 💬（3）<div>只是不太明白image.asset使用的是一个完整的uri，如果项目内图片资源比较多，我希望图片资源进行目录分类，那个路径就相对较长，如果是iOS的话，统一在一个地方创建xx.imageset就可以直接使用这个图片标识符了</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/55/48de9a24.jpg" width="30px"><span>Carlo</span> 👍（1） 💬（1）<div>依赖管理中的版本冲突很麻烦。pub每个包只下载一个版本。这就造成了如果第三方库很旧，依赖了A包很老的版本。如果我在自己的工程中用了A包最新版本。那就会造成冲突。请问这种情况怎么解决？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/25/c4cc1e9f.jpg" width="30px"><span>巫山老妖</span> 👍（1） 💬（1）<div>思考题1 ：
- pubspec.yaml（设置包的元数据（比如，包的名称和版本）、运行环境（比如Dart SDK与Flutter SDK版本）、外部依赖和内部配置）
- .packages（将依赖包名与系统缓存中的包文件路径进行映射，方便后续维护）
- pubspec.lock（用于记录当前状态下实际安装的各个直接依赖、间接依赖的包的具体来源和版本号）

思考题2：
.package文件不用托管，因为这个文件是自动生成的，存储的是包映射的是本地路径，不同开发环境路径不一样。
pubspec.lock需要托管，每次变更版本都会更新这个文件，我们也能知道实际安装版本。</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6e/23/9fce5f72.jpg" width="30px"><span>毛哥来了</span> 👍（0） 💬（1）<div>是否跟package.json一样也支持 ~1.2.3 这样的格式</div>2019-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hrTPJATib69H8PvsFNl8HHdn2C2JgDEyrotB1tJKZwQOBgYLl4GulFmafuLLCbichrYTT1NBG6qTjNx4yTtj1jLA/132" width="30px"><span>kkliu</span> 👍（0） 💬（1）<div>pubspec.yaml设定引用第三方SDK的版本范围，如果要指定对应版本可以直接在pubspec.lock 文件里指定sdk的版本号？</div>2019-09-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7qto0CCztcWE5A2cpKOYyvkCyyMMjjMoZ3Pz8h2GMKynUthxqCs0hk0pONXk198yKibHH4Jxrjgw/132" width="30px"><span>andy</span> 👍（0） 💬（3）<div>随着课程的节数增加，每节课的评论人数越来越少了，是不是好多放弃的</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（0） 💬（0）<div>最近看到这样的：

dev_dependencies:
  build_runner:

build_runner冒号后面不带任何版本信息，这样是否表示取库的最新版本？</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/89/a7/82827b76.jpg" width="30px"><span>outman</span> 👍（0） 💬（0）<div>请教个混合开发遇到的问题，资源，比如图片，文字，或尺寸，这些在app中都是通用的。那么flutter和android，ios能共用一个资源库吗？</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/8a/aed13671.jpg" width="30px"><span>鸡蛋石头</span> 👍（0） 💬（0）<div>能使用iconfont吗？怎么使用？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/7f/c50d520e.jpg" width="30px"><span>颜为晨</span> 👍（0） 💬（0）<div>Git 依赖的例子中，package2 写成了 date_format</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/3c/0e2a08b1.jpg" width="30px"><span>杨闯</span> 👍（0） 💬（2）<div>对于包管理，如果我所需要的包是git仓库的，但是如果同事在git仓库的同一分支下进行修改，可能会出现不更新包的问题，这个有什么解决方案吗？</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/3c/0e2a08b1.jpg" width="30px"><span>杨闯</span> 👍（0） 💬（0）<div>如果写死flutter的版本，但是和本地安装的sdk版本不一致的话，是不是就不能正常打包了，如果不能正常打包的话，是不是就要强制开发者修改本地SDK的版本号啊</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/c7/26485903.jpg" width="30px"><span>Yolo七夜</span> 👍（0） 💬（0）<div>学到了，环境相关的sdk最好统一，其他依赖的第三方库最好放开</div>2019-08-13</li><br/>
</ul>