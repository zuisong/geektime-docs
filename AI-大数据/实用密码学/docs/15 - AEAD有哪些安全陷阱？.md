你好，我是范学雷。

上一讲，我们讨论了加密数据如何才能够自我验证，自我验证就是指解密的时候，还能够同时检验数据的完整性。我们还谈到了带关联数据的认证加密（AEAD）是目前市场的主流思路。

我们有了带关联的认证加密算法，应用程序再也不需要自行设计、解决数据的完整性问题了。但问题是，如果我们要在应用程序中使用带关联数据的认证加密，有哪些算法可以使用？

带关联数据的认证加密算法，有没有需要小心的安全陷阱？这是我们这一次需要解决的问题。

## 有哪些常见的算法？

还是老规矩，我们先来看看有哪些常见的算法。现在，常见的AEAD模式有三种：

- GCM；
- CCM；
- Poly1305。

一般地，我们可以把带关联数据的认证加密看做一个加密模式，就像CBC模式一样，我们可以和前面提到的AES等加密算法进行组合。但ChaCha20和Poly1305通常组合在一起；Camellia与AES通常和GCM以及CCM组合在一起。

由于AEAD模式相对较新，而3DES/DES等遗留或者退役算法又存在明显的安全缺陷，所以，我们一般不会使用遗留或者退役算法的AEAD模式。

如果我们重新整理一下，综合考虑加密算法和加密模式，那么，当前推荐使用的、有广泛支持的、风险最小的算法是：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/b5/32374f93.jpg" width="30px"><span>可怜大灰狼</span> 👍（2） 💬（1）<div>1.密钥固定不变
2.密钥定期变化，但是没用初始化向量
3.用上了初始化向量，但是这个向量是固定值
4.没用MAC，没用AEAD
完了，完了，该犯的问题，都有了。</div>2020-12-28</li><br/><li><img src="" width="30px"><span>韩露</span> 👍（1） 💬（2）<div>AEAD 模式能跟国密算法结合吗？现在都在提倡国产化，如果不能跟国密算法结合，还是用不了AEAD模式。</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（4）<div>老师，后面讲完 非对称加密，可以再来个密码学应用实战，把这些理论知识实践上</div>2022-08-12</li><br/><li><img src="" width="30px"><span>harryZ</span> 👍（0） 💬（2）<div>对于国密老师什么时候开个专题</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cb/6f/b6693f43.jpg" width="30px"><span>Litt1eQ</span> 👍（3） 💬（1）<div>想到了802.11当中的wep算法采用了24位的初始化向量与同一把密钥进行运算 从而导致了严重的安全问题</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>初始化向量的重复问题，就是使用 AEAD 算法的最大风险，也是最难处理的风险。--记下来</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-11-10</li><br/>
</ul>