import os,sys,re
import subprocess
from xml.dom.minidom import parseString
import shutil

'''
 process a single apk, get permission used and
 check whether key functions are invoked in the program
'''
class SingleAPKParse():

    def __init__(self,papk_name,papkdir,pfiltered_dir,pdelete_tmpfolder):
        self.apk_name = papk_name
        self.apkdir = papkdir
        self.apk_in_path = os.path.join(self.apkdir,self.apk_name)
        # print(self.apk_in_path)
        self.apk_out_path = os.path.join(self.apkdir, self.apk_name[:self.apk_name.index(".apk")])
        # print(self.apk_out_path)
        self.filtered_dir = pfiltered_dir

        # whether use camera
        self.use_camera_permission = False
        self.use_camera_api = False

        # whether use recorder
        self.use_recorder_permission = False
        self.use_recorder_api = False

        # whether use GPS
        self.use_gps_permission = False
        self.use_gps_api = False

        # whether use sensor
        self.use_sensor_api = False

        # whether use
        self.parse()

        self.copy_target_file()


        # delete tmp file
        if pdelete_tmpfolder:
            shutil.rmtree(self.apk_out_path, ignore_errors=True)



    def copy_target_file(self):
        if self.use_camera_permission and self.use_camera_api:
            shutil.copy2(self.apk_in_path, self.filtered_dir)
        elif self.use_recorder_api and self.use_recorder_permission:
            shutil.copy2(self.apk_in_path, self.filtered_dir)
        elif self.use_gps_api and self.use_gps_permission:
            shutil.copy2(self.apk_in_path, self.filtered_dir)
        elif self.use_sensor_api:
            shutil.copy2(self.apk_in_path, self.filtered_dir)


    def parse(self):
        # create the output folder
        subprocess.call(['java','-jar','apktool.jar','d',self.apk_in_path,'-o',self.apk_out_path])

        manifest_path = os.path.join(self.apk_out_path, 'AndroidManifest.xml')

        # cannot find and open android manifest file
        if manifest_path == None:
            print("Cannot find the AndroidManifest.xml created, please check again!")
            raise IOError

        with open(manifest_path, 'r',encoding='utf-8') as f:
            manifest_content = f.read()

        dom = parseString(manifest_content)
        permissions_xml = dom.getElementsByTagName('uses-permission')

        for permission_xml in permissions_xml:
            permission = permission_xml.getAttribute('android:name')
            # use audio recorder permission
            if "android.permission.RECORD_AUDIO" in permission:
                self.use_recorder_permission = True

            # use gps permission
            elif "android.permission.ACCESS_FINE_LOCATION" in permission or "android.permission.ACCESS_COARSE_LOCATION" in permission:
                self.use_gps_permission = True

            # use camera permission
            elif "android.permission.CAMERA" in permission:
                self.use_camera_permission = True

        # get smali file path
        self.smali_path = os.path.join(self.apk_out_path, 'smali')
        # cannot find and open smali directory
        if self.smali_path == None:
            print("Cannot find the samli directory, please check again!")
            raise IOError


        for r, d, f in os.walk(self.smali_path):
            for file in f:
                if ".smali" in file:
                    self.process_smalifile(os.path.join(r,file))




    def process_smalifile(self,smali_file):
        with open(smali_file, 'r',encoding='utf-8') as f:
            smali_content = f.read()

        for line in smali_content.split("\n"):
            # use location service api
            if "Landroid/location/LocationManager;->requestLocationUpdates" in line:
                self.use_gps_api = True

            # use recorder api
            elif "Landroid/media/AudioRecord;->startRecording" in line or "Landroid/media/MediaRecorder;->start()" in line:
                self.use_recorder_api = True

            # use camera api
            elif ("Landroid/hardware/Camera;->open" and "invoke-static") in line:
                self.use_camera_api = True

            elif ("Landroid/media/MediaRecorder;->setVideoSource" and "invoke-static") in line:
                self.use_camera_api = True

            elif "Landroid/hardware/SensorManager;->getDefaultSensor" in line or \
                    "Landroid/hardware/SensorManager;->getDynamicSensorList" in line:
                self.use_sensor_api = True



