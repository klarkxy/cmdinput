import sys
from typing import TextIO, TypeVar, Union, Tuple, List, Optional, Type

_buffer = None


def clear_buffer() -> None:
    """
    清空缓冲区

    用于在需要时清除读取的输入数据
    """
    global _buffer
    _buffer = None


T = TypeVar("T")


def _read_one_str(sep: Optional[str] = None, file: TextIO = sys.stdin) -> Optional[str]:
    """
    从输入源读取单个数据

    参数:
        sep: 分隔符 (可选)
        file: 输入源 (默认: sys.stdin)

    返回:
        分割后的第一个字符串部分
    """
    global _buffer
    if not _buffer:
        # 从文件或标准输入读取一行数据
        _buffer = file.readline().strip()

    # 按空白或指定分隔符分割缓冲区
    parts = _buffer.strip().split(sep, 1)

    # 更新缓冲区供下次读取(保留剩余部分)
    _buffer = parts[1] if len(parts) > 1 else None

    return parts[0] if parts else None


def _read_one(
    typ: Type[T], sep: Optional[str] = None, file: TextIO = sys.stdin
) -> Optional[str]:
    """
    从输入源读取单个数据并转换为指定类型

    """
    if typ is list:  # 如果是列表，循环读取
        ret = []
        for ty in typ:
            value = _read_one(ty, sep, file)
            if value is not None:
                ret.append(value)
            else:
                raise ValueError("List type requires non-null values")
        return ret

    value = _read_one_str(sep, file)
    # 处理布尔类型
    if typ == bool:
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        raise ValueError(f"Invalid boolean value: {value}")

    # 基础类型转换
    try:
        return typ(value) if callable(typ) else value
    except (ValueError, TypeError):
        raise ValueError(f"Could not convert {value} to {typ}")


def read(
    *types: Union[Type[T], list, dict],
    sep: Optional[str] = None,
    file: TextIO = sys.stdin,
) -> Union[T, Tuple[T, ...]]:
    """
    读取输入并返回指定类型的值

    参数:
        *types: 可变长度类型参数 (int, float, str等)
        sep: 分隔符 (可选)
        file: 输入源 (默认: sys.stdin)

    返回:
        单个值或指定类型的值元组

    示例:
        a, b = read(int, float)  # 读取一个整数和一个浮点数
        c = read(str)  # 读取单个字符串
    """

    result = []
    for typ in types:
        value = _read_one(typ, sep, file)

        result.append(value)

    return result[0] if len(result) == 1 else tuple(result)


def readline(file: TextIO = sys.stdin) -> str:
    """
    读取一行输入

    参数:
        file: 输入源 (默认: sys.stdin)

    返回:
        输入的字符串
    """
    global _buffer
    if _buffer:
        ret = _buffer
        _buffer = None
        return ret
    else:
        return file.readline().strip()
