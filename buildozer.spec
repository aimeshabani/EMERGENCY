[app]

# (str) Title of your application
title = Emergency

# (str) Package name
package.name = Emergency

# (str) Package domain (needed for android/ios packaging)
package.domain =org.kivy

# (str) Source code where the main.py live
source.dir =./
icon.filename = src/ico.png
android.presplash=src/splash.png

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,java,shabani,json,txt

# (list) List of inclusions using pattern matching
source.include_patterns = SD/*

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version.regex = __version__ = '(.*)'
version.filename = %(source.dir)s/main.py

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy    opencv-python==4.8.1.78, numpy==1.25.0   , opencv-python-headless, numpy      bleak, typing-extensions, dbus_fast,    , pybluez
requirements = python3,kivy,oscpy,plyer,jnius,pyjnius,kivymd, pillow
#android.python3 = True

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
presplash.filename =src/splash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait, landscape

# (list) List of service to declare  Pong:service.py:foreground:sticky, , LOC:location.py:foreground:sticky
services =Sos:SOS.py:foreground:sticky
# services =Sos:SOS.py:background:sticky

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
android.presplash_color = darkgray

# (list) Permissions                        , HIGH_SAMPLING_RATE_SENSORS
android.permissions = INTERNET,FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED, ACCESS_FINE_LOCATION, ACCESS_BACKGROUND_LOCATION, ACCESS_COARSE_LOCATION, VIBRATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MEDIA_BUTTON, RECORD_AUDIO, CAMERA, BLUETOOTH_SCAN, BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_CONNECT, BLUETOOTH_ADVERTISE


# (list) XML file to include as additional elements in the AndroidManifest.xml
#android.manifest=src/AndroidManifest.tmpl.xml


# (int) Target Android API, should be as high as possible.
android.api = 31

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (int) Minimum API your APK / AAB will support.
android.minapi = 21
android.sdk = 33

# (str) Android NDK version to use
#android.ndk = 19c

# (int) Android NDK API to use (optional). This is the minimum API your app will support. 
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =SD

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)    old:  ./src/main/java      /media/aime/USER-DATA/dataset/PGS/source/main/java/org/kivy/emergency
android.add_src = source/main/java
android.package = org.kivy.emergency


# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
#android.add_aars =

# (list) Gradle dependencies to add (currently works only with sdl2_gradle
# bootstrap)
#android.gradle_dependencies =

# (list) Java classes to add as activities to the manifest.
#android.add_activites = src/org.kivy.oscservice.BootCompletedReceiver.java

# (str) python-for-android branch to use, defaults to stable
p4a.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data =android.app.lib_name=app, android.app.bridges=sdl2, android.app.start_path=main.py


# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86
android.arch = arm64-v8a, armeabi-v7a

#
# Python for android (p4a) specific
#

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir = /home/gabriel/dev/python-for-android/

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug
