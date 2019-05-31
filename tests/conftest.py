import platform


def pytest_addoption(parser):
    parser.addoption(
        "--terminate", action="store_true", default=False, help="cleanup tika proccess"
    )


def pytest_unconfigure(config):
    if platform.system() == "Windows":
        print("We are on Windows")
        terminate = config.getoption('--terminate')
        if terminate:
            import subprocess
            print("Terminate Tika Java Server")
            subprocess.call("taskkill /F /T /IM java.exe")
