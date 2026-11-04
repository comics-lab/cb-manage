# <Topic Title>

> Logging rules: [`Extended_Logging_Runbook.md`](../system/runbooks/Extended_Logging_Runbook.md)

> Startup mode: basic/standard. Topic logging never changes `config/local.yaml`;
> detail/verbatim and extended modes are session-scoped runtime instructions.

## Agent Runtime Identity (Current)
- agent_type: <browser|ide|terminal>
- host: <ChatGPT|Gemini|Codex|Copilot|Other>
- runtime: <codex-cli|vscode|other>
- session_id: <stable session identifier>
- task_id: <bounded task identifier>
- environment: <browser name/version OR IDE name/version OR shell name>
- os: <os name/version>
- workspace: <repo path or project name>
- boundaries: <tools, filesystem, network>
- model: <if disclosed by host>
- timestamp: <YYYY-MM-DD HH:MM America/Los_Angeles>
- method: <auto|manual>

## Invocation Metadata
- primary_agent: <stable registry agent ID>
- supporting_agents: <comma-separated stable IDs, or none>
- skills_loaded: <stable skill names, or none>
- contracts_applied: <contract IDs, or none>
- attribution_source: <runtime|exit-summary|manual|estimate>
- attribution_confidence: <high|medium|low|unknown>

## Session — <YYYY-MM-DD HH:MM America/Los_Angeles> — <Short Summary>

### User Prompt
<Brief summary of the user's prompt; use exact text only in merged detail/verbatim mode>

### Agent Response
<Brief summary of the agent's response; use exact text only in merged detail/verbatim mode>

### Artifacts / References
- <relative paths, docs, or external sources>

### Code Changes
#### File: <relative/path>
<Language>
<Summary or excerpt of changes>

### Notes
- Decisions made
- Trade-offs discussed
- Open questions

### Detail / Verbatim Log (Optional, Session-Only)
Standard logging uses concise summaries in this topic file. If the user requests
either **detail logging** or **verbatim logging**, treat both phrases as the
same merged session mode and create:

`docs/agents/chats/<topic>__detail_YYYY-MM-DD.md`

Capture expanded context plus the exact user prompt and final response. If the
user requests **extended logging**, use
`docs/agents/chats/<topic>__extended_YYYY-MM-DD.md` and include summarized
progress and tool actions. Any unresolved error automatically triggers
extended logging until resolved. See the runbook above for redaction and exit
rules.

---
**Agent**: <Agent Name / Tool>
