# Metrics server installed (for HPA):

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Apply Manifests

kubectl apply -f kubernetes/deployment.yaml

kubectl apply -f kubernetes/service.yaml

kubectl apply -f kubernetes/ingress.yaml

kubectl apply -f kubernetes/hpa.yaml
