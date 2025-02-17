from fastapi import FastAPI

from nc_py_api import NextcloudApp, ex_app

APP = FastAPI()


def enabled_handler(_enabled: bool, _nc: NextcloudApp) -> str:
    return ""


@APP.on_event("startup")
def initialization():
    ex_app.set_handlers(APP, enabled_handler)


if __name__ == "__main__":
    ex_app.run_app("_install_only_enabled_handler:APP", log_level="warning")
