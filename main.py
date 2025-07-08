import sys
import os
import platform
import subprocess
import json
import tempfile
import ctypes
import winreg
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                              QFileDialog, QLabel)
from PySide6.QtCore import QFile, QProcess, Qt
from ui import Ui_MainWindow

# 平台相关设置
class SystemSettings:
    def __init__(self):
        self.os_type = platform.system()
        self.reg_backup = {}
        self.plist_backup = ""
        self.format_tip = ""
        self.current_format = ""
        
        if self.os_type == "Windows":
            self.init_windows()
        elif self.os_type == "Darwin":  # macOS
            self.init_macos()
        elif self.os_type == "Linux":
            self.init_linux()
    
    def init_windows(self):
        self.format_tip = "Windows格式: HH:mm (24小时), h:mm tt (12小时)\n例如: HH:mm:ss, hh:mm:ss tt"
        
        # 尝试读取当前设置
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\International",
                0, winreg.KEY_READ
            ) as key:
                self.current_format = winreg.QueryValueEx(key, "sTimeFormat")[0]
                # 备份原始值
                self.reg_backup = {
                    "sShortTime": winreg.QueryValueEx(key, "sShortTime")[0],
                    "sTimeFormat": self.current_format
                }
        except:
            self.current_format = "无法获取当前格式"
    
    def init_macos(self):
        self.format_tip = "macOS格式: HH:mm (24小时), h:mm a (12小时)\n例如: HH:mm:ss, h:mm:ss a"
        
        # 尝试读取当前设置
        try:
            result = subprocess.run(
                ['defaults', 'read', 'com.apple.menuextra.clock'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                plist_data = result.stdout
                self.plist_backup = plist_data
                
                # 解析plist数据
                if "DateFormat" in plist_data:
                    for line in plist_data.splitlines():
                        if "DateFormat" in line:
                            self.current_format = line.split('"')[1]
                            break
                else:
                    self.current_format = "默认格式"
            else:
                self.current_format = "无法获取当前格式"
        except:
            self.current_format = "无法获取当前格式"
    
    def init_linux(self):
        self.format_tip = "Linux格式: %H:%M (24小时), %I:%M %p (12小时)\n例如: %H:%M:%S, %I:%M:%S %p"
        
        # 尝试读取当前设置
        try:
            result = subprocess.run(
                ['gsettings', 'get', 'org.gnome.desktop.interface', 'clock-format'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.current_format = result.stdout.strip().strip("'")
            else:
                self.current_format = "无法获取当前格式"
        except:
            self.current_format = "无法获取当前格式"
    
    def apply_settings(self, format_type, custom_format=""):
        if self.os_type == "Windows":
            return self.apply_windows(format_type, custom_format)
        elif self.os_type == "Darwin":
            return self.apply_macos(format_type, custom_format)
        elif self.os_type == "Linux":
            return self.apply_linux(format_type, custom_format)
        return False
    
    def apply_windows(self, format_type, custom_format):
        try:
            # 需要管理员权限
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "需要管理员权限"
            
            key_path = r"Control Panel\International"
            
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0, winreg.KEY_WRITE
            ) as key:
                if format_type == "12h":
                    winreg.SetValueEx(key, "sShortTime", 0, winreg.REG_SZ, "h:mm tt")
                    winreg.SetValueEx(key, "sTimeFormat", 0, winreg.REG_SZ, "h:mm:ss tt")
                elif format_type == "24h":
                    winreg.SetValueEx(key, "sShortTime", 0, winreg.REG_SZ, "HH:mm")
                    winreg.SetValueEx(key, "sTimeFormat", 0, winreg.REG_SZ, "HH:mm:ss")
                else:  # custom
                    if not custom_format:
                        return False, "请输入自定义格式"
                    winreg.SetValueEx(key, "sShortTime", 0, winreg.REG_SZ, custom_format)
                    winreg.SetValueEx(key, "sTimeFormat", 0, winreg.REG_SZ, custom_format)
            
            # 通知系统设置改变
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "International", 0x0002, 5000, None
            )
            return True, "设置已生效，可能需要注销后重新登录才能看到变化"
        except PermissionError:
            return False, "没有写入注册表的权限"
        except Exception as e:
            return False, f"注册表操作失败: {str(e)}"
    
    def apply_macos(self, format_type, custom_format):
        try:
            # 创建临时plist文件
            temp_dir = tempfile.mkdtemp()
            plist_path = os.path.join(temp_dir, "clock.plist")
            
            # 构建plist内容
            if format_type == "12h":
                format_str = "h:mm a"
            elif format_type == "24h":
                format_str = "HH:mm"
            else:  # custom
                if not custom_format:
                    return False, "请输入自定义格式"
                format_str = custom_format
            
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DateFormat</key>
    <string>{format_str}</string>
    <key>FlashDateSeparators</key>
    <false/>
    <key>IsAnalog</key>
    <false/>
</dict>
</plist>"""
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            # 应用设置
            subprocess.run(['defaults', 'import', 'com.apple.menuextra.clock', plist_path], check=True)
            
            # 重启菜单栏
            subprocess.run(['killall', 'SystemUIServer'], check=True)
            
            return True, "设置已生效，菜单栏时钟已更新"
        except subprocess.CalledProcessError as e:
            return False, f"命令执行失败: {str(e)}"
        except Exception as e:
            return False, f"设置失败: {str(e)}"
    
    def apply_linux(self, format_type, custom_format):
        try:
            if format_type == "12h":
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.desktop.interface', 'clock-format', '12h'],
                    check=True
                )
            elif format_type == "24h":
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.desktop.interface', 'clock-format', '24h'],
                    check=True
                )
            else:  # custom
                if not custom_format:
                    return False, "请输入自定义格式"
                
                # 使用Clock Override扩展
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.shell.extensions.clock-override', 'custom-format', f"'{custom_format}'"],
                    check=True
                )
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.shell.extensions.clock-override', 'enabled', 'true'],
                    check=True
                )
            
            return True, "设置已应用，可能需要重新登录生效"
        except subprocess.CalledProcessError as e:
            return False, f"命令执行失败: {str(e)}"
        except FileNotFoundError:
            return False, "未找到gsettings命令，请确保在GNOME桌面环境中运行"
        except Exception as e:
            return False, f"设置失败: {str(e)}"
    
    def restore_default(self):
        if self.os_type == "Windows":
            return self.restore_windows()
        elif self.os_type == "Darwin":
            return self.restore_macos()
        elif self.os_type == "Linux":
            return self.restore_linux()
        return False
    
    def restore_windows(self):
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "需要管理员权限"
            
            key_path = r"Control Panel\International"
            
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                key_path,
                0, winreg.KEY_WRITE
            ) as key:
                if "sShortTime" in self.reg_backup and "sTimeFormat" in self.reg_backup:
                    winreg.SetValueEx(key, "sShortTime", 0, winreg.REG_SZ, self.reg_backup['sShortTime'])
                    winreg.SetValueEx(key, "sTimeFormat", 0, winreg.REG_SZ, self.reg_backup['sTimeFormat'])
                else:
                    # 尝试恢复默认值
                    winreg.SetValueEx(key, "sShortTime", 0, winreg.REG_SZ, "HH:mm")
                    winreg.SetValueEx(key, "sTimeFormat", 0, winreg.REG_SZ, "HH:mm:ss")
            
            # 通知系统设置改变
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "International", 0x0002, 5000, None
            )
            return True, "已恢复默认设置"
        except Exception as e:
            return False, f"恢复失败: {str(e)}"
    
    def restore_macos(self):
        try:
            # 恢复备份或默认值
            if self.plist_backup:
                temp_dir = tempfile.mkdtemp()
                plist_path = os.path.join(temp_dir, "clock_backup.plist")
                
                with open(plist_path, 'w') as f:
                    f.write(self.plist_backup)
                
                subprocess.run(['defaults', 'import', 'com.apple.menuextra.clock', plist_path], check=True)
            else:
                # 删除自定义设置
                subprocess.run(['defaults', 'delete', 'com.apple.menuextra.clock', 'DateFormat'], check=True)
            
            # 重启菜单栏
            subprocess.run(['killall', 'SystemUIServer'], check=True)
            return True, "已恢复默认设置"
        except Exception as e:
            return False, f"恢复失败: {str(e)}"
    
    def restore_linux(self):
        try:
            # 恢复默认设置
            subprocess.run(
                ['gsettings', 'reset', 'org.gnome.desktop.interface', 'clock-format'],
                check=True
            )
            
            # 禁用Clock Override扩展
            subprocess.run(
                ['gsettings', 'set', 'org.gnome.shell.extensions.clock-override', 'enabled', 'false'],
                check=True
            )
            return True, "已恢复默认设置"
        except Exception as e:
            return False, f"恢复失败: {str(e)}"

class TimeFormatChanger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 初始化系统设置
        self.settings = SystemSettings()
        
        # 设置UI初始状态
        self.ui.lineEdit.setVisible(False)
        # 添加语言状态变量 (zh/en)
        self.current_language = "zh"
        self.update_ui_language()
        
        # 连接信号槽
        self.ui.radio_custom.toggled.connect(self.toggle_custom_input)
        self.ui.btn_confirm.clicked.connect(self.apply_settings)
        self.ui.btn_cancel.clicked.connect(self.close)
        self.ui.btn_restore.clicked.connect(self.restore_default)
        # 添加语言按钮点击事件
        self.ui.btn_language.clicked.connect(self.toggle_language)
        
        # 根据当前格式设置单选按钮
        if "12" in self.settings.current_format or "tt" in self.settings.current_format or "a" in self.settings.current_format:
            self.ui.radio_12h.setChecked(True)
        elif "24" in self.settings.current_format or "HH" in self.settings.current_format:
            self.ui.radio_24h.setChecked(True)

    # 添加语言切换功能
    def toggle_language(self):
        """切换界面语言"""
        if self.current_language == "zh":
            self.current_language = "en"
        else:
            self.current_language = "zh"
        self.update_ui_language()
    
    def update_ui_language(self):
        """根据当前语言更新界面文本"""
        if self.current_language == "zh":
            self.setWindowTitle("时间格式设置工具")
            self.ui.groupBox.setTitle("时间显示格式")
            self.ui.radio_12h.setText("12小时制 (上午/下午)")
            self.ui.radio_24h.setText("24小时制")
            self.ui.radio_custom.setText("自定义格式")
            self.ui.lineEdit.setPlaceholderText("输入自定义格式")
            self.ui.label_format_tip.setText(self.settings.format_tip)
            self.ui.groupBox_2.setTitle("系统状态")
            self.ui.label_status.setText(f"当前系统: {platform.system()} {platform.release()}")
            self.ui.label_current_format.setText(f"当前时间格式: {self.settings.current_format}")
            self.ui.btn_confirm.setText("应用设置")
            self.ui.btn_cancel.setText("取消")
            self.ui.btn_restore.setText("恢复默认")
            self.ui.btn_language.setText("English")
        else:  # English
            self.setWindowTitle("Time Format Setting Tool")
            self.ui.groupBox.setTitle("Time Display Format")
            self.ui.radio_12h.setText("12-hour (AM/PM)")
            self.ui.radio_24h.setText("24-hour")
            self.ui.radio_custom.setText("Custom Format")
            self.ui.lineEdit.setPlaceholderText("Enter custom format")
            self.ui.label_format_tip.setText(self.settings.format_tip)
            self.ui.groupBox_2.setTitle("System Status")
            self.ui.label_status.setText(f"Current System: {platform.system()} {platform.release()}")
            self.ui.label_current_format.setText(f"Current Time Format: {self.settings.current_format}")
            self.ui.btn_confirm.setText("Apply Settings")
            self.ui.btn_cancel.setText("Cancel")
            self.ui.btn_restore.setText("Restore Default")
            self.ui.btn_language.setText("中文")
    
    def toggle_custom_input(self, checked):
        self.ui.lineEdit.setVisible(checked)

    def apply_settings(self):
        if self.ui.radio_12h.isChecked():
            format_type = "12h"
            custom_format = ""
        elif self.ui.radio_24h.isChecked():
            format_type = "24h"
            custom_format = ""
        else:  # custom
            format_type = "custom"
            custom_format = self.ui.lineEdit.text()
        
        success, message = self.settings.apply_settings(format_type, custom_format)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.close()
        else:
            QMessageBox.critical(self, "错误", message)

    def restore_default(self):
        success, message = self.settings.restore_default()
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.close()
        else:
            QMessageBox.critical(self, "错误", message)

# Windows UAC处理
def is_admin_windows():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    # Windows UAC处理
    if platform.system() == "Windows":
        if not is_admin_windows():
            # 重新启动并请求管理员权限
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(['"{}"'.format(arg) for arg in sys.argv]),
                None,
                1
            )
            sys.exit(0)
    
    app = QApplication(sys.argv)
    window = TimeFormatChanger()
    window.show()
    sys.exit(app.exec())