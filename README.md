# Đồ án tương tác dữ liệu trực quan - 2022
## Đề tài: Xây dựng Dashboard trực quan hoá dữ liệu các kì thi THPT QG 2019-2021

> 
    Nguyễn Thanh Sang   - 19133048
    Lê Thị Nhung        - 19133043


#### [Đánh giá các nhóm khác](#)

<!-- ## 1. Diagram 
![](./assets/pipeline.png) -->
## 1. Dịch vụ AWS được sử dụng
-   AWS RDS Potsgres:
    -   Store data
-   AWS EC2:
    -   Run Apache Superset and Demo

## 2. Framework sử dụng 
-   Apache Superset:
    - Trực quan hoá dự liệu, tạo dashboard
- Streamlit:
    - Tạo demo tương tác với Superset



## 2. Quy trình
### 2.1 Chuẩn bị dữ liệu
#### 2.1.1 Nguồn dữ liệu
Nguồn dữ liệu được lấy từ các web tra cứu điểm thi như VNPT, VN-Express

#### 2.1.2 Crawl dữ liệu
Sử dụng công cụ [bee-university](https://github.com/beecost/bee-university)

#### 2.1.3 Tiền xử lý dữ liệu
##### 2.1.3.1 Chuyển dataset được crawl về format dataframe
```python
for i in tqdm(dataset.iloc):
    year = i['schoolYear']
    student_code = i['studentCode']
    subject = ['TOAN', 'VAN', 'LY', 'HOA', 'SINH', 'SU',\
       'DIA', 'GDCD', 'NGOAINGU']
    
    for sub in subject:
        note = ''
        if sub == 'NGOAINGU':
            note = i['CODE_NGOAINGU']
            score = i[sub]
        json_data = {
            "year" : year,
            "student_code" : student_code,
            "subject" : sub,
            "point" : i[sub],
            "city" : int(str(student_code)[:2])
        }
        
        data.append(json_data)

dataset['city'] = dataset['studentCode'].map(lambda x:str(x)[:2])
```
##### 2.1.3.4 Tạo PostgreDB sử dụng AWS RDS

##### 2.1.3.5 Upload dataset lên RDS
```python
endpoint = ""
username = ""
password = ""
database = ""

conection_str = f"postgresql://{username}:{password}@{endpoint}/{database}"

from sqlalchemy import create_engine
engine = create_engine('')
data.to_sql('diemthi', engine)
```

### 2.2 Superset
#### 2.2.1 Cài đặt Docker
follow this [guideline]()
#### 2.2.2 Cài đặt Superset
```bash
git clone https://github.com/apache/superset.git

cd superset

docker-compose -f docker-compose-non-dev.yml pull

docker-compose -f docker-compose-non-dev.yml up
```
### 2.3 Enable Jinja

Trong file **superset/docker/pythonenv_dev/superset_config.py**

```python 
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING" = True 
}
```
### 2.3 Enable public access
Trong file **superset/docker/pythonenv_dev/superset_config.py**

```python
PUBLIC_ROLE_LIKE_GAMMA = True
PUBLIC_ROLE_LIKE_ALPHA = True
SQLLAB_CTAS_NO_LIMIT = True
PUBLIC_ROLE_LIKE: Optional[str] = "Gamma"
SESSION_COOKIE_SAMESITE=None
```



### 2.3 Dashboard trên Superset
![](./assets/dashboard.gif)

### 2.4 Superset API 
#### 2.4.1 Define superset host, username and password in .env
```py
SUPPERSET_USERNAME="admin"
SUPPERSET_PASSWORD="admin"
SUPPERSET_HOST="http://54.237.126.11:8088/api/v1/"
```
#### 2.4.1 Get access token
```python
    def get_access_token(self):
        payload = {
            "username" : self.username,
            "password" : self.password,
            "provider" : "db"
        }

        r = requests.post(self.host + "/security/login", json=payload)
        access_token = r.json()['access_token']

        return {"Authorization": f"Bearer {access_token}"}
```

#### 2.4.1 Get dashboard json
```py
    
    def get_dashboard(self, id):
        endpoint = f"{self.host}dashboard/{id}"

        return requests.get(endpoint, headers=self.access_token).json()
    
```