你好，我是雪飞。

上节课我和你一起体验了 CKA 认证考试的报名流程，你按照课程中的步骤操作就可以成功预约考试。最后两节课，我来给你讲一讲本专栏的超级干货——考试真题。实际上 CKA 考试真题的复现率很高，理解真题的考点，多动手写几遍代码，相信你就能高分通过。

CKA 考试是 17 道题目，我分为上下两个部分。接下来就开始第一部分的真题讲解，你准备好了吗？开始吧！

首先要说明一下，在每道题答题开始之前都需要切换集群，考试题目中会给出切换集群的命令，你直接复制粘贴执行即可。**注意：一定要先执行题目中的切换集群命令，否则答题时可能当前集群没有你需要的环境，或者会破坏当前的集群环境。**

```bash
# 答题时先执行题目中的切换集群命令，例如：
kubectl config use-context k8s
```

## 第一题 RBAC

#### 题目

为部署流水线创建一个新的 ClusterRole 并将其绑定到范围为特定的 Namespace 的特定 ServiceAccount。

1. 创建一个名为 deployment-clusterrole 且仅允许创建以下资源类型的新 ClusterRole：Deployment StatefulSet DaemonSet。
2. 在现有的 Namespace “app-team1” 中创建一个名为 cicd-token 的新 ServiceAccount。限于 Namespace “app-team1” 中，将新的 ClusterRole “deployment-clusterrole” 绑定到新的 ServiceAccount “cicd-token”。