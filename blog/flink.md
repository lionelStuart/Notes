## flink


### 概念

1. 工作模式

- session: 资源共享模式，一个任务挂了都挂

- per-job：资源独占，消耗更大

- application: 介于两者之间，由client分配一个集群

2. 部署模式

- standalone: 由flink管理集群，也可以k8s部署，不支持per-job

- native模式：由k8s管理，不支持per-job

- yarn: 三种模式都支持

- k8s operator 官方推荐的k8s native模式


3. 关键词
- 有界流、无界流
- 批处理、流处理
- 算子、source\sink、dataflows


## 学习

1. 使用flink op模式部署测试 应用，通过web ui查看测试任务


 
