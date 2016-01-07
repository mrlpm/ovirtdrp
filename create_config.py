import yaml

d = {'manager': 'a', 'B': {'C': 'c', 'D': 'd', 'E': 'e'}}
with open('result.yml', 'w') as f:
    yaml.dump(d, f, default_flow_style=False)
