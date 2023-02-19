#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart

from imports import k8s

class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        label = {"app": "hello-k8s"}

        # notice that there is no assignment necessary when creating resources.
        # simply instantiating the resource is enough because it adds it to the construct tree via
        # the first argument, which is always the parent construct.
        # its a little confusing at first glance, but this is an inherent aspect of the constructs
        # programming model, and you will encounter it many times.
        # you can still perform an assignment of course, if you need to access
        # attributes of the resource in other parts of the code.

        k8s.KubeService(self, 'service',
                    spec=k8s.ServiceSpec(
                    type='LoadBalancer',
                    ports=[k8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(8080))],
                    selector=label))

        k8s.KubeDeployment(self, 'deployment',
                    spec=k8s.DeploymentSpec(
                        replicas=2,
                        selector=k8s.LabelSelector(match_labels=label),
                        template=k8s.PodTemplateSpec(
                        metadata=k8s.ObjectMeta(labels=label),
                        spec=k8s.PodSpec(containers=[
                            k8s.Container(
                            name='hello-kubernetes',
                            image='paulbouwer/hello-kubernetes:1.7',
                            ports=[k8s.ContainerPort(container_port=8080)])]))))


app = App()
MyChart(app, "hello")

app.synth()
