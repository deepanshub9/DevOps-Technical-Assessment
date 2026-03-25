# Beginner Step-by-Step Runbook (AWS DevOps Assignment)

This guide follows your assignment exactly and keeps things simple.

---

## 0) Important cost truth (must know first)

- Amazon EKS control plane has fixed cost, so **full month under $10 is not realistic**.
- Best learning method: build, verify, take screenshots, then destroy same day.

---

## 1) Install required tools

Install these on your laptop:

- AWS CLI v2
- Terraform (>= 1.6)
- kubectl

Verify:

```bash
aws --version
terraform --version
kubectl version --client
```

---

## 2) Configure AWS account access

Configure your AWS profile:

```bash
aws configure
```

Enter Access Key, Secret Key, region (example `ap-south-1`), output format `json`.

Check identity:

```bash
aws sts get-caller-identity
```

---

## 3) Prepare remote Terraform state (industry style)

You selected S3 + DynamoDB locking.

### 3.1 Create S3 bucket (choose unique name)

```bash
aws s3 mb s3://deepanshu-tf-state-unique-12345 --region ap-south-1
```

### 3.2 Enable bucket versioning

```bash
aws s3api put-bucket-versioning \
  --bucket deepanshu-tf-state-unique-12345 \
  --versioning-configuration Status=Enabled
```

### 3.3 Create DynamoDB lock table

```bash
aws dynamodb create-table \
  --table-name deepanshu-tf-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1
```

### 3.4 Update backend block

Edit `terraform/provider.tf` and uncomment backend block:

- bucket = your bucket name
- dynamodb_table = your table name
- region = your chosen region

---

## 4) Initialize and plan Terraform

Go into Terraform folder:

```bash
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan -out tfplan
```

This project now uses a **true modular design**:

- `modules/vpc`
- `modules/eks`
- `modules/nodegroup`

Root files call these modules, which is the industry-style reusable approach.

If no errors, apply:

```bash
terraform apply tfplan
```

Creation can take 15–25 minutes.

---

## 5) Verify assignment requirements (Part A)

### 5.1 Required outputs

```bash
terraform output
```

You should see:

- EKS cluster name
- VPC ID
- Node group name

### 5.2 Confirm API endpoint is private-only

```bash
aws eks describe-cluster --name private-eks-assignment --region ap-south-1 \
  --query "cluster.resourcesVpcConfig.{private:endpointPrivateAccess,public:endpointPublicAccess}" \
  --output table
```

Expected:

- private = true
- public = false

### 5.3 Confirm nodes in private subnets

In EC2 console, worker node instances should have:

- no public IP
- subnet = private subnet

---

## 6) Connect kubectl to EKS

```bash
aws eks update-kubeconfig --region ap-south-1 --name private-eks-assignment
kubectl get nodes
```

Expected: 3 nodes in `Ready` state.

> If this command fails from your laptop, that is normal for private endpoint clusters.
> In that case, use a small admin EC2 in the same VPC and run kubectl from there through SSM.

---

## 7) Deploy Kubernetes app stack (Part B)

Go to kubernetes folder and apply files in order:

```bash
cd ../kubernetes
kubectl apply -f 00-namespace.yaml
kubectl apply -f 02-haproxy-configmap.yaml
kubectl apply -f 01-tomcat-deployment.yaml
kubectl apply -f 03-haproxy-deployment.yaml
kubectl apply -f 04-haproxy-service.yaml
```

Optional industry-learning files (safe to apply after core stack works):

```bash
kubectl apply -f 05-tomcat-pdb.yaml
kubectl apply -f 06-haproxy-pdb.yaml
kubectl apply -f 07-haproxy-hpa.yaml
kubectl apply -f 08-network-policy.yaml
```

Notes:

- `07-haproxy-hpa.yaml` needs metrics-server.
- `08-network-policy.yaml` is for security learning; apply only after you confirm app works.

Check objects:

```bash
kubectl get deploy,svc,pods -n app-stack
```

Expected:

- `tomcat` deployment replicas = 2
- `tomcat-service` type = ClusterIP
- `haproxy-service` type = ClusterIP
- no LoadBalancer service

---

## 8) Functional check inside cluster

Use port-forward to test HAProxy locally from your laptop:

```bash
kubectl port-forward -n app-stack service/haproxy-service 8081:80
```

Open browser: `http://localhost:8081`

HAProxy should route to Tomcat.

---

## 8.1) How to access app in private cluster (important)

Because this cluster is private-only, there is no public application URL by default.

### Option A (recommended for this assignment): test from admin EC2 inside VPC

1. Create one small EC2 (t3.micro) in same VPC.
2. Attach IAM role with EKS read + SSM access.
3. Connect via Session Manager (no public SSH).
4. Run:

```bash
aws eks update-kubeconfig --region ap-south-1 --name private-eks-assignment
kubectl get pods -n app-stack
kubectl port-forward -n app-stack service/haproxy-service 8081:80
curl http://localhost:8081
```

### Option B (advanced): connect laptop to VPC using VPN/Direct Connect

Then run the same kubectl commands from local machine.

---

## 8.2) Local run vs AWS run (your exact question)

### Local run (without AWS)

- You can run the same YAML on `minikube` or `kind` for learning Kubernetes basics.
- This does **not** validate private-EKS networking requirements from assignment.

### AWS run (for assignment submission)

- Must use Terraform to create private VPC + private EKS + private nodes.
- Must deploy manifests to that EKS cluster and capture proof.

---

## 8.3) Why no Dockerfile and no app source code here?

- This assignment is about **infra + deployment**, not app development.
- We used ready-made images:
  - `tomcat:9.0-jdk17-temurin`
  - `haproxy:2.9`
- Since we are not building custom code, Dockerfile is optional and not required.
- If you later build your own Java/Node/Python app, then yes, Dockerfile is needed.

---

## 9) Private worker access explanation (Part C)

Use document:

- `docs/ssh-access.md`

Key statement for submission:

- worker nodes private only
- no direct internet SSH
- SSM Session Manager for controlled admin access

---

## 10) Deliverables checklist

Submit these folders/files:

- `terraform/` (source code)
- `kubernetes/` (YAML manifests)
- `docs/ssh-access.md` (SSH/SSM explanation)
- optional architecture diagram (you can draw later)

Also mention in your README/report:

- Terraform is modular (`modules/vpc`, `modules/eks`, `modules/nodegroup`).
- Core app manifests are required files; extra files are optional best-practice learning add-ons.

---

## 11) Cost control (very important)

After screenshots and verification:

```bash
cd ../terraform
terraform destroy
```

This prevents high billing.

---

## Troubleshooting quick map

- `kubectl get nodes` empty/not ready:
  - wait 5–10 min more
  - check node group status in EKS console
- Pods pending:
  - check node CPU/memory usage
- Cannot pull images:
  - check NAT gateway and private route table
- Cannot access cluster:
  - re-run `aws eks update-kubeconfig`
