import unittest
import io
from cmdinput import read, readline, clear_buffer


class TestCmdInput(unittest.TestCase):
    def setUp(self):
        """在每个测试前清空缓冲区"""
        clear_buffer()

    def test_read_single_value(self):
        """测试读取单个值"""
        input_str = "42\n"
        with io.StringIO(input_str) as f:
            result = read(int, file=f)
            self.assertEqual(result, 42)

    def test_read_multiple_values(self):
        """测试读取多个值"""
        input_str = "42 3.14 hello\n"
        with io.StringIO(input_str) as f:
            a, b, c = read(int, float, str, file=f)
            self.assertEqual(a, 42)
            self.assertAlmostEqual(b, 3.14)
            self.assertEqual(c, "hello")

    def test_read_with_custom_separator(self):
        """测试使用自定义分隔符"""
        input_str = "42,3.14,hello\n"
        with io.StringIO(input_str) as f:
            a, b, c = read(int, float, str, sep=",", file=f)
            self.assertEqual(a, 42)
            self.assertAlmostEqual(b, 3.14)
            self.assertEqual(c, "hello")

    def test_read_bool(self):
        """测试读取布尔值"""
        input_str = "true\nfalse\nTrue\nFalse\n"
        with io.StringIO(input_str) as f:
            self.assertTrue(read(bool, file=f))
            self.assertFalse(read(bool, file=f))
            self.assertTrue(read(bool, file=f))
            self.assertFalse(read(bool, file=f))

    def test_read_binary(self):
        """测试读取二进制数值"""
        input_str = "1010\n1111\n100000\n102\n"
        with io.StringIO(input_str) as f:
            # 有效二进制测试
            self.assertEqual(read(lambda x: int(x, 2), file=f), 0b1010)
            self.assertEqual(read(lambda x: int(x, 2), file=f), 0b1111)
            self.assertEqual(read(lambda x: int(x, 2), file=f), 0b100000)

            # 无效二进制测试
            with self.assertRaises(ValueError):
                read(lambda x: int(x, 2), file=f)

    def test_readline(self):
        """测试读取整行"""
        input_str = "this is a complete line\n"
        with io.StringIO(input_str) as f:
            self.assertEqual(readline(file=f), "this is a complete line")

    def test_read_list(self):
        """测试读取列表"""
        input_str = "1 2 3 4 5\n"
        with io.StringIO(input_str) as f:
            lst = read([int] * 5, file=f)
            self.assertEqual(lst, [1, 2, 3, 4, 5])

    def test_buffer_management(self):
        """测试缓冲区管理"""
        input_str = "1 2 3\n4 5 6\n"
        with io.StringIO(input_str) as f:
            # 第一次读取会消耗第一行
            a = read(int, file=f)
            self.assertEqual(a, 1)

            # 清空缓冲区后应该从第二行开始读取
            clear_buffer()
            b = read(int, file=f)
            self.assertEqual(b, 4)

    def test_empty_input(self):
        """测试空输入"""
        with io.StringIO("") as f:
            with self.assertRaises(ValueError):
                read(int, file=f)

    def test_type_conversion_error(self):
        """测试类型转换错误"""
        with io.StringIO("not_a_number\n") as f:
            with self.assertRaises(ValueError):
                read(int, file=f)

    def test_mixed_type_reading(self):
        """测试混合类型读取"""
        input_str = "42 3.14 True hello\n"
        with io.StringIO(input_str) as f:
            a, b, c, d = read(int, float, bool, str, file=f)
            self.assertEqual(a, 42)
            self.assertAlmostEqual(b, 3.14)
            self.assertTrue(c)
            self.assertEqual(d, "hello")

    def test_long_string_reading(self):
        """测试长字符串读取"""
        long_str = "a" * 1000
        input_str = f"{long_str}\n"
        with io.StringIO(input_str) as f:
            self.assertEqual(read(str, file=f), long_str)

    def test_special_separator(self):
        """测试特殊分隔符"""
        input_str = "42|3.14|hello\n"
        with io.StringIO(input_str) as f:
            a, b, c = read(int, float, str, sep="|", file=f)
            self.assertEqual(a, 42)
            self.assertAlmostEqual(b, 3.14)
            self.assertEqual(c, "hello")

    def test_multiline_buffer_management(self):
        """测试多行缓冲区管理"""
        input_str = "1 2\n3 4\n5 6\n"
        with io.StringIO(input_str) as f:
            a = read(int, file=f)  # 读取1
            b = read(int, file=f)  # 读取2
            clear_buffer()
            c = read(int, file=f)  # 应该读取3
            self.assertEqual(a, 1)
            self.assertEqual(b, 2)
            self.assertEqual(c, 3)

    def test_partial_read_then_clear(self):
        """测试部分读取后清空缓冲区"""
        input_str = "1 2 3\n4 5 6\n"
        with io.StringIO(input_str) as f:
            a = read(int, file=f)  # 读取1
            clear_buffer()
            b = read(int, file=f)  # 应该读取4
            self.assertEqual(a, 1)
            self.assertEqual(b, 4)

    def test_read_empty_list(self):
        """测试读取空列表"""
        input_str = "\n"
        with io.StringIO(input_str) as f:
            with self.assertRaises(ValueError):
                read([int] * 0, file=f)

    def test_read_single_element_list(self):
        """测试读取单元素列表"""
        input_str = "42\n"
        with io.StringIO(input_str) as f:
            lst = read([int] * 1, file=f)
            self.assertEqual(lst, [42])

    def test_read_large_list(self):
        """测试读取大列表"""
        input_str = " ".join(str(i) for i in range(100)) + "\n"
        with io.StringIO(input_str) as f:
            lst = read([int] * 100, file=f)
            self.assertEqual(lst, list(range(100)))

    def test_mixed_read_and_readline(self):
        """测试混合使用read和readline"""
        input_str = "1 2\ncomplete line\n3 4\n"
        with io.StringIO(input_str) as f:
            a = read(int, file=f)  # 读取1
            line1 = readline(file=f)  # 读取"2"
            line2 = readline(file=f)  # 读取"complete line"
            b, c = read(int, int, file=f)  # 读取3和4
            self.assertEqual(a, 1)
            self.assertEqual(line1, "2")
            self.assertEqual(line2, "complete line")
            self.assertEqual(b, 3)
            self.assertEqual(c, 4)

    def test_read_string_with_spaces(self):
        """测试读取带空格的字符串"""
        input_str = "hello world\n"
        with io.StringIO(input_str) as f:
            self.assertEqual(read(str, file=f), "hello")

    def test_read_string_with_newlines(self):
        """测试读取带换行符的字符串"""
        input_str = "hello\nworld\n"
        with io.StringIO(input_str) as f:
            self.assertEqual(read(str, file=f), "hello")
            self.assertEqual(readline(file=f), "world")

    def test_read_string_with_tabs(self):
        """测试读取带制表符的字符串"""
        input_str = "hello\tworld\n"
        with io.StringIO(input_str) as f:
            a, b = read(str, str, file=f)
            self.assertEqual(a, "hello")
            self.assertEqual(b, "world")

    def test_read_string_with_special_chars(self):
        """测试读取带特殊符号的字符串"""
        input_str = "hello!@#$%^&*()world\n"
        with io.StringIO(input_str) as f:
            self.assertEqual(read(str, file=f), "hello!@#$%^&*()world")

    def test_read_very_long_line(self):
        """测试读取超长行"""
        long_line = "a" * 10000 + " " + "b" * 10000 + "\n"
        with io.StringIO(long_line) as f:
            a, b = read(str, str, file=f)
            self.assertEqual(a, "a" * 10000)
            self.assertEqual(b, "b" * 10000)

    def test_read_multiline_list(self):
        """测试读取多行列表"""
        input_str = "1 2\n3 4\n5 6\n"
        with io.StringIO(input_str) as f:
            lst = []
            for _ in range(3):
                lst.extend(read([int] * 2, file=f))
            self.assertEqual(lst, [1, 2, 3, 4, 5, 6])

    def test_read_then_immediate_clear(self):
        """测试读取后立即清空缓冲区"""
        input_str = "1 2\n3 4\n"
        with io.StringIO(input_str) as f:
            a = read(int, file=f)
            clear_buffer()
            b = read(int, file=f)
            self.assertEqual(a, 1)
            self.assertEqual(b, 3)

    def test_read_various_bool_values(self):
        """测试读取不同类型布尔值"""
        input_str = "True\ntrue\nFalse\nfalse\n1\n0\nyes\nno\n"
        with io.StringIO(input_str) as f:
            self.assertTrue(read(bool, file=f))
            self.assertTrue(read(bool, file=f))
            self.assertFalse(read(bool, file=f))
            self.assertFalse(read(bool, file=f))
            with self.assertRaises(ValueError):
                read(bool, file=f)  # 1
            with self.assertRaises(ValueError):
                read(bool, file=f)  # 0
            with self.assertRaises(ValueError):
                read(bool, file=f)  # yes
            with self.assertRaises(ValueError):
                read(bool, file=f)  # no

    def test_read_with_leading_trailing_spaces(self):
        """测试读取带前导/后缀空格的值"""
        input_str = "   42   \n   3.14   \n   hello   \n"
        with io.StringIO(input_str) as f:
            a, b, c = read(int, float, str, file=f)
            self.assertEqual(a, 42)
            self.assertAlmostEqual(b, 3.14)
            self.assertEqual(c, "hello")

    def test_read_list_with_leading_trailing_spaces(self):
        """测试读取带前导/后缀空格的列表"""
        input_str = "   1   2   3   \n"
        with io.StringIO(input_str) as f:
            lst = read([int] * 3, file=f)
            self.assertEqual(lst, [1, 2, 3])

    def test_mixed_int_float_list(self):
        """测试混合整型和浮点型列表"""
        input_str = "1 2 3 4 5 1.1 2.2 3.3\n"
        with io.StringIO(input_str) as f:
            lis = read([int] * 5 + [float] * 3, file=f)
            self.assertEqual(lis, [1, 2, 3, 4, 5, 1.1, 2.2, 3.3])

    def test_nested_int_lists(self):
        """测试嵌套整型列表"""
        input_str = "1 2 3 4\n5 6 7 8\n9 10 11 12\n"
        with io.StringIO(input_str) as f:
            matrix = read([[int] * 4] * 3, file=f)
            self.assertEqual(matrix, [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

    def test_multidimensional_list(self):
        """测试三维列表读取"""
        input_str = "1 2\n3 4\n5 6\n7 8\n9 10\n11 12\n"
        with io.StringIO(input_str) as f:
            cube = read([[[int] * 2] * 2] * 3, file=f)

            self.assertEqual(
                cube, [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]]
            )


if __name__ == "__main__":
    unittest.main()
