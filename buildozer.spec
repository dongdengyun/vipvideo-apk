[app]

title = VIP追剧神器
package.name = vipvideo
package.domain = org.vipvideo

source.include_exts = py,png,jpg,kv,atlas,json
source.dir = .

version = 1.0.0

requirements = python3,kivy,kivy-deps.angle,kivy-deps.glew,kivy-deps.sdl2,pyjnius,beautifulsoup4,requests,android

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

[buildozer]

log_level = 2

warn_on_root = 1
