import os
from dotenv import load_dotenv
import customtkinter as ctk
import requests
from PIL import Image, ImageTk

load_dotenv()

ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Weather")
root.geometry("500x500+600+300")
root.resizable(False, False)
root.iconbitmap("icon.ico")

is_selected_city = False
selected_city = None
return_button = None
temperature = None  # Declare temperature as a global variable
all_custom_tkinter_data = []

degrees = {
    "N": list(range(360 - 23, 361)) + list(range(0, 23)),
    "NE": list(range(23, 23 + 46)),
    "E": list(range(90 - 22, 90 + 23)),
    "SE": list(range(113, 113 + 46)),
    "S": list(range(180 - 22, 180 + 23)),
    "SW": list(range(203, 203 + 46)),
    "W": list(range(270 - 22, 270 + 23)),
    "NW": list(range(293, 293 + 46)),
}


def select_city():
    global selected_city, is_selected_city, return_button, temperature, custom_tkinter_data

    for x in all_custom_tkinter_data:
        x.destroy()

    def on_choose():
        global selected_city, is_selected_city
        selected_city = city_entry.get()
        city_entry.destroy()
        on_choose_button.destroy()
        is_selected_city = True
        show_weather()

    def check_entry_content(event):
        if city_entry.get():
            on_choose_button.configure(state="normal")
        else:
            on_choose_button.configure(state="disabled")

    city_entry = ctk.CTkEntry(
        root,
        placeholder_text="Enter City",
        width=150,
        height=50,
        font=ctk.CTkFont(size=20),
    )
    city_entry.place(relx=0.5, rely=0.35, anchor="center")

    on_choose_button = ctk.CTkButton(
        root,
        text="Choose City",
        command=on_choose,
        corner_radius=50,
        width=15,
        height=40,
        state="disabled",
    )
    on_choose_button.place(relx=0.5, rely=0.5, anchor="center")

    city_entry.bind("<KeyRelease>", check_entry_content)


def hide_return_button():
    global return_button
    if return_button is not None:
        return_button.destroy()


def show_weather():
    global selected_city, return_button, temperature, all_custom_tkinter_data
    city = selected_city
    api = os.getenv("API")
    url1 = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api}'
    response1 = requests.get(url1)
    url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&cnt=5&appid={api}'
    response2 = requests.get(url2)

    if response1.status_code == 200:
        weather_data = response1.json()
        weather_data2 = response2.json()
        print(weather_data)
        print(weather_data2)

        city_name = ctk.CTkLabel(
            root,
            text=weather_data['name'],
            font=ctk.CTkFont(size=30),
        )
        all_custom_tkinter_data.append(city_name)
        city_name.place(relx=0.3, rely=0.09, anchor="center")

        # temperature
        temperature_info = f"{weather_data['main']['temp']:.1f}°C"
        temperature = ctk.CTkLabel(
            root,
            text=temperature_info,
            font=ctk.CTkFont(size=30)
        )
        all_custom_tkinter_data.append(temperature)
        temperature.place(relx=0.3, rely=0.18, anchor="center")

        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"

        image = Image.open(requests.get(icon_url, stream=True).raw)
        new_width = int(image.width * 1.5)
        new_height = int(image.height * 1.5)
        resized_image = image.resize((new_width, new_height))
        icon_image = ImageTk.PhotoImage(resized_image)

        # icon
        weather_icon_label = ctk.CTkLabel(
            root,
            image=icon_image,
            text="",
        )
        all_custom_tkinter_data.append(weather_icon_label)
        weather_icon_label.image = icon_image
        weather_icon_label.place(relx=0.1, rely=0.21, anchor="center")

        # weather
        weather_type_info = weather_data['weather'][0]['main']
        weather_type = ctk.CTkLabel(
            root,
            text=weather_type_info,
            font=ctk.CTkFont(size=30)
        )
        all_custom_tkinter_data.append(weather_type)
        weather_type.place(relx=0.3, rely=0.3, anchor="center")

        # wind
        wind_speed_info = f"{weather_data['wind']['speed']:.1f} m/s"
        wind_direction_info = weather_data['wind']['deg']
        for key, value in degrees.items():
            if wind_direction_info in value:
                wind_direction_info = key
                break

        wind_direction = ctk.CTkLabel(
            root,
            text=f"Wind: {wind_direction_info}  {wind_speed_info}",
            font=ctk.CTkFont(size=25)
        )
        all_custom_tkinter_data.append(wind_direction)
        wind_direction.place(relx=0.75, rely=0.3, anchor="center")

        # forecast
        place = 1
        for index, x in enumerate(weather_data2['list']):
            forecast_info = f"{x['main']['temp']:.1f}°C"
            forecast = ctk.CTkLabel(
                root,
                text=forecast_info,
                font=ctk.CTkFont(size=30)
            )
            all_custom_tkinter_data.append(forecast)
            forecast.place(relx=0.26, rely=0.4 + place * 0.09, anchor="center")

            current_icon_code = x['weather'][0]['icon']
            current_icon_url = f"http://openweathermap.org/img/w/{current_icon_code}.png"
            current_icon = Image.open(requests.get(current_icon_url, stream=True).raw)
            current_icon = ImageTk.PhotoImage(current_icon)
            weather_current_icon_label = ctk.CTkLabel(
                root,
                image=current_icon,
                text="",
            )
            all_custom_tkinter_data.append(weather_current_icon_label)
            weather_current_icon_label.image = current_icon
            weather_current_icon_label.place(relx=0.42, rely=0.4 + place * 0.09, anchor="center")

            x['dt_txt'] = x['dt_txt'].split(' ')[1]
            time = ctk.CTkLabel(
                root,
                text=x['dt_txt'],
                font=ctk.CTkFont(size=20)
            )
            all_custom_tkinter_data.append(time)
            time.place(relx=0.6, rely=0.4 + place * 0.09, anchor="center")

            current_wind_speed_info = f"{x['wind']['speed']:.1f} m/s"
            current_wind_direction_info = x['wind']['deg']

            for k, v in degrees.items():
                if current_wind_direction_info in v:
                    current_wind_direction_info = k
                    break

            current_wind_speed = ctk.CTkLabel(
                root,
                text=f"{current_wind_direction_info} {current_wind_speed_info}",
                font=ctk.CTkFont(size=20)
            )
            all_custom_tkinter_data.append(current_wind_speed)
            current_wind_speed.place(relx=0.8, rely=0.4 + place * 0.09, anchor="center")
            place += 1

        return_button = ctk.CTkButton(
            root,
            text="Other city",
            command=choose_other_city,
        )
        all_custom_tkinter_data.append(return_button)
        return_button.place(relx=0.85, rely=0.2, anchor="center")

    else:
        hide_return_button()
        select_city()


def choose_other_city():
    global is_selected_city, return_button, temperature
    is_selected_city = False
    select_city()


def dark_mode():
    if switch_button.get():
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")


switch_button = ctk.CTkSwitch(
    root,
    text="Dark Mode",
    command=dark_mode,
    onvalue=True,
    offvalue=False,
)
switch_button.place(relx=0.85, rely=0.1, anchor="center")
ctk.set_appearance_mode("light")

if not is_selected_city:
    select_city()

root.mainloop()
