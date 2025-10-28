# Flink WordCount Stream Project

This project demonstrates a simple **Flink streaming application** that counts words from a TCP socket.

---

## How to Start the Project

### 1. Start a Listener
Open a PowerShell terminal and run:

```powershell
ncat -lk 9999
```

- `-l` → listen mode  
- `-k` → keep the listener alive after each connection  
- `9999` → port number  

To verify the listener is running:

```powershell
netstat -ano | findstr :9999
```

You should see a line showing that port `9999` is listening.

---

### 2. Start the Flink Application
1. Open a terminal at the project folder:

```
D:\Data_Projects\Flink_wordcount
```

2. Run the application:

```powershell
java -jar target/Flink_wordcount-1.0-SNAPSHOT.jar
```

The Flink job will start and wait for input from the TCP listener.

---

### 3. Type Words in the Listener
- Switch to the PowerShell terminal running:

```powershell
ncat -lk 9999
```

- Type any words you want, then press **Enter**.  
- The Flink application will process the words and print word counts every 5 seconds.

---

### 4. Stop the Application
- Press **Ctrl+C** in the Flink terminal to stop the job.  
- Press **Ctrl+C** in the ncat terminal to stop the listener.

---
### 5. View Results
- Results can be viewed in Demo.png
---

### Notes
- Make sure you have **Java 19** installed.  
- Ensure **ncat** is installed and available in your PATH.  
- This project uses **Flink 1.18.1** and Maven for building.