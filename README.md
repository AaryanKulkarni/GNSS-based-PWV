# GNSS-based-PWV
Prediction and inter-dependence of rainfall and PWV.
1. Download orbital files from nasa with ML project->1DATA.py
2. Those .o archived files should be directly uploaded to gypsy oasis with ML project->2GYPSYPROCESSING.py->.zip files will be saved at location where the project directory is saved. Copy those files to a folder then run ML project->3automatic extract files.py it will be saved in the same folder woth a new folder which is created inside it.
3.Run python code in ML->4.excel files form txt.py which will make excel files from txt
4.Download the meteorological files from sopac with the python code met data download auto(Not checked) 
5.ML->5.Meterological download to download all the meterological files.
6. Create two folder T and Z keep temp excel files in T and Gypsy processed files in in Z and then copy path of root folder and keep in ML->6.rename excel code to rename excel based on dates.
7. Convert the excel data of both T and Z to 24 hrs by specifiying the main folder path in the ML->7.convert T and Z 24 hrs python code.Same folder path as in step 6.
8. To get the final PWV values excel, give the path of main folder containing Z and T sub folders in the python code named ML->8.PWV from Z and T folders.(same path of folder as in 6 and 7).
