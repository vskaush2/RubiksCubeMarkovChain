# Downloading Requirements
* Download PyCharm (free edition) from https://www.jetbrains.com/pycharm/.
* Download the latest version of Python 3 from https://www.python.org/downloads/.
# Importing Project
* Open PyCharm and select `Get from VCS`.
* Enter this project's .git link.
* Specify the download location to be the `PyCharmProjects` folder.
# Installing Project Dependencies
* Open PyCharm Settings and locate the `Project: RubiksCubeGroup` pane.
* Click on `Project Interpreter`.
* Add a new `VirtualEnv` environment with your system Python.
* Restart PyCharm and open its local `Terminal`.
* Type the command `pip3 install -r requirements.txt` to install project dependencies.
# Jupyter Server Instructions
* Open the local `Terminal` on PyCharm.
* Type the command `jupyter notebook` to open up a new Jupyter Server.
* Click on the `RubiksCubeGroupDemo.ipynb` file to open the notebook.
* Run each code cell using the toolbar on top of the window.