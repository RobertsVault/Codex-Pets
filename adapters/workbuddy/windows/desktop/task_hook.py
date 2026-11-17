"""WorkBuddy lifecycle receiver. Persists content-free status only."""
import json,sys
from events import write_event
STATES={'UserPromptSubmit':'coding','PermissionRequest':'waiting','PreToolUse':'coding',
        'PostToolUse':'coding','Stop':'celebrate','SessionEnd':'idle','StopFailure':'failed','Notification':None}
def main():
    try:
        raw=sys.stdin.read(1024*1024+1)
        if len(raw)>1024*1024:return 0
        payload=json.loads(raw)
        if not isinstance(payload,dict):return 0
        event=payload.get('hook_event_name')
        if not event and '--event' in sys.argv:
            event=sys.argv[sys.argv.index('--event')+1]
        state=STATES.get(event)
        if event=='Notification':
            if payload.get('notification_type') in ('permission_prompt','elicitation_dialog'):state='waiting'
        if state:
            session=str(payload.get('session_id') or payload.get('conversation_id') or 'unknown')
            write_event(state,'workbuddy|'+session,'')
    except Exception:pass
    return 0
if __name__=='__main__':raise SystemExit(main())
