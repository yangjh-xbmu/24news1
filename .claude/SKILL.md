---
name: get-current-date
description: 当用户需要UTC格式的时间时，请执行此技能
---

当用户获取当前时间的时候，请执行如下脚本

```bash
date -u '+%Y-%m-%dT%H:%M:%SZ'
```
