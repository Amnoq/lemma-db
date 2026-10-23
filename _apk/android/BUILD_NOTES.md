# Lemma Bank APK — build notes

App: "Lemma Bank" (`org.lemmabank.app`), single Activity with a full-screen
WebView loading `file:///android_asset/web-lemmatizer.html` (the exported
web-lemmatizer page, bundled in `app/src/main/assets/`). Works fully offline.
minSdk 24, targetSdk 34, versionCode 1 / versionName 1.0.

## Why not Gradle
The VM has ~630MB free RAM; the Gradle daemon cannot start here
("Could not receive a message from the daemon" at any heap size).
The APK is built with the SDK tools directly — same inputs, same output
shape as `./gradlew assembleDebug`.

## Toolchain (all under ~/ — persistent)
- JDK: `~/jdk/jdk-17.0.11+9` (Temurin tarball)
- SDK: `~/android-sdk` — cmdline-tools, `platforms/android-34`
  (platform-34-ext8 full layout + ext12 android.jar/data overlaid;
  Google no longer ships a base `platform-34_rXX.zip`),
  `build-tools/34.0.0`
- Note: sdkmanager's repo fetch fails through this VM's egress proxy
  (JDK HttpURLConnection tunneling bug); packages were fetched with curl
  from the repository2-1.xml URLs instead.

## Rebuild
```sh
export JAVA_HOME=~/jdk/jdk-17.0.11+9
export PATH=$JAVA_HOME/bin:~/android-sdk/build-tools/34.0.0:$PATH
export ANDROID_HOME=~/android-sdk
B=build; rm -rf $B; mkdir -p $B/classes $B/dex
javac -source 17 -target 17 -nowarn \
  -cp $ANDROID_HOME/platforms/android-34/android.jar \
  -d $B/classes app/src/main/java/org/lemmabank/app/MainActivity.java
d8 --min-api 24 --lib $ANDROID_HOME/platforms/android-34/android.jar \
  --output $B/dex $B/classes/org/lemmabank/app/MainActivity.class
aapt2 link -o $B/unsigned.apk \
  -I $ANDROID_HOME/platforms/android-34/android.jar \
  --manifest app/src/main/AndroidManifest.xml \
  --min-sdk-version 24 --target-sdk-version 34 \
  --version-code 1 --version-name 1.0 -A app/src/main/assets
(cd $B/dex && zip -q -j ../unsigned.apk classes.dex)
zipalign -f 4 $B/unsigned.apk $B/aligned.apk
# debug keystore (generate once; NOTE: `rm -rf build` deletes it —
# regenerate with the command below before signing if you wiped build):
# keytool -genkeypair -keystore $B/debug.keystore -alias androiddebugkey \
#   -storepass android -keypass android -keyalg RSA -keysize 2048 \
#   -validity 10950 -dname "CN=Android Debug,O=Android,C=US"
apksigner sign --ks $B/debug.keystore --ks-pass pass:android \
  --key-pass pass:android --out ../lemma-bank-debug.apk $B/aligned.apk
```

## Install (sideload)
Debug-signed: Android will warn the app is from an unknown developer —
expected. On the phone: transfer the APK, open it, allow "Install unknown
apps" for the file manager/browser when prompted, tap Install. No network
needed; the page runs from the bundled asset.
