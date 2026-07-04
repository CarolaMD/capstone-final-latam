#!/usr/bin/env python
"""PostToolUse / PostToolUseFailure hook for Bash: append a line to session-log.md.

Claude Code passes hook data as a JSON object on STDIN (there are no
$CLAUDE_TOOL_INPUT / $CLAUDE_TOOL_RESULT_EXIT_CODE env vars). The executed
command lives at tool_input.command. PostToolUse fires only on success
(exit 0); a non-zero exit fires PostToolUseFailure, where the code is embedded
in the `error` string, e.g. "Exit code 7\n...".
"""
import sys
import os
import re
import json
import datetime


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    command = (data.get("tool_input") or {}).get("command", "")
    command = " ".join(command.split())  # collapse newlines/whitespace

    if data.get("hook_event_name") == "PostToolUseFailure":
        error = data.get("error") or ""
        match = re.search(r"Exit code (\d+)", error)
        code = match.group(1) if match else "nonzero"
    else:
        code = "0"

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | exit:{code} | {command[:120]}"

    log_path = os.path.join(data.get("cwd") or ".", "session-log.md")
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


if __name__ == "__main__":
    main()
