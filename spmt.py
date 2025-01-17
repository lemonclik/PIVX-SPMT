#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
      
    
if __name__ == '__main__':
    
    # parse input if there's `--clear[?]Data` flags
    import argparse
    parser = argparse.ArgumentParser(description='Secure PIVX Masternode Tool')
    parser.add_argument('--clearAppData', dest='clearAppData', action='store_true',
                    help='clear all previously saved application data')
    parser.add_argument('--clearMnData', dest='clearMnData', action='store_true',
                    help='clear all previously saved masternodes')
    parser.add_argument('--clearRpcData', dest='clearRpcData', action='store_true',
                    help='clear all previously saved custom RPC servers')

    parser.set_defaults(clearAppData=False)
    parser.set_defaults(clearMnData=False)
    parser.set_defaults(clearRpcData=False)
    args = parser.parse_args()
    
    if getattr( sys, 'frozen', False ) :
        # running in a bundle
        sys.path.append(os.path.join(sys._MEIPASS, 'src'))
        imgDir = os.path.join(sys._MEIPASS, 'img')
        
        # if linux export qt plugins path
        if sys.platform == 'linux':
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt', 'plugins')

    else:
        # running live
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
        imgDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
        
    from PyQt5.QtWidgets import QApplication
    from PyQt5.Qt import Qt, QPixmap, QSplashScreen, QProgressBar, QColor, QPalette, QLabel
    
    from misc import updateSplash
    from spmtApp import App 
    
    # Create App
    app = QApplication(sys.argv)
        
    ### -- style stuff        
    spmtLogo_file = os.path.join(imgDir, 'splashscreen.png')
    labelstyle = "QLabel { font-size: 14px; color: purple; font-style: italic; text-align: center;}"
    barStyle = "QProgressBar::chunk {background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,stop: 0 #372f43,stop: 0.6 #5c4c7a, stop: 0.8 #663399);border-bottom-right-radius: 7px;border-bottom-left-radius: 7px;border-top: 2px solid #8A2BE2;}"
    
    splash_pix = QPixmap(spmtLogo_file)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    
    progressBar = QProgressBar(splash)
    progressBar.setGeometry(0, splash_pix.height()-13, splash_pix.width(), 13)
    progressBar.setStyleSheet(barStyle)
    progressBar.setAlignment(Qt.AlignRight)

    label = QLabel(splash)
    label.setStyleSheet(labelstyle)
    label.setGeometry((splash_pix.width()-500)/2, splash_pix.height()-40, 500, 20)
    label.setAlignment(Qt.AlignCenter)
    
    progressText = "loading..."
    label.setText(progressText)
    
    splash.show()

    for i in range(0, 100):
        progressBar.setValue(i)
        updateSplash(label, i)
        progressBar.setFormat(str(i) + "%")
        t = time.time()
        while time.time() < t + 0.01:
            app.processEvents()
           
    ### --------------       
    
    # Create QMainWindow Widget
    ex = App(imgDir, app, args)
    
    # Close Splashscreen
    splash.close()
    
    ##-- Launch RPC watchdog
    ex.mainWindow.rpc_watchdogThread.start()
    
    # Execute App
    app.exec_()
    try:
        app.deleteLater()
    except Exception as e:
        print(e)
        
    sys.exit()
    
    
