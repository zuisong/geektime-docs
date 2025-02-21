你好，我是术子米德，是一名边干边学、边学边想、边想边干的码农。如今工龄20+，依然在代码一线奋战。

最近几个月，我在探索基于AIGC的代码开发，采用GitHub的Copilot结合TDD方法，在实践中摸索代码助手的效果。在得出自己的初步结论，并冒出更多问题的时候，和这门徐8叉老师的课不期而遇。

于是，我边干边学、边学边想、边想边干的劲头更足了。现在还在兴奋状态，特别想把我的探索经验和课程带来的启发分享一下，期望也能激发你的兴趣。

## 老“码农”遇到新局面

先展示一个采用Copilot写测试代码的阶段性成果。在我探索用Copilot进行代码开发，多轮迭代改进之后，总结了一个注释型提示词模板，你有兴趣的话，不妨打开文稿看一眼。

```typescript
//===TEMPLATE OF UT CASE===
/**
 * @[Name]: ${verifyBehivorX_byDoABC}
 * @[Purpose]: ${according to what in SPEC, and why to verify in this way}
 * @[Steps]: ${how to do}
 *   1) do ..., with ..., as SETUP
 *   2) do ..., with ..., as BEHAVIOR
 *   3) do ..., with ..., as VERIFY
 *   4) do ..., with ..., as CLEANUP
 * @[Expect]: ${how to verify}
 * @[Notes]:
 */
TEST(UT_NameOfCategory, CaseNN_verifyBehivorX_byDoABC) {
  //===SETUP===
  // 1. ...

  //===BEHAVIOR===
  //@VerifyPoint xN(each case MAY have many 'ASSERT_XYZ' check points)

  //===VERIFY===
  //@KeyVerifyPoint<=3(each case SHOULD has less than 3 key 'ASSERT_XYZ' verify points)

  //===CLEANUP===
}
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/c8/79/0e91a8bd.jpg" width="30px"><span>Aoinatsume</span> 👍（0） 💬（0）<div>很好的分享，很有启发，太棒了！</div>2024-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/30/4a/5b1d1018.jpg" width="30px"><span>zhsky</span> 👍（0） 💬（0）<div>米德大哥分享的太棒了，争取一起坐上AI这辆时代的列车，抵达软件开发更美好的彼岸</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（0） 💬（1）<div>空手道项目，蹲个 github 链接，哈哈哈，好不好？</div>2024-05-28</li><br/>
</ul>