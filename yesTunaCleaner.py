import random
import os
import pandas as pd

def cleanFile(sourceFile, targetFolderForCleanedFiles):
    try:
        dataFrameLatLngSource = pd.read_csv(sourceFile)
    except Exception as e:
        print("An error happened when trying to read the CSV :(", e)
    listOfLat = []
    listOfLng = []
    listOfSST = []  # new
    listOfChlorophyll = []  # new
    listOfTuna = []#new tuna

    for i in range(0, len(dataFrameLatLngSource["lat"])):

        if dataFrameLatLngSource["tuna"][i] == 1:
            # access first dataframe index (after header)
            listOfLat.append(dataFrameLatLngSource["lat"][i])
            listOfLng.append(dataFrameLatLngSource["lon"][i])

            listOfSST.append(dataFrameLatLngSource["sst"][i])  # new
            listOfChlorophyll.append(
                dataFrameLatLngSource["chlorophyll"][i])  # new
            listOfTuna.append(dataFrameLatLngSource["tuna"][i]) #new tuna
       
    #----If tuna ==1 then keep, else delete

    #----


    dataCoba = {"lat": listOfLat,
                "lon": listOfLng,
                "sst": listOfSST,
                "chlorophyll": listOfChlorophyll,
                "tuna": listOfTuna}
    dataFrameCoba = pd.DataFrame(dataCoba)
    # print("--\n\n")
    # print(dataFrameCoba[["lat", "lon"]])

    dataFrameToSave = pd.DataFrame(listOfLat, columns=["Latitude"])
    try:
        dataFrameCoba.to_csv(
            str(".\\"+targetFolderForCleanedFiles+"\\"+sourceFile[-14:]), index=False)
        print("Data saved successfuly to", str(
            ".\\"+targetFolderForCleanedFiles+"\\"+sourceFile[-14:]))
    except Exception as e:
        print("Error: failed to save to csv :( \n", e)  # TODO: Fix this


#---MAIN---#
# ---Load Tuna CSV File Folder---#
listOfFiles = []
# by default the "." value will make it the current working directory of the py file
defaultFolderDirectory = "."
folderOfDataToClean = "\\oldPredictedTuna\\"
try:
    for folderName, subFolders, fileNames in os.walk(defaultFolderDirectory+folderOfDataToClean):
        for files in fileNames:
            listOfFiles.append(files)
    print("\nSuccessfuly loaded List of Files:",
          len(listOfFiles), "files total")

except Exception as e:
    print("ERROR files not found in: ", os.getcwd())
    print(e)
    print("\nI stopped the app for you :)")
    raise SystemExit
# END OF: Load Tuna CSV File Folder---

# Check if the target folder for the cleaned data exists, if it doesnt then create one
cleanedFolderPath = "oldPredictedTunaCleaned"
if(os.path.exists(cleanedFolderPath)):
    print(cleanedFolderPath, "exists")
else:
    print("Doesnt exist, and creating the folder")
    try:
        os.makedirs(cleanedFolderPath)
        print("Successfuly created the 'Cleaned' folder path")
    except Exception as e:
        print("Failed to created the 'Cleaned' folder path", e)

# For-loop to clean the files
for i in range(len(listOfFiles)):
    cleanFile(defaultFolderDirectory+folderOfDataToClean +
              listOfFiles[i], cleanedFolderPath)
print("Successfully cleaned", len(listOfFiles), "files")
