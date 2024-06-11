import netCDF4 as nc
import pandas as pd
import glob
import os
import numpy as np

# 指定.nc文件的目录路径
nc_files_path = r'Dataset\01\02\*.nc'

# 初始化一个空的DataFrame来存储提取的数据
data_frame = pd.DataFrame()

# 遍历文件夹中的所有.nc文件
for file_path in glob.glob(nc_files_path):
    # 使用netCDF4打开.nc文件
    dataset = nc.Dataset(file_path)
    
    file_name = os.path.basename(file_path)
    
    # 初始化字典来收集数据
    data = {
        'file_name': file_name,
        'storm_speed': None,
        'central_min_pressure': None,
        'storm_latitude': None,
        'basin': None,
        'ERA5_time': None,
        'time': None,
        'intensity': None
    }
    
    # 定义一个辅助函数来安全地提取数组中的第一个元素
    def get_first_item(key, group):
        if key in dataset[group].variables:
            return dataset[group].variables[key][:][0] if dataset[group].variables[key][:].size > 0 else None
        else:
            return None
    
    # 为每个特征提取数据，如果数据缺失则留空
    data['storm_speed'] = get_first_item('storm_speed', 'overpass_storm_metadata')
    data['central_min_pressure'] = get_first_item('central_min_pressure', 'overpass_storm_metadata')
    data['storm_latitude'] = get_first_item('storm_latitude', 'overpass_storm_metadata')
    data['basin'] = get_first_item('basin', 'overpass_metadata')
    data['ERA5_time'] = get_first_item('ERA5_time', 'overpass_metadata')
    data['time'] = get_first_item('time', 'overpass_storm_metadata')
    data['intensity'] = get_first_item('intensity', 'overpass_storm_metadata')
    
    # 创建一个DataFrame来存储每个文件的数据
    file_data = pd.DataFrame([data])
    
    # 将当前文件的数据添加到主DataFrame
    data_frame = pd.concat([data_frame, file_data], ignore_index=True)

    # 关闭文件
    dataset.close()

# 保存DataFrame到CSV文件
# data_frame.replace('--', np.nan, inplace=True)
# data_frame.replace('', np.nan, inplace=True)
data_frame.to_csv('output_train.csv', index=True)

print("数据已成功保存到 output_train.csv")



