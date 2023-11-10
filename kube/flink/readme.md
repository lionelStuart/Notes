https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/try-flink-kubernetes-operator/quick-start/



flink run-application \
  --target kubernetes-application \
  --parallelism 8 \
  -Dkubernetes.cluster-id=word-count \
  -Dtaskmanager.memory.process.size=4096m \
  -Dkubernetes.namespace=flink \
  -Dkubernetes.jobmanager.service-account=flink \
  -Dkubernetes.taskmanager.cpu=2 \
  -Dtaskmanager.numberOfTaskSlots=4 \
  -Dkubernetes.container.image=alphajc/pyflink:1.12 \
  --pyModule word_count \
  --pyFiles /opt/flink/examples/python/table/batch/word_count.py



  client/flink-1.17.1/bin/flink run-application \
  --target kubernetes-application \
  --parallelism 1 \
  -Dkubernetes.cluster-id=pyflink-app \
  -Dtaskmanager.memory.process.size=1096m \
  -Dkubernetes.namespace=default \
  -Dkubernetes.jobmanager.service-account=flink \
  -Dkubernetes.taskmanager.cpu=1 \
  -Dtaskmanager.numberOfTaskSlots=1 \
  -Dkubernetes.container.image=flink-test:v1.0 \
  --pyModule gogo-info \
  --pyFiles /app/gogo-info.py


 flink-1.17.1/bin/flink run-application \
  --target kubernetes-application \
  --parallelism 2 \
  -Dkubernetes.cluster-id=pyflink-app \
  -Dtaskmanager.memory.process.size=1096m \
  -Dkubernetes.namespace=default \
  -Dkubernetes.jobmanager.service-account=flink \
  -Dkubernetes.taskmanager.cpu=1 \
  -Dtaskmanager.numberOfTaskSlots=2 \
  -Dkubernetes.container.image=flink-test:v1.0 \
  --pyModule word_count \
  --pyFiles /opt/flink/examples/python/table/word_count.py

/opt/flink/examples/python/table/word_count.py

  https://mydream.ink/posts/cloud-native/kubernetes/pyflink-in-kubernetes/