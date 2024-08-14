import unittest
from types import SimpleNamespace

from sglang.srt.utils import kill_child_process
from sglang.test.run_eval import run_eval
from sglang.test.test_utils import (
    DEFAULT_MODEL_NAME_FOR_TEST,
    DEFAULT_URL_FOR_UNIT_TEST,
    popen_launch_server,
)


class TestTritonAttnBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = DEFAULT_MODEL_NAME_FOR_TEST
        cls.base_url = DEFAULT_URL_FOR_UNIT_TEST
        cls.process = popen_launch_server(
            cls.model, cls.base_url, timeout=300, other_args=["--disable-flashinfer"]
        )

    @classmethod
    def tearDownClass(cls):
        kill_child_process(cls.process.pid)

    def test_mmlu(self):
        args = SimpleNamespace(
            base_url=self.base_url,
            model=self.model,
            eval_name="mmlu",
            num_examples=32,
            num_threads=32,
        )

        metrics = run_eval(args)
        assert metrics["score"] >= 0.6


if __name__ == "__main__":
    unittest.main()
