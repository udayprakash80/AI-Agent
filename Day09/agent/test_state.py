from state import create_state, add_action, record_observation, next_step, can_continue, finish

state = create_state("What is the time and generate a password?")
print("initial state")
print(state)

add_action(state, "generate_password")
record_observation(state, "generate_password", "klsj#kldf")
next_step(state)
print("state after first step")
print(state)
add_action(state, "get_time")
record_observation(state, "get_time", "12:30")
next_step(state)
finish(state, "12:30")
print(state)
print("final state")