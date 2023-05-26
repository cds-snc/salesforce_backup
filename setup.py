import os

def setup_local_env() -> None:
    if not os.path.exists("./csv"):
        os.makedirs("./csv")

    if not os.path.exists("./failed"):
        os.makedirs("./failed")