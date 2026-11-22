
from psychopy import visual, core, event
import random
import csv
from datetime import datetime

# -----------------------------
# SETUP
# -----------------------------

win = visual.Window(
    size=(1000, 700),
    color="black",
    units="height",
    fullscr=False
)

shapes = ["circle", "square", "triangle"]

def make_shape(shape_name, position):
    if shape_name == "circle":
        return visual.Circle(
            win, radius=0.15, pos=position,
            fillColor="white", lineColor="white"
        )

    elif shape_name == "square":
        return visual.Rect(
            win, width=0.3, height=0.3,
            pos=position, fillColor="white",
            lineColor="white"
        )

    elif shape_name == "triangle":
        return visual.ShapeStim(
            win,
            vertices=[(0, 0.18), (-0.17, -0.15), (0.17, -0.15)],
            pos=position,
            fillColor="white",
            lineColor="white"
        )


def show_text(message):
    text = visual.TextStim(
        win, text=message, color="white",
        height=0.035, wrapWidth=1.3
    )
    text.draw()
    win.flip()


# -----------------------------
# INSTRUCTIONS
# -----------------------------

instructions = (
    "MEMORY EXPERIMENT\n\n"
    "You will see one or two shapes on the screen.\n"
    "Try to remember the shape or shapes.\n\n"
    "After a short delay, another shape will appear.\n"
    "Decide whether you saw that shape earlier.\n\n"
    "Press UP if you saw it before.\n"
    "Press DOWN if you did not see it before.\n\n"
    "Respond as accurately and quickly as possible.\n\n"
    "Press SPACE to begin."
)

show_text(instructions)
event.waitKeys(keyList=["space"])


# -----------------------------
# CREATE TRIALS
# -----------------------------

trials = []

for condition, memory_load in [("Low", 1), ("High", 2)]:

    for trial_type in ["Old"] * 5 + ["New"] * 5:

        remembered = random.sample(shapes, memory_load)

        if trial_type == "Old":
            probe = random.choice(remembered)
        else:
            remaining = [
                shape for shape in shapes
                if shape not in remembered
            ]
            probe = random.choice(remaining)

        trials.append({
            "condition": condition,
            "memory_load": memory_load,
            "remembered": remembered,
            "probe": probe,
            "trial_type": trial_type
        })

random.shuffle(trials)


# -----------------------------
# RUN EXPERIMENT
# -----------------------------

results = []

for trial_number, trial in enumerate(trials, start=1):

    # Show memory shapes
    positions = (
        [(0, 0)] if trial["memory_load"] == 1
        else [(-0.25, 0), (0.25, 0)]
    )

    for shape_name, position in zip(
        trial["remembered"], positions
    ):
        shape = make_shape(shape_name, position)
        shape.draw()

    win.flip()
    core.wait(2)

    # Blank delay
    win.flip()
    core.wait(1)

    # Show recognition probe
    probe_shape = make_shape(trial["probe"], (0, 0))
    probe_shape.draw()

    prompt = visual.TextStim(
        win,
        text="Was this shape shown earlier?\n\nUP = YES     DOWN = NO",
        color="white",
        pos=(0, -0.35),
        height=0.035
    )
    prompt.draw()
    win.flip()

    # Record response time
    reaction_clock = core.Clock()

    response = event.waitKeys(
        keyList=["up", "down", "escape"],
        timeStamped=reaction_clock
    )

    key, reaction_time = response[0]

    if key == "escape":
        break

    if trial["trial_type"] == "Old":
        correct_response = "up"
    else:
        correct_response = "down"

    accuracy = int(key == correct_response)

    results.append({
        "trial": trial_number,
        "condition": trial["condition"],
        "memory_load": trial["memory_load"],
        "remembered_shapes": ", ".join(trial["remembered"]),
        "probe_shape": trial["probe"],
        "trial_type": trial["trial_type"],
        "response": key,
        "accuracy": accuracy,
        "reaction_time": reaction_time
    })

    # Short interval between trials
    win.flip()
    core.wait(0.5)


# -----------------------------
# SAVE DATA
# -----------------------------

filename = "memory_data_" + datetime.now().strftime(
    "%Y%m%d_%H%M%S"
) + ".csv"

if results:
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

show_text(
    "Experiment complete!\n\n"
    "Thank you for participating.\n\n"
    "Press SPACE to close."
)

event.waitKeys(keyList=["space"])
win.close()
core.quit()
