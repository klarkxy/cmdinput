# CMD-Input
还在用 `input()` 吗？还在用 `map(int, input().split())` 吗？
```python
a, b, c = map(int, input().split())
```
不如试试 `cmdinput` 吧！
```python
a, b, c = cmdinput.read(int, int, int)
```