docker stop combustion-scheduler-api-pct2
docker rm combustion-scheduler-api-pct2
docker image rm  combustion-scheduler-api-pct2:v1.5.4
docker image load -i combustion-scheduler-api-pct2-v1.5.4.tar
docker run -itd --name combustion-scheduler-api-pct2 --restart unless-stopped --memory="300M" -p 0.0.0.0:8083:8083 combustion-scheduler-api-pct2:v1.5.4
