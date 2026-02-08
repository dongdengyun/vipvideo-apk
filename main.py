import json
import os
import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from jnius import autoclass


class VIPVideoApp(App):
    def build(self):
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_history.json')
        self.history = self.load_history()
        self.quality_interfaces = {
            '高清': 'https://jx.xmflv.cc/?url=',
            '超清': 'https://jx.aidouer.net/?url=',
            '4K': 'https://jx.quankan.app/?url=',
            '蓝光': 'https://jx.m3u8.tv/jiexi/?url=',
            '原画': 'https://jx.618g.com/?url='
        }
        
        Window.size = (360, 640)
        
        self.root = self.create_main_layout()
        return self.root

    def create_main_layout(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title_label = Label(
            text='VIP追剧神器',
            font_size=24,
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title_label)
        
        url_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        url_label = Label(text='视频网址：', size_hint_x=0.3)
        self.url_input = TextInput(multiline=False, size_hint_x=0.6)
        clear_button = Button(text='清空', size_hint_x=0.1, on_press=self.clear_url)
        url_layout.add_widget(url_label)
        url_layout.add_widget(self.url_input)
        url_layout.add_widget(clear_button)
        main_layout.add_widget(url_layout)
        
        platform_layout = GridLayout(cols=2, size_hint_y=None, height=80, spacing=5)
        platforms = [
            ('爱奇艺', self.open_iqy),
            ('腾讯视频', self.open_tx),
            ('优酷视频', self.open_yq),
            ('哔哩哔哩', self.open_bili)
        ]
        for text, command in platforms:
            btn = Button(text=text, on_press=command)
            platform_layout.add_widget(btn)
        main_layout.add_widget(platform_layout)
        
        option_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        quality_label = Label(text='画质：', size_hint_x=0.2)
        self.quality_spinner = Spinner(
            text='高清',
            values=list(self.quality_interfaces.keys()),
            size_hint_x=0.4
        )
        mode_label = Label(text='模式：', size_hint_x=0.2)
        self.mode_spinner = Spinner(
            text='浏览器播放',
            values=['浏览器播放', '内置播放器'],
            size_hint_x=0.4
        )
        option_layout.add_widget(quality_label)
        option_layout.add_widget(self.quality_spinner)
        option_layout.add_widget(mode_label)
        option_layout.add_widget(self.mode_spinner)
        main_layout.add_widget(option_layout)
        
        play_button = Button(
            text='播放VIP视频',
            size_hint_y=None,
            height=60,
            font_size=18,
            background_color=(0.3, 0.8, 0.3, 1),
            on_press=self.play_video
        )
        main_layout.add_widget(play_button)
        
        history_button = Button(
            text='历史记录',
            size_hint_y=None,
            height=50,
            on_press=self.show_history
        )
        main_layout.add_widget(history_button)
        
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        minimize_button = Button(text='最小化', on_press=self.minimize_window)
        exit_button = Button(text='退出', on_press=self.exit_app)
        control_layout.add_widget(minimize_button)
        control_layout.add_widget(exit_button)
        main_layout.add_widget(control_layout)
        
        hint_label = Label(
            text='提示：本案例仅供学习使用，不可作为他用',
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=30,
            font_size=12
        )
        main_layout.add_widget(hint_label)
        
        return main_layout

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def extract_title_from_url(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if 'iqiyi.com' in url:
                title = soup.find('title')
                if title:
                    title_text = title.get_text().strip()
                    if '_高清视频在线观看' in title_text:
                        title_text = title_text.split('_高清视频在线观看')[0]
                    elif '-高清视频' in title_text:
                        title_text = title_text.split('-高清视频')[0]
                    return f"爱奇艺-{title_text}"
                    
            elif 'v.qq.com' in url:
                title = soup.find('title')
                if title:
                    title_text = title.get_text().strip()
                    if '_腾讯视频' in title_text:
                        title_text = title_text.split('_腾讯视频')[0]
                    elif '-腾讯视频' in title_text:
                        title_text = title_text.split('-腾讯视频')[0]
                    return f"腾讯-{title_text}"
                    
            elif 'youku.com' in url:
                title = soup.find('title')
                if title:
                    title_text = title.get_text().strip()
                    if '-优酷' in title_text:
                        title_text = title_text.split('-优酷')[0]
                    elif '高清在线观看' in title_text:
                        title_text = title_text.split('高清在线观看')[0]
                    return f"优酷-{title_text}"
                    
            elif 'bilibili.com' in url:
                title = soup.find('title')
                if title:
                    title_text = title.get_text().strip()
                    if '_哔哩哔哩' in title_text:
                        title_text = title_text.split('_哔哩哔哩')[0]
                    elif '-哔哩哔哩' in title_text:
                        title_text = title_text.split('-哔哩哔哩')[0]
                    return f"哔哩-{title_text}"
            
            return url[:50] + '...' if len(url) > 50 else url
            
        except Exception as e:
            return url[:50] + '...' if len(url) > 50 else url

    def add_to_history(self, url):
        title = self.extract_title_from_url(url)
        for item in self.history:
            if item['url'] == url:
                self.history.remove(item)
                break
        self.history.insert(0, {'title': title, 'url': url})
        if len(self.history) > 50:
            self.history = self.history[:50]
        self.save_history()

    def clear_url(self, instance):
        self.url_input.text = ''

    def open_iqy(self, instance):
        self.open_url('https://www.iqiyi.com')

    def open_tx(self, instance):
        self.open_url('https://v.qq.com')

    def open_yq(self, instance):
        self.open_url('https://www.youku.com/')

    def open_bili(self, instance):
        self.open_url('https://www.bilibili.com')

    def open_url(self, url):
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            currentActivity = PythonActivity.mActivity
            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(url))
            currentActivity.startActivity(intent)
        else:
            import webbrowser
            webbrowser.open(url)

    def play_video(self, instance):
        url = self.url_input.text.strip()
        if url:
            self.add_to_history(url)
            quality = self.quality_spinner.text
            interface = self.quality_interfaces.get(quality, 'https://jx.xmflv.cc/?url=')
            play_url = f'{interface}{url}'
            
            play_mode = self.mode_spinner.text
            
            if play_mode == '内置播放器':
                self.play_in_internal_player(play_url)
            else:
                self.open_url(play_url)
        else:
            self.show_popup('提示', '请输入视频网址！')

    def play_in_internal_player(self, url):
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            currentActivity = PythonActivity.mActivity
            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(url))
            currentActivity.startActivity(intent)
        else:
            import webbrowser
            webbrowser.open(url)

    def show_history(self, instance):
        if not self.history:
            self.show_popup('历史记录', '暂无历史记录')
            return
        
        content = BoxLayout(orientation='vertical')
        
        scroll_view = ScrollView()
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for idx, item in enumerate(self.history):
            btn = Button(
                text=item['title'],
                size_hint_y=None,
                height=50,
                halign='left'
            )
            btn.bind(on_press=lambda btn, idx=idx: self.play_from_history(idx))
            list_layout.add_widget(btn)
        
        scroll_view.add_widget(list_layout)
        content.add_widget(scroll_view)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        clear_button = Button(text='清空历史', on_press=lambda x: self.clear_history())
        close_button = Button(text='关闭', on_press=lambda x: popup.dismiss())
        button_layout.add_widget(clear_button)
        button_layout.add_widget(close_button)
        content.add_widget(button_layout)
        
        popup = Popup(title='播放历史记录', content=content, size_hint=(0.9, 0.8))
        popup.open()

    def play_from_history(self, index):
        url = self.history[index]['url']
        self.url_input.text = url
        quality = self.quality_spinner.text
        interface = self.quality_interfaces.get(quality, 'https://jx.xmflv.cc/?url=')
        play_url = f'{interface}{url}'
        
        play_mode = self.mode_spinner.text
        
        if play_mode == '内置播放器':
            self.play_in_internal_player(play_url)
        else:
            self.open_url(play_url)

    def clear_history(self):
        self.history = []
        self.save_history()
        self.show_popup('提示', '历史记录已清空')

    def minimize_window(self, instance):
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = PythonActivity.mActivity
            currentActivity.moveTaskToBack(True)
        else:
            Window.minimize()

    def exit_app(self, instance):
        App.get_running_app().stop()

    def show_popup(self, title, message):
        content = Label(text=message, font_size=16)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
        popup.open()


if __name__ == '__main__':
    VIPVideoApp().run()
