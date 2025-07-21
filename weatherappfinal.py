import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from PIL.Image import Resampling
import requests
from datetime import datetime, timezone

# ===== Configuration =====
API_KEY = '459af2579b0884849cef1b7dcb8d93e2'

INDIAN_CITIES = sorted([
    "Agartala", "Agra", "Ahmedabad", "Aizawl", "Ajmer", "Amritsar", "Aurangabad", 
    "Bangalore", "Bareilly", "Bhopal", "Bhubaneswar", "Chandigarh", "Chennai", "Coimbatore", 
    "Cuttack", "Dehradun", "Delhi", "Durgapur", "Gangtok", "Goa", "Gorakhpur", "Guwahati", 
    "Gwalior", "Hyderabad", "Indore", "Itanagar", "Jaipur", "Jalandhar", "Jammu", "Jamshedpur", 
    "Jhansi", "Jodhpur", "Kanpur", "Kochi", "Kolhapur", "Kolkata", "Kozhikode", "Lucknow", 
    "Ludhiana", "Madurai", "Mangaluru", "Meerut", "Moradabad", "Mumbai", "Mysuru", "Nagpur", 
    "Nashik", "Noida", "Panaji", "Patna", "Port Blair", "Prayagraj", "Puducherry", "Pune", 
    "Raipur", "Rajkot", "Ranchi", "Rohtak", "Shimla", "Silchar", "Siliguri", "Srinagar", 
    "Surat", "Thane", "Thiruvananthapuram", "Tiruchirappalli", "Tirunelveli", "Udaipur", 
    "Vadodara", "Varanasi", "Vellore", "Vijayawada", "Visakhapatnam"
])

AQI_DESCRIPTION = {
    1: 'Good',
    2: 'Fair',
    3: 'Moderate',
    4: 'Poor',
    5: 'Very Poor'
}

# ===== Weather Function =====
def get_weather(city):
    try:
        current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric'
        current_data = requests.get(current_url).json()
        if 'coord' not in current_data:
            raise ValueError(current_data.get("message", "City not found"))

        lat = current_data['coord']['lat']
        lon = current_data['coord']['lon']
        temp = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        description = current_data['weather'][0]['description'].title()

        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={API_KEY}&units=metric'
        forecast_data = requests.get(forecast_url).json()
        today = datetime.now(timezone.utc).date()
        temps = [entry['main']['temp'] for entry in forecast_data['list']
                 if datetime.fromtimestamp(entry['dt'], timezone.utc).date() == today]
        min_temp = min(temps) if temps else temp
        max_temp = max(temps) if temps else temp

        air_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
        air_data = requests.get(air_url).json()
        aqi = air_data['list'][0]['main']['aqi']
        aqi_desc = AQI_DESCRIPTION.get(aqi, 'Unknown')

        result = f"""📍 City: {city}
🌤 Weather: {description}
🌡 Temperature: {temp}°C
🔻 Min Today: {min_temp:.1f}°C   🔺 Max Today: {max_temp:.1f}°C
💧 Humidity: {humidity}%
🌀 Air Quality: {aqi_desc} (AQI: {aqi})"""

        result_label.config(text=result)
        result_label.update_idletasks()
        result_label.place_configure(
            width=result_label.winfo_reqwidth() + 30,
            height=result_label.winfo_reqheight() + 20
        )
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve weather: {e}")

# ===== GUI Setup =====
root = tk.Tk()
root.title("🌞 India Weather App")
root.geometry("700x600")
root.resizable(False, False)

bg_image = Image.open(r"C:\Users\LENOVO\OneDrive\Desktop\python codes\pic1.jpg")  # Change path as needed
bg_image = bg_image.resize((700, 600), Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

header = tk.Label(root, text="India Weather App", font=("Helvetica", 22, "bold"),
                  bg="#DAA520", fg="#4B3621")
header.place(x=0, y=0, width=700, height=60)

city_frame = tk.Frame(root, bg="#F5F5DC")
city_frame.place(relx=0.5, y=90, anchor="center")

city_label = tk.Label(city_frame, text="Select City:", font=("Arial", 12), bg="#F5F5DC", fg="#4B3621")
city_label.pack(side="left", padx=(0, 10))

city_var = tk.StringVar()
city_dropdown = ttk.Combobox(city_frame, textvariable=city_var, values=INDIAN_CITIES,
                             state='readonly', font=("Arial", 12), width=28)
city_dropdown.current(0)
city_dropdown.pack(side="left")

search_button = tk.Button(root, text="Get Weather", font=("Arial", 12, "bold"),
                          bg="#DAA520", fg="#4B3621", width=15,
                          command=lambda: get_weather(city_var.get()))
search_button.place(relx=0.5, y=140, anchor="center")

result_label = tk.Label(root, text="", font=("Courier", 12),
                        bg="#FFF8DC", fg="#000000", justify="left", anchor="nw",
                        bd=2, relief="ridge", padx=10, pady=10)
result_label.place(relx=0.5, y=250, anchor="n")

root.mainloop()
