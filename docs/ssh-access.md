# Secure Access to Private EKS Worker Nodes (SSM Preferred)

## Why worker nodes stay private

- In this assignment, worker nodes are in **private subnets**.
- Private subnet means EC2 instances do **not** have direct public internet route.
- So nodes do not get public IP and cannot be SSH'ed from internet directly.

## Public vs Private subnet (simple meaning)

- **Public subnet**: route table has `0.0.0.0/0 -> Internet Gateway`.
  - Resources here can be internet-reachable (if public IP + security group allow).
- **Private subnet**: route table does **not** go to Internet Gateway directly.
  - Outbound internet (for package/image pull) goes via NAT Gateway.
  - Inbound internet access is blocked by design.

## Recommended access method: AWS Systems Manager Session Manager

This is preferred because:

- No inbound port 22 needed
- No bastion host needed
- Fully auditable via AWS

## Prerequisites already included in Terraform

- Worker node IAM role has `AmazonSSMManagedInstanceCore` policy.
- Nodes are in private subnet with outbound access through NAT gateway.

## How to open session (if needed)

1. Find an EKS worker node instance in EC2 console.
2. Copy the instance ID (example: `i-0123456789abcdef0`).
3. Start session from terminal:
   ```bash
   aws ssm start-session --target i-0123456789abcdef0
   ```

## Security best practice statement for submission

- Worker nodes have no public IP.
- Kubernetes API public endpoint is disabled.
- Direct SSH from internet is not allowed.
- Administrative node access is only through SSM Session Manager.
