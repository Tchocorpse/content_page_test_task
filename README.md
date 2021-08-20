# content_page_test_task

## Prerequsites
Developed and tested in Linux (Ubuntu) environment only. Requires `git` and `docker` to be installed. 

## Project setup, testing and dev server
### Setup
```
git clone 
cd ./content_page_test_task
docker-compose -f dc-start.yml build
```
### Autotesting
```
docker-compose -f dc-start.yml up django-autotests
```
### Run dev server
```
docker-compose -f dc-start.yml up django-runserver
```

Please note that after completing both the `docker-compose up` commands you are required to shut down the services `postgres_test_conpage` and `redis_conpage_task` manually, if you wish so.

### Django admin
Pre generated superuser username: `admin` password: `admin`

## API examples
### request pages
`curl --location --request GET 'http://0.0.0.0:8000/pages/?limit=1&offset=2'`

```
{
    "count": 4,
    "next": "http://0.0.0.0:8000/pages/?limit=1&offset=3",
    "previous": "http://0.0.0.0:8000/pages/?limit=1&offset=1",
    "results": [
        {   
            "url": "http://0.0.0.0:8000/pages/4/"
            "id": 4,
            "title": "title 4",
            "created": "2021-08-18T19:38:12.305815Z",
            "updated": "2021-08-18T19:38:12.305837Z",
        }
    ]
}
```

### request page details
`curl --location --request GET 'http://0.0.0.0:8000/pages/1/'`

```
{
    "page_detail": {
        "id": 1,
        "title": "title 1",
        "created": "2021-08-17T01:42:02.480Z",
        "updated": "2021-08-17T04:07:35.476Z",
        "page_content": [
            {
                "id": 2,
                "title": "text content title 1",
                "counter": 25,
                "basecontent_ptr": 2,
                "text": "test text"
            },
            {
                "id": 3,
                "title": "audio test title 1",
                "counter": 25,
                "basecontent_ptr": 3,
                "bitrate": 23
            }
        ]
    }
}
```