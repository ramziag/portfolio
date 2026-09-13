from cenpy import products
import matplotlib.pyplot as plt

sanantonio = products.ACS(2019).from_place('San Antonio, TX', level='tract', variables=['B25091', 'B25070', 'B19013', 'B25003', 'B25002', 'B25001'])

print(sanantonio)
