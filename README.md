# Run Project

* Install RabbitMQ
* Install Redis
* Install project dependencies:

```bash
pip install -r requirements.txt
```

* Prepare database (Run once):

```bash
./manage.py migrate
./manage.py createsuperuser  # Follow steps
```

* Run celery worker:

See README.md file in `workers` project.

* Run Django project:

```bash
./manage.py runserver 0.0.0.0:8000
```

* Go to http://locahost:8000/ or IP from a remote machine.

# Run Tests

* Install requirements:

```bash
pip install -r requirements_dev.txt
```

Then just write:

```bash
py.test
```
