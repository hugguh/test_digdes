docker stop
docker build -t insta_test_digdes .
docker run  --name insta_test_digdes \
            --rm \
            --net=host \
            -v $(pwd)/src:/src \
            -it insta_test_digdes