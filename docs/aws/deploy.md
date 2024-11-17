# hosteamento da API na AWS usando EKS

o deploy da API criada na primeira etapa foi feito através da AWS, utilizando-se o EKS (Elastic Kubernetes Service).

## infraestrutura utilizada

- **Amazon EKS**: serviço gerenciado de Kubernetes
- **EC2**: instâncias para os nodes do cluster
- **ELB**: *load-balancer* para distribuição de tráfego
- **IAM**: gerenciamento de permissões do cluster

## processo de implementação

você pode baixar os arquivos `.yaml` de deploy <a href="https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fbrunozalc%2Fprojeto-cloud%2Ftree%2Fmain%2Fk8s" target="_blank">aqui</a>.

### 1. preparação do ambiente

```bash
# criação do cluster
eksctl create cluster \
      --name dogfacts \
      --region us-east-1 \
      --node-type t3.small \
      --nodes 2 \
      --nodes-min 1 \
      --nodes-max 3 \
      --managed
```

### 2. deploy da aplicação

a aplicação foi implantada usando o arquivo `api-deploy.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: projeto
spec:
  replicas: 1
  selector:
    matchLabels:
      app: projeto
  template:
    metadata:
      labels:
        app: projeto
    spec:
      containers:
        - name: projeto
          image: brunozalc/apicloud:latest
          ports:
            - containerPort: 8000
          # readiness test
          readinessProbe:
            httpGet:
              path: /
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
          # wait for database
          startupProbe:
            httpGet:
              path: /
              port: 8000
            failureThreshold: 30
            periodSeconds: 10
```

### 3. configuração do banco de dados

o `postgres` também foi inicializado através de um arquivo `postgres-deploy.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres
          ports:
            - containerPort: 5432
          envFrom:
            - configMapRef:
                name: postgres-config
            - secretRef:
                name: postgres-secret
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
                - -d
                - dogfacts
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 5
            failureThreshold: 5
```

### 4. exposição do serviço

o `postgres` foi exposto através de um serviço do tipo `ClusterIP`, na porta `5432`

a API foi exposta através de um LoadBalancer:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: projeto
spec:
  type: LoadBalancer
  selector:
    app: projeto
  ports:
    - port: 8000
      targetPort: 8000
```

## comandos posteriores

```bash
# checa que os pods estão em execução
kubectl get pods

# verifica os serviços (postgres e API)
kubectl get services

# logs do deployment da API
kubectl logs deployment/projeto
```

## medidas de segurança

- conta da AWS segura com MFA
- cluster em VPC isolada
- *roles* do IAM com permissões necessárias
- *secrets* para credenciais do banco de dados
- *network policies* para isolamento de recursos

## demonstração

<iframe width="560" height="315" src="https://www.youtube.com/embed/kp1-KOJTn48"
    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
</iframe>
