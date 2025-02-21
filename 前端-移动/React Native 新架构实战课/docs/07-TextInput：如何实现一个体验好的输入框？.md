你好，我是蒋宏伟。

上一讲，我们介绍了如何去打磨点按组件的体验细节，这一讲我们就开始介绍如何打磨一个文本输入组件 TextInput 的体验细节。

作为一个优秀工程师，要想优化页面的用户体验，只知道打磨点按组件是远远不够的，而且，相对于点按组件组件来说，要把文本输入组件 TextInput 的细节体验弄好，要更难一些。

这个难点主要有两方面。首先，TextInput 组件是自带状态的宿主组件。TextInput 输入框中的文字状态、光标状态、焦点状态在 React Native 的 JavaScript 框架层的框架层有一份，在 Native 的还有一份，有时候业务代码中还有一份。那多份状态到底以谁为主呢？这件事我们得搞清楚。

其次，TextInput 组件和键盘是联动的，在处理好 TextInput 组件的同时，我们还得关心一下键盘。当然键盘本身是有 `Keyboard` API 的，但是键盘类型是“普通键盘”还是“纯数字键盘”，或者键盘右下角的按钮文字是“确定”还是“搜索”，都是由 TextInput 组件控制的。

这一讲，我将以如何实现一个体验好的输入框为线索，和你介绍使用 TextInput 组件应该知道的三件事。

## 输入框的文字

第一件事，你得知道如何处理输入框的文字。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/d0/b9/4870af0b.jpg" width="30px"><span>AEPKILL</span> 👍（8） 💬（3）<div>iOS 模拟器也是可以弹出键盘的，只要把 Hardware -&gt; Keyboard -&gt; Connect HardWare KeyBoard 的勾去掉就可以了。
验证码组件我的思路是这样的:
1. 放置一个隐藏的 TextInput
2. 画短信验证码输入的 UI (其实就是几个格子)
3. 点击验证码 UI 的时候调用 textInptRef.focus()
4. 接受输入，划到对应的验证码格子里

完整代码: https:&#47;&#47;gist.github.com&#47;AEPKILL&#47;3557c4b5b621a3aec36e7e3cd8571e56</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/6e/d0/6875ea5a.jpg" width="30px"><span>小天儿</span> 👍（3） 💬（1）<div>老师，TextInput 间进行跳转时，键盘总是会先收起再弹出，而在某些应用中，多个输入框之间跳转是不会收起键盘的，如何解决这个问题呢？</div>2022-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（3）<div>1， 新手，代码 https:&#47;&#47;github.com&#47;hdouhua&#47;hybrid-mobile-app&#47;tree&#47;main&#47;AwesomeProject&#47;src&#47;c07。
2，不知道怎么的，在文档里找不到 TextInput 的方法 onChangeSync</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4c/fd/2e4cd48f.jpg" width="30px"><span>见字如晤</span> 👍（2） 💬（0）<div>还有一个特别重要的细节是，输入框与键盘的位置。键盘弹起的时候，是否有遮盖输入框的表现；如果没有，键盘会不会把整个页面往上顶起；Android和iOS表现这方面表现是否一致</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a1/14/b487945f.jpg" width="30px"><span>Zeke</span> 👍（0） 💬（0）<div>并没有 `onChangeSync` 这个方法，从 RN 官网没有找到有这个，只有 onChange 和 onChangeText </div>2024-10-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJsnP3W12jSoGYBoAbjMW7kKqWsD1Imnic4TX9nOR0kvkTq5ap4n0aNfuicXibKDJib0zl0PEvhcBHe3g/132" width="30px"><span>demoker</span> 👍（0） 💬（0）<div>下载的demo在iPhone上运行报错呢？Invariant Violation: requireNativeComponent: &quot;RTNCustomView&quot; was not found in the UIManager.</div>2023-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ba/5c/ca8f01b4.jpg" width="30px"><span>Wcly👺</span> 👍（0） 💬（0）<div>要做一个文本编辑器，怎么控制光标适中在可视区域，就是横向输入长文本到输入框的时候能自动横向滚动，垂直换行的时候能自动垂直滚动，类似vscode的编辑页面。</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/fa/b88b8b4e.jpg" width="30px"><span>郭浩</span> 👍（0） 💬（0）<div>TextInput是不是没法禁止它复制粘贴？在Android上不生效</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（0）<div>“但是 Fabric 之后（包括 Fabric 预览版），setNativeProps 就不能用了。”

有传送门吗？</div>2022-07-05</li><br/><li><img src="https://thirdqq.qlogo.cn/qqapp/101423631/0FD57A9C0C5BFBDA3DA69AE26B3514FB/100" width="30px"><span>下一刻。</span> 👍（0） 💬（0）<div>老师问一下：TextInput如何插入图片（自定义表情），如何使不同段的文字颜色不一样（话题）。</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/6e/d0/6875ea5a.jpg" width="30px"><span>小天儿</span> 👍（0） 💬（0）<div>1. 代码：https:&#47;&#47;snack.expo.dev&#47;@sh-winter&#47;textinput
2. onChnage 与 onChangeSync 的区别：个人认为 onChangeSync 比 onChange 响应的更快，适用于更高优先级的场景；Fabric 同步的特性与 react 18 结合将带来并发渲染，可中断渲染等新特性，实现在大规模 UI 更新时保持响应</div>2022-05-16</li><br/>
</ul>