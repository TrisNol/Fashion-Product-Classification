docker build . -t fashion-product-classification
docker run --name fashion-product-classification-container -p 5000:5000 fashion-product-classification