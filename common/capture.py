import subprocess
import shlex
from pathlib import Path

class AdbCmd:
    def __init__(self, device_id=None):
        self.device_id = device_id

    def _base_cmd(self):
        if self.device_id:
            return f"adb -s {self.device_id}"
        return "adb"

    def _run(self, cmd, check=True, capture_output=True, text=True):
        full = f"{self._base_cmd()} {cmd}"
        result = subprocess.run(
            shlex.split(full),
            check=check,
            capture_output=capture_output,
            text=text
        )
        return result

    def devices(self):
        return self._run("devices").stdout.strip()

    def dump_ui(self, remote_path="/sdcard/uidump.xml"):
        self._run(f"shell uiautomator dump {remote_path}")
        return self.pull(remote_path)

    def pull(self, remote_path, local_path=None):
        if local_path is None:
            local_path = Path.cwd() / Path(remote_path).name
        self._run(f"pull {remote_path} {local_path}")
        return Path(local_path).resolve()

    def screenshot(self, remote_path="/sdcard/screen.png", local_path=None):
        self._run(f"shell screencap -p {remote_path}")
        return self.pull(remote_path, local_path)

    def install(self, apk_path):
        return self._run(f"install {apk_path}").stdout

    def uninstall(self, package_name):
        return self._run(f"uninstall {package_name}").stdout

    def shell(self, cmd):
        return self._run(f"shell {cmd}").stdout
    
    def tap(self, x, y):
        return self.shell(f"input tap {x} {y}")
        #x = 593, y = 2370
    
    def pull_file(self, remote_path, local_path):
        return self.pull(remote_path, local_path)
    
    #/sdcard/DCIM/Camera ---> C:\Users\jianjialin1\Documents\Test\L_OpenCV\common\Camera

    def start_app(self, package_name, activity_name):
        return self.shell(f"am start -n {package_name}/{activity_name}")
    
    def delete_files(self, remote_path):
        # 使用 rm -rf 删除所有文件，忽略不存在的错误
        return self.shell(f"rm -rf {remote_path}")
    
    def get_img_name(self, remote_path):
        """获取远程路径下最新的图片文件名"""
        # 列出目录下所有文件，按修改时间排序，取最新的
        result = self.shell(f"ls -t {remote_path} | head -n 1")
        return result.strip()

    def get_all_img_names(self, remote_path):
        """获取远程路径下所有图片文件名"""
        result = self.shell(f"ls {remote_path}")
        return [f.strip() for f in result.split('\n') if f.strip()]

    def get_img_names_by_ext(self, remote_path, ext=".jpg"):
        """获取指定扩展名的图片"""
        result = self.shell(f"ls {remote_path}/*{ext}")
        return [Path(f.strip()).name for f in result.split('\n') if f.strip()]

# 使用
# adb = AdbCmd()
# print(adb.devices())
# ui_xml = adb.dump_ui()
# print("ui xml file", ui_xml)