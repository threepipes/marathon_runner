# requirements

- docker
- docker-compose >= 1.13.0

# run

```
# setup
cd worker
mkdir archive
mkdir data
./create_db.sh test.db
```

```
docker-compose up --scale worker=4
```
