# Rex - AI Assistant  
### (IN PROGRESS)
## Overview  
Rex is an intelligent AI assistant designed to work seamlessly both online and offline. It can automate tasks, interact with applications, execute commands, and learn from user interactions to improve over time.  

## Features  
- **Custom Wake Word**: Uses "Rex" as the activation trigger.  
- **Voice Recognition**: Supports offline and online speech processing.  
- **Command Execution**: Performs system and application-level actions.  
- **Fuzzy Matching**: Understands approximate commands using natural language processing.  
- **Modular Architecture**: Each functionality is a separate module for easy expansion.  
- **Learning Mechanism**: Learns from user corrections to improve future interactions.  
- **Animation Integration**: Uses a 3D animated model for a more interactive experience.  

## Project Structure  
```sh
Rex/
│── backend/                # Core AI processing
│   ├── modules/            # Functional modules
│   │   ├── akinator.py
│   │   ├── file_manager.py
│   │   ├── medium.py
│   │   ├── search.py
│   │   ├── slack.py
│   │   ├── spotify.py
│   │   ├── system_commands.py
│   ├── nlp/                # Natural Language Processing (NLP)
│   │   ├── command_parser.py
│   │   ├── fuzzy_match.py
│   │   ├── voice_recognition.py
│   ├── agent.py            # Main AI assistant script
│   ├── config.py           # Configuration settings
│   ├── main.py             # Entry point for execution
│   ├── requirements.txt    # Dependencies
│── frontend/               # 3D UI and animation
│   ├── assets/             # UI assets and models
│   ├── scripts/            # Godot scripts for animation
│   │   ├── animation.gd
│   │   ├── assistant_overlay.gd
│   │   ├── user_interaction.gd
│   │   ├── main_scene.tscn
│   │   ├── main_script.gd
│── integration/            # OS-specific automation
│   ├── linux/
│   │   ├── bash_commands.sh
│   ├── macos/
│   │   ├── applescript_commands.scpt
│   ├── windows/
│   │   ├── autohotkey_commands.ahk
│── docs/                   # Documentation
│── README.md               # Project documentation             # Project documentation
```
## Installation  
### Prerequisites  
- Python 3.x  
- Required dependencies (install using `pip install -r requirements.txt`)  
- Godot Engine (for animation overlay)  

### Setup  
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-repo/rex-ai.git
   cd rex-ai```
   
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the AI assistant:
   ```bash
   python backend/agent.py
   
### Future Enhancements

- ✅ Integrate Learning Mechanism (Store successful command responses)

- ✅ Improve Fuzzy Matching for better accuracy

- ⏳ Add animations using Godot Engine

- ⏳ Extend AI capabilities to control more applications

### Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

### License

This project is open-source under the MIT License.

