import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QPalette, QColor, QBrush, QLinearGradient
from PyQt6.QtCore import Qt
import game
import pygame

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Game")
        self.setFixedSize(1280, 800)
        self.setStyleSheet("background-color: #1a1a1a;")  # Dark background
        # Create a central widget and set a layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Add a game title
        title_font = QFont("Arial", 48, QFont.Weight.Bold)
        title_label = QLabel("Slicing Samurai")
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #ffffff;")  # White text color
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout = QVBoxLayout()
        title_layout.addStretch(1)  # Add vertical spacer
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)  # Add vertical spacer
        main_layout.addLayout(title_layout)

        # Add menu buttons
        button_font = QFont("Arial", 16, QFont.Weight.Bold)
        button_style = """
            QPushButton {
                background-color: #303030;
                color: #ffffff;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
        """
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        left_button_layout = QVBoxLayout()
        right_button_layout = QVBoxLayout()
        button_layout.addLayout(left_button_layout)
        button_layout.addLayout(right_button_layout)

        play_button = QPushButton("Play")
        play_button.setFont(button_font)
        play_button.setStyleSheet(button_style)
        play_button.clicked.connect(self.start_game)
        left_button_layout.addWidget(play_button)

        how_to_play_button = QPushButton("How to Play")
        how_to_play_button.setFont(button_font)
        how_to_play_button.setStyleSheet(button_style)
        how_to_play_button.clicked.connect(self.show_how_to_play)
        left_button_layout.addWidget(how_to_play_button)

        options_button = QPushButton("Options")
        options_button.setFont(button_font)
        options_button.setStyleSheet(button_style)
        options_button.clicked.connect(self.show_options)
        right_button_layout.addWidget(options_button)

        quit_button = QPushButton("Quit")
        quit_button.setFont(button_font)
        quit_button.setStyleSheet(button_style)
        quit_button.clicked.connect(self.quit_game)
        right_button_layout.addWidget(quit_button)

        # Add a background gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#1a1a1a"))
        gradient.setColorAt(1, QColor("#333333"))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

    def start_game(self): #Currently only button that works
        self.hide()  # Hide the main menu
        game.SCREEN = pygame.display.set_mode((1280, 800), flags=pygame.SHOWN)
        game_over = game.game()


    def show_how_to_play(self):
        # Code to show the "How to Play" instructions
        how_to_play_window = QMainWindow()
        how_to_play_window.setWindowTitle("How to Play")
        how_to_play_window.setFixedSize(800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        instructions_label = QLabel("Instructions:")
        instructions_label.setWordWrap(True)
        layout.addWidget(instructions_label)

        back_button = QPushButton("Back")
        back_button.clicked.connect(how_to_play_window.close)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignRight)

        how_to_play_window.setCentralWidget(central_widget)
        how_to_play_window.show()

    def show_options(self):
        options_window = QMainWindow()
        options_window.setWindowTitle("Options")
        options_window.setFixedSize(400, 300)

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        options_label = QLabel("Options go here...")
        layout.addWidget(options_label)

        back_button = QPushButton("Back")
        back_button.clicked.connect(options_window.close)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignRight)

        options_window.setCentralWidget(central_widget)
        options_window.show()

    def show_game_over_menu(self):
        game_over_window = QMainWindow()
        game_over_window.setWindowTitle("Game Over")
        game_over_window.setFixedSize(400, 200)

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        game_over_label = QLabel("Game Over")
        game_over_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(game_over_label, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        restart_button = QPushButton("Restart")
        restart_button.clicked.connect(self.start_game)
        button_layout.addWidget(restart_button)

        main_menu_button = QPushButton("Main Menu")
        main_menu_button.clicked.connect(lambda: self.show_main_menu(game_over_window))
        button_layout.addWidget(main_menu_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.quit_game)
        button_layout.addWidget(quit_button)

        game_over_window.setCentralWidget(central_widget)
        game_over_window.show()

    def show_main_menu(self, window_to_close):
        window_to_close.close()
        self.show()

    def quit_game(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec())