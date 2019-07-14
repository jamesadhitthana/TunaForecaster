import random
import os
import pandas as pd
#--How to use--#
# 1. Place this python file in the same folder that contains the seaPort.csv file.
# 2. Place the folder that contains the data to clean into a new folder inside the folder and change the "folderOfDataToClean" variable to the name of your chosen folder you placed previously to clean
# 3. Change the "cleanedFolderPath" variable to a new folder name you want to have the cleaned files to be put in
# 4. Modify the checkPort(... 0.2) function and change the number to the desired decimal degree


#--Decimal Degrees Converted to KM--#
# 1.0 = 111.32 km
# 0.1 = 11.132 km
# 0.01 = 	1.1132 km
# So for every 0.01 degrees it means a distance of 1.1132 km
# --

# if lat is less than or over than 0.01degrees from the port then clear
# if long is less than or over than 0.01 degrees from the port then clear


def checkLatLng(portLat, portLng, latList, lngList,decimalToCheck):

    latAfterCheckLat = []
    lngAfterCheckLat = []
    # print("Harus dibawah", (portLat-0.01), "dan di atas", (portLat+0.01))

    for i in range(len(latList)):
        # print(latList[i])
        if latList[i] <= (portLat-decimalToCheck) or latList[i] >= (portLat+decimalToCheck):
            latAfterCheckLat.append(latList[i])
            lngAfterCheckLat.append(lngList[i])
    # # print("total latAfterCheckLat[]=", len(latAfterCheckLat))
    # for i in range(len(latAfterCheckLat)):
    #     print(latAfterCheckLat[i], ",", lngAfterCheckLat[i])
        else:
            # else = berarti dia in between daerah ga boleh
            # then check the lng
            if lngList[i] <= (portLng-decimalToCheck) or lngList[i] >= (portLng+decimalToCheck):
                latAfterCheckLat.append(latList[i])
                lngAfterCheckLat.append(lngList[i])

    return latAfterCheckLat, lngAfterCheckLat


def checkPort(portLat, portLong, listOfLat, listOfLng,decimalToCheck):

    latChecked, lngChecked = checkLatLng(
        portLat, portLong, listOfLat, listOfLng,decimalToCheck)

    return latChecked, lngChecked


def cleanFile(sourceFile, targetFolderForCleanedFiles, seaPortFile):

    # ----Read seaport CSV----
    try:
        dataFrameLatLngSource = pd.read_csv(sourceFile)
    except Exception as e:
        print("An error happened when trying to read the CSV :(", e)
    listOfLat = []
    listOfLng = []
    for i in range(0, len(dataFrameLatLngSource["lat"])):
        # access first dataframe index (after header)
        listOfLat.append(dataFrameLatLngSource["lat"][i])
        listOfLng.append(dataFrameLatLngSource["lon"][i])
    # for i in range(len(listOfLat)):
    #     print(listOfLat[i], ",", listOfLng[i])
    #----#

    # Read the sea_ports CSV
    try:
        # precision set to get the EXACT coordinate decimal values
        dataFrameIndoSeaPorts = pd.read_csv(
            seaPortFile, float_precision='round_trip')
    except Exception as e:
        print("An error happened when trying to read the CSV :(", e)

    for i in range(0, len(dataFrameIndoSeaPorts)):
        # print(i, dataFrameIndoSeaPorts["Latitude"][i],
        #       ",", dataFrameIndoSeaPorts["Longitude"][i])
        listOfLat, listOfLng = checkPort(dataFrameIndoSeaPorts["Latitude"][i], dataFrameIndoSeaPorts["Longitude"][i],
                                         listOfLat, listOfLng, 0.2)

    dataCoba = {"lat": listOfLat,
                "lon": listOfLng}
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
folderOfDataToClean = "\\prediction_data\\"
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
cleanedFolderPath = "cleaned_data_11kmV2"
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
              listOfFiles[i], cleanedFolderPath, "seaPorts.csv")
print("Successfully cleaned", len(listOfFiles), "files")
