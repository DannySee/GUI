import sys
from PyQt6.QtWidgets import QApplication
from app_view.view import View
from app_presenter.presenter import Presenter
from app_model.model import Model


if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = Model()
    view = View()
    presenter = Presenter(model, view)
    
    presenter.run()

    sys.exit(app.exec())
