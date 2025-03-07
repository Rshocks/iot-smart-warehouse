# IoT Simulator Setup Guide  

This project simulates real-time inventory tracking using AWS IoT Core and Python.  

---

## **Prerequisites**  
Before you start, ensure you have:  
- **Python 3+** installed  
- **pip** (Python package manager) installed  
- **AWS IoT Core credentials** (certificates & keys)  

---

## **Setup & Run**  

### **Create/Activate a Virtual Environment**  
To keep dependencies isolated, create/Activate a virtual environment:  

```sh
python -m venv venv
```
```sh
venv\Scripts\activate
```

### **Install Dependencies**
Once the virtual environment is activated, install the required dependencies:
```sh
pip install -r requirements.txt
```

### **Install Dependencies**
Once the virtual environment is activated, install the required dependencies:
```sh
pip install -r requirements.txt
```

### **Set Up Configuration**
Copy configTemplate.json and rename it config.json, then add your own endpoint/certs to the JSON file.