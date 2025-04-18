import sys
from typing import TextIO, TypeVar

_buffer = None

def _read_one(sep : str=None, file : TextIO=sys.stdin) -> str:
    """
    从输入源读取单行数据
    
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

def clear_buffer() -> None:
    """
    清空缓冲区
    
    用于在需要时清除读取的输入数据
    """
    global _buffer
    _buffer = None

T = TypeVar('T')

def _transform(value: str, typ: type[T]) -> T:
    """
    将输入字符串转换为指定类型
    
    参数:
        value: 输入字符串
        typ: 目标类型 (int, float, str, bool等)
    
    返回:
        转换后的指定类型值
        
    注意:
        对于bool类型，会将'true'(不区分大小写)转换为True
        其他类型则调用类型构造函数进行转换
    """
    if typ == bool:
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        raise ValueError(f"Invalid boolean value: {value}")
    try:
        return typ(value) if callable(typ) else value
    except (ValueError, TypeError):
        raise ValueError(f"Could not convert {value} to {typ}")

def read(*types : type[T], sep : str=None, file : TextIO=sys.stdin) -> T | tuple[T, ...]:
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
        value_str = _read_one(sep, file)
        if not value_str:
            raise ValueError("No input provided")
        
        value = _transform(value_str, typ)
            
        result.append(value)
    
    return result[0] if len(result) == 1 else tuple(result)

def readline(file : TextIO=sys.stdin) -> str:
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
        
def read_list(typ : type[T], n : int, sep : str=None, file : TextIO=sys.stdin) -> list[T]:
    """
    读取输入并返回指定类型的列表
    
    参数:
        typ: 目标类型 (int, float, str等)
        sep: 分隔符 (可选)
        file: 输入源 (默认: sys.stdin)
    
    返回:
        指定类型的列表
        
    示例:
        lst = read_list(int)  # 读取一个整数列表
    """
    if n == 0:
        raise ValueError("Cannot read empty list")
    result = []
    for _ in range(n):
        value_str = _read_one(sep, file)
        if not value_str:
            raise ValueError("No input provided")
        
        value = _transform(value_str, typ)
            
        result.append(value)
    
    return result
