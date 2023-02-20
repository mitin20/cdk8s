# cdk8s

# install
brew install cdk8s
npm install -g cdk8s-cli
yarn global add cdk8s-cli

# new project
$ mkdir hello
$ cd hello
$ cdk8s init python-app
Initializing a project from the python-app template
...

# produce and inspect
cdk8s synth
dist/hello.k8s.yaml

cat dist/hello.k8s.yaml
<EMPTY>

# synthesize
cdk8s synth

# install
kubectl apply -f dist/hello.k8s.yaml

# example
```py
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
```
# using java
$ mkdir hello
$ cd hello
$ cdk8s init java-app
Initializing a project from the java-app template
...
useful
    "build": "cdk8s import --language java", 
    "synth": "mvn install && mvn compile && cdk8s synth",

# example
```java
package com.mycompany.app;

import software.constructs.Construct;

import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

import org.cdk8s.App;
import org.cdk8s.Chart;
import org.cdk8s.ChartProps;

import imports.k8s.IntOrString;
import imports.k8s.LabelSelector;
import imports.k8s.ObjectMeta;
import imports.k8s.PodTemplateSpec;
import imports.k8s.KubeService;
import imports.k8s.KubeServiceProps;
import imports.k8s.ServicePort;
import imports.k8s.ServiceSpec;
import imports.k8s.DeploymentSpec;
import imports.k8s.PodSpec;
import imports.k8s.Container;
import imports.k8s.ContainerPort;
import imports.k8s.KubeDeployment;
import imports.k8s.KubeDeploymentProps;

public class Main extends Chart
{

    public Main(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public Main(final Construct scope, final String id, final ChartProps options) {
        super(scope, id, options);

        // Defining a LoadBalancer Service
        final String serviceType = "LoadBalancer";
        final Map<String, String> selector = new HashMap<>();
        selector.put("app", "hello-k8s");
        final List<ServicePort> servicePorts = new ArrayList<>();
        final ServicePort servicePort = new ServicePort.Builder()
            .port(80)
            .targetPort(IntOrString.fromNumber(8080))
            .build();
        servicePorts.add(servicePort);
        final ServiceSpec serviceSpec = new ServiceSpec.Builder()
            .type(serviceType)
            .selector(selector)
            .ports(servicePorts)
            .build();
        final KubeServiceProps serviceProps = new KubeServiceProps.Builder()
            .spec(serviceSpec)
            .build();

        // notice that there is no assignment necessary when creating resources.
        // simply instantiating the resource is enough because it adds it to the construct tree via
        // the first argument, which is always the parent construct.
        // its a little confusing at first glance, but this is an inherent aspect of the constructs
        // programming model, and you will encounter it many times.
        // you can still perform an assignment of course, if you need to access
        // attributes of the resource in other parts of the code.

        new KubeService(this, "service", serviceProps);

        // Defining a Deployment
        final LabelSelector labelSelector = new LabelSelector.Builder().matchLabels(selector).build();
        final ObjectMeta objectMeta = new ObjectMeta.Builder().labels(selector).build();
        final List<ContainerPort> containerPorts = new ArrayList<>();
        final ContainerPort containerPort = new ContainerPort.Builder()
            .containerPort(8080)
            .build();
        containerPorts.add(containerPort);
        final List<Container> containers = new ArrayList<>();
        final Container container = new Container.Builder()
            .name("hello-kubernetes")
            .image("paulbouwer/hello-kubernetes:1.7")
            .ports(containerPorts)
            .build();
        containers.add(container);
        final PodSpec podSpec = new PodSpec.Builder()
            .containers(containers)
            .build();
        final PodTemplateSpec podTemplateSpec = new PodTemplateSpec.Builder()
            .metadata(objectMeta)
            .spec(podSpec)
            .build();
        final DeploymentSpec deploymentSpec = new DeploymentSpec.Builder()
            .replicas(1)
            .selector(labelSelector)
            .template(podTemplateSpec)
            .build();
        final KubeDeploymentProps deploymentProps = new KubeDeploymentProps.Builder()
            .spec(deploymentSpec)
            .build();

        new KubeDeployment(this, "deployment", deploymentProps);

    }

    public static void main(String[] args) {
        final App app = new App();
        new Main(app, "hello");
        app.synth();
    }
}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      }
```
