# 批量文件去重工具 (file-dedup)

基于 MD5 哈希值的重复文件查找与清理工具。

## 功能

- 按文件内容（MD5）识别重复文件
- 先按文件大小分组，提升扫描速度
- 支持递归子目录
- 预览重复文件及可释放空间
- 一键删除重复文件（保留每组第一个）

## 使用方法

```bash
# 预览重复文件
python main.py ./downloads

# 不递归子目录
python main.py ./downloads --no-recursive

# 删除重复文件（保留每组第一个）
python main.py ./downloads --delete
```

## 依赖

仅使用 Python 标准库，无需额外安装。
