# Steps

- Create EC2 instances
    - name few as `dev` and others as anything
    - use `t2.micro` instances for cost saving
    - delete the instances once the experimentation is done to save on costs as they are chargable
- Create lambda function with python as runtime and paste the from the `lambda_function.py`
- Add a trigger
    - Select EventBridge
    - Create a new rule and add schedule as per your needs
        - eg. rate(2 minutes)
- Update permissions
    - Go to the function role under Configuration -> Permissions
    - Attach `AmazonEC2FullAccess` policy
    