import tkinter as tk
from tkinter import ttk
import serial
import time
import threading

# 기본 시리얼 설정
arduino = None
baud_rate = 9600

# 시리얼 포트 연결 함수
def connect_to_arduino():
    global arduino
    port = entry_port.get()  # 사용자가 입력한 포트 가져오기
    try:
        arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=1)
        time.sleep(2)  # 아두이노 초기화 시간 대기
        text_output.insert(tk.END, f"Connected to {port}\n")
        text_output.see(tk.END)
        
        thread = threading.Thread(target=read_from_arduino, daemon=True)
        thread.start()
    except serial.SerialException:
        arduino = None
        text_output.insert(tk.END, f"Failed to connect to {port}. Check your port.\n")
        text_output.see(tk.END)

# 시리얼 포트 닫기 함수
def disconnect_from_arduino():
    global arduino
    if arduino:
        arduino.close()
        arduino = None
        text_output.insert(tk.END, "Serial port closed.\n")
        text_output.see(tk.END)

# 아두이노로 데이터 전송
def send_to_arduino(command):
    if arduino:
        arduino.write(command.encode())  # 데이터를 바이트로 변환해 전송

# START_VOLTAGE 값 전송
def send_start_voltage():
    start_voltage = entry_start.get()  # 입력 필드에서 값 가져오기
    if start_voltage:  # 값이 비어 있지 않은 경우에만 전송
        send_to_arduino(f"START:{start_voltage}")

# END_VOLTAGE 값 전송
def send_end_voltage():
    end_voltage = entry_end.get()  # 입력 필드에서 값 가져오기
    if end_voltage:  # 값이 비어 있지 않은 경우에만 전송
        send_to_arduino(f"END:{end_voltage}")

# 내리기 버튼 클릭 처리
def lower_action():
    send_to_arduino("1")

# 올리기 버튼 클릭 처리
def raise_action():
    send_to_arduino("0")

# SHOW 버튼 클릭 처리
def show_action():
    send_to_arduino("SHOW")

# STOP 버튼 클릭 처리
def stop_action():
    send_to_arduino("STOP")

# 아두이노에서 데이터 읽기
def read_from_arduino():
    while True:
        if arduino and arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                text_output.insert(tk.END, f"{data}\n")
                text_output.see(tk.END)

# Tkinter GUI 설정
root = tk.Tk()
root.title("Brake Setting Program")
root.geometry("600x600")
root.configure(bg="#f5f5f5")

# 스타일 설정
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
style.configure("TButton", font=("Arial", 10))
style.configure("TEntry", font=("Arial", 10))

# Frame 생성
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# 시리얼 포트 설정 UI
label_port = ttk.Label(frame, text="Serial Port:")
label_port.grid(row=0, column=0, sticky=tk.W, pady=5)

entry_port = ttk.Entry(frame, width=20)
entry_port.grid(row=0, column=1, pady=5)

button_connect = ttk.Button(frame, text="Connect", command=connect_to_arduino)
button_connect.grid(row=0, column=2, padx=10, pady=5)

button_disconnect = ttk.Button(frame, text="Disconnect", command=disconnect_from_arduino)
button_disconnect.grid(row=0, column=3, padx=10, pady=5)

# START_VOLTAGE 입력 UI
label_start = ttk.Label(frame, text="START_VOLTAGE:")
label_start.grid(row=1, column=0, sticky=tk.W, pady=5)

entry_start = ttk.Entry(frame, width=20)
entry_start.grid(row=1, column=1, pady=5)

button_start = ttk.Button(frame, text="확인", command=send_start_voltage)
button_start.grid(row=1, column=2, padx=10, pady=5)

# END_VOLTAGE 입력 UI
label_end = ttk.Label(frame, text="END_VOLTAGE:")
label_end.grid(row=2, column=0, sticky=tk.W, pady=5)

entry_end = ttk.Entry(frame, width=20)
entry_end.grid(row=2, column=1, pady=5)

button_end = ttk.Button(frame, text="확인", command=send_end_voltage)
button_end.grid(row=2, column=2, padx=10, pady=5)

# 내리기 버튼
button_lower = ttk.Button(frame, text="DOWN", command=lower_action)
button_lower.grid(row=3, column=0, columnspan=4, pady=10, sticky=tk.EW)

# 올리기 버튼
button_raise = ttk.Button(frame, text="UP", command=raise_action)
button_raise.grid(row=4, column=0, columnspan=4, pady=10, sticky=tk.EW)

# SHOW 버튼
button_show = ttk.Button(frame, text="SHOW", command=show_action)
button_show.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.EW)

# STOP 버튼
button_stop = ttk.Button(frame, text="STOP", command=stop_action)
button_stop.grid(row=5, column=2, columnspan=2, pady=10, sticky=tk.EW)

# 시리얼 모니터 출력 UI
label_output = ttk.Label(frame, text="Arduino Monitor:")
label_output.grid(row=6, column=0, columnspan=4, sticky=tk.W, pady=10)

text_output = tk.Text(frame, height=15, width=60, font=("Courier", 10), bg="#ffffff", relief=tk.SOLID, borderwidth=1)
text_output.grid(row=7, column=0, columnspan=4, pady=5)

# GUI 실행
root.mainloop()

# 시리얼 포트 닫기
if arduino:
    arduino.close()
    print("Serial port closed.")
