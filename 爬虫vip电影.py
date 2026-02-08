import tkinter
import webbrowser
import json
import os
import requests
from bs4 import BeautifulSoup
from tkinter import PhotoImage, messagebox, Toplevel, Scrollbar, Listbox, END, SINGLE, Frame, Label, Entry, Button
try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False


class VIPVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('VIP追剧神器')
        
        self.is_mobile = self.detect_mobile()
        
        self.root.geometry('580x290')
        
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_history.json')
        self.history = self.load_history()
        self.quality_var = tkinter.StringVar(value='高清')
        self.play_mode_var = tkinter.StringVar(value='浏览器播放')
        self.quality_interfaces = {
            '高清': 'https://jx.xmflv.cc/?url=',
            '超清': 'https://jx.aidouer.net/?url=',
            '4K': 'https://jx.quankan.app/?url=',
            '蓝光': 'https://jx.m3u8.tv/jiexi/?url=',
            '原画': 'https://jx.618g.com/?url='
        }
        self.create_widgets()
        self.bind_shortcuts()

    def bind_shortcuts(self):
        self.root.bind('<Escape>', self.on_escape)

    def on_escape(self, event=None):
        if messagebox.askyesno('退出', '确定要退出程序吗？'):
            self.root.quit()
            self.root.destroy()

    def minimize_window(self):
        self.root.iconify()

    def detect_mobile(self):
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            return screen_width <= 768 or screen_height <= 1024
        except:
            return False

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

    def create_widgets(self):
        if self.is_mobile:
            self.create_mobile_widgets()
        else:
            self.create_desktop_widgets()

    def create_desktop_widgets(self):
        # 输入区域
        label_movie_link = tkinter.Label(self.root, text='输入视频网址：')
        label_movie_link.place(x=20, y=20, width=100, height=30)

        self.entry_movie_link = tkinter.Entry(self.root)
        self.entry_movie_link.place(x=125, y=20, width=260, height=30)

        button_movie_link = tkinter.Button(self.root, text='清空', command=self.empty)
        button_movie_link.place(x=400, y=20, width=50, height=30)

        # 平台按钮
        platforms = [
            ('爱奇艺', self.open_iqy, 25),
            ('腾讯视频', self.open_tx, 125),
            ('优酷视频', self.open_yq, 225),
            ('哔哩哔哩', self.open_bili, 325)
        ]
        for text, command, xpos in platforms:
            tkinter.Button(self.root, text=text, command=command)\
                .place(x=xpos, y=60, width=80, height=40)

        # 播放按钮
        tkinter.Button(self.root, text='播放VIP视频', command=self.play_video)\
            .place(x=425, y=60, width=125, height=40)

        # 画质选择
        quality_label = tkinter.Label(self.root, text='选择画质：')
        quality_label.place(x=20, y=110, width=80, height=30)
        
        quality_menu = tkinter.OptionMenu(self.root, self.quality_var, *self.quality_interfaces.keys())
        quality_menu.place(x=105, y=110, width=120, height=30)

        # 播放模式选择
        mode_label = tkinter.Label(self.root, text='播放模式：')
        mode_label.place(x=240, y=110, width=80, height=30)
        
        mode_menu = tkinter.OptionMenu(self.root, self.play_mode_var, '浏览器播放', '内置播放器')
        mode_menu.place(x=325, y=110, width=120, height=30)

        # 历史记录按钮
        tkinter.Button(self.root, text='历史记录', command=self.show_history)\
            .place(x=425, y=105, width=125, height=30)

        # 窗口控制按钮
        control_frame = Frame(self.root)
        control_frame.place(x=425, y=140, width=125, height=30)
        
        tkinter.Button(control_frame, text='最小化', command=self.minimize_window, width=8).pack(side='left', padx=2)
        tkinter.Button(control_frame, text='退出', command=self.on_escape, width=8).pack(side='left', padx=2)

        # 底部提示
        tkinter.Label(self.root,
                    text='提示：本案例仅供学习使用，不可作为他用。ESC退出',
                    fg='red',
                    font=('Arial', 10))\
            .place(x=50, y=175, width=400, height=25)

        # 锁定窗口尺寸
        self.root.resizable(False, False)

    def create_mobile_widgets(self):
        # 主容器
        main_frame = Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 输入区域
        input_frame = Frame(main_frame)
        input_frame.pack(fill='x', pady=5)
        
        tkinter.Label(input_frame, text='视频网址：', font=('Arial', 12)).pack(side='left', padx=5)
        
        self.entry_movie_link = Entry(input_frame, font=('Arial', 12))
        self.entry_movie_link.pack(side='left', fill='x', expand=True, padx=5)
        
        tkinter.Button(input_frame, text='清空', command=self.empty, font=('Arial', 10)).pack(side='left', padx=5)

        # 平台按钮
        platform_frame = Frame(main_frame)
        platform_frame.pack(fill='x', pady=10)
        
        platforms = [
            ('爱奇艺', self.open_iqy),
            ('腾讯视频', self.open_tx),
            ('优酷视频', self.open_yq),
            ('哔哩哔哩', self.open_bili)
        ]
        for text, command in platforms:
            tkinter.Button(platform_frame, text=text, command=command, font=('Arial', 11), width=10).pack(side='left', padx=5)

        # 画质和播放模式
        option_frame = Frame(main_frame)
        option_frame.pack(fill='x', pady=10)
        
        tkinter.Label(option_frame, text='画质：', font=('Arial', 12)).pack(side='left', padx=5)
        quality_menu = tkinter.OptionMenu(option_frame, self.quality_var, *self.quality_interfaces.keys())
        quality_menu.pack(side='left', padx=5)
        
        tkinter.Label(option_frame, text='模式：', font=('Arial', 12)).pack(side='left', padx=5)
        mode_menu = tkinter.OptionMenu(option_frame, self.play_mode_var, '浏览器播放', '内置播放器')
        mode_menu.pack(side='left', padx=5)

        # 播放按钮
        tkinter.Button(main_frame, text='播放VIP视频', command=self.play_video, 
                    font=('Arial', 14, 'bold'), bg='#4CAF50', fg='white', height=2).pack(fill='x', pady=10)

        # 历史记录按钮
        tkinter.Button(main_frame, text='历史记录', command=self.show_history, 
                    font=('Arial', 12), height=2).pack(fill='x', pady=5)

        # 窗口控制按钮
        control_frame = Frame(main_frame)
        control_frame.pack(fill='x', pady=5)
        
        tkinter.Button(control_frame, text='最小化', command=self.minimize_window, 
                    font=('Arial', 11), width=10).pack(side='left', padx=5, expand=True)
        tkinter.Button(control_frame, text='退出', command=self.on_escape, 
                    font=('Arial', 11), width=10).pack(side='left', padx=5, expand=True)

        # 底部提示
        tkinter.Label(main_frame,
                    text='提示：本案例仅供学习使用，不可作为他用。ESC退出',
                    fg='red',
                    font=('Arial', 10))\
            .pack(pady=10)

    # 原有功能保持不变
    def open_iqy(self): webbrowser.open('https://www.iqiyi.com')
    def open_tx(self): webbrowser.open('https://v.qq.com')
    def open_yq(self): webbrowser.open('https://www.youku.com/')
    def open_bili(self): webbrowser.open('https://www.bilibili.com')
    def play_video(self):
        url = self.entry_movie_link.get()
        if url:
            self.add_to_history(url)
            quality = self.quality_var.get()
            interface = self.quality_interfaces.get(quality, 'https://jx.xmflv.cc/?url=')
            play_url = f'{interface}{url}'
            
            play_mode = self.play_mode_var.get()
            
            if play_mode == '内置播放器':
                self.play_in_internal_player(play_url)
            else:
                webbrowser.open(play_url)
        else:
            messagebox.showwarning('提示', '请输入视频网址！')

    def play_in_internal_player(self, url):
        if HAS_WEBVIEW:
            try:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                webview.create_window('VIP视频播放器', url, 
                                    width=screen_width, 
                                    height=screen_height,
                                    resizable=True, 
                                    fullscreen=False)
                webview.start()
            except Exception as e:
                messagebox.showerror('错误', f'内置播放器启动失败：{str(e)}\n将使用浏览器播放。')
                webbrowser.open(url)
        else:
            messagebox.showinfo('提示', '未安装pywebview库，将使用浏览器播放。\n请运行：pip install pywebview')
            webbrowser.open(url)

    def show_history(self):
        history_window = Toplevel(self.root)
        history_window.title('播放历史记录')
        history_window.geometry('600x400')
        history_window.resizable(True, True)
        
        history_window.bind('<Escape>', lambda e: history_window.destroy())

        frame = tkinter.Frame(history_window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')

        history_list = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=SINGLE, font=('Arial', 10))
        history_list.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=history_list.yview)

        for item in self.history:
            history_list.insert(END, item['title'])

        def play_selected():
            selection = history_list.curselection()
            if selection:
                index = selection[0]
                url = self.history[index]['url']
                self.entry_movie_link.delete(0, 'end')
                self.entry_movie_link.insert(0, url)
                quality = self.quality_var.get()
                interface = self.quality_interfaces.get(quality, 'https://jx.xmflv.cc/?url=')
                play_url = f'{interface}{url}'
                
                play_mode = self.play_mode_var.get()
                
                if play_mode == '内置播放器':
                    self.play_in_internal_player(play_url)
                else:
                    webbrowser.open(play_url)

        def delete_selected():
            selection = history_list.curselection()
            if selection:
                index = selection[0]
                del self.history[index]
                self.save_history()
                history_list.delete(selection[0])

        button_frame = tkinter.Frame(history_window)
        button_frame.pack(fill='x', padx=10, pady=10)

        tkinter.Button(button_frame, text='播放选中', command=play_selected, width=15).pack(side='left', padx=5)
        tkinter.Button(button_frame, text='删除选中', command=delete_selected, width=15).pack(side='left', padx=5)
        tkinter.Button(button_frame, text='清空历史', command=lambda: self.clear_all_history(history_list), width=15).pack(side='left', padx=5)
        tkinter.Button(button_frame, text='关闭', command=history_window.destroy, width=15).pack(side='right', padx=5)

    def clear_all_history(self, history_list):
        self.history = []
        self.save_history()
        history_list.delete(0, END)
    def empty(self): self.entry_movie_link.delete(0, 'end')


if __name__ == '__main__':
    root = tkinter.Tk()
    VIPVideoApp(root)
    root.mainloop()
