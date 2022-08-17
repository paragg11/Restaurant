# Restaurant

- An example & template for Django projects
- Use the following to commit till pre-commit is configured
    ```zsh
    git commit --no-verify -m "commit message"
    ```

## Setting the ENVIRONMENT

- Run the below command to create a directory `envs` and the required `.env` files.
  ```zsh
  make create_env
  ```

- Add the following to the .env files according to the environment you want to use.

    ```bash
    DJANGO_SECRET_KEY=<your-secret-key> 
    DB_NAME=<your-db-name>
    DB_USER=<your-db-user>
    DB_PASSWORD=<your-db-password>
    DEBUG=0 or 1 (0 for false and 1 for true)
    DB_HOST=<your-db-host>
    DB_PORT=<your-db-port>
    LOG_LEVEL=DEBUG or INFO or WARNING or ERROR or CRITICAL
    DEBUG_LOG_DIR=<your-debug-log-dir>
    ```
- Make sure you have a database created with the name configured above and that it is accessible with the configured
  credentials
- Run the below command to create virtual environment
  ```zsh
  make create_env VENV=<desired-name-for-venv>
  ```
- once created, run the following command to start the django app
  ```zsh
  make start
  ```



#### For more options on make, run

  ```zsh
  make help
  ```

  