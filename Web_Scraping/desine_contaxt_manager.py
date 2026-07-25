from contaxt_manager import Connect

with Connect('Saraserver') as server:
    print("Installing python")
    print("Installing and updating more tools")

print("This is after __exit__")