# SUI Usernames DB

Scratch Usernames and User ID lookup database.

## Running

1. Install requirements

```
python -m pip install -r requirements.txt
```

2. Create the database:

```
python db.py
```

> [!NOTE]
> Alternatively, the database is available in the [Releases](https://github.com/uukelele-scratch/sui-usernames-db/releases/latest) tab. You can download this and use it, to save time, but note that it is 750MB.

3. Run the API

```
python -m uvicorn api:app
```

4. Test

```
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/id/1234' \
  -H 'accept: application/json'
```