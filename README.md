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
(Consider printing them for safekeeping.)

> 🔬 **Note:** If you are part of the MDS Lab or enrolled in one of our courses, we will provide the necessary credentials for you.

## create virtual environment
```bash
python -m venv venv
```
## activate the virtual environment

On Windows (Command Prompt):
```bash
venv\Scripts\activate
```
On Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```
On macOS/Linux:
```bash
source venv/bin/activate

```

> 💡 **Hint:** Many popular IDEs, such as VS Code and PyCharm, allow you to select the Python interpreter associated with your virtual environment. Doing so will automatically activate the environment for you when you open the project or run scripts.
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

