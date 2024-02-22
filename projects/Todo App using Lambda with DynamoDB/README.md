# Steps

- Create a DynamoDB Table
    - Table name - todo
    - Partition key - data_type
    - Sort key - task_id
    - Table settings - on-demand Capacity mode
- Create lambda function 
    - runtime - python
    - check function url under Advanced settings
        - Auth type - None
        - copy the url from the configuration tab
    - paste the contents from the `lambda_function.py` and `db.py` in the lambda code editor
- Update permissions
    - Go to the function role under Configuration -> Permissions
    - Attach `AmazonDynamoDBFullAccess` policy
    