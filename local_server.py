from flask import Flask, request
import logging
import multiprocessing

log = logging.getLogger(__name__)


def create_flask(auth_queue):
    app = Flask(__name__)

    @app.route("/choco_auth", methods=["GET"])
    def choco_auth():
        code = request.args.get("code")
        if code:
            log.info(f"Authorization code received: {code}")
            auth_queue.put(code)
            return f"Authorization code received: {code}"
        else:
            log.warning("No authorization code received")
            return "No authorization code received"

    return app


def run_flask(auth_queue):
    app = create_flask(auth_queue)
    app.run(host="0.0.0.0", port=5000)


class TempServer:
    def __init__(self):
        self.auth_queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(
            target=run_flask, args=(self.auth_queue,)
        )

    def start(self):
        log.info("Starting Flask app...")
        self.process.start()

    def stop(self):
        log.info("Stopping Flask app...")
        self.process.terminate()
        self.process.join()

    def get_auth_code(self):
        return self.auth_queue.get(block=True)


if __name__ == "__main__":
    app = TempServer()
    app.start()
