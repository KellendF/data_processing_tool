#!/bin/bash

# =============================================
# 批量下载脚本 - macOS curl 版
# 用法: ./batch_download.sh urls.txt [输出目录]
# =============================================

set -euo pipefail

# 获取 urls.txt 绝对路径
URLS_FILE="$(cd "$(dirname "${1:-}")" 2>/dev/null && pwd)/$(basename "${1:-}")"
OUTPUT_DIR="${2:-downloads}"

# 检查参数
if [ -z "${1:-}" ] || [ ! -f "$URLS_FILE" ]; then
    echo "用法: $0 <url列表文件> [输出目录]"
    echo "示例: $0 urls.txt ./resources"
    exit 1
fi

# 创建输出目录并进入
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

echo "🚀 开始批量下载 (使用 curl)..."
echo "URL列表文件: $URLS_FILE"
echo "输出目录: $(pwd)"
echo "========================================"

# 统计有效URL数量
total=$(grep -vE '^\s*#|^\s*$' "$URLS_FILE" | wc -l)
count=0
success=0

while IFS= read -r url || [ -n "$url" ]; do
    # 跳过空行和注释
    [[ -z "$url" || "$url" =~ ^[[:space:]]*# ]] && continue
    
    ((count++))
    echo -e "\n[$count/$total] 下载: $url"
    
    # 从URL中提取文件名（如果URL有查询参数则清理）
    filename=$(basename "$url" | sed 's/[?#].*//')
    
    # 如果文件名为空或无效，则使用序号命名
    if [ -z "$filename" ] || [ "$filename" = "/" ]; then
        filename="file_$count"
    fi
    
    # 使用 curl 下载（支持断点续传）
    if curl -L -C - --progress-bar --fail --retry 3 --retry-delay 5 \
         --connect-timeout 30 "$url" -o "$filename"; then
        echo "✅ 下载成功: $filename"
        ((success++))
    else
        echo "❌ 下载失败: $url"
    fi

done < "$URLS_FILE"

echo -e "\n========================================"
echo "🎉 下载完成！"
echo "成功: $success / $total"
echo "文件保存在: $(pwd)"
