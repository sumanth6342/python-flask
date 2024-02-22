from argparse import ArgumentParser

# 1 get the parser
parser = ArgumentParser(
    description="Greeting utility"
)

# 2 give arguments
parser.add_argument(
    "--name",
    type=str,
    help="Name of the user",
    required=True
    # default="admin"
)

parser.add_argument(
    "--role",
    type=str,
    help="Role of the user",
    required=True
    # default="bench"
)

# name = input("Please enter your name : ")
# role = input("Please enter your role : ")

# 3 parse the arguments
args = parser.parse_args()
# print(args)

name = args.name
role = args.role

if name and role:
    print(f"Hello {name}, welcome to the {role} team!")
else:
    print("need name and role values")


# file run
# python greeting.py --name firoz --role dba


_ = """
#!/bin/bash -> bash

python greeting.py --name firoz --role dba

python greeting.py \
    --name firoz \
    --role dba
"""
