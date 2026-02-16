# Browser Relay Incident Report Format

When failure occurs, report in this order:

1. Time (KST)
2. Immediate previous action
3. Raw error message
4. Impact
5. Immediate mitigation
6. Next plan

Example (single line each):

- Time: 2026-02-16 14:49 KST
- Previous action: Scholar `navigate(start=30)` then `snapshot`
- Error: `Error: Error: tab not found`
- Impact: Post-navigation page capture failed
- Immediate mitigation: switched to Atomic Tab open/snapshot/close
- Next plan: continue URL-parameter sweep and defer click-based transitions
