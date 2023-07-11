import sys
import os

sys.path.append(os.getcwd())
sys.path.append(f"{os.getcwd()}/src/pyno_logger")

from unittest.mock import patch
from unittest import TestCase
from pyno_logger import Pyno


class PynoTests(TestCase):
    @patch("builtins.print")
    def test_should_print(self, mock_print):
        logger = Pyno(
            {
                "level": "DEBUG",
            }
        )
        logger.debug("debug log")
        assert mock_print.called

    @patch("builtins.print")
    def test_should_not_log_on_silent(self, mock_print):
        logger = Pyno(
            {
                "level": "SILENT",
            }
        )
        logger.debug("debug log")
        assert not mock_print.called

    @patch("builtins.print")
    def test_should_omit(self, mock_print):
        # list
        logger = Pyno(
            {
                "omit": ["foo"],
            }
        )
        logger.info({"foo": "bar"}, "dict log")
        assert mock_print.called
        assert "foo" not in mock_print.call_args[0][0]

        # comma separated string
        logger = Pyno(
            {
                "omit": "foo,bar",
            }
        )
        logger.info({"foo": "bar", "bar": "foo"}, "dict log")
        assert mock_print.called
        assert "foo" not in mock_print.call_args[0][0]
        assert "bar" not in mock_print.call_args[0][0]

        # tuple
        logger = Pyno(
            {
                "omit": ("foo", "bar"),
            }
        )
        logger.info({"foo": "bar", "bar": "foo"}, "dict log")
        assert mock_print.called
        assert "foo" not in mock_print.call_args[0][0]
        assert "bar" not in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_redact(self, mock_print):
        logger = Pyno({"redact": ["foo"]})
        logger.info({"foo": "bar"}, "dict log")
        assert "[REDACTED]" in mock_print.call_args[0][0]

        # comma separated string
        logger = Pyno({"redact": "foo,bar"})
        logger.info({"foo": "bar"}, "dict log")
        assert "[REDACTED]" in mock_print.call_args[0][0]

        logger = Pyno({"redact": ("foo", "bar")})
        logger.info({"foo": "bar"}, "dict log")
        assert "[REDACTED]" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_set_redact_value(self, mock_print):
        logger = Pyno({"redact": "foo,bar", "redact_value": "***"})
        logger.info({"foo": "bar"}, "dict log")
        assert "***" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_log_newlines(self, mock_print):
        logger = Pyno(
            {
                "newlines": True,
            }
        )
        logger.info("foo")
        assert mock_print.called
        assert "\n" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_set_base_config(self, mock_print):
        logger = Pyno(
            {
                "base": {
                    "foo": "bar",
                }
            }
        )
        logger.info("info log")
        assert mock_print.called
        assert "foo" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_set_mixin_config(self, mock_print):
        def mixin():
            return {
                "foo": "bar",
            }

        logger = Pyno(
            mixin=mixin,
        )
        logger.info("info log")
        assert mock_print.called
        assert "foo" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_set_error_key(self, mock_print):
        logger = Pyno(
            {
                "error_key": "test_error",
            }
        )
        logger.error(Exception("this is a test"), "dict log")
        assert mock_print.called
        assert "test_error" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_set_message_key(self, mock_print):
        logger = Pyno(
            {
                "msg_key": "message",
            }
        )
        logger.info("info log")
        assert mock_print.called
        assert "message" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_be_able_to_disable(self, mock_print):
        logger = Pyno()
        logger.enabled(False)
        logger.info("info log")
        assert not mock_print.called

    @patch("builtins.print")
    def test_should_log_lists(self, mocK_print):
        logger = Pyno()
        logger.info(["foo", "bar"], "list log")
        assert mocK_print.called
        assert '"0": "foo"' in mocK_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_log_strings_as_msg(self, mock_print):
        logger = Pyno()
        logger.info("info log")
        assert '"msg": "info log"' in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_child_logger_should_inherit(self, mock_print):
        logger = Pyno(
            {
                "level": "DEBUG",
            }
        )
        child_logger = logger.child(name={"foo": "bar"})
        assert child_logger.log_level == "DEBUG"
        child_logger.info("info log")
        assert mock_print.called
        assert "foo" in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_log_none(self, mock_print):
        logger = Pyno(
            {
                "log_none": True,
            }
        )
        logger.info({"foo": None}, "dict log")
        assert mock_print.called
        assert "foo" in mock_print.call_args[0][0]
        logger = Pyno(
            {
                "log_none": False,
            }
        )
        logger.info({"foo": None}, "dict log")
        assert mock_print.called
        assert "foo" not in mock_print.call_args[0][0]

    @patch("builtins.print")
    def test_should_log_data_in_both_orders(self, mock_print):
        logger = Pyno()
        logger.info("info log", {"foo": "bar"})
        assert mock_print.called
        assert '"foo": "bar"' in mock_print.call_args[0][0]
        assert '"msg": "info log"' in mock_print.call_args[0][0]


if __name__ == "__main__":
    PynoTests.main()
