你好，我是LMOS。

上节课，我们一起了解了套接字的工作机制和数据结构，但套接字有哪些基本接口实现呢？相信学完这节课，你就能够解决这个问题了。

今天我会和你探讨套接字从创建、协议接口注册与初始化过程，还会为你深入分析套接字系统，是怎样调用各个功能函数的。通过这节课，相信你可以学会基于套接字来编写网络应用程序。有了之前的基础，想理解这节课并不难，让我们正式开始吧。

## 套接字接口

套接字接口最初是BSD操作系统的一部分，在应用层与TCP/IP协议栈之间接供了一套标准的独立于协议的接口。

Linux内核实现的套接字接口，将UNIX的“一切都是文件操作”的概念应用在了网络连接访问上，让应用程序可以用常规文件操作API访问网络连接。

从TCP/IP协议栈的角度来看，传输层以上的都是应用程序的一部分，Linux与传统的UNIX类似，TCP/IP协议栈驻留在内核中，与内核的其他组件共享内存。传输层以上执行的网络功能，都是在用户地址空间完成的。

Linux使用内核套接字概念与用户空间套接字通信，这样可以让实现和操作变得更简单。Linux提供了一套API和套接字数据结构，这些服务向下与内核接口对接，向上与用户空间接口对接，应用程序正是使用这一套API访问内核中的网络功能。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（5） 💬（1）<div>四次挥手过程分析下【V5.8，正常流程】
5、客户端收到FIN包，子状态从TCP_FIN_WAIT2变为TCP_TIME_WAIT，返回ACK包
A、状态和子状态都为TCP_TIME_WAIT
【tcp_protocol.handler】tcp_v4_rcv-&gt;
-&gt;if (sk-&gt;sk_state == TCP_TIME_WAIT) goto do_time_wait;
-&gt;do_time_wait:
-&gt;tcp_timewait_state_process
-&gt;-&gt;if (tw-&gt;tw_substate == TCP_FIN_WAIT2)
-&gt;-&gt;tw-&gt;tw_substate = TCP_TIME_WAIT;
-&gt;-&gt;inet_twsk_reschedule，重新设置回调时间
-&gt;-&gt;return TCP_TW_ACK;

B、返回ACK
-&gt;case TCP_TW_ACK:
-&gt;tcp_v4_timewait_ack(sk, skb);

6、服务端收到ACK包，状态从TCP_LAST_ACK变为TCP_CLOSE
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_state_process
-&gt;case TCP_LAST_ACK:
-&gt;tcp_done
-&gt;-&gt;tcp_set_state(sk, TCP_CLOSE);

7、客户端超时回调
A、超时时间定义
#define TCP_TIMEWAIT_LEN (60*HZ)
#define TCP_FIN_TIMEOUT TCP_TIMEWAIT_LEN

B、超时后，回调tw_timer_handler-&gt;inet_twsk_kill，进行inet_timewait_sock清理工作

C、没有找到状态变从TCP_TIME_WAIT变为TCP_CLOSE的代码

D、只看没调，有问题的，欢迎小伙伴告诉一下</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（3） 💬（0）<div>四次挥手过程分析上【V5.8，正常流程】
1、客户端主动断开连接，状态从TCP_ESTABLISHED变为TCP_FIN_WAIT1，发送FIN包给服务端
A、状态变为TCP_FIN_WAIT1
tcp_close-&gt;tcp_close_state
-&gt;tcp_set_state(sk, new_state[TCP_ESTABLISHED])，也就是TCP_FIN_WAIT1

B、发送FIN包
tcp_close-&gt;tcp_close_state
-&gt;tcp_send_fin

2、服务端收到FIN包，状态从TCP_ESTABLISHED变为TCP_CLOSE_WAIT，并返回ACK包
A、状态变为TCP_CLOSE_WAIT
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_established
-&gt;tcp_data_queue
-&gt;-&gt;tcp_fin
-&gt;-&gt;-&gt;inet_csk_schedule_ack; 安排ack
-&gt;-&gt;-&gt;sk-&gt;sk_shutdown |= RCV_SHUTDOWN; 模拟了close
-&gt;-&gt;-&gt;sock_set_flag(sk, SOCK_DONE);
-&gt;-&gt;-&gt;case TCP_ESTABLISHED:
-&gt;-&gt;-&gt;tcp_set_state(sk, TCP_CLOSE_WAIT); 修改状态
-&gt;-&gt;inet_csk(sk)-&gt;icsk_ack.pending |= ICSK_ACK_NOW;  ACS是否立即发送

B、发送ACK包
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_established【接上面】
-&gt;tcp_ack_snd_check-&gt;__tcp_ack_snd_check-&gt;tcp_send_ack

3、客户端收到ACK包，状态从TCP_FIN_WAIT1变为TCP_FIN_WAIT2，然后被替换为状态TCP_TIME_WAIT，子状态TCP_FIN_WAIT2
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_state_process
-&gt;case TCP_FIN_WAIT1:
-&gt;tcp_set_state(sk, TCP_FIN_WAIT2);
-&gt;tcp_time_wait(sk, TCP_FIN_WAIT2, tmo);
-&gt;-&gt;tw = inet_twsk_alloc(sk, tcp_death_row, state);
-&gt;-&gt;-&gt;tw-&gt;tw_state = TCP_TIME_WAIT;   
-&gt;-&gt;-&gt;tw-&gt;tw_substate = TCP_FIN_WAIT2;
-&gt;-&gt;-&gt;timer_setup(&amp;tw-&gt;tw_timer, tw_timer_handler, TIMER_PINNED);

4、服务端状态从TCP_CLOSE_WAIT变为TCP_LAST_ACK，发送FIN包
A、状态变为TCP_LAST_ACK
tcp_close-&gt;tcp_close_state
-&gt;tcp_set_state(sk, new_state[TCP_CLOSE_WAIT])，也就是TCP_LAST_ACK

B、发送FIN包
tcp_close-&gt;tcp_close_state
-&gt;tcp_send_fin</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（6） 💬（1）<div>三次握手过程分析【V5.8，正常流程】
1、客户端发起第一次握手，状态调变为TCP_SYN_SENT，发送SYN包
connect-&gt;__sys_connect-&gt;__sys_connect_file-&gt;【sock-&gt;ops-&gt;connect】tcp_v4_connect
A、状态变化
-&gt;tcp_set_state(sk, TCP_SYN_SENT);
B、发送SYN
-&gt;tcp_connect-&gt;tcp_send_syn_data

2、服务端收到客户端的SYN包，初始化socket，状态从TCP_LISTEN变为TCP_NEW_SYN_RECV，发送第二次握手SYN_ACK包
A、收到连接，初始化socket
accept-&gt;__sys_accept4-&gt;__sys_accept4_file-&gt;【sock-&gt;ops-&gt;accept】inet_csk_accept

B、收到SYN，改变状态
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_state_process-&gt;
-&gt;case TCP_LISTEN:
-&gt;[sock-&gt;ops-&gt;conn_request]tcp_v4_conn_request-&gt;tcp_conn_request
-&gt;-&gt;inet_reqsk_alloc
-&gt;-&gt;-&gt;ireq-&gt;ireq_state = TCP_NEW_SYN_RECV;

C、发送SYN_ACK包
-&gt;[sock-&gt;ops-&gt;conn_request]tcp_v4_conn_request-&gt;tcp_conn_request【和B路径一样】
-&gt;-&gt;【af_ops-&gt;send_synack】tcp_v4_send_synack
-&gt;-&gt;-&gt;tcp_make_synack
-&gt;-&gt;-&gt;__tcp_v4_send_check

3、客户端收到SYN_ACK包，状态从TCP_SYN_SENT变为TCP_ESTABLISHED，并发送ACK包
A、收到SYN_ACK包
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_state_process
-&gt;case TCP_SYN_SENT:
-&gt;tcp_rcv_synsent_state_process-&gt;tcp_finish_connect
-&gt;-&gt;tcp_set_state(sk, TCP_ESTABLISHED);

B、发送ACK包
-&gt;tcp_rcv_synsent_state_process-&gt;tcp_send_ack-&gt;__tcp_send_ack

4、服务端收到ACK包，状态从TCP_NEW_SYN_RECV变为TCP_SYN_RECV【实际上是新建了一个sock】
【tcp_protocol.handler】tcp_v4_rcv-&gt;
-&gt;if (sk-&gt;sk_state == TCP_NEW_SYN_RECV)
-&gt;tcp_check_req
-&gt;-&gt;【inet_csk(sk)-&gt;icsk_af_ops-&gt;syn_recv_sock】tcp_v4_syn_recv_sock-&gt;tcp_create_openreq_child-&gt;inet_csk_clone_lock
-&gt;-&gt;-&gt;inet_sk_set_state(newsk, TCP_SYN_RECV);

5、服务端状态从TCP_SYN_RECV变为TCP_ESTABLISHED
【tcp_protocol.handler】tcp_v4_rcv-&gt;tcp_v4_do_rcv-&gt;tcp_rcv_state_process
-&gt;case TCP_SYN_RECV:
-&gt;tcp_set_state(sk, TCP_ESTABLISHED);

只看没调，有问题的欢迎各位小伙伴指出。</div>2021-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（3）<div>今天的问题不好回答，因为文中无明显三次握手的代码，而且三次握手的机制其实比较复杂，涉及到几个状态和几个队列之间的切换，笼统的 connect 和 accept 函数是说不清楚的，感兴趣可以看看这里：
https:&#47;&#47;blog.csdn.net&#47;tennysonsky&#47;article&#47;details&#47;45621341

当然这些不能全信，所以还是得自己看linux内核代码，待我看了再来补充😂</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b4/7c/59e24b60.jpg" width="30px"><span>王子虾</span> 👍（0） 💬（1）<div>老师，有一个问题，tcp在调用listen的时候，有全连接队列的概念，一般上限是128。但是问题是，我们比如实现单机百万链接的时候，一个server端的源组（server_ip+port），比如有65535个client，那会不会受限于这个全连接队列？</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>nice</div>2022-02-25</li><br/><li><img src="" width="30px"><span>GeekCoder</span> 👍（0） 💬（1）<div>能讲讲epoll吗？</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（0） 💬（1）<div>这里有一篇三次握手的源码图解：https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;vlrzGc5bFrPIr9a7HIr2eA</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/85/87/727142bc.jpg" width="30px"><span>MacBao</span> 👍（1） 💬（0）<div>服务器端处于listen状态，客户端connect发起TCP三次握手？</div>2021-08-09</li><br/>
</ul>