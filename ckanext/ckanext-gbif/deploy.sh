# /bin/bash
#sudo cp -r ../ckanext-gbif /var/lib/docker/volumes/docker_ckan_home/_data/venv/src/ckan/ckanext/
#echo "copied files"
#sudo docker exec -it ckan /bin/bash -c 'cd /usr/lib/ckan/venv/src/ckan/ckanext/ckanext-gbif && ckan-pip install -e .'

#echo "reloaded pip"
cd  ../../contrib/docker 
#sudo docker  kill redis solr datapusher && sudo docker system prune -a && sudo docker-compose build && sudo docker-compose up -d && \
#sudo docker-compose up -d && sudo docker logs -f ckan
#sudo docker exec -it ckan /bin/bash -c 'ckan-paster serve --reload /etc/ckan/production.ini'
sudo docker-compose build && sudo docker-compose up -d && \
cd -
sleep 30s
python3 ../../../gbif2ckan/gbif2ckan.py
echo "reran gbif2ckan"
sudo docker logs -f ckan
