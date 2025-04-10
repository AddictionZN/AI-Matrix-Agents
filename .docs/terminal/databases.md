
# Databases
## PostgreSQL

### Step 1.Starting Your PostgreSQL Container
```
docker run --name dummy-postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=my_dummy_db \
  -p 5432:5432 \
  -d postgres
```

### Step 2: Connecting to the PostgreSQL Shell
```
docker exec -it dummy-postgres bash
```

### Step 3: Connecting to the PostgreSQL Database
```
psql -U myuser -d my_dummy_db
```

### Step 4: Creating a Table
```
CREATE TABLE my_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT
);

```
### Step 5: Inserting Data into the Table
```
INSERT INTO my_table (name, age) VALUES ('John Doe', 30);
INSERT INTO my_table (name, age) VALUES ('Jane Smith', 25);
```

### Step 6: Querying Data from the Table
```
SELECT * FROM my_table;
```

## Other: 

### Copy the CSV File to the Docker Container
```
docker cp data/[file_name].csv dummy-postgres:/tmp/[file_name].csv
docker exec -it dummy-postgres bash
ls /tmp
```

### Docker Commands
```
- docker logs dummy-postgres
- docker stop dummy-postgres
- docker rm dummy-postgres
```