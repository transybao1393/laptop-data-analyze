# laptop-data-analyze
Laptop data analyze

## How to run
```console
macbook@johnny:~$ make setup
Conda env create...
Conda init shell...
Conda activate...
Pip install....
macbook@johnny:~$ make run
result type <class 'dict'>
                title    price      storage_capacity  review
0    Asus VivoBook X4   295.99             128GB SSD       1
1    Prestigio SmartB   299.00                  32GB       9
2    Prestigio SmartB   299.00                  32GB       9
3       Aspire E1-510   306.99                 500GB       2
4    Lenovo V110-15IA   321.94             128GB SSD       1
..                ...      ...                   ...     ...
112  Lenovo Legion Y7  1399.00   128GB SSD + 2TB HDD       1
113  Asus ROG Strix G  1399.00       1TB + 128GB SSD       1
114  Asus ROG Strix G  1769.00       256GB + 1TB HDD       1
115  Asus ROG Strix G  1769.00   256GB SSD + 1TB HDD       1
116  Asus ROG Strix S  1799.00  256GB SSD + 1TB SSHD       1

[117 rows x 4 columns]

laptop with max price
                 title   price      storage_capacity  review
116  Asus ROG Strix S  1799.0  256GB SSD + 1TB SSHD       1

laptop has max review
                 title    price storage_capacity  review
1    Prestigio SmartB   299.00             32GB       9
2    Prestigio SmartB   299.00             32GB       9
34     Dell Vostro 15   488.78        128GB SSD       9
36     Dell Vostro 15   497.17              1TB       9
44   Dell Inspiron 15   679.00              1TB       9
54   Dell Inspiron 15  1098.42        256GB SSD       9
58   Dell Latitude 52  1102.66        256GB SSD       9
59   Dell Latitude 54  1110.14            500GB       9
64   Dell Inspiron 17  1124.20              1TB       9
65   Dell Latitude 54  1133.82            500GB       9
69   Dell Latitude 54  1143.40        256GB SSD       9
70   Dell Inspiron 15  1144.20              1TB       9
71   Dell Latitude 55  1144.40        256GB SSD       9
77   Dell Latitude 55  1178.19        256GB SSD       9
80   Dell Latitude 54  1187.88        256GB SSD       9
90   Dell Latitude 54  1238.37        256GB SSD       9
95   Dell Latitude 54  1271.06              1TB       9
97        Dell XPS 13  1281.99        128GB SSD       9
100  Dell Latitude 54  1310.39        256GB SSD       9
104  Dell Latitude 55  1337.28        256GB SSD       9
105  Dell Latitude 54  1338.37        256GB SSD       9
106  Dell Latitude 55  1341.22        256GB SSD       9
```