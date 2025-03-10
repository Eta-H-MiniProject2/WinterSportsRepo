# importing pandas 
import pandas as pd 
  
# merging two csv files 
helsinki_radiation_df = pd.concat( 
    map(pd.read_csv, ['Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2014 - 10.3.2015_4c8360ac-a85b-415a-bc87-e95b0eeb249c.csv', 'Kumpula Solar Radiation\Helsinki Kumpula_ 10.3.2015 - 10.3.2016_b62b5db1-d784-465e-809d-dd5c63fb7f6c.csv', 'Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2016 - 10.3.2017_6e994a96-7922-466a-b26d-d55868ca488d.csv', 'Kumpula Solar Radiation\Helsinki Kumpula_ 10.3.2017 - 10.3.2018_52ef618e-c727-45b0-a4d4-b4cf2cfef1ae.csv', 'Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2018 - 10.3.2019_1738e6a8-e42e-4f15-b3d4-e1870efef1c0.csv', 'Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2019 - 10.3.2020_90909a4d-e736-4eb2-bc03-5a18a0a97c7e.csv', 'Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2020 - 10.3.2021_dd473254-c8ef-485e-aee3-2e6c7e6ee2bb.csv', 'Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2021 - 10.3.2022_7a574a4f-46d5-463e-929b-9881fe2bbd3e.csv', 'Kumpula Solar Radiation/Helsinki Kumpula_ 10.3.2022 - 10.3.2023_6ccb6ba1-e6a0-4e06-8506-0506509cc2dc.csv', 'Kumpula Solar Radiation\Helsinki Kumpula_ 10.3.2023 - 10.3.2024_f94298f1-dca9-4a52-ba9e-4239b8d81db7.csv']), ignore_index=True) 
print(helsinki_radiation_df)

helsinki_radiation_df.to_csv('helsinki_radiation_all')