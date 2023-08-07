import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "DatabaseGUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.currentTextChanged.connect(self.cityChanged)
        self.ui.searchLocationBut.pressed.connect(self.searchButtonPressed)
        self.ui.searchLocationBut.pressed.connect(self.setZipcodeStats)
        self.ui.zipList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.filterCatBut.pressed.connect(self.filterButtonPressed)
        self.ui.refreshButton.pressed.connect(self.setPopular)
        self.ui.refreshButton.pressed.connect(self.setSuccessful)


    def executeQuery(self,sql_str):
        try:
            conn = psycopg2.connect("dbname='yelp_challenge' user='postgres' host='localhost' password='**'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print('Query failed!')
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex()>=0):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print('Query failed!')

    def cityChanged(self):
        self.ui.zipList.clear()
        state = self.ui.stateList.currentText()
        city = self.ui.cityList.currentText()
        if (self.ui.stateList.currentIndex() >= 0) and (self.ui.cityList.currentIndex() >= 0):
            sql_str = "SELECT distinct postal_code FROM business WHERE state ='" + state + "' AND city = '" + city + "'ORDER BY postal_code;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print('Query failed!')

    def zipcodeChanged(self):
        self.ui.categoryList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (self.ui.cityList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.currentText()
            zipcode = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT distinct type FROM category WHERE business_id IN (SELECT business_id FROM business WHERE state ='" + state + "' AND city = '" + city + "' AND postal_code = '" + zipcode + "'ORDER BY city);"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print('Query failed!')

    def searchButtonPressed(self):
        self.ui.businessList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (self.ui.cityList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.currentText()
            zipcode = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business WHERE state ='" + state + "' AND city = '" + city + "' AND postal_code = '" + zipcode + "'ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessList.horizontalHeader().setStyleSheet(style)
                self.ui.businessList.setColumnCount(len(results[0]))
                self.ui.businessList.setRowCount(len(results))
                self.ui.businessList.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating','# Checkins'])
                self.ui.businessList.resizeColumnsToContents()
                self.ui.businessList.setColumnWidth(0, 250)
                self.ui.businessList.setColumnWidth(1, 200)
                self.ui.businessList.setColumnWidth(2, 100)
                self.ui.businessList.setColumnWidth(3, 50)
                self.ui.businessList.setColumnWidth(4, 50)
                self.ui.businessList.setColumnWidth(5, 50)
                self.ui.businessList.setColumnWidth(5, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessList.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Query failed!')

    def filterButtonPressed(self):
        self.ui.businessList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (self.ui.cityList.currentIndex() >= 0) and (
                len(self.ui.zipList.selectedItems()) > 0) and (len(self.ui.categoryList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.currentText()
            zipcode = self.ui.zipList.selectedItems()[0].text()
            category = self.ui.categoryList.selectedItems()[0].text()
            sql_str = "SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business, category WHERE business.business_id = category.business_id AND state ='" + state + "' AND city = '" + city + "' AND postal_code = '" + zipcode + "' AND type = '" + category + "'ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessList.horizontalHeader().setStyleSheet(style)
                self.ui.businessList.setColumnCount(len(results[0]))
                self.ui.businessList.setRowCount(len(results))
                self.ui.businessList.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating','# Checkins'])
                self.ui.businessList.resizeColumnsToContents()
                self.ui.businessList.setColumnWidth(0, 250)
                self.ui.businessList.setColumnWidth(1, 200)
                self.ui.businessList.setColumnWidth(2, 100)
                self.ui.businessList.setColumnWidth(3, 50)
                self.ui.businessList.setColumnWidth(4, 50)
                self.ui.businessList.setColumnWidth(5, 50)
                self.ui.businessList.setColumnWidth(5, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessList.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Query failed!')

    def setZipcodeStats(self):
        self.ui.numberBusinesses.clear()
        self.ui.totalPopulation.clear()
        self.ui.avIncome.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (self.ui.cityList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0):
            zipcode = self.ui.zipList.selectedItems()[0].text()
            sql_str_count = "select count(postal_code) from business where postal_code = '" + zipcode + "'"
            sql_str_population = "select population from zipcodedata where zipcode = '" + zipcode + "'"
            sql_str_income = "select medianincome from zipcodedata where zipcode = '" + zipcode + "'"
            resultsCount = self.executeQuery(sql_str_count)
            resultsPopulation = self.executeQuery(sql_str_population)
            resultsIncome = self.executeQuery(sql_str_income)
            valueC = resultsCount[0][0]
            valueP = resultsPopulation[0][0]
            valueI = resultsIncome[0][0]
            self.ui.numberBusinesses.addItem(str(valueC))
            self.ui.totalPopulation.addItem(str(valueP))
            self.ui.avIncome.addItem(str(valueI))

    def setSuccessful(self):
        self.ui.successfulList.clear()
        zipcode = self.ui.zipList.selectedItems()[0].text()
        sql_str = "SELECT name, stars, reviewrating, review_count FROM business WHERE postal_code = '" + zipcode + "' AND reviewrating >  (SELECT SUM(reviewrating)/COUNT(reviewrating) FROM business WHERE   postal_code = '" + zipcode + "') LIMIT 10"
        print(sql_str)
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.successfulList.horizontalHeader().setStyleSheet(style)
            self.ui.successfulList.setColumnCount(len(results[0]))
            self.ui.successfulList.setRowCount(len(results))
            self.ui.successfulList.setHorizontalHeaderLabels(
                ['Business Name', 'Stars', 'Review Rating', 'Review Count'])
            self.ui.successfulList.resizeColumnsToContents()
            self.ui.successfulList.setColumnWidth(0, 200)
            self.ui.successfulList.setColumnWidth(1, 40)
            self.ui.successfulList.setColumnWidth(2, 70)
            self.ui.successfulList.setColumnWidth(3, 30)
            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.successfulList.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            print('Query failed!')

    def setPopular(self):
        self.ui.popularList.clear()
        zipcode = self.ui.zipList.selectedItems()[0].text()
        sql_str = "SELECT name, stars, reviewrating, review_count FROM business WHERE postal_code = '" + zipcode + "' AND numcheckins IS NOT NULL ORDER BY numcheckins DESC LIMIT 10"
        print(sql_str)
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.popularList.horizontalHeader().setStyleSheet(style)
            self.ui.popularList.setColumnCount(len(results[0]))
            self.ui.popularList.setRowCount(len(results))
            self.ui.popularList.setHorizontalHeaderLabels(
                ['Business Name', 'Stars', 'Review Rating', 'Review Count'])
            self.ui.popularList.resizeColumnsToContents()
            self.ui.popularList.setColumnWidth(0, 200)
            self.ui.popularList.setColumnWidth(1, 40)
            self.ui.popularList.setColumnWidth(2, 70)
            self.ui.popularList.setColumnWidth(3, 30)
            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.popularList.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            print('Query failed!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())
