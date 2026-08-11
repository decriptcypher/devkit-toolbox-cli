import hashlib


def run(value: str, algo: str, as_text: bool) -> None:
    hasher = hashlib.new(algo)

    if as_text:
        hasher.update(value.encode())
    else:
        with open(value, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)

    print(hasher.hexdigest())
