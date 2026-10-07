def upload(client, filename, content):
    return client.post("/api/files/", files={"file": (filename, content)})
