from task_planner import decompose_task
from state import create_state, add_task, complete_task, add_action, record_observation, add_result, get_pending_tasks, all_tasks_completed, next_step, can_continue, finish

async def run_agent_loop(user_request, planner, execute_action, format_answer, tools, client):
    state = create_state(user_request)
    planned_tasks = decompose_task(state)
    for task in planned_tasks:
        add_task(state, task)
    print("Tasks plan:")
    print("----------------------------------")
    for item in state["tasks"]:
        print("-", item["task"])

    while can_continue(state):
        print("Step " f"{state['current_step'] + 1}---")
        decision = planner(state, tools)
        print("Planner Decision:", decision)
        if decision.strip().upper() == "FINISH":
            answer = format_answer(state)
            finish(state, answer)
            break
        task, tool = parse_decision(decision)
        if not task or not tool:
            add_result(state, "Invalid planner decision")
            next_step(state)
            continue
        state["current_task"] = task
        observation = await execute_action(tool, state, client)
        print("observation:", observation)
        add_action(state, tool)
        record_observation(state, tool, observation)
        add_result(state, observation)

        if not observation.lower().startswith("error"):
            complete_task(state, task)
        else:
            add_result(state, "The previous action failed. The planner must reconsider")
        next_step(state)
    return state




def parse_decision(decision):
    task = None
    tool = None
    for line in decision.splitlines():
        line = line.strip()
        if line.startswith("TASK:"):
            task = line[len("TASK:"):].strip()
        elif line.startswith("TOOL:"):
            tool = line[len("TOOL:"):].strip()
    if task and "TOOL:" in task:
        parts = task.split("TOOL:", 1)
        task = parts[0].strip()
        if not tool:
            tool = parts[1].strip()
    return task, tool