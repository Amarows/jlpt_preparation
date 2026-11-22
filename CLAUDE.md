# JLPT_Vocabulary

## Python environment (`.venv`)

The portal (`start_portal.vbs`), the tests and the pre-push gate (`.aop/adapter.yaml`) all run `.venv\Scripts\python.exe`. `.venv` is not in git and is deleted between work sessions because the repo lives in OneDrive (~0.9 GB synced for nothing).

Rebuild it when it is missing, or when `.venv\pyvenv.cfg` names a `home` Python that no longer exists. From the repo root:

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Done when `.venv\Scripts\python -m pytest -q -p no:cacheprovider tests` runs with no collection errors.
