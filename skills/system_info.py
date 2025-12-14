import platform

def system_info(query):
    query = query.lower()

    if "system" in query and ("info" in query or "information" in query):
        return f"Running on {platform.system()} {platform.release()}"

    elif "python" in query and ("version" in query or "ver" in query):
        return f"Running on Python {platform.python_version()}"

    else:
        return None


if __name__ == "__main__":
    print(system_info("system info"))
    print(system_info("python version"))
