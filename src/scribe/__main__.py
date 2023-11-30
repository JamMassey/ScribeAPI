from __future__ import annotations

import logging
import os

from flask import Flask

from scribe.blueprints import blueprints
from scribe.utils.args_utils import parse_flask_server_args

# from scribe.utils.concurrency_utils.multiprocessing_utils import BackgroundProcessManager
from scribe.utils.concurrency_utils.threading_utils import ThreadManager
from scribe.utils.file_utils import initialise_filesystem
from scribe.utils.logging_utils import setup_logger
from scribe.utils.tts_utils.synthesis import InMemoryModels

logger = logging.getLogger(__name__)

app = Flask(__name__)


for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route("/healthcheck")
def healthcheck():
    return "OK"


def main(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    logger.info("Starting server...")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    args = parse_flask_server_args()
    setup_logger(args.log_level, args.console_log)

    filesystem_root = os.path.abspath(args.filesystem_root)
    initialise_filesystem(filesystem_root)
    app.config["FILESYSTEM_ROOT"] = filesystem_root
    # app.config["PROCESS_MANAGER"] = (
    #     None if (args.max_processes == None or args.max_processes == 0) else BackgroundProcessManager(max_processes=1)
    # )
    app.config[
        "THREAD_MANAGER"
    ] = (
        ThreadManager()
    )  # If both PROCESS_MANAGER and THREAD_MANAGER exist, I can just give a ThreadManager to a ProcessManager, as long as I setup my processes to take queues
    app.config["MODELS"] = InMemoryModels()
    main(args.host, args.port, False if args.log_level == logging.DEBUG else True)
