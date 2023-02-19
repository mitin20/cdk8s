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

