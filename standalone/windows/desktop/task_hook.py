"""Codex command hook: ignores prompt, transcript, arguments and output."""
import json
import sys
from events import write_event

STATES={'UserPromptSubmit':'coding','PermissionRequest':'waiting',
        'PreToolUse':'coding','PostToolUse':'coding','Stop':'celebrate',
        'Interrupt':'idle','SessionEnd':'idle'}

def main():
    try:
        raw=sys.stdin.read(1024*1024+1)
        if len(raw)>1024*1024:return 0
        payload=json.loads(raw)
        if not isinstance(payload,dict): return 0
        state=STATES.get(payload.get('hook_event_name'))
        if state:
            write_event(state,str(payload.get('session_id','unknown')),str(payload.get('turn_id','')))
    except Exception:
        pass  # A companion must never block a Codex task.
    return 0  # No output, approval decision, context, or continuation instruction.

if __name__=='__main__': raise SystemExit(main())
