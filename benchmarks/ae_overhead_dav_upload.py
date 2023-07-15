from getpass import getuser
from random import randbytes
from time import perf_counter
from typing import Any, Union

import matplotlib.pyplot as plt
from ae_overhead_common import measure_overhead, os_id

from nc_py_api import Nextcloud, NextcloudApp

ITERS = 30
CACHE_SESS = True


def measure_upload_1mb(nc_obj: Union[Nextcloud, NextcloudApp]) -> [Any, float]:
    __result = None
    small_file_name = "1Mb.bin"
    small_file = randbytes(1024 * 1024)
    start_time = perf_counter()
    for _ in range(ITERS):
        nc_obj.files.upload(small_file_name, small_file)
        nc_obj._session.init_adapter(restart=not CACHE_SESS)  # noqa
    end_time = perf_counter()
    nc_obj.files.delete(small_file_name, not_fail=True)
    return __result, round((end_time - start_time) / ITERS, 3)


if __name__ == "__main__":
    title = f"upload 1mb, {ITERS} iters, CACHE={CACHE_SESS} - {os_id()}"
    measure_overhead(measure_upload_1mb, title)
    plt.savefig(f"results/dav_upload_1mb__cache{int(CACHE_SESS)}_iters{ITERS}__{getuser()}.png", dpi=200)
