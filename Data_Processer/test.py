import h5netcdf

# 打开NetCDF文件
file_path = 'TCPRIMED_v01r00-final_AL012021_SSMIS_F18_059809_20210523203023.nc'
dataset = h5netcdf.File(file_path, 'r')

# 访问Group "passive_microwave"内的Group "S4"内的变量
passive_microwave_group = dataset['passive_microwave']
infrared_group = dataset['infrared']
s4_group = passive_microwave_group['S4']

# 提取变量数据
latitude_data = s4_group['latitude'][:]
longitude_data = s4_group['longitude'][:]
tb_91_665h_data = s4_group['TB_91.665H'][:]
x = infrared_group['x'][:]
latitude = infrared_group['latitude'][:]
longitude = infrared_group['longitude'][:]


# 打印数据的形状和类型
print(f"Latitude Data Shape: {latitude_data.shape}")
print(f"Longitude Data Shape: {longitude_data.shape}")
print(f"TB_91.665H Data Shape: {tb_91_665h_data.shape}")
print(f"x: {x.shape}")
print(f"latitude: {latitude.shape}")
print(f"latitude: {longitude.shape}")


# 输出部分数据
# print("Latitude Data (sample):", latitude_data)
print("Longitude Data (sample):", longitude_data)
# print("TB_91.665H Data (sample):", tb_91_665h_data)
# print(f"x: {x}")
# print(f"latitude: {latitude}")
print(f"longitude: {longitude}")



