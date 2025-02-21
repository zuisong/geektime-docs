你好，我是陈航。今天，我来和你聊聊如何在原生应用中接入Flutter。

在前面两篇文章中，我与你分享了如何在Dart层引入Android/iOS平台特定的能力，来提升App的功能体验。

使用Flutter从头开始写一个App，是一件轻松惬意的事情。但，对于成熟产品来说，完全摒弃原有App的历史沉淀，而全面转向Flutter并不现实。用Flutter去统一iOS/Android技术栈，把它作为已有原生App的扩展能力，通过逐步试验有序推进从而提升终端开发效率，可能才是现阶段Flutter最具吸引力的地方。

那么，Flutter工程与原生工程该如何组织管理？不同平台的Flutter工程打包构建产物该如何抽取封装？封装后的产物该如何引入原生工程？原生工程又该如何使用封装后的Flutter能力？

这些问题使得在已有原生App中接入Flutter看似并不是一件容易的事情。那接下来，我就和你介绍下如何在原生App中以最自然的方式接入Flutter。

## 准备工作

既然是要在原生应用中混编Flutter，相信你一定已经准备好原生应用工程来实施今天的改造了。如果你还没有准备好也没关系，我会以一个最小化的示例和你演示这个改造过程。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_a9f943</span> 👍（5） 💬（2）<div>如果在flutter中添加了第三方依赖，打包时就会报错，所以这种方式本质上还是不适用于混合开发。最理想的状态是将flutter作为一个单独的项目，然后把最终产物提供给android，ios，这样原生的开发人员也不需要安装flutter运行环境。这一节可以当作是混合开发的预习，希望老师后续能把混合开发讲的更彻底一些，毕竟这才是flutter存在的主要目的</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/c8/773ff168.jpg" width="30px"><span>千の星</span> 👍（3） 💬（2）<div>老师，按照您的混编方法，再 flutter build apk --release，之后生产的aar&#47;assets&#47;flutter_assets&#47;,里面缺少isolate_snapshot_data，isolate_snapshot_instr，vm_snapshot_data，vm_snapshot_instr。aar拷贝到公司nativeapp运行到flutter就会报错：Abort message: &#39;[FATAL:flutter&#47;shell&#47;common&#47;shell.cc(218)] Check failed: vm. Must be able to initialize the VM.。请问是缺少什么环节
或者配置吗</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/7f/c50d520e.jpg" width="30px"><span>颜为晨</span> 👍（2） 💬（1）<div>包体积最少会增加多少呢？</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（2） 💬（2）<div>老师，三端分离的话，是要建三个git仓库吗？还是有什么其它的方式管理？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（1） 💬（1）<div>老师，发现了一种依赖源码的方式，不用打包aar再引用这么麻烦了，非常适合小团队开发。https:&#47;&#47;github.com&#47;flutter&#47;flutter&#47;wiki&#47;Add-Flutter-to-existing-apps，官方出的依赖flutter module源码的方式，直接run就可以的，今天实测了一下，没有问题</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（1） 💬（2）<div>flutter build ios --debug
打出来的 Flutter.framework 没有 Header 文件夹</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/45/9aa91b75.jpg" width="30px"><span>矮个子先生😝</span> 👍（1） 💬（1）<div>对于flutter module的测试,可以手动添加入口,以IDEA为例,add configurations-&gt; + -&gt;flutter -&gt;
name随便取个标识,Dart entrypoint指明入口dart文件,比如main.dart,其他不用管,这样可以边编写flutter时边看效果了</div>2019-09-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLDYJY1Eibric4sxmtzgTbdWOspnqZ7dRUOBtKbghf2KUELG4CfP6p66q1TD8T0ico9mAvvfcwJU5V4ibw/132" width="30px"><span>啥玩意儿啊</span> 👍（0） 💬（2）<div>老师,ios启动后白屏
Engine run configuration was invalid.
Could not launch engine with configuration.
是打包环节出现问题了吗</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/d6/5edc9af1.jpg" width="30px"><span>八面玲珑</span> 👍（0） 💬（1）<div>老师，iOS 构建报这个错怎么处理呀
BUILD TARGET Runner OF PROJECT Runner WITH CONFIGURATION Debug ===
    Code Signing Error: No profiles for &#39;com.****.***&#39; were
    found:  Xcode couldn&#39;t find any iOS App Development provisioning profiles
    matching &#39;com.lvdingtao.blackHoleModule&#39;. Automatic signing is disabled and
    unable to generate a profile. To enable automatic signing, pass
    -allowProvisioningUpdates to xcodebuild.</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/04/ada1734e.jpg" width="30px"><span>17岁码农想当架构师</span> 👍（0） 💬（1）<div>为什么从安卓原生工程进入flutter页面时先是黑屏一会儿，然后才出来页面？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/f9/af80b4da.jpg" width="30px"><span>谭鹏</span> 👍（0） 💬（1）<div>Flutter.framework里面 没有headers 文件夹    clean了好多遍  </div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/f9/af80b4da.jpg" width="30px"><span>谭鹏</span> 👍（0） 💬（2）<div>Flutter build ios 后 没有发现app 和 flutter framework</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/f9/af80b4da.jpg" width="30px"><span>谭鹏</span> 👍（0） 💬（1）<div>Flutter_library 是什么目录</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8a/97/7ab3a22c.jpg" width="30px"><span>蜥蜴1214</span> 👍（0） 💬（1）<div>老师，我flutter项目通过
Flutter build apk --debug打包后。aar只有9.7m。添加到安卓项目后运行，会报错误: 无法访问FlutterView
找不到io.flutter.view.FlutterView的类文件。</div>2019-11-18</li><br/><li><img src="" width="30px"><span>Geek_0ea3e4</span> 👍（0） 💬（1）<div>我执行Flutter create -t module flutter_library  为什么没有生产那么多文件？bogon:Documents liudongdong$ Flutter create -t module flutter_library
Creating project flutter_library...
  flutter_library&#47;test&#47;widget_test.dart (created)
  flutter_library&#47;flutter_library.iml (created)
  flutter_library&#47;.gitignore (created)
  flutter_library&#47;.metadata (created)
  flutter_library&#47;pubspec.yaml (created)
  flutter_library&#47;README.md (created)
  flutter_library&#47;lib&#47;main.dart (created)
  flutter_library&#47;flutter_library_android.iml (created)
  flutter_library&#47;.idea&#47;libraries&#47;Flutter_for_Android.xml (created)
  flutter_library&#47;.idea&#47;libraries&#47;Dart_SDK.xml (created)
  flutter_library&#47;.idea&#47;modules.xml (created)
  flutter_library&#47;.idea&#47;workspace.xml (created)
Running &quot;flutter pub get&quot; in flutter_library...                    14.5s</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/13/2afd6bdb.jpg" width="30px"><span>AmazingYu</span> 👍（0） 💬（1）<div>三端分离后，Flutter 工程怎么依赖 iOS 原生工程呢？</div>2019-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJ3dLlYr6tznfnZXJNsD7Jw48BVnFSib3RO3VWEN0pgebRY1jaR8YXLQ6iaAjTsFiamOWSA3UPAa37A/132" width="30px"><span>Geek_e7jq8k</span> 👍（0） 💬（1）<div>请问下 Flutter build ios --debug 出来的包，是没有X86_64架构的，是需要在打一个Flutter build ios --debug --simulator的包，然后把所有的plungin以及App.framework 自己来lipo合并下么？ 同样 使用Flutter build ios --release 中Flutter.framework 中又包含了X86_64架构，也需要手动的lipo删除么？ 这两个问题是需要我们自己来使用lipo操作 还是系统提供了什么支持？</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b5/c6/d39d31b0.jpg" width="30px"><span>zjhuang</span> 👍（0） 💬（1）<div>如何将Flutter Module抽离出原有工程的Git仓库，将Flutter Module放到另一个Git仓库（目的是Android、iOS共用 Flutter 的lib）。即如何将 Flutter Module 的Git 仓库放在原工程的Git目录下？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/17/fdc5d955.jpg" width="30px"><span>汉之风云</span> 👍（0） 💬（1）<div>老师，为啥打出来的debug aar包里面没有Flutter.jar呢</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（0） 💬（1）<div>flutter build ios --debug 
生成的 Flutter.framework 没有 Header 文件夹
请问这个问题有遇到过吗</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（0） 💬（1）<div>老师，有个问题，如果每次flutter的代码都要导出成aar，放到libs下面给native工程依赖的话，调试是不是太麻烦了，而且，flutter debug模式下打出来的aar都是很大的，这个aar到底要不要纳入Git或者SVN管理？我感觉正常的流程（虽然现在IDE不支持，没法实现）应该是像Android中C&#47;C++和Java混合编译（NDK）的模式一样，每次run的时候，编译一堆东西到build底下，我们管理的都是代码。</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>发现个问题，在有些 Android 手机上用这种方式在 Android 工程里面引用 flutter 页面，加载的时候会先黑屏然后才能加载成功 flutter 页面，老师这是为什么呢？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/55/fb/95e360b5.jpg" width="30px"><span>周斌</span> 👍（0） 💬（1）<div>老师您好，请问如何在原生的activity中只引用一个可以控制大小和形状的container呢</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/17/3cc47076.jpg" width="30px"><span>柯昌合</span> 👍（0） 💬（1）<div>老师，flutter支持armv5 架构的cpu吗</div>2019-09-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJ3dLlYr6tznfnZXJNsD7Jw48BVnFSib3RO3VWEN0pgebRY1jaR8YXLQ6iaAjTsFiamOWSA3UPAa37A/132" width="30px"><span>Geek_e7jq8k</span> 👍（0） 💬（1）<div>您好，请问老师在上述的讲解中，iOS打包使用了build iOS --debug这个命令，请问下这个的命令可以简单的理解为执行 xcode_backend.sh + 签名这两个功能么？如果想和公司内部的CI流程协同的话，有些时候是不能直接获取到证书的，这种时候是不是只能使用xcode_backend.sh来生成framework，这两种方式生成的有什么区别呢？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/64/d88cd94b.jpg" width="30px"><span>Lhh</span> 👍（0） 💬（1）<div>老师 执行Flutter build apk --debug后得到的是apk而不是aar 是需要对build.gradle进行修改吗</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/32/31/449513a1.jpg" width="30px"><span>CarlXu</span> 👍（0） 💬（2）<div>在开发阶段，开发调试的时候如何让原生页面的数据和flutter模块页面数据进行传递呢？如果每次都要打包好再pod进入原生项目调试，效率会非常低了</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/7f/c50d520e.jpg" width="30px"><span>颜为晨</span> 👍（0） 💬（1）<div>“Flutter create -t module Flutter_library”，flutter_library 应该是小写</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/45/9aa91b75.jpg" width="30px"><span>矮个子先生😝</span> 👍（0） 💬（1）<div>- (void)touchesBegan:(NSSet&lt;UITouch *&gt; *)touches withEvent:(UIEvent *)event {
    FlutterViewController *vc = [[FlutterViewController alloc] init];
    [vc setInitialRoute:@&quot;custome&quot;]; &#47;&#47; 路由标识符
    
    FlutterViewController *vc2 = [[FlutterViewController alloc] init];
    [vc2 setInitialRoute:@&quot;custome2&quot;]; &#47;&#47; 路由标识符
    [self.navigationController pushViewController:vc animated:YES];
}
老师,为什么在创建vc2之后,但是没有使用,运行直接崩溃,不创建vc2,只创建vc则不会有问题.</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/45/9aa91b75.jpg" width="30px"><span>矮个子先生😝</span> 👍（0） 💬（1）<div>先自己用脚本写了部分CI功能,看看和老师后面讲的有哪些需要改进的、未做的

#f flutter_library库,p 存放依赖库的pod文件夹  d编译模式 debug release v:flutter pod version
#.&#47;build.sh -v x -f x -p -d x
#支持写死文件路径,或者通过参数传递路径
# .&#47;user.sh -f flutter_library -p NativeEmbedFlutterDemo&#47;FlutterEngine -v 1.1.1 -d debug -i YES

SCRIPT_PATH=$(cd &quot;$(dirname &quot;$0&quot;)&quot;; pwd) #脚本路径

fpath=&quot;flutter_library&quot;
ppath=&quot;NativeEmbedFlutterDemo&#47;FlutterEngine&quot;
debug=&quot;debug&quot;
version=&#39;0.0.1&#39;
#是否执行pod install,在更新完flutter文件之后,除了第一次需要install,其他时候都不需要
install=&quot;YES&quot;
echo &quot;${fpath}&quot;
while getopts &quot;:f:p:d:v:i:&quot; opt
do
    case $opt in
        f)
        fpath=&quot;$OPTARG&quot;
        ;;
        p)
        ppath=&quot;$OPTARG&quot;
        ;;
        d)
        # 大写转小写
        debug=$(echo &quot;$OPTARG&quot; | tr &#39;A-Z&#39; &#39;a-z&#39;)
        ;;
        v)
        version=&quot;$OPTARG&quot;
        ;;
        i)
        install=&quot;$OPTARG&quot;
        ;;
        ?)
        echo &quot;未知参数&quot;
        exit 1;;
    esac
done

if [[ $debug == debug ]]
then
debug=&quot;flutter build ios --${debug}&quot;
else
#默认为release模式
debug=&quot;flutter build ios&quot;
fi
echo &quot;$debug&quot;

#echo &quot;$SCRIPT_PATH&quot;
if [[ $fpath != *$SCRIPT_PATH* ]]
then
    fpath=&quot;${SCRIPT_PATH}&#47;${fpath}&quot;
fi
echo &quot;${fpath}&quot;

if [[ $ppath != *$SCRIPT_PATH* ]]
then
ppath=&quot;${SCRIPT_PATH}&#47;${ppath}&quot;
fi
echo &quot;${ppath}&quot;

cd &quot;${fpath}&quot;
#执行字符串命令 打包flutter组件
${debug}

#build的两个flutter产物
buildPath=&quot;${fpath}&#47;.ios&#47;Flutter&quot;
fappPath=&quot;${buildPath}&#47;App.framework&quot;
#echo &quot;fappPath=${fappPath}&quot;
fflutterPath=&quot;${buildPath}&#47;engine&#47;Flutter.framework&quot;

#先删掉旧的,直接覆盖存在问题
if [ -d &quot;${ppath}&#47;App.framework&quot; ]
then
rm -rf &quot;${ppath}&#47;App.framework&quot;
fi

if [ -d &quot;${ppath}&#47;Flutter.framework&quot; ]
then
rm -rf &quot;${ppath}&#47;Flutter.framework&quot;
fi

#拷贝文件 目录拷贝 -R
cp -R -f &quot;${fappPath}&quot; &quot;${ppath}&quot;
cp -R -f &quot;${fflutterPath}&quot; &quot;${ppath}&quot;

cd &quot;${ppath}&quot;


#是否执行install
if [[ $(echo &quot;$install&quot; | tr &#39;A-Z&#39; &#39;a-z&#39;) == y* ]]
then
pod lib lint --no-clean
pod install
fi</div>2019-09-04</li><br/>
</ul>