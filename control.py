import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                print(event.axis, event.value)
            elif event.type == pygame.JOYBALLMOTION:
                print(event.dict, event.joy, event.ball, event.rel)
            elif event.type == pygame.JOYBUTTONDOWN:
                print(event.instance_id, event.button, 'pressed')
            elif event.type == pygame.JOYBUTTONUP:
                print(event.dict, event.joy, event.button, 'released')
            elif event.type == pygame.JOYHATMOTION:
                print(event.hat, event.value)

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()