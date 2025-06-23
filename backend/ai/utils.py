def calculate_pm25_aqi(pm25):
    bps = [(0.0,12.0,0,50),(12.1,35.4,51,100),(35.5,55.4,101,150),(55.5,150.4,151,200),(150.5,250.4,201,300),(250.5,500.4,301,500)]
    for c_lo,c_hi,i_lo,i_hi in bps:
        if c_lo <= pm25 <= c_hi:
            return round((i_hi - i_lo)/(c_hi - c_lo)*(pm25 - c_lo) + i_lo)
    return None

def calculate_pm10_aqi(pm10):
    bps = [(0,54,0,50),(55,154,51,100),(155,254,101,150),(255,354,151,200),(355,424,201,300),(425,604,301,500)]
    for c_lo,c_hi,i_lo,i_hi in bps:
        if c_lo <= pm10 <= c_hi:
            return round((i_hi - i_lo)/(c_hi - c_lo)*(pm10 - c_lo) + i_lo)
    return None

def calculate_no2_aqi(no2):
    bps = [(0,53,0,50),(54,100,51,100),(101,360,101,150),(361,649,151,200),(650,1249,201,300),(1250,2049,301,500)]
    for c_lo,c_hi,i_lo,i_hi in bps:
        if c_lo <= no2 <= c_hi:
            return round((i_hi - i_lo)/(c_hi - c_lo)*(no2 - c_lo) + i_lo)
    return None

def calculate_co_aqi(co):
    bps = [(0.0,4.4,0,50),(4.5,9.4,51,100),(9.5,12.4,101,150),(12.5,15.4,151,200),(15.5,30.4,201,300),(30.5,50.4,301,500)]
    for c_lo,c_hi,i_lo,i_hi in bps:
        if c_lo <= co <= c_hi:
            return round((i_hi - i_lo)/(c_hi - c_lo)*(co - c_lo) + i_lo)
    return None

def calculate_o3_aqi(o3):
    bps = [(0,54,0,50),(55,70,51,100),(71,85,101,150),(86,105,151,200),(106,200,201,300),(201,604,301,500)]
    for c_lo,c_hi,i_lo,i_hi in bps:
        if c_lo <= o3 <= c_hi:
            return round((i_hi - i_lo)/(c_hi - c_lo)*(o3 - c_lo) + i_lo)
    return None

def calculate_overall_aqi(pm25, pm10, no2, co, o3):
    aqi_list = [
        calculate_pm25_aqi(pm25),
        calculate_pm10_aqi(pm10),
        calculate_no2_aqi(no2),
        calculate_co_aqi(co),
        calculate_o3_aqi(o3)
    ]
    return max(filter(None, aqi_list))