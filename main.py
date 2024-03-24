import sys
from PySide6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QListWidget, QGridLayout, QFrame, QDialog, QDialogButtonBox, QListWidgetItem, QLineEdit, QFormLayout, QSizePolicy
from PySide6.QtCore import Qt, QObject, Signal, QRect, Qt, QUrl
from PySide6.QtGui import QShortcut, QKeySequence, QDesktopServices
import threading
from utils import utils
from data import dbcreate

# Window containing the settings of the application
class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 691, 431)
        self.setStyleSheet("background-color: #333; color: white;")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Initialize db object
        self.db = dbcreate.Database("interview_manager.db")

        self.setup_ui()

    def setup_ui(self):
        mainLayout = QGridLayout(self.centralwidget)

        # OpenAI Key and Input Device ID Form
        self.keyForm = QFormLayout()
        self.openAIKeyLineEdit = QLineEdit()
        self.inputDeviceIDLineEdit = QLineEdit()
        self.openAIKeyLabel = QLabel("OpenAI Key:")
        self.inputDeviceIDLabel = QLabel("Input Device ID")
        self.keyForm.addRow(self.openAIKeyLabel, self.openAIKeyLineEdit)
        self.keyForm.addRow(self.inputDeviceIDLabel, self.inputDeviceIDLineEdit)

        # Submit buttons layout
        self.SubmitButtonGridLayout = QGridLayout()
        self.openAIButton = QPushButton("Submit")
        self.inputDeviceButton = QPushButton("Submit")
        self.SubmitButtonGridLayout.addWidget(self.openAIButton, 0, 0)
        self.SubmitButtonGridLayout.addWidget(self.inputDeviceButton, 1, 0)
        self.inputDeviceButton.clicked.connect(self.submit_input_device_id)
        self.openAIButton.clicked.connect(self.submit_openai_key)

        # Top center layout for key form and submit buttons
        topCenterLayout = QHBoxLayout()
        topCenterLayout.addStretch()  # Add stretch to center the following widgets
        topCenterLayout.addLayout(self.keyForm)
        topCenterLayout.addLayout(self.SubmitButtonGridLayout)
        topCenterLayout.addStretch()  # Add stretch to maintain center alignment

        # Add the top center layout to the main layout
        mainLayout.addLayout(topCenterLayout, 0, 0, 1, 2)

        # Device search output
        self.deviceSearchOutputVerticalLayout = QVBoxLayout()
        self.deviceSearchLabel = QLabel("Looking for Input Device ID for VB-Audio?\nClick the button below to list them")
        self.deviceSearchOutputTextEdit = QTextEdit()
        self.deviceSearchOutputButton = QPushButton("View input_device ID's")
        self.deviceSearchOutputVerticalLayout.addWidget(self.deviceSearchLabel)
        self.deviceSearchOutputVerticalLayout.addWidget(self.deviceSearchOutputTextEdit)
        self.deviceSearchOutputVerticalLayout.addWidget(self.deviceSearchOutputButton)
        self.deviceSearchOutputButton.clicked.connect(self.get_devices)
        mainLayout.addLayout(self.deviceSearchOutputVerticalLayout, 1, 1)

        # Database layout
        self.databaseVerticalLayout = QVBoxLayout()
        self.databaseLabel = QLabel("View the database tables below")
        self.databaseTable = QTableWidget()
        self.databaseTable.horizontalHeader().setStyleSheet("background-color: #333; color: white;")
        self.databaseTable.verticalHeader().setStyleSheet("background-color: #333; color: white;")
        self.databaseButtonHorizontalLayout = QHBoxLayout()
        self.databaseInterviewButton = QPushButton("interviews")
        self.databaseQuestionsButton = QPushButton("questions")
        self.databaseSettingsButton = QPushButton("settings")
        self.databaseVoiceRespButton = QPushButton("voice_resp")
        self.databaseInterviewButton.clicked.connect(self.load_interview_data)
        self.databaseQuestionsButton.clicked.connect(self.load_questions_data)
        self.databaseSettingsButton.clicked.connect(self.load_settings_data)
        self.databaseVoiceRespButton.clicked.connect(self.load_voice_resp_data)
        self.databaseButtonHorizontalLayout.addWidget(self.databaseInterviewButton)
        self.databaseButtonHorizontalLayout.addWidget(self.databaseQuestionsButton)
        self.databaseButtonHorizontalLayout.addWidget(self.databaseSettingsButton)
        self.databaseButtonHorizontalLayout.addWidget(self.databaseVoiceRespButton)
        self.databaseVerticalLayout.addWidget(self.databaseLabel)
        self.databaseVerticalLayout.addWidget(self.databaseTable)
        self.databaseVerticalLayout.addLayout(self.databaseButtonHorizontalLayout)
        mainLayout.addLayout(self.databaseVerticalLayout, 1, 0, 2, 1)

        # Guides layout
        self.guidesVerticalLayout = QVBoxLayout()
        self.guidesLabel = QLabel("Guides")
        self.guidesVBButton = QPushButton("VB-Audio setup guide\n(needed to mask output audio to input)")
        self.guidesOpenAIButton = QPushButton("Getting your OpenAI key")
        self.guidesProjectButton = QPushButton("Project overview with code")

        self.guidesProjectButton.clicked.connect(self.overview_link)
        self.guidesOpenAIButton.clicked.connect(self.ai_link)
        self.guidesVBButton.clicked.connect(self.vb_link)

        buttonWidth = 400
        buttonHeight = 40

        self.guidesVBButton.setFixedSize(buttonWidth, buttonHeight)
        self.guidesOpenAIButton.setFixedSize(buttonWidth, buttonHeight)
        self.guidesProjectButton.setFixedSize(buttonWidth, buttonHeight)

        self.guidesVerticalLayout.addWidget(self.guidesLabel)
        self.guidesVerticalLayout.addWidget(self.guidesVBButton)
        self.guidesVerticalLayout.addWidget(self.guidesOpenAIButton)
        self.guidesVerticalLayout.addWidget(self.guidesProjectButton)
        mainLayout.addLayout(self.guidesVerticalLayout, 2, 1)

    def overview_link(self):
        overview_url = "https://www.kianjolley.com/projects/interview_excelerator/"
        QDesktopServices.openUrl(QUrl(overview_url))

    def ai_link(self):
        ai_url = "https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key"
        QDesktopServices.openUrl(QUrl(ai_url))

    def vb_link(self):
        vb_url = "https://www.kianjolley.com/blogs/blogpost/vb_audio_setup_for_interview_excelerator/"
        QDesktopServices.openUrl(QUrl(vb_url))

    def get_devices(self):
        devices = utils.find_devices()
        self.deviceSearchOutputTextEdit.clear()  # Clear existing text
        self.deviceSearchOutputTextEdit.append(devices)  # Add new text

    def submit_openai_key(self):
        key = self.openAIKeyLineEdit.text()
        self.db.insert_setting('openai_key', key)
        print("OpenAI Key updated")  # For confirmation

    def submit_input_device_id(self):
        device_id = self.inputDeviceIDLineEdit.text()
        self.db.insert_setting('input_device_id', device_id)
        print("Input Device ID updated")  # For confirmation

    def load_interview_data(self):
        # Fetch interview data from the database and populate the table
        data = self.db.get_interview_data()  # Assume this method exists and returns data suitable for the table
        self.populate_table(data)

    def load_questions_data(self):
        data = self.db.get_questions_data()  # Assume this method exists and returns data suitable for the table
        self.populate_table(data)

    def load_settings_data(self):
        data = self.db.get_settings_data()  # Assume this method exists and returns data suitable for the table
        self.populate_table(data)

    def load_voice_resp_data(self):
        data = self.db.get_voice_resp_data()  # Assume this method exists and returns data suitable for the table
        self.populate_table(data)

    def populate_table(self, data):
        self.databaseTable.setRowCount(len(data))
        self.databaseTable.setColumnCount(len(data[0]) if data else 0)

        for row, rowData in enumerate(data):
            for column, cellData in enumerate(rowData):
                self.databaseTable.setItem(row, column, QTableWidgetItem(str(cellData)))

# Pop up for adding a new interview to the list
class AddInterviewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Interview")
        self.setGeometry(200, 200, 400, 200)

        self.setup_widgets()

    def setup_widgets(self):
        layout = QVBoxLayout()

        label = QLabel("Enter Interview Details:")
        layout.addWidget(label)

        self.interviewTextEdit = QTextEdit()
        layout.addWidget(self.interviewTextEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

# Pop up to add/edit/delete questions and answers
class AddQuestionAndAnswerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Question and Answer")

        self.layout = QVBoxLayout()

        self.questionTextEdit = QTextEdit()
        self.layout.addWidget(QLabel("Question:"))
        self.layout.addWidget(self.questionTextEdit)

        self.answerTextEdit = QTextEdit()
        self.layout.addWidget(QLabel("Answer:"))
        self.layout.addWidget(self.answerTextEdit)

        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.accept)
        self.layout.addWidget(self.addButton)

        self.setLayout(self.layout)

# Pip up to view pas responses from voice to text
class ViewPastResponsesDialog(QDialog):
    def __init__(self, interview_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Past Responses")
        self.interview_id = interview_id

        # Initialize db object
        self.db = dbcreate.Database("interview_manager.db")

        self.setup_widgets()
        self.resize(600, 400)

    def setup_widgets(self):
        layout = QVBoxLayout()

        self.responseListWidget = QListWidget()
        self.populate_response_list()
        layout.addWidget(self.responseListWidget)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def populate_response_list(self):
        responses = self.db.get_past_responses_by_interview_id(self.interview_id)
        for question, response in responses:
            item = QListWidgetItem(f"Question: {question}\nResponse:\n {response}\n")
            self.responseListWidget.addItem(item)

# This is the main bot window
class BotManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interview Excelerator")
        self.setGeometry(100, 100, 1161, 641)
        self.setStyleSheet("background-color: #333; color: white;")

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.mainLayout = QGridLayout(self.centralwidget)

        # Initialize db object
        self.db = dbcreate.Database("interview_manager.db")
        self.db.create_tables()

        self.setup_widgets()
        self.setup_interview_list()

        # Adjust the column widths in the main layout
        self.mainLayout.setColumnStretch(0, 0)  # 10% for interview layout
        self.mainLayout.setColumnStretch(1, 1)  # 90% for the rest of the layout

        # Adjust row stretch factors for custom question and voice to text layouts
        self.mainLayout.setRowStretch(0, 2)  # Smaller portion for voice to text layout
        self.mainLayout.setRowStretch(1, 3)  # Larger portion for custom question layout

    def setup_widgets(self):
        # Layout for Interviews
        self.setup_interview_layout()

        # Layout for Custom Questions and Responses
        self.setup_custom_question_layout()

        # Layout for Voice to Text and OpenAI responses
        self.setup_voice_to_text_layout()

        # Layout for Donation Buttons
        self.setup_donation_layout()

    def setup_interview_layout(self):
        self.interviewLayout = QVBoxLayout()

        self.interviewTitleLabel = QLabel("Interviews")
        self.interviewTitleLabel.setStyleSheet("font-size: 15px;")
        self.interviewLayout.addWidget(self.interviewTitleLabel)

        self.interviewList = QListWidget()
        self.interviewList.addItems(["Job {}".format(i) for i in range(1, 11)])
        self.interviewLayout.addWidget(self.interviewList)

        self.addInterviewButton = QPushButton("Add Interview")
        self.addInterviewButton.clicked.connect(self.open_add_interview_dialog)
        self.interviewLayout.addWidget(self.addInterviewButton)

        self.mainLayout.addLayout(self.interviewLayout, 0, 0, 2, 1)

    def setup_custom_question_layout(self):
        self.customQuestionListLayout = QVBoxLayout()

        self.customQuestionTitle = QLabel("Your Pre-Made Questions & Answers")
        self.customQuestionTitle.setStyleSheet("font-size: 15px;")
        self.customQuestionListLayout.addWidget(self.customQuestionTitle)

        self.customQuestionList = QListWidget()
        self.customQuestionListLayout.addWidget(self.customQuestionList)

        # Create a horizontal layout for the buttons
        self.buttonLayout = QHBoxLayout()

        self.addAddResponseButton = QPushButton("Add Responses")
        self.addEditResponseButton = QPushButton("Edit Responses")
        self.addDeleteResponseButton = QPushButton("Delete Responses")
        self.addAddResponseButton.clicked.connect(self.add_response)
        self.addEditResponseButton.clicked.connect(self.edit_response)
        self.addDeleteResponseButton.clicked.connect(self.delete_response)
        
        self.buttonLayout.addWidget(self.addAddResponseButton)
        self.buttonLayout.addWidget(self.addEditResponseButton)
        self.buttonLayout.addWidget(self.addDeleteResponseButton)

        self.addAddResponseButton.setEnabled(False)
        self.addEditResponseButton.setEnabled(False)
        self.addDeleteResponseButton.setEnabled(False)

        # Add the button layout to the customQuestionListLayout
        self.customQuestionListLayout.addLayout(self.buttonLayout)

        # Assuming mainLayout is a grid layout that's already defined
        self.mainLayout.addLayout(self.customQuestionListLayout, 1, 1, 2, 1)

    def setup_voice_to_text_layout(self):
        self.gridLayout = QGridLayout()

        self.voiceToTextTitle = QLabel("Voice to Text Feed")
        self.voiceToTextTitle.setStyleSheet("font-size: 15px;")
        self.gridLayout.addWidget(self.voiceToTextTitle, 2, 1)

        self.aiResponseTitle = QLabel("OpenAI Output")
        self.aiResponseTitle.setStyleSheet("font-size: 15px;")
        self.gridLayout.addWidget(self.aiResponseTitle, 2, 2)

        self.voiceToTextTextEdit = QTextEdit()
        self.voiceToTextTextEdit.setStyleSheet("color: #41e8d7")
        self.gridLayout.addWidget(self.voiceToTextTextEdit, 3, 1)

        self.aiResponseTextEdit = QTextEdit()
        self.aiResponseTextEdit.setStyleSheet("color: #41e8d7")
        self.gridLayout.addWidget(self.aiResponseTextEdit, 3, 2)

        # Create a horizontal layout for the buttons
        self.buttonLayout = QHBoxLayout()

        # Add Start Listening button
        self.startListeningButton = QPushButton("Start Listening (or ctrl+up)")
        self.startListeningButton.setEnabled(False)
        self.startListeningButton.clicked.connect(self.start_listening)
        self.buttonLayout.addWidget(self.startListeningButton)

        # Add Stop Listening button
        self.stopListeningButton = QPushButton("Stop Listening (or ctrl+down)")
        self.stopListeningButton.clicked.connect(self.stop_listening)
        self.stopListeningButton.setEnabled(False)
        self.buttonLayout.addWidget(self.stopListeningButton)

        # Add the button layout to the grid layout
        self.gridLayout.addLayout(self.buttonLayout, 4, 1)

        # Create a shortcut to start/stop listening with a keyboard key
        self.listenShortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Up), self)
        self.listenShortcut.activated.connect(self.start_listening)
        self.listenShortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Down), self)
        self.listenShortcut.activated.connect(self.stop_listening)

        self.pastResponseButton = QPushButton("View All Past Responses")
        self.gridLayout.addWidget(self.pastResponseButton, 4, 2)
        self.pastResponseButton.setEnabled(False)
        self.pastResponseButton.clicked.connect(self.view_past_responses)

        self.mainLayout.addLayout(self.gridLayout, 0, 1)

    def setup_donation_layout(self):
        self.donationGridLayout = QGridLayout()

        self.settingsButton = QPushButton("Settings")
        self.donationGridLayout.addWidget(self.settingsButton, 0, 0)
        self.settingsButton.clicked.connect(self.open_settings_window)

        # https://www.paypal.com/donate/?business=5VUMMAU4TRZP6&no_recurring=1&currency_code=USD
        self.paypalButton = QPushButton("Paypal Donation")
        self.donationGridLayout.addWidget(self.paypalButton, 1, 0)
        self.paypalButton.clicked.connect(self.open_paypal_link)

        # 0x40c7F2eBFCFd91E6414cCD18382179E309116284
        self.ethButton = QPushButton("Eth Donation")
        self.donationGridLayout.addWidget(self.ethButton, 2, 0)
        self.ethButton.clicked.connect(self.show_eth_address)

        self.mainLayout.addLayout(self.donationGridLayout, 2, 0)

    def open_paypal_link(self):
        paypal_url = "https://www.paypal.com/donate/?business=5VUMMAU4TRZP6&no_recurring=1&currency_code=USD"
        QDesktopServices.openUrl(QUrl(paypal_url))

    def show_eth_address(self):
        eth_address = "0x40c7F2eBFCFd91E6414cCD18382179E309116284"
        QMessageBox.information(self, "ETH Donation", f"Please send your donations to the following ETH address:\n{eth_address}")

    def open_add_interview_dialog(self):
        dialog = AddInterviewDialog(self)
        # Calculate the center position of the main window
        x = self.x() + (self.width() - dialog.width()) / 2
        y = self.y() + (self.height() - dialog.height()) / 2
        dialog.move(x, y)
        
        if dialog.exec():
            interview_details = dialog.interviewTextEdit.toPlainText()
            self.db.insert_interview(interview_details)
        self.setup_interview_list()

    def setup_interview_list(self):
        interviews = self.db.get_interviews()
        # Clear existing items in the list
        self.interviewList.clear()
        # Add new items
        for interview in interviews:
            item = QListWidgetItem(interview)
            self.interviewList.addItem(item)
        # Connect itemClicked signal to handle_interview_selected method
        self.interviewList.itemClicked.connect(self.handle_interview_selected)

    def handle_interview_selected(self, item):
        # Disable buttons
        self.startListeningButton.setEnabled(True)
        self.pastResponseButton.setEnabled(True)
        self.addEditResponseButton.setEnabled(True)
        self.addAddResponseButton.setEnabled(True)
        self.addDeleteResponseButton.setEnabled(True)
        
        # Get interview details
        selected_interview = item.text()
        interview_id = self.db.get_interview_id(selected_interview)

        # Update customQuestionList
        self.update_custom_question_list(interview_id)

    def update_custom_question_list(self, interview_id):
        question_answers = self.db.get_questions_by_interview_id(interview_id)
        self.customQuestionList.clear()
        for question_text, answer_text in question_answers:
            item = f"Question: {question_text}\nAnswer: {answer_text}\n"
            self.customQuestionList.addItem(item)

    def get_selected_interview_id(self):
        selected_item = self.interviewList.currentItem()
        if selected_item is not None:
            interview_name = selected_item.text()
            return self.db.get_interview_id(interview_name)
        else:
            return None

    def add_response(self):
        dialog = AddQuestionAndAnswerDialog(self)
        if dialog.exec():
            question_text = dialog.questionTextEdit.toPlainText()
            answer_text = dialog.answerTextEdit.toPlainText()
            interview_id = self.get_selected_interview_id()  # Assuming you have a method to get the selected interview ID
            if interview_id is not None:
                self.db.add_question_and_answer(interview_id, question_text, answer_text)
                self.update_custom_question_list(interview_id)  # Update the custom question list

    def edit_response(self):
        selected_item = self.customQuestionList.currentItem()
        if selected_item:
            dialog = AddQuestionAndAnswerDialog(self)
            # Assuming you have a way to parse question and answer from the selected_item text
            question_text, answer_text = self.parse_question_answer(selected_item.text())
            dialog.questionTextEdit.setPlainText(question_text)
            dialog.answerTextEdit.setPlainText(answer_text)

            if dialog.exec():
                updated_question_text = dialog.questionTextEdit.toPlainText()
                updated_answer_text = dialog.answerTextEdit.toPlainText()
                interview_id = self.get_selected_interview_id()
                if interview_id is not None:
                    self.db.update_question_and_answer(interview_id, question_text, updated_question_text, updated_answer_text)
                    self.update_custom_question_list(interview_id)

    def delete_response(self):
        selected_item = self.customQuestionList.currentItem()
        if selected_item:
            question_text, _ = self.parse_question_answer(selected_item.text())
            interview_id = self.get_selected_interview_id()
            if interview_id is not None:
                self.db.delete_question_and_answer(interview_id, question_text)
                self.update_custom_question_list(interview_id)

    def parse_question_answer(self, item_text):
        # Trim leading and trailing whitespace and newlines
        item_text = item_text.strip()

        # Find the index of the line that starts with "Answer:" since "Question:" should always be the first line
        answer_index = item_text.find("\nAnswer:")
        if answer_index != -1:
            question_text = item_text[:answer_index].replace("Question: ", "").strip()
            answer_text = item_text[answer_index:].replace("\nAnswer: ", "").strip()
        else:
            question_text = item_text.replace("Question: ", "").strip()
            answer_text = ""

        return question_text, answer_text

    def open_settings_window(self):
        self.settings_window = SettingsWindow()
        # Calculate the center position of the main window
        x = self.x() + (self.width() - self.settings_window.width()) / 2
        y = self.y() + (self.height() - self.settings_window.height()) / 2
        self.settings_window.move(x, y)
        self.settings_window.show()

    def start_listening(self):
        # Disable start button and enable stop button
        self.startListeningButton.setEnabled(False)
        self.stopListeningButton.setEnabled(True)

        # Create voice listener object and connect signal
        self.listener = utils.VoiceListener()
        self.listener.textChanged.connect(self.update_text)

        # Start voice listener thread
        self.voice_listener_thread = threading.Thread(target=self.listener.voice_to_text)
        self.voice_listener_thread.start()

    def stop_listening(self):
        # Disable stop button (to prevent multiple clicks)
        self.stopListeningButton.setEnabled(False)

        # Call the stop_listening method of the listener object
        if self.listener:
            self.listener.stop_listening()

    def update_text(self, text):  
        if text != "NA":
            self.listener = utils.VoiceListener()
            self.voiceToTextTextEdit.setPlainText(text)
            # Get GPT response
            gpt_response = self.listener.get_ai_response(text)
            # Display GPT response
            self.aiResponseTextEdit.setPlainText(gpt_response)
            # Get the interview ID
            interview_id = self.get_selected_interview_id()
            # Check if there's a selected interview
            if interview_id is not None:
                # Insert voice response into the database
                self.db.insert_voice_response(interview_id, text, gpt_response)
        self.startListeningButton.setEnabled(True)

    def view_past_responses(self):
        interview_id = self.get_selected_interview_id()
        if interview_id is not None:
            dialog = ViewPastResponsesDialog(interview_id, self)
            dialog.exec()

def main():
    # Creating tables if they don't exist
    db = dbcreate.Database("interview_manager.db")
    db.create_tables()
    db.close()

    app = QApplication(sys.argv)
    window = BotManagerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()