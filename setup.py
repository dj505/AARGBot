import json

config = {}
temp_vars = {}
wallets = {}

print("Any field marked * can be left blank, but may disable some features.\n")

config["prefix"] = input("Prefix? ")
config["token"] = input("Token? ")
config["bot_creator"] = input("*Bot creator ID? ")
config["log_channel"] = input("*Log channel ID? ")
config["welcome_channel"] = input("*Welcome channel ID? ")
config["admin_role"] = input("*Admin role ID? ")
config["bot_creator"] = input("*Bot creator ID? ")

with open("configs/config.json", "w") as f:
    json.dump(config, f, indent=2)

with open("configs/temp_vars.json", "w") as f:
    json.dump(temp_vars, f, indent=2)

with open("data/wallets.json", "w") as f:
    json.dump(wallets, f, indent=2)
