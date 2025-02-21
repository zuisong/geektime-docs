你好，我是李程远。很高兴受邀来到这门课做一期分享。如果你之前学过极客时间上的另一个专栏[《容器实战高手课》](https://time.geekbang.org/column/intro/100063801?tab=catalog)，应该会对我比较熟悉。

今天想跟你聊的，是一些我自己关于用 eBPF 进行系统黑盒诊断的思考，特别是在云原生平台上的应用。从 2014 年进入到 Linux 内核以来，eBPF 一直是 Linux 内核中最火的领域。作为 eBPF 的三大应用领域之一，在 Linux 内核的追踪/调试中，特别是在云平台来定位一些复杂问题时，eBPF 已经处于不可替代的地位了。

在《容器实战高手课》的一篇[加餐](https://time.geekbang.org/column/article/341820)里，我也简单介绍过 eBPF 这个技术。当时我给了同学们一个例子，通过它看了如何用 eBPF 来定位我们生产环境中的数据包网络延时偶尔增大的原因。最近，我又碰到一个生产环境中的网络问题，仍然还是依靠 eBPF 程序的帮助，定位到了原因。今天，我就先跟你分享下这个问题的具体情况，以及用 eBPF 定位原因的过程。然后，我会从这个例子出发，聊聊 eBPF 程序可以怎样更好地在云原生平台上应用。

## 一个例子：用eBPF解决生产环境中的网络问题

关于遇到的这个问题，先来说一下我看到的现象。

把线上的问题简化之后，我看到 Client 向一个 Server Pod 里的服务上传数据的时候，偶尔连接会发生中断。通过对 Server Pod 所在的宿主机节点上 tcpdump 数据包的抓取，我们会看到，从 Server Pod 向 Client 发送了一个 TCP RST(reset) 数据包之后，上传数据的连接就中断了。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（12） 💬（0）<div>一纵一横，直击要点。

李老师是 eBPF 实战派高手，深谙底层技术原理，《容器实战高手课》加餐篇可见一斑。曾受益匪浅，再次表达感谢与钦佩。</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（1） 💬（0）<div>老师之前出的专栏学习完了，功力深厚啊。另外关于老师提到的纵，深表认同，一直想掌握，但是不知如何下手。</div>2022-08-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/9dQtP7dtB4KRg1N3YOuadm01w2lW31a4CUibrKbpibQxSicrKmVDI5wMfq97aFIAncCR6xibfia4RicK5aIZON7Oz7RQ/132" width="30px"><span>DBA_Roland</span> 👍（1） 💬（0）<div>请问老师：“纵”的学习，有没有好的学习资料或课程？</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>根本枝叶论</div>2022-09-17</li><br/>
</ul>