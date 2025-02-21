你好，我是蒋宏伟。

上一讲我们说到，搭建页面的第一步是搭建静态页面，拿到设计稿后要从上往下拆成组件，再从下往上把组件进行实现。

但组件只是页面的架子。如果你不使用任何样式，组件只能遵循默认的布局规则、默认字号颜色，铺在屏幕上，看起来就像调试的 log 信息一样，也没有什么体验可言。

俗话说人靠衣装、佛靠金装，页面体验要好就离不开样式的帮助。大家对 App 的第一印象，就是对页面样式的第一印象。虽说样式设计上是由设计师负责，但最终落地还得靠代码。如何把设计师给的设计稿在不同大小的机型上还原实现，通过验收，是工作中实实在在要面对的考验。

还原设计稿还只是最基本的要求，作为开发者，你还得要关心开发成本、可维护性、布局性能等事情。比如，有哪些样式库可以节约开发成本？代码量大了需求有变动，样式怎么改起来更方便？React Native 的布局性能究竟怎样，多层嵌套的复杂布局会不会导致性能问题？

所以今天，围绕着上面这些话题，我和你一起聊聊，关于样式你需要知道的三件事：

- React Native 组件样式都有哪些？
- React Native 的 Flex 布局有哪些特点？
- React Native 样式代码如何管理？

## 组件样式 = 通用样式 + “私有”样式
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/d0/b9/4870af0b.jpg" width="30px"><span>AEPKILL</span> 👍（11） 💬（2）<div>设置 Text 默认样式之前我们用的非常 hack 的方案，是这样写的:
```tsx
&#47;&#47; fix: 安卓 Text 组件的文字会被截断
&#47;&#47; issue: https:&#47;&#47;github.com&#47;facebook&#47;react-native&#47;issues&#47;15114
if (RN.Platform.OS === &#39;android&#39;) {
  const defaultFontFamily = {
    fontFamily: &#39;&#39;,
    &#47;&#47; fix: 部分安卓机器上的主题会设置系统字体颜色为白色
    color: &#39;#000&#39;,
  };
  const OldTextRender = (RN.Text as any).render;
  (RN.Text as any).render = (props: any, ref: any) =&gt; {
    const {style} = props;
    return OldTextRender(
      {
        ...props,
        style: RN.StyleSheet.compose(defaultFontFamily, style),
      },
      ref
    );
  };
}

```

</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（1） 💬（1）<div>includeFontPadding: false, textAlignVertical: &#39;center&#39;,

这是说的android 字体居中的问题的处理吗</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d0/b9/4870af0b.jpg" width="30px"><span>AEPKILL</span> 👍（1） 💬（1）<div>请问该如何实现图文混排类似 float: left 这种效果?</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/dd/21ab7107.jpg" width="30px"><span>Archer_Shu</span> 👍（0） 💬（1）<div>设计部门如果缺失开发背景，设计的组件属性不统一（比如文字标题使用多种字体和颜色），导致更多时候只能使用绝对定位。开发和QA也因此难以使用可复用的样式。最终也就导致了代码的冗长以及难以维护。</div>2022-04-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ergUHnv5Vl1G10iaSiaGZ2FDJ4f3qCAWvQzLRkmxLAtfMPuDial5fI8tjSOsMNMicUMAeQKTibEbx71EbA/132" width="30px"><span>yuxizhe</span> 👍（0） 💬（1）<div>请问 Text 组件设置全局默认样式，一般是用组件进行封装，相当于每个Text都会重新调用 StyleSheet 来生成样式，会有性能问题么？</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e3/76/4c8da01e.jpg" width="30px"><span>hawksun</span> 👍（0） 💬（2）<div>写样式的时候怎么处理不同机型适配的问题呢？</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（2） 💬（0）<div>作业2:
方法1. 封装通用 Text 组件
方法2: 重写 Text 组件的 Render 方法</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ad/92/98a1fd3c.jpg" width="30px"><span>Geek_e4a05b</span> 👍（1） 💬（2）<div>瀑布流目前开源的MasonryList使用的是Flatlist嵌套左右两个Flatlist方式。这种方式在数据变多快速滑动情况下白屏现象严重，请问老师有什么好的实现方式吗？</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/35/f6/fc3881e7.jpg" width="30px"><span>稀饭</span> 👍（0） 💬（0）<div>作业一没有参考答案吗？</div>2024-09-20</li><br/><li><img src="" width="30px"><span>Geek_cf32ac</span> 👍（0） 💬（0）<div>使用 React Native 提供的 &quot;Text.defaultProps&quot; 属性。这个属性允许设置 Text 组件的默认属性，包括样式。
import { Text } from &#39;react-native&#39;;

Text.defaultProps = Text.defaultProps || {};
Text.defaultProps.style = { fontFamily: &#39;Arial&#39;, fontSize: 16 };</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/62/a8/05dee453.jpg" width="30px"><span>风会停息</span> 👍（0） 💬（1）<div>老师您好，我想问下，RN的原理不是相当于说  用JS描述ui然后底层其实是映射的原生api去实现的吗，原生的api再去进行渲染绘制，也就是说最后运行的时候Android还是绘制的原生View 使用Android的引擎 ios也一样用ios的引擎，那么为什么还说React Native 的布局引擎 Yoga， 是 Android、iOS 通用的，如何做到的呢？</div>2023-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e7/35/ba2cc0d7.jpg" width="30px"><span>王昭策</span> 👍（0） 💬（0）<div>学完react的直接来听老师的这些课可以吗？</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/86/ba472895.jpg" width="30px"><span>黄金分割</span> 👍（0） 💬（0）<div>关于第二个问题, 我们不能直接简单的直接使用react native自带的text组件, 需要对text进行封装.
这里需要和ui同事沟通好, 定制统一的字体, 字重, 大小的规格.
在自己的text组件中自己枚举所有的规格参数.
使用时直接根据ui的规格引用自己的规格参数即可.</div>2022-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/8e/e75ecc5e.jpg" width="30px"><span>浩明啦</span> 👍（0） 💬（0）<div>老师，使用tailwind 来写会不会更好维护呢</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/6e/d0/6875ea5a.jpg" width="30px"><span>小天儿</span> 👍（0） 💬（1）<div>老师，我是初学者，抱歉，这个作业想了很久还是没想出来如何实现，`Image`组件在使用的时候好像必须指定固定宽高，否则图片就不显示了，这个到底是怎么做到的呀</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/c5/a64b3217.jpg" width="30px"><span>一方天涯</span> 👍（0） 💬（1）<div>如果你要给 Text 组件设置全局的默认样式，比如字体，你会怎么设置？
项目中恰好有这个需求，本来打算重写Text.render方法，然而很奇怪重写的render不生效，最后只能自定义一个Text解决……</div>2022-04-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ergUHnv5Vl1G10iaSiaGZ2FDJ4f3qCAWvQzLRkmxLAtfMPuDial5fI8tjSOsMNMicUMAeQKTibEbx71EbA/132" width="30px"><span>yuxizhe</span> 👍（0） 💬（4）<div>请问 inline-block 行内元素怎么实现呢？比如多行文字内加个有样式的tag ，很麻烦。Text也不支持margin</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4b/37/97caebe6.jpg" width="30px"><span>D先生</span> 👍（0） 💬（1）<div>设置全局默认样式的话，我会默认封装一个MyText组件，然后内置一些样式，同时提供通过props覆盖默认样式的能力</div>2022-04-01</li><br/>
</ul>