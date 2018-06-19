import yaml

with open("reports/controls.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

print cfg['1.1.3 Set nosuid option for /tmp Partition (Scored)']['remedation']
