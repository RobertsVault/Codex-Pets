"""All visible companion text; state identifiers remain language-neutral."""
STATE_LABELS={
 'zh':{'idle':'待机陪伴','coding':'任务处理中','waiting':'等待输入／批准','review':'检查结果',
       'celebrate':'完成啦','failed':'遇到问题','petting':'摸摸头','eating':'吃点零食','ball':'一起玩球',
       'begging':'握个爪','roll':'摸摸肚皮','run':'奔跑','trot':'散步','sniff':'看看周围','sleep':'睡觉充电','curious':'思考一下'},
 'en':{'idle':'Idle','coding':'Working','waiting':'Awaiting input / approval','review':'Reviewing results',
       'celebrate':'All done!','failed':'Something went wrong','petting':'Head pats','eating':'Snack time','ball':'Play ball',
       'begging':'Shake paws','roll':'Belly rubs','run':'Running','trot':'Walking','sniff':'Exploring','sleep':'Sleeping','curious':'Thinking'}
}
TEXT={
 'zh':{'name_mikan':'橘宝 Mikan','name_doubao':'豆包 Doubao','window':'{name} · WorkBuddy 伙伴',
       'minimum':'{name}（至少 {seconds} 秒）','demo_menu':'手动切换状态（暂停任务跟随）',
       'follow':'跟随 WorkBuddy 任务','roam':'空闲时自动散步','topmost':'始终置顶','gaze':'视线跟随鼠标','size':'显示大小','await_events':'WorkBuddy · 等待事件',
       'reset':'清除任务／解除卡住状态','exit':'退出','language':'语言 / Language','expanded':'细致动画',
       'hint':'右键打开互动菜单','busy':'任务优先，结束或解除等待后再来玩',
       'result_first':'先展示任务结果，稍后再来玩','demo_notice':'手动模式；右键可恢复任务跟随',
       'follow_on':'已恢复任务跟随','follow_off':'已暂停任务跟随','reset_notice':'已清除当前任务状态',
       'waiting_suffix':' · 持续等待','working_suffix':' · 持续展示','countdown':' · {seconds} 秒',
       'follow_status':'WorkBuddy · 已收到事件','demo_status':'手动模式','affection':' · 亲密度 {value}'},
 'en':{'name_mikan':'Mikan','name_doubao':'Doubao','window':'{name} · WorkBuddy companion',
       'minimum':'{name} (at least {seconds}s)','demo_menu':'Choose state (pause task following)',
       'follow':'Follow WorkBuddy tasks','roam':'Roam while idle','topmost':'Always on top','gaze':'Look toward pointer','size':'Display size','await_events':'WorkBuddy · awaiting events',
       'reset':'Clear tasks / unstick state','exit':'Quit','language':'Language / 语言','expanded':'Detailed animation',
       'hint':'Right-click for interactions','busy':'Task comes first. Let me finish, then we can play!',
       'result_first':'Showing task results. We can play in a moment.',
       'demo_notice':'Manual mode; right-click to resume task following',
       'follow_on':'Task following resumed','follow_off':'Task following paused','reset_notice':'Task state cleared',
       'waiting_suffix':' · waiting','working_suffix':' · active','countdown':' · {seconds}s',
       'follow_status':'WorkBuddy · events received','demo_status':'Manual mode','affection':' · Bond {value}'}
}

def tr(language,key,**values):
    language=language if language in TEXT else 'zh'
    if key.startswith('state_'):return STATE_LABELS[language][key[6:]]
    return TEXT[language][key].format(**values)
