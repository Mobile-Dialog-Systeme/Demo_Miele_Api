## create your config
```bash
cp config.json.example config.json
```
(on windows):
```bash
copy config.json.example config.json
```

Modify the config.py file according to your needs.
(at least `client_id`, `client_secret`)

#### if necessary you need to create a new account

register at https://www.miele.com/f/com/en/register_api.aspx
make sure to save the `client_id` and `client_secret` , you will only see it once.
(maybe you print it ? )

## create virtual environment
```bash
python -m venv venv
```

## install dependencies
```bash
pip install -r requirements.txt
```

## update depencendies

If you do not want to update the dependencies manually, you can use the following command to update the requirements.txt file.
(But it will also write the dependencies of the installed packages, so you may want to remove the unnecessary ones)

```bash 
pip freeze > requirements.txt
``` 

