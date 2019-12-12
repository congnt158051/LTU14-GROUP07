# LTU14-GROUP07
# Yêu cầu
- docker
- docker-compose
- docker-machine
- docker swarm
- Download https://pjreddie.com/media/files/yolov3.weights vào folder `modelserver`
# Chạy trên single host
Chạy lệnh 
```
docker-compose up
```
để khởi tạo server sau đó chạy file html trong folder `client` upload ảnh và nhấn submit để server datect ảnh


# Chạy trên multi host
## Khởi tạo máy ảo
Khởi tạo 3 máy ảo với 1 swarm manager và 2 swarm worker
```
docker-machine create manager
docker-machine create worker1
docker-machine create worker2
```
Sau khi chạy xong ta kiểm tra list machine:
```
docker-machine ls
```
```
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER     ERRORS
manager   -        virtualbox   Running   tcp://192.168.99.100:2376           v19.03.4
worker1   -        virtualbox   Running   tcp://192.168.99.101:2376           v19.03.4
worker2   -        virtualbox   Running   tcp://192.168.99.102:2376           v19.03.4
```
Để truy cập vào các máy manager hay worker thì ta sử dụng SSH cự thể như sau:
```
docker-machine ssh <name-machine>
```
để quay lại host local:
```
exit
```
## Khởi tạo swarm
```
docker swarm init --advertise-addr <IP Machine> 
```


docker-machine scp /Users/tunguyen/Desktop/LTU14-GROUP07/docker-compose.yml manager:/home/docker/docker-compose.yml

docker-machine scp /Users/tunguyen/Desktop/LTU14-GROUP07/app.env manager:/home/docker/app.env

docker stack deploy -c docker-compose.yml mldeploy