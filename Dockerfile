FROM quentinn42/seleniumpython

COPY app.py /app/runner.py

# adding config files
COPY xpaths.json /app/
COPY env_vars_str.json /app/
COPY env_vars_bool.json /app/
