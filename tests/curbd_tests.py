import curbd
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock


class CurbdJsonTest(TestCase):
    def setUp(self):
        self.consul_conn = MagicMock()
        self.options = MagicMock()
        self.options.service_name = 'service'
        self.options.program = 'prog'
        self.key_prefix = self.options.program + "/" + self.options.service_name + "/"
        self.path = "../curbd/" + self.options.program + "/" + self.options.service_name + ".json"
        self.curbd = curbd.CurbdJson(self.consul_conn, self.options)

    @patch('curbd.curbd.populate_json')
    def test_populate(self, populate_json):
        self.curbd.populate()
        populate_json.assert_called_with(self.consul_conn, self.path, self.key_prefix)


class CurbdCfTest(TestCase):
    def setUp(self):
        self.consul_conn = MagicMock()
        self.consul_conn.kv = MagicMock()
        self.cf_conn = MagicMock()
        self.output = MagicMock()
        self.output.key = 'key'
        self.output.value = 'value'
        self.outputs = [self.output]
        self.stack = MagicMock()
        self.stack.outputs = self.outputs
        self.stacks = [self.stack]
        self.cf_conn.describe_stacks = MagicMock(return_value=self.stacks)
        self.options = MagicMock()
        self.options.service_name = 'service'
        self.options.environment = 'mock'
        self.key_prefix = "cf/" + self.options.service_name + "/"
        self.path = "../curbd/mock-cf/" + self.options.service_name + ".json"

    @patch('curbd.curbd.populate_json')
    def test_populate_mock_env(self, populate_json):
        c = curbd.CurbdCf(self.cf_conn, self.consul_conn, self.options)
        c.populate()
        populate_json.assert_called_with(self.consul_conn, self.path, self.key_prefix)

    def test_populate(self):
        self.options.environment = 'test'
        stack_name = self.options.environment + "-" + self.options.service_name
        c = curbd.CurbdCf(self.cf_conn, self.consul_conn, self.options)
        c.populate()
        self.cf_conn.describe_stacks.assert_called_with(stack_name)
        self.consul_conn.kv.put.assert_called_with('cf/service/key', 'value')


class CurbdFuncTest(TestCase):
    def setUp(self):
        self.options = MagicMock()
        self.consul_conn = MagicMock()
        self.consul_conn.kv = MagicMock()

    def test_convert(self):
        converted = curbd.curbd.convert('HelloWorld')
        self.assertEqual(converted, "hello_world")

    @patch('builtins.open', mock_open(read_data="{\"hello\":\"world\"}"))
    def test_populate_json(self):
        curbd.curbd.populate_json(self.consul_conn, 'path/', 'key_prefix/')
        self.consul_conn.kv.put.assert_called_with('key_prefix/hello', 'world')

    def test_new_json(self):
        self.options.subcommand = 'from_json'
        c = curbd.new_curbd(self.options)
        self.assertIsInstance(c, curbd.CurbdJson)

    def test_new_cf(self):
        self.options.subcommand = 'from_cf'
        c = curbd.new_curbd(self.options)
        self.assertIsInstance(c, curbd.CurbdCf)

    def test_new_exception(self):
        self.options.subcommand = 'notfound'
        with self.assertRaises(BaseException):
            curbd.new_curbd(self.options)

