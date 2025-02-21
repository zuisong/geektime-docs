你好，我是戴铭。今天，我和你分享的主题是，如何编写 Clang 插件。

Clang 使用的是模块化设计，可以将自身功能以库的方式来供上层应用来调用。比如，编码规范检查、IDE 中的语法高亮、语法检查等上层应用，都是使用 Clang 库的接口开发出来的。Clang 库对接上层应用有三个接口库，分别是 LibClang、Clang 插件、LibTooling。关于这三个接口库的介绍，我已经在[第8篇文章](https://time.geekbang.org/column/article/87844)中和你详细分享过。

其中，LibClang 为了兼容更多 Clang 版本，相比Clang少了很多功能；Clang 插件和 LibTooling 具备Clang 的全量能力。Clang 插件编写代码的方式，和 LibTooling 几乎一样，不同的是 Clang 插件还能够控制编译过程，可以加 warning，或者直接中断编译提示错误。另外，编写好的 LibTooling 还能够非常方便地转成 Clang 插件。

所以说，Clang 插件在功能上是最全的。今天这篇文章，我们就一起来看看怎样编写和运行 Clang 插件。

Clang 插件代码编写后进行编译的前置条件是编译 Clang。要想编译 Clang ，你就需要先安装 [CMake 工具](https://cmake.org/)，来解决跨平台编译规范问题。

我们可以先通过 CMakeList.txt 文件，来定制CMake编译流程，再根据 CMakeList.txt 文件生成目标平台所需的编译文件。这个编译文件，在类UNIX平台就是 Makefile，在 Windows 平台就是 Visual Studio 工程，macOS 里还可以生成 Xcode 工程。所以，你可以使用熟悉的 Xcode 来编译 Clang。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/86/c9e17412.jpg" width="30px"><span>Sam</span> 👍（1） 💬（1）<div>只会 c 可以进行插件开发吗？</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/34/40/a84b6612.jpg" width="30px"><span>FR</span> 👍（10） 💬（3）<div>同问，苹果新推出swiftUI还有意义吗</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b1/75/60a71bbd.jpg" width="30px"><span>Ankhetsin</span> 👍（6） 💬（1）<div>如何评价苹果新出的SwiftUI</div>2019-06-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVegfjqa0gM4hcRrBhZkIf7Uc5oeTMYsg6o5pd76IQlUoIIh2ic6P22xVEFtRnAzjyLtiaPVstkKug/132" width="30px"><span>xilie</span> 👍（3） 💬（2）<div>老师，请假个问题，热更新的很多方案都被苹果封了，其中有一个没开源的，据说手机 QQ ，他们通过 clang 把 OC 代码编译成自己定制的字节码动态下发，然后开发一个虚拟机去执行（惊呆了），同样实现了原生开发，动态运行。

我自己试了一下，runtime可以动态生成类、属性、方法，但是怎么动态生成方法的实现（IMP）呢？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b9/58/c6c74278.jpg" width="30px"><span>Chauncey</span> 👍（1） 💬（0）<div>macOS不能说是类unix好吧，是真正的unix分支啊</div>2019-06-14</li><br/><li><img src="" width="30px"><span>Geek_ac42dc</span> 👍（0） 💬（0）<div>这个可以使用ninja 编译 ，Xcode 编译速度有点慢啊</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/0b/2ccf7908.jpg" width="30px"><span>...</span> 👍（0） 💬（0）<div>方法名混淆后审核会有影响吗</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/f1/54575096.jpg" width="30px"><span>Master</span> 👍（0） 💬（0）<div>老师，您好！
cmake -G Xcode -DLLVM_ENABLE_PROJECTS=clang ..&#47;llvm
我使用上面这个命令来构建 xcode project，scheme 和 文件目录下一个 clang 相关的内容都没有，这是为何？我的 Xcode 版本是 11。
网上找了其他人相关教程，与您讲的步骤不完全一样，试着他们的做法，也还是一样。求助</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/b7/87da0cc1.jpg" width="30px"><span>苹果直播网体育</span> 👍（0） 💬（2）<div>没有写如何将 .cpp 生成 .dylib 吧</div>2019-08-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJC2enzAlVibSfsP03Pk1ueNHzbDUn9JQrwAK9OwJkLRjpR2jffanXqf8nMwkl4SqERBCiadqMr85CA/132" width="30px"><span>Geek__f56783130103</span> 👍（0） 💬（0）<div>[ 72%] Built target clangCrossTU
make[2]: *** No rule to make target `ClangOpenCLBuiltinsImpl&#39;, needed by `tools&#47;clang&#47;lib&#47;Sema&#47;CMakeFiles&#47;obj.clangSema.dir&#47;SemaLookup.cpp.o&#39;.  Stop.
make[1]: *** [tools&#47;clang&#47;lib&#47;Sema&#47;CMakeFiles&#47;obj.clangSema.dir&#47;all] Error 2
make: *** [all] Error 2</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/40/c3c00fe2.jpg" width="30px"><span>云无心</span> 👍（0） 💬（0）<div>学习了</div>2019-06-04</li><br/>
</ul>