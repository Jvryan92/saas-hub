import json
import datetime
import os

REGISTRY_PATH = "agents/agent_registry.json"
LOG_PATH = "logs/agent_actions.jsonl"

def register_agent(agent_id, agent_role, status="active", last_action="initialized self-registration"):
    try:
        with open(REGISTRY_PATH, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"agents": []}

    agents = data.get("agents", [])
    found = False
    for agent in agents:
        if agent["id"] == agent_id:
            agent["status"] = status
            agent["last_action"] = last_action
            agent["role"] = agent_role
            found = True
    if not found:
        agents.append({
            "id": agent_id,
            "role": agent_role,
            "status": status,
            "last_action": last_action
        })
    data["agents"] = agents
    data["updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def log_action(agent_id, action, file):
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "agent": agent_id,
        "action": action,
        "file": file
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

# Example usage:
if __name__ == "__main__":
    agent_id = os.getenv("AGENT_ID", "EpochWizard")
    agent_role = os.getenv("AGENT_ROLE", "automation, review, orchestration")
    last_action = "initialized self-registration"
    register_agent(agent_id, agent_role, "active", last_action)
    log_action(agent_id, "register", REGISTRY_PATH)