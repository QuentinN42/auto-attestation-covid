FROM quentinn42/seleniumpython

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# adding config files
COPY xpaths.json /app/
COPY env_vars_str.json /app/
COPY env_vars_bool.json /app/

COPY app.py /app/runner.py
