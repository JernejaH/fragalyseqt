# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

import boxes
from os import name, getenv, path
try:
    from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QTableWidget, QTableWidgetItem, QLabel
    from PyQt5.QtCore import QRect
except ImportError:
    from PyQt6.QtWidgets import QWidget, QPushButton, QCheckBox, QTableWidget, QTableWidgetItem, QLabel
    from PyQt6.QtCore import QRect
#Using FileDialog and SpinBox from pyqtgraph to prevent some possible problems for macOS users and to allow more fine variable setting.
from pyqtgraph import PlotWidget, FileDialog, SpinBox
from Bio.SeqIO import read as fsaread
from charset_normalizer import from_bytes
from scipy.signal import find_peaks
ftype = "ABI fragment analysis files (*.fsa)"
global show_channels
show_channels = [1] * 8
homedir = getenv('HOME')
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("FragalyseQt")
        MainWindow.resize(1280, 720)
        global ch_inact_msg, aboutbtn, infoboxtxt, openfragmentfile, exportinternal, csvexport, unsupportedeq, unsupportedeqmsg, dmgdfile, nodatamsg, hidechannel, minph, minpw, minpp, savecsv
        if name == 'posix':
            langvar = getenv('LANG')
        elif name == 'nt':
            from locale import windows_locale
            from ctypes import windll
            langvar = windows_locale[windll.kernel32.GetUserDefaultUILanguage()]
        else:
            langvar = "en"
        if "en" in langvar:
            ch_inact_msg = "Inactive channel"
            aboutbtn = "About"
            infoboxtxt = "FragalyseQt version 0.3, codename \"DiGeorge\".\n\nThis program version supports analysis of up to 8 different fluorescense channels simultaneously, selective channel hiding, non-Latin run names and can correctly handle damaged files, exporting peaks locations, areas, FWHM's and channel names in CSV for any *.FSA files and export in CSV internal analysis data for *.FSA files generated by ABI 3500 and SeqStudio series equipment.\n\nPeaks areas are calculated assuming they are Gaussian peaks.\n\nLicensed under GNU GPL version 3.\n\nIf you wish to contact author for any reason - please write at dorif11@gmail.com"
            openfragmentfile = "Open FSA file"
            exportinternal = "Export Internal Analysis Data"
            csvexport = "Export in CSV"
            unsupportedeq = "Unsupported equipment!"
            unsupportedeqmsg = "Internal analysis data could be exported only from files generated by ABI 3500 and SeqStudio family sequencers!"
            dmgdfile = "Damaged file!"
            nodatamsg = "There are no data in file!"
            hidechannel = "Hide "
            minph = "Select minimal peak height"
            minpw = "Select minimal peak width"
            minpp = "Select minimal peak prominence"
            savecsv = "Save CSV"
        elif "ru" in langvar:
            ch_inact_msg = "Неактивный канал"
            aboutbtn = "О программе"
            infoboxtxt = "FragalyseQt версия 0.3, кодовое имя \"ДиДжорджи\".\n\nЭта версия программы поддерживает одновременный анализ до 8 каналов флуоресценции, избирательное сокрытие каналов, не-латинские имена запусков, может правильно работать с повреждёнными файлами, поддерживает экспорт имён каналов, положений, площадей и FWHM пиков в формат CSV для любого файла *.FSA и экспорт данных внутреннего анализа данных для файлов *.FSA, полученных на инструментах ABI 3500 и SeqStudio.\n\nПлощади пиков рассчитываются исходя из того, что пики являются гауссовыми.\n\nЛицензировано под GNU GPL версии 3.\n\nЕсли по какой-либо причине вы хотите проконтактировать с автором - пишите, пожалуйста, на dorif11@gmail.com"
            openfragmentfile = "Открыть файл FSA"
            exportinternal = "Экспорт Данных Внутреннего Анализа"
            csvexport = "Экспорт в CSV"
            unsupportedeq = "Неподдерживаемое оборудование!"
            unsupportedeqmsg = "Данные внутреннего анализа могут быть экспортированы только из файлов, полученных на ABI 3500 или семействе SeqStudio!"
            dmgdfile = "Повреждённый файл!"
            nodatamsg = "В файле отсутствуют данные!"
            hidechannel = "Скрыть "
            minph = "Выберите минимальную высоту пика"
            minpw = "Выберите минимальную ширину пика"
            minpp = "Выберите минимальное возвышение пика"
            savecsv = "Сохранить CSV"
        elif "ua" in langvar:
            ch_inact_msg = "Неактивний канал"
            aboutbtn = "О програмі"
            infoboxtxt = "FragalyseQt версія 0.3, кодове ім'я \"ДіДжорджі\".\n\n Версія програми підтримує одночасний аналіз до 8 каналів флуоресценции, вибіркове приховування каналів, не-латинські імена запусків, може правильно працювати з пошкодженими файлами, підтримує експорт імен каналів, положень, площадей і FWHM піков у формат CSV для будь-якого файла *.FSA та експорт даних внутрішнього аналізу даних для файлів *.FSA, отриманих на інструментах ABI 3500 и SeqStudio.\n\nПлощаді піков розраховуються виходячи з того, що піки є гауссовими.\n\Ліцензовано під GNU GPL версії 3.\n\nЯкщо з будь-якої причини ви хочете проконтактувати з автором - пишіть, будь ласка, на dorif11@gmail.com"
            openfragmentfile = "Відкрити файл FSA"
            exportinternal = "Експорт Даних Внутренього Аналіза"
            csvexport = "Експорт в CSV"
            unsupportedeq = "Непідтримуване оболаднення!"
            unsupportedeqmsg = "Дані внутренього аналіза можуть бути експортовані тільки із файлів, отриманих на ABI 3500 або сімействі SeqStudio!"
            dmgdfile = "Пошкоджений файл!"
            nodatamsg = "У файлі відсутні дані!"
            hidechannel = "Сховати "
            minph = "Виберіть мінімальну висоту піку"
            minpw = "Виберіть мінімальну ширину піку"
            minpp = "Виберіть мінімальне підвищення піку"
            savecsv = "Зберегти CSV"
        elif "ro" in langvar:
            ch_inact_msg = "Canal inactiv"
            aboutbtn = "Despre program"
            infoboxtxt = "FragalyseQt versiune 0.3, codename \"DiGeorge\".\n\nAceastă versiune permite analiza simultană a pînă la 8 canale de fluorescență, ascunderea selectivă a canalelor, nume non-latine a runurilor, poate funcționa corect cu fișiere deteriorate, permite exportarea numelor de canale, locațiile, suprafețele și FWHMurile a vîrfurilor în formatul CSV, pentru orice fișierul de tip *.FSA și exportarea în formatul CSV a datelor analizei interne pentru fișiere de tip *.FSA generate de echipamentele de model ABI 3500 și SeqStudio.\n\nSuprafețele vîrfurilor, sunt calculate presupunînd că vîrfurile sunt gausiene.\n\nLicențiat sub GNU GPL versiunea 3.\n\nDacă doriți să contactați autorul, pentru orice întrebare - scrieți, vă rog, la adresa dorif11@gmail.com"
            openfragmentfile = "Deschideți fișierul FSA"
            exportinternal = "Exportul Datelor Analizei Interne"
            csvexport = "Exportul în CSV"
            unsupportedeq = "Echipament nesusținut!"
            unsupportedeqmsg = "Datele analizei interne pot fi exportate numai pentru fișierile generate de echipamentele de model ABI 3500 și SeqStudio!"
            dmgdfile = "Fișier deteriorat!"
            nodatamsg = "In fișier lipsesc datele!"
            hidechannel = "Ascunde "
            minph = "Selectaţi înălţimea minimală a vîrfului"
            minpw = "Selectaţi lăţimea minimală a vîrfului"
            minpp = "Selectaţi proeminenţa minimală a vîrfului"
            savecsv = "Salvează CSV"
        elif "fr" in langvar:
            ch_inact_msg = "Canal inactif"
            aboutbtn = "Au sujet de"
            infoboxtxt = "FragalyseQt version 0.3, alias \"DiGeorge\".\n\nCette version du programme prend en charge l'analyse simultanée de jusqu'à 8 canaux de fluorescence différents, le masquage sélectif des canaux, les noms d'exécution non latins et peut gérer correctement les Fichiers endommagés, exporter les emplacements des pics, zones, FWHM et noms de canal au format CSV pour tous les Fichiers *.FSA et exportation au format CSV des données d'analyse interne pour les Fichiers *.FSA générés par les équipements des séries ABI 3500 et SeqStudio.\n\nLes zones de pics sont calculées en supposant qu'il s'agit de pics gaussiens.\n \nLicence sous GNU GPL version 3.\n\nSi vous souhaitez contacter l'auteur pour une raison quelconque, veuillez écrire à dorif11@gmail.com"
            openfragmentfile = "Ouvrer le Fichier FSA"
            exportinternal = "Exporter des données d'analyse interne"
            csvexport = "Exporter en CSV"
            unsupportedeq = "L'équipement non supportés!"
            unsupportedeqmsg = "Les données d'analyse internes ne pouvaient être exportées qu'à partir de Fichiers générés par les séquenceurs de la famille ABI 3500 et SeqStudio!"
            dmgdfile = "Fichier endommagé!"
            nodatamsg = "Il n'y a pas de données dans le Fichier!"
            hidechannel = "Masquer"
            minph = "Sélectionnez la hauteur de pic minimale"
            minpw = "Sélectionnez la largeur de pic minimale"
            minpp = "Sélectionnez la proéminence de pic minimale"
            savecsv = "Enregistrer CSV"
        elif "bg" in langvar:
            ch_inact_msg = "Неактивен канал"
            aboutbtn = "Относно програмата"
            infoboxtxt = "FragalyseQt версия 0.3, кодово име \"ДиДжорджи\".\n\nТази версия на програмата поддържа едновременен анализ до 8 флуоресцентни канала, селективно скриване на канали, не-латински имена на изпълнения, може да работи правилно с повредени файлове, поддържа експорт на имена на канали, позиции, области и FWHM пикове в CSV формат за всеки *.FSA файл и експортиране на вътрешни данни за анализ на данни за *.FSA файлове, получени с ABI 3500 и инструменти SeqStudio.\n\nПлощите на пиковете се изчисляват, като се приема, че пиковете са гаусови.\n\nЛицензирано под GNU GPL версия 3.\n\nАко по някаква причина искате да се свържете с автора, моля, изпратете имейл на dorif11@gmail.com"
            openfragmentfile = "Отвори файла FSA"
            exportinternal = "Експорт на Данни от Вътрешен Анализ"
            csvexport = "Експорт в CSV"
            unsupportedeq = "Неподдържан оборудване!"
            unsupportedeqmsg = "Данните за вътрешен анализ могат да бъдат експортирани само от файлове, придобити на ABI 3500 или фамилията SeqStudio!"
            dmgdfile = "Повреден файл!"
            nodatamsg = "Във файла няма данни!"
            hidechannel = "Крия "
            minph = "Изберете минимална височина на върха"
            minpw = "Изберете минимална ширина на върха"
            minpp = "Изберете минимална надморска височина"
            savecsv = "Запазване на CSV"
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.openFSA = QPushButton(self.centralwidget)
        self.openFSA.setGeometry(QRect(0, 0, 160, 20))
        self.openFSA.setCheckable(True)
        self.openFSA.setText(openfragmentfile)
        self.openFSA.clicked.connect(self.open_and_plot)
        self.aboutInfo = QPushButton(self.centralwidget)
        self.aboutInfo.setGeometry(QRect(161, 0, 100, 20))
        self.aboutInfo.setCheckable(True)
        self.aboutInfo.setText(aboutbtn)
        self.aboutInfo.clicked.connect(self.about)
        self.exportInternalAnalysisData = QPushButton(self.centralwidget)
        self.exportInternalAnalysisData.setGeometry(QRect(261, 0, 260, 20))
        self.exportInternalAnalysisData.setCheckable(True)
        self.exportInternalAnalysisData.setObjectName("IA")
        self.exportInternalAnalysisData.setText(exportinternal)
        self.exportInternalAnalysisData.clicked.connect(self.export_csv)
        self.exportCSV = QPushButton(self.centralwidget)
        self.exportCSV.setGeometry(QRect(521, 0, 120, 20))
        self.exportCSV.setCheckable(True)
        self.exportCSV.setObjectName("CSV")
        self.exportCSV.setText(csvexport)
        self.exportCSV.clicked.connect(self.export_csv)
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QRect(0, 21, 1280, 360))
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', 'Signal intensity, arbitrary units')
        self.graphWidget.setLabel('bottom', 'Size, data points')
        self.fsatab = QTableWidget(self.centralwidget)
        self.fsatab.setGeometry(QRect(0, 380, 960, 340))
        self.fsatab.setColumnCount(5)
        self.fsatab.setHorizontalHeaderLabels(['Peak Channel', 'Peak Position in Datapoints', 'Peak Height', 'Peak FWHM', 'Peak Area in Datapoints'])
        self.fsatab.resizeColumnsToContents()
        self.getheightlabel = QLabel(self)
        self.getheightlabel.setGeometry(961, 380, 320, 20)
        self.getheightlabel.setText(minph)
        self.getheight = SpinBox(self)
        self.getheight.setGeometry(961, 400, 320, 20)
        self.getheight.setRange(1, 64000)
        self.getheight.setValue(175)
        self.getheight.valueChanged.connect(self.retab)
        self.getwidthlabel = QLabel(self)
        self.getwidthlabel.setGeometry(961, 420, 320, 20)
        self.getwidthlabel.setText(minpw)
        self.getwidth = SpinBox(self)
        self.getwidth.setGeometry(961, 440, 320, 20)
        self.getwidth.setRange(1, 16000)
        self.getwidth.setValue(2)
        self.getwidth.valueChanged.connect(self.retab)
        self.getprominencelabel = QLabel(self)
        self.getprominencelabel.setGeometry(961, 460, 320, 20)
        self.getprominencelabel.setText(minpp)
        self.getprominence = SpinBox(self)
        self.getprominence.setGeometry(961, 480, 320, 20)
        self.getprominence.setRange(1, 64000)
        self.getprominence.setValue(175)
        self.getprominence.valueChanged.connect(self.retab)
        self.hidech1 = QCheckBox(self.centralwidget)
        self.hidech1.setGeometry(QRect(961, 500, 320, 20))
        self.hidech1.number = 0
        self.hidech1.toggled.connect(self.hide_ch)
        self.hidech2 = QCheckBox(self.centralwidget)
        self.hidech2.setGeometry(QRect(961, 520, 320, 20))
        self.hidech2.number = 1
        self.hidech2.toggled.connect(self.hide_ch)
        self.hidech3 = QCheckBox(self.centralwidget)
        self.hidech3.setGeometry(QRect(961, 540, 320, 20))
        self.hidech3.number = 2
        self.hidech3.toggled.connect(self.hide_ch)
        self.hidech4 = QCheckBox(self.centralwidget)
        self.hidech4.setGeometry(QRect(961, 560, 320, 20))
        self.hidech4.number = 3
        self.hidech4.toggled.connect(self.hide_ch)
        self.hidech5 = QCheckBox(self.centralwidget)
        self.hidech5.setGeometry(QRect(961, 580, 320, 20))
        self.hidech5.number = 4
        self.hidech5.toggled.connect(self.hide_ch)
        self.hidech6 = QCheckBox(self.centralwidget)
        self.hidech6.setGeometry(QRect(961, 600, 320, 20))
        self.hidech6.number = 5
        self.hidech6.toggled.connect(self.hide_ch)
        self.hidech7 = QCheckBox(self.centralwidget)
        self.hidech7.setGeometry(QRect(961, 620, 320, 20))
        self.hidech7.number = 6
        self.hidech7.toggled.connect(self.hide_ch)
        self.hidech8 = QCheckBox(self.centralwidget)
        self.hidech8.setGeometry(QRect(961, 640, 320, 20))
        self.hidech8.number = 7
        self.hidech8.toggled.connect(self.hide_ch)
        self.inactivatechkboxes()
    def inactivatechkboxes(self):
#Checkboxes without designations or with designations of nonexistent channels would look weird, so let's inactivate them correctly.
        self.hidech1.setText(ch_inact_msg)
        self.hidech2.setText(ch_inact_msg)
        self.hidech3.setText(ch_inact_msg)
        self.hidech4.setText(ch_inact_msg)
        self.hidech5.setText(ch_inact_msg)
        self.hidech6.setText(ch_inact_msg)
        self.hidech7.setText(ch_inact_msg)
        self.hidech8.setText(ch_inact_msg)
    def open_and_plot(self):
        openBtn = self.sender()
        if openBtn.isChecked():
            global homedir
            fname, _ = FileDialog.getOpenFileName(self, 'Open FSA file for analysis', homedir, ftype)
            global record, DN, x, Dye, graph_name, pen
            FAfile = open(fname, "rb")
            tmprecord = fsaread(FAfile, "abi")
#Preventing data corruption in a case if target file is corrupted.
            FAfile.close()
#Closing file to save memory and avoid unexpected things.
            if tmprecord.annotations["abif_raw"]["DATA1"] == None:
#Assuming what if no data in first channel - no data would be in other channels too.
                boxes.msgbox(dmgdfile, nodatamsg, 2)
                try:
                    record
                except NameError:
                    self.open_and_plot()
            else:
                record = tmprecord
            homedir = path.dirname(fname)
            x = []
            Dye = ['']*8
            self.inactivatechkboxes()
            graph_name = size_standard = equipment = ""
            DN = 4
#Assuming no less than 4 dyes are present.
            DN = record.annotations["abif_raw"]["Dye#1"]
            pen = [''] * DN
            pen[0] = 'b'
            pen[1] = 'g'
            pen[2] = 'y'
            pen[3] = 'r'
            if DN >= 5:
                pen[4] = 'orange'
                y5 = record.annotations["abif_raw"]["DATA105"]
            if DN >= 6:
                pen[5] = 'c'
                y6 = record.annotations["abif_raw"]["DATA106"]
            if DN >= 7:
                pen[6] = 'm'
                y7 = record.annotations["abif_raw"]["DATA107"]
            if DN == 8:
                pen[7] = 'k'
                y8 = record.annotations["abif_raw"]["DATA108"]
            if "DyeN1" not in record.annotations["abif_raw"].keys() or record.annotations["abif_raw"]["DyeN1"] == None:
#If dye names are not indicated... Well, it is absolutely sure, wavelengths are not indicated too.
                Dye[0] = "FAM"
                Dye[1] = "VIC"
                Dye[2] = "TAMRA"
                Dye[3] = "ROX"
                if DN >= 5:
                    Dye[4] = "LIZ"
                if DN >= 6:
                    Dye[5] = "SID"
                if DN >= 7:
                    Dye[5] = "Channel 7"
                if DN == 8:
                    Dye[5] = "Channel 8"
            else:
                iteration = 1
                while iteration <= DN:
                    DyeCH = "DyeN" + str(iteration)
                    Dye[iteration-1] = str(record.annotations["abif_raw"][DyeCH], 'UTF-8')
#A little strange, but possible situation - dye names are present, but without emission wavelengths or with wavelengths equal to zero.
                    DyeWL = "DyeW" + str(iteration)
                    if DyeWL in record.annotations["abif_raw"].keys():
                        Dye[iteration-1] += " " + str(record.annotations["abif_raw"][DyeWL]) + " nm"
                    iteration += 1
            self.hidech1.setText(hidechannel + Dye[0])
            self.hidech2.setText(hidechannel + Dye[1])
            self.hidech3.setText(hidechannel + Dye[2])
            self.hidech4.setText(hidechannel + Dye[3])
            if DN >= 5:
                self.hidech5.setText(hidechannel + Dye[4])
            if DN >= 6:
                self.hidech6.setText(hidechannel + Dye[5])
            if DN >= 7:
                self.hidech7.setText(hidechannel + Dye[6])
            if DN == 8:
                self.hidech8.setText(hidechannel + Dye[7])
#Assuming no more than 8 dyes are met at once.
            x = list(dict(enumerate(record.annotations["abif_raw"]["DATA1"])))
#Traces for different dyes have equal number of data points.
            if "StdF1" in record.annotations["abif_raw"].keys():
                size_standard = str(record.annotations["abif_raw"]["StdF1"], 'UTF-8') + " size standard"
            else:
                size_standard = "Unknown size marker"
            if ("DySN1" and "MODF1") not in record.annotations["abif_raw"].keys():
                equipment = "RapidHIT ID v1.X"
#RapidHIT ID v1.X *.FSA files lack DySN1 and MODF1 keys, because there are only one dye set and only one run module.
            elif "RunN1" in record.annotations["abif_raw"].keys() and (b'\xd1\xca' in record.annotations["abif_raw"]["DySN1"] or b'.avt' in record.annotations["abif_raw"]["RunN1"]) and "HCFG3" in record.annotations["abif_raw"].keys() and record.annotations["abif_raw"]["HCFG3"] == b'3130xl':
                equipment = "Nanophore-05"
            elif record.annotations["abif_raw"]["MODL1"] == b'3200':
                equipment = "SeqStudio"
            elif "HCFG3" in record.annotations["abif_raw"].keys():
                equipment = "ABI " + str(record.annotations["abif_raw"]["HCFG3"], 'UTF-8')
            else:
                equipment = "ABI " + str(record.annotations["abif_raw"]["MODL1"], 'UTF-8')
            graph_name = size_standard + ", " + equipment
            if "RunN1" in record.annotations["abif_raw"].keys():
                graph_name = str(from_bytes(record.annotations["abif_raw"]["RunN1"]).best()) + ", " + graph_name
            self.replot()
            self.retab()
    def replot(self):
        self.graphWidget.clear()
        self.graphWidget.setTitle(graph_name, color="b", size="12pt")
        self.graphWidget.plotItem.setLimits(xMin=0, xMax=len(x), yMin=0, yMax=64000)
#Maximum peak height in files generated by new ABI 3500 and SeqStudio family sequencers is 64000 arbitrary units.
        i = 1
        while i <= DN:
            chd = ""
            if i <= 4:
                chd = "DATA" + str(i)
            else:
                chd = "DATA10" + str(i)
            if show_channels[i-1]:
                self.graphWidget.plot(x, record.annotations["abif_raw"][chd], pen=pen[i-1])
            i += 1
    def about(self):
        boxes.msgbox(aboutbtn, infoboxtxt, 0)
    def findpeaks(self):
#Detecting peaks and calculating peaks data.
        h = self.getheight.value()
        w = self.getwidth.value()
        p = self.getprominence.value()
        global peakpositions, peakprominences, peakheights, peakfwhms, peakchannels, peakareas
        ch = [0]*DN
        chN = ['']*DN
        iterator = 0
        while iterator < DN:
            chd = ''
            if iterator < 4:
                chd = "DATA" + str(iterator + 1)
            else:
                chd = "DATA10" + str(iterator + 1)
            ch[iterator] = list(record.annotations["abif_raw"][chd])
            iterator += 1
        ch1data = find_peaks(ch[0], height=h, width=w, prominence=p)
        ch2data = find_peaks(ch[1], height=h, width=w, prominence=p)
        ch3data = find_peaks(ch[2], height=h, width=w, prominence=p)
        ch4data = find_peaks(ch[3], height=h, width=w, prominence=p)
        chN[0] = [Dye[0]]*len(ch1data[0])
        chN[1] = [Dye[1]]*len(ch2data[0])
        chN[2] = [Dye[2]]*len(ch3data[0])
        chN[3] = [Dye[3]]*len(ch4data[0])
        peakchannels = list(chN[0]) + list(chN[1]) + list(chN[2]) + list(chN[3])
        peakpositions = ch1data[0].tolist() + ch2data[0].tolist() + ch3data[0].tolist() + ch4data[0].tolist()
        peakprominences = ch1data[1]['prominences'].tolist() + ch2data[1]['prominences'].tolist() + ch3data[1]['prominences'].tolist() + ch4data[1]['prominences'].tolist()
        peakfwhms = ch1data[1]['widths'].tolist() + ch2data[1]['widths'].tolist() + ch3data[1]['widths'].tolist() + ch4data[1]['widths'].tolist()
        if DN>=5:
            ch5data = find_peaks(ch[4], height=h, width=w, prominence=p)
            peakpositions += ch5data[0].tolist()
            peakprominences += ch5data[1]['prominences'].tolist()
            peakfwhms += ch5data[1]['widths'].tolist()
            chN[4] = [Dye[4]]*len(ch5data[0])
            peakchannels += list(chN[4])
        if DN>=6:
            ch6data = find_peaks(ch[5], height=h, width=w, prominence=p)
            peakpositions += ch6data[0].tolist()
            peakprominences += ch6data[1]['prominences'].tolist()
            peakfwhms += ch6data[1]['widths'].tolist()
            chN[5] = [Dye[5]]*len(ch6data[0])
            peakchannels += list(chN[5])
        if DN>=7:
            ch7data = find_peaks(ch[6], height=h, width=w, prominence=p)
            peakpositions += ch7data[0].tolist()
            peakprominences += ch7data[1]['prominences'].tolist()
            peakfwhms += ch7data[1]['widths'].tolist()
            chN[6] = [Dye[6]]*len(ch7data[0])
            peakchannels += list(chN[6])
        if DN==8:
            ch8data = find_peaks(ch[7], height=h, width=w, prominence=p)
            peakpositions += ch8data[0].tolist()
            peakprominences += ch8data[1]['prominences'].tolist()
            peakfwhms += ch8data[1]['widths'].tolist()
            chN[7] = [Dye[7]]*len(ch8data[0])
            peakchannels += list(chN[7])
#Well, we don't need all the digits after the point.
        peakareas = list(peakprominences)
        for i, n in enumerate(peakfwhms):
                peakfwhms[i] = round(peakfwhms[i], 2)
                peakareas[i] = round((peakareas[i]*peakfwhms[i]/0.94), 2)
#Calculating peaks areas using formula for Gaussian peaks: A = FWHM*H/(2sqrt(2ln(2))/sqrt(2*pi)) = FWHM*H/0.94.
#FWHM is Full Width at Half Maximum.
#https://www.physicsforums.com/threads/area-under-gaussian-peak-by-easy-measurements.419285/
#Real area may be different if peak is non-Gaussian, but at least majority of them are.
#For real, peak prominence is used as a height value, because only that part of peak has meaning.
#By default, find_peaks function measures width at half maximum of prominence.
    def export_csv(self):
#Exporting CSV with data generated by findpeaks().
        expbox = self.sender()
        header = []
        do_export = False
        if expbox.focusWidget().objectName() == "CSV":
            peak_data = zip(
                    peakchannels,
                    peakpositions,
                    peakprominences,
                    peakfwhms,
                    peakareas,
                    )
            header = ['Peak Channel', 'Peak Position in Datapoints', 'Peak Height', 'Peak FWHM', 'Peak Area in Datapoints']
            do_export = True
        elif expbox.focusWidget().objectName() == "IA":
#Exporting internal analysis data.            
            if "Peak1" in record.annotations["abif_raw"].keys():
#Checking if file has internal analysis data, assuming if Peak1 field is present, other fields are too.
                peak_channel = list(record.annotations["abif_raw"]["Peak1"])
                for i, n in enumerate(peak_channel):
                    peak_channel[i] = Dye[n-1]
                peak_data = zip(
                    peak_channel,
                    list(record.annotations["abif_raw"]["Peak2"]),
                    list(record.annotations["abif_raw"]["Peak5"]),
                    list(record.annotations["abif_raw"]["Peak7"]),
                    list(record.annotations["abif_raw"]["Peak10"]),
                    list(record.annotations["abif_raw"]["Peak12"]),
                    list(record.annotations["abif_raw"]["Peak17"])
                    )
                header = ['Peak Channel', 'Peak Position in Datapoints', 'Peak FWHM', 'Peak Height', 'Peak Area in Datapoints',
                          'Peak Position in Bases', 'Peak Area in Bases']
                do_export = True
            else:
                boxes.msgbox(unsupportedeq, unsupportedeqmsg, 1)
        if do_export == True:
            import csv
            csvname, _ = FileDialog.getSaveFileName(self, savecsv, homedir, 'CSV(*.csv)')
            f = open(csvname, 'w', encoding='UTF8', newline ='')
            writer = csv.writer(f)
            writer.writerow(header)
            for row in peak_data:
                writer.writerow(row)
            f.close()
    def hide_ch(self):
        checkBox = self.sender()
        if checkBox.isChecked():
            show_channels[checkBox.number] = 0
            self.replot()
        else:
            show_channels[checkBox.number] = 1
            self.replot()
    def retab(self):
        self.findpeaks()
        rowcount = len(peakchannels)
        self.fsatab.setRowCount(rowcount)
        count = 0
        while count < rowcount:
            self.fsatab.setItem(count, 0, QTableWidgetItem(str(peakchannels[count])))
            self.fsatab.setItem(count, 1, QTableWidgetItem(str(peakpositions[count])))
            self.fsatab.setItem(count, 2, QTableWidgetItem(str(peakprominences[count])))
            self.fsatab.setItem(count, 3, QTableWidgetItem(str(peakfwhms[count])))
            self.fsatab.setItem(count, 4, QTableWidgetItem(str(peakareas[count])))
            count += 1
