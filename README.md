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
để khởi tạo server


Sau đó vào `client/index.html` đổi phần tham số của dòng 14 phần `action` từ `http://192.168.99.100/predict` thành `http://localhost/predict` và chạy file html đó để upload ảnh. Sau đó nhấn `submit` để server tiến hành nhận diện đối tượng.

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
chạy dòng lệnh sau tại node manager
```
docker swarm init --advertise-addr <IP Machine> 
```
```
docker@manager:~$ docker swarm init --advertise-addr 192.168.99.100
Swarm initialized: current node (zt9vclmhy9sjq2fwqlsl7vtps) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-38do30egwjxcmnrc2r1i0g50htcfx4bw8sz76nkay6c3ewc9t0-1qe6qoqmzzaf0faax6iwst9f9 192.168.99.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```
để xem ip của máy:
```
docker-machine ip <name-machine>
```
```
docker-machine ip manager
192.168.99.100
```
Sau đó chuyển lần lượt sang con worker1 và worker2. Tại 2 con worker này ta tiến hành join nó vào swarm như một worker 
```
docker swarm join --token <token> <host>:<port>
```
Trong đó:
- **host**: Địa chỉ ip của con manager.
- **port**: Cổng port của con manager

```
docker@worker1:~$ docker swarm join --token SWMTKN-1-38do30egwjxcmnrc2r1i0g50htcfx4bw8sz76nkay6c3ewc9t0-1qe6qoqmzzaf0faax6iwst9f9 192.168.99.100:2377
This node joined a swarm as a worker.
````
làm tương tự với worker2


Sau khi worker1 và worker2 đã join vào trong swarm chạy dòng lệnh sau tại manager để kiểm tra các node
```
docker node ls
```
```
docker@manager:~$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
zt9vclmhy9sjq2fwqlsl7vtps *   manager             Ready               Active              Leader              19.03.4
vpc31gz0pu81jz0l1u9x6de25     worker1             Ready               Active                                  19.03.4
yomdq4cf8swzql9c3pc77lm1v     worker2             Ready               Active                                  19.03.4
```
Dễ thấy 2 node worker kia có chung 1 status là rỗng tại cột **MANAGER STATUS**. Điều này cho ta biết chúng là node worker.


Vậy là ta đã tạo thành công 2 con worker và 1 con manager và gom chúng thành một swarm (cluster).

## Deploy hệ thống vào docker
Comment dòng 11, 16, 17, 33, 38, 39 và uncomment 2 dòng 10, 32 tại file docker-compose.yml


sau đó copy file docker-compose.yml và app.env sang cho node manager:
```
docker-machine scp filesource name-machine:/path-docker-machine/
```
trong demo tại máy tính cá nhân
```
docker-machine scp /Users/tunguyen/Desktop/LTU14-GRUP07/docker-compose.yml manager:/home/docker/docker-compose.yml
docker-machine scp /Users/tunguyen/Desktop/LTU14-GROUP07/app.env manager:/home/docker/app.env
```
sau đó vào node manager và chạy:
```
docker stack deploy -c docker-compose.yml mldeploy
```
để kiểm tra list service:
```
docker@manager:~$ docker service ls
ID                  NAME                   MODE                REPLICAS            IMAGE                                      PORTS
bvcqihnc93k7        mldeploy_modelserver   replicated          1/1                 ndtu1511/project_dsa_modelserver:model_2
gbqdgqefnigb        mldeploy_redis         replicated          1/1                 redis:latest
d2g6gqhekvbz        mldeploy_webserver     replicated          1/1                 ndtu1511/project_dsa_webserver:web_2       *:80->80/tcp
```
để kiểm tra các bản replicas chạy trên node nào:
```
docker@manager:~$ docker stack ps mldeploy
ID                  NAME                     IMAGE                                      NODE                DESIRED STATE       CURRENT STATE                ERROR               PORTS
aclvtil1wpi4        mldeploy_webserver.1     ndtu1511/project_dsa_webserver:web_2       manager             Running             Running about a minute ago
v3krkrt8tnip        mldeploy_modelserver.1   ndtu1511/project_dsa_modelserver:model_2   worker2             Running             Running about a minute ago
5osh0e6x7jid        mldeploy_redis.1         redis:latest                               manager             Running             Running about a minute ago
```
Như vậy là đã chạy thành công hệ thống lên một swarm. Chạy file `index.html` của folder `client` để tiến hành demo.


Khi demo xong thì ta sẽ tắt các máy ảo đi:
```
docker-machine stop <name-machine>
```
Nếu muốn xoá hệ thống đã deploy vào swarm:
```
docker stack rm mldeploy
```
Nếu muốn thoát node ra khỏi swarm:
```
docker swarm leave
```