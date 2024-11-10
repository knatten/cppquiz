import subprocess


def format(source: str) -> str:
    try:
        process = subprocess.run(
            ["clang-format", f"--style=LLVM"],
            input=source.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return process.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"clang-format failed: {e.stderr.decode('utf-8')}")
