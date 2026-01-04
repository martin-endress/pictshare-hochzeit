echo "Building pictshare..."
docker build -f docker/Dockerfile -t pictshare-hochzeit:local .

echo "Building image-generator..."
docker build -f image-generator/Dockerfile -t image-generator:local image-generator    
