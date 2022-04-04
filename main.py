import connection
import speaker
import keyboard
from time import sleep


# run_program is meant to be changed manually in order to choose whether to execute the main function when run or not
run_program = True

is_on = False
intensity = None


def toggle():
    show_output = True
    global is_on

    # Toggle the global variable is_on from True to False or vice versa
    is_on = not is_on
    if show_output:
        print(is_on)


def on_f7():
    global intensity
    toggle()

    # If F7 is pressed to toggle off, pause music
    if not is_on:
        speaker.pause()

    # If F7 is pressed to toggle on
    if is_on:
        # and the intensity has changed (or it's the first time being toggled on)
        if intensity != connection.get_intensity():
            # update the intensity
            intensity = connection.get_intensity()
            # and play music w/new intensity
            speaker.activate(intensity, 1)
        else:
            # If the intensity has not changed, just resume playing the music
            speaker.resume()


def main():
    global intensity
    iterations = 0

    # Instructions
    print('\nPress "F7" to toggle music and press & hold the "alt" and "F7" keys simultaneously to stop program.\n'
          'Additionally, press "shift" and "f7" simultaneously to restore default settings')

    # Defining hotkeys
    keyboard.add_hotkey("f7", lambda: on_f7())
    keyboard.add_hotkey("shift+f7", lambda: connection.restore_default_preferences())

    # Program loop waiting for keys to be pressed
    while True:
        # The "alt+f7" hotkey stops the program
        if keyboard.is_pressed("alt+f7"):
            print(f"\nDone\nLooped {iterations} times")
            break

        # Only while toggled on
        if is_on:
            # If the intensity has changed
            if connection.get_intensity() != intensity:
                # Update intensity variable to the new intensity
                intensity = connection.get_intensity()
                # and play music for the new intensity
                speaker.activate(intensity, 3)

        iterations += 1
        sleep(0.1)


if __name__ == "__main__" and run_program:
    speaker.create_amp()
    main()
