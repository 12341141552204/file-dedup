#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量文件去重工具
通过 MD5 哈希值识别重复文件，支持预览和删除
"""

import os
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict


def get_file_md5(filepath, chunk_size=8192):
    """计算文件 MD5"""
    md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        print(f"[警告] 无法读取 {filepath}: {e}")
        return None


def find_duplicates(folder, recursive=True):
    """查找重复文件"""
    folder = Path(folder)
    if not folder.is_dir():
        print(f"[错误] 目录不存在: {folder}")
        return {}

    # 先按文件大小分组，缩小比对范围
    size_groups = defaultdict(list)
    if recursive:
        files = folder.rglob("*")
    else:
        files = folder.iterdir()

    for f in files:
        if f.is_file():
            try:
                size_groups[f.stat().st_size].append(f)
            except Exception:
                pass

    # 对大小相同的文件计算 MD5
    md5_groups = defaultdict(list)
    for size, file_list in size_groups.items():
        if len(file_list) < 2:
            continue
        for f in file_list:
            md5 = get_file_md5(f)
            if md5:
                md5_groups[md5].append(f)

    # 只保留有重复的
    duplicates = {k: v for k, v in md5_groups.items() if len(v) > 1}
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="批量文件去重工具")
    parser.add_argument("folder", help="目标文件夹路径")
    parser.add_argument("--no-recursive", action="store_true", help="不递归子目录")
    parser.add_argument("--delete", action="store_true", help="删除重复文件（保留每组第一个）")
    args = parser.parse_args()

    print(f"扫描目录: {args.folder}")
    print("正在查找重复文件...\n")

    duplicates = find_duplicates(args.folder, recursive=not args.no_recursive)

    if not duplicates:
        print("没有发现重复文件")
        return

    total_dup = 0
    total_size = 0
    for md5, files in duplicates.items():
        print(f"MD5: {md5}")
        for i, f in enumerate(files):
            size = f.stat().st_size
            total_size += size
            tag = " [保留]" if i == 0 else " [重复]"
            print(f"  {tag} {f}  ({size / 1024:.1f} KB)")
            if i > 0:
                total_dup += 1
        print()

    print(f"共发现 {len(duplicates)} 组重复，{total_dup} 个重复文件")
    print(f"可释放空间: {total_size / 1024 / 1024:.2f} MB")

    if args.delete:
        print("\n开始删除重复文件...")
        deleted = 0
        for md5, files in duplicates.items():
            for f in files[1:]:
                try:
                    f.unlink()
                    print(f"  [已删除] {f}")
                    deleted += 1
                except Exception as e:
                    print(f"  [失败] {f}: {e}")
        print(f"\n已删除 {deleted} 个重复文件")


if __name__ == "__main__":
    main()
