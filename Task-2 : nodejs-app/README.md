# Triggered On:
- Every push to the main branch
# Pipeline Stages:

# 1. Build & Test
   - Install dependencies
   - Run tests
   - Build Docker image

# 2. Push
   - Push Docker image to DockerHub

# 3. Deploy
   - Deploy image to Kubernetes
   - Rollback if deployment fails

#  Docker Commands (Local)

# Build the Docker image
docker build -t dockerhubusername/nodejs-app .

# Run locally 
docker run -p 3000:3000 dockerhubusername/nodejs-app

# Kubernetes Deployment
# Start Minikube
minikube start

# Deploy to K8s
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Get the service URL
minikube service nodejs-service
