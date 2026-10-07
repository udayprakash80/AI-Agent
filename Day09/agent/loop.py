from state import create_state, add_action, record_observation, next_step, can_continue, finish

async def run_agent_loop(user_request, planner, execute_action, format_answer, tools, client):
    state = create_state(user_request)
    while can_continue(state):
        action = planner(state, tools)
        print("planner selected action: ", action)
        if(action == "FINISH"):
            answer = format_answer(state)
            finish(state, answer)
            break
        observation = await execute_action(action, state, client)
        add_action(state, action)
        record_observation(state, action, observation)
        next_step(state)
    return state