import pygame

from contents.launcher_screen import LauncherScreen

pygame.init()


def main():
    launcher = LauncherScreen()
    launcher.run()
    pygame.quit()

main()
