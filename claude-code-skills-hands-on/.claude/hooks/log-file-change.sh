#!/bin/sh

file_path=$(jq -r '.tool_input.file_path // ""')

printf '[%s] %s が編集されました\n' \
  "$(date)" \
  "$file_path" \
  >> /tmp/claude-hook.log