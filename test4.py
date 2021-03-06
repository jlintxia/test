"""
@Date    : 2021-09-07
@Author  : liyachao
"""
import time
import pymysql.cursors
import tidevice
from ios_device import py_ios_device
from ios_device.py_ios_device import PyiOSDevice
from tidevice import Device

app_bundle_id = "com.XXXXX" #测试iOS应用包名
device_id="000-0XXXX0XXXXXX"#测试设备ID

def callback_fps(res):
  print('FPS打印',res)
  #fps数据
  ss=str(res)
  fps_test=ss.split("'FPS':")[1].split(".")[0]
  jank_test=ss.split("'jank':")[1].split(",")[0]
  big_jank=ss.split("'big_jank':")[1].split(",")[0]
  stutter=ss.split("'stutter':")[1][0:5].split("}")[0]
# 数据存数据库连接数据库
  connect = pymysql.Connect(
  host='10XXXXXX',
  port=3306,
  user='root',
  passwd='AXXX',
  db='test',
  charset='utf8'
  )
   # 获取游标
  cursor = connect.cursor()
  sql = "INSERT INTO my_fps (fps,jank,big_jank,stutter) VALUES('"+fps_test+"','"+jank_test+"','"+big_jank+"','"+stutter+"')"
  cursor.execute(sql)
  connect.commit()
   # 关闭连接
  cursor.close()
  connect.close()

def callback_gpu(res): 
  print('GPU打印',res) 
    #gpu数据
  ss=str(res)#转数据类型
  gpu_Device=ss.split("'Device Utilization %':")[1].split(",")[0]
  gpu_Renderer=ss.split("'Renderer Utilization %':")[1].split(",")[0]
  gpu_Tiler=ss.split("'Tiler Utilization %':")[1].split(",")[0]
     # 数据存数据库连接数据库
  connect = pymysql.Connect(
  host='10XXXX',
  port=3306,
  user='root',
  passwd='AXXX1',
  db='test',
  charset='utf8'
  )
   # 获取游标
  cursor = connect.cursor()
  sql = "INSERT INTO my_gpu (gpu_Device,gpu_Renderer,gpu_Tiler) VALUES('"+gpu_Device+"','"+gpu_Renderer+"','"+gpu_Tiler+"')"
  cursor.execute(sql)
  connect.commit()
  #print('GPU成功插入', cursor.rowcount, '条数据')
   # 关闭连接
  cursor.close()
  connect.close()

def test_get_myZtest():
    channel = py_ios_device.start_get_gpu(callback=callback_gpu)
    channel2 = py_ios_device.start_get_fps(callback=callback_fps)
    t = tidevice.Device(device_id)#iOS设备
    perf = tidevice.Performance(t,perfs=list(tidevice.DataType))
    def callback(_type: tidevice.DataType, value: dict):
        if _type.value == "cpu":
            print('CPU打印',value)
            ss=str(value)#转成str
            use_cpu=ss.split("'value':")[1][0:6].split("}")[0]
            sys_cpu=ss.split("'sys_value':")[1][0:7].split("}")[0]
            count_cpu=ss.split("'count':")[1].split("}")[0]
# 数据存数据库连接数据库
            connect = pymysql.Connect(
            host='10XXXX',
            port=3306,
            user='root',
            passwd='Axxxxx',
            db='test',
            charset='utf8'
            )
    # 获取游标
            cursor = connect.cursor()
            sql = "INSERT INTO my_cpu (use_cpu,sys_cpu,count_cpu) VALUES('"+use_cpu+"','"+sys_cpu+"','"+count_cpu+"')"
            cursor.execute(sql)
            connect.commit()
                # 关闭连接
            cursor.close()
            connect.close()
        if _type.value == "memory":
            print('内存打印',value)
            ss=str(value)
            memory=ss.split("'value':")[1][0:6].split("}")[0]
            # 数据存数据库连接数据库
            connect = pymysql.Connect(
            host='10XXXX',
            port=3306,
            user='root',
            passwd='AXXXXS',
            db='test',
            charset='utf8'
            )
    # 获取游标
            cursor = connect.cursor()
            sql = "INSERT INTO my_memory (memory) VALUES('"+memory+"')"
            cursor.execute(sql)
            connect.commit()
                # 关闭连接
            cursor.close()
            connect.close()
    perf.start(app_bundle_id, callback=callback)
    time.sleep(30) #测试时长
    perf.stop()
    py_ios_device.stop_get_gpu(channel)
    py_ios_device.stop_get_fps(channel2)
    channel.stop()
    channel2.stop()

if __name__ == "__main__":
     test_get_myZtest()