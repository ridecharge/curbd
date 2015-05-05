import curbd
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock


class CurbdTest(TestCase):
    def setUp(self):
        self.consul_conn = MagicMock()
        self.options = MagicMock()
        self.options.config = 'config'
        self.options.key_prefix = 'key_prefix'
        self.key_prefix = self.options.key_prefix + "/" + self.options.config + "/"
        self.path = "../curbd-config/" + self.options.key_prefix + "/" \
                    + self.options.config + ".json"
        self.service = MagicMock()
        self.curbd = curbd.Curbd(self.service, self.options)

    def test_populate(self):
        self.curbd.populate()
        self.service.populate_json.assert_called_with(self.path, self.key_prefix)

    def test_new_json(self):
        c = curbd.new_curbd(self.options)
        self.assertIsInstance(c, curbd.Curbd)
        self.assertIsInstance(c.service, curbd.CurbdService)


class CurbdServiceTest(TestCase):
    def setUp(self):
        self.options = MagicMock()
        self.consul_conn = MagicMock()
        self.consul_conn.kv = MagicMock()
        self.service = curbd.CurbdService(self.consul_conn)

    @patch('builtins.open', mock_open(read_data="{\"hello\":\"world\"}"))
    def test_populate_json(self):
        self.service.populate_json('path/', 'key_prefix/')
        self.consul_conn.kv.put.assert_called_with('key_prefix/hello', 'world')
