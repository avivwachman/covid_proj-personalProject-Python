__author__ = "Aviv Wachman"

import tkinter as tk
import requests
import json
import time
import datetime as dt


def get_part_of_day(hour):
    """Gets an int representing an hour and returns The time of day as a String"""

    return (
        "Morning" if 5 <= hour <= 11
        else
        "Afternoon" if 12 <= hour <= 17
        else
        "Evening" if 18 <= hour <= 22
        else
        "Night"
    )


def set_visual():
    """Builds Creates the main and secondary canvases and adds the clock and greeting message """

    global master  # main window
    main_window = tk.Canvas(master, bg='white', height=800, width=800)
    secondary_wind = tk.Canvas(main_window, bg='white', cursor='circle', height=200, width=200)
    clock = tk.Label(secondary_wind, font=("Arial", 30, 'bold'), bg="black", fg="PaleGreen3", bd=30)
    clock.pack()
    now = dt.datetime.now()
    part_day = get_part_of_day(now.hour)
    time_from_day_greet = tk.Label(secondary_wind, text=f"Good {part_day}!", font=("Montserrat", 22))
    time_from_day_greet.pack()
    secondary_wind.grid(column=3)

    def run():
        """Changes the Time on the clock every 990 millisecond"""

        text_input = time.strftime("%H:%M")  # gets formatted string and returns by it
        clock.config(text=text_input)  # add text
        clock.after(990, run)  # every 200 millisecond, can try 55,000

    run()
    return main_window


def human_format(num):
    """Gets a number and formats the number to a String that is easier to read"""

    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def init():
    """ Api call for the COVID-19 info and returns a list of dictionaries """

    global url
    r = requests.get(url, params={'token': 'APIkeyHERE'})
    return json.loads(r.text)


def dash_visual(states, calan):
    """Creates the visual representation of the COVID-19 info """

    not_state_lst = ['Veteran Affair', 'Federal Bureau of Prisons', 'US Military', 'Northern Mariana Islands',
                     'Wuhan Evacuee', 'US Virgin Islands', 'Diamond Princess', 'Guam', 'Grand Princess']
    global canvi
    summer_death = 0
    summer_case = 0
    i = 0
    j = 0
    for state in states:
        if j % 7 == 0:
            i = i + 1
            j = 0
        summer_death += int(state['death'])
        summer_case += int(state['case'])
        frame = tk.Frame(
            master=canvi,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        count = 0
        for info_title in state:
            if count == 0:
                # add if state[info_title] is in list of none states write territory
                if state[info_title] in not_state_lst:
                    label = tk.Label(master=frame, text=f"Other: {state[info_title]}",
                                     font=("Montserrat", 18, 'bold'),
                                     fg='#559364')
                else:
                    label = tk.Label(master=frame, text=f"{info_title.title()}: {state[info_title]}",
                                     font=("Montserrat", 18, 'bold'), fg='#559364')
                label.pack()
                count = count + 1
                continue
            if count < 3:
                label = tk.Label(master=frame, text=f"{info_title.title()}s : {human_format(int(state[info_title]))}",
                                 font=("Montserrat", 18))
                label.pack()
                count = count + 1
                continue
            label = tk.Label(master=frame, text=f"{info_title.title()}: {state[info_title]}",
                             font=("Montserrat", 18))
            label.pack()
            count = count + 1
        j = j + 1
    frame = tk.Frame(master=canvi, relief=tk.RAISED, borderwidth=1)
    frame.grid(row=i, column=j, padx=5, pady=5)
    label = tk.Label(master=frame, text=f"TOTAL CASES: {human_format(summer_case)}", font=("Montserrat", 26, 'bold'),
                     fg='#cf1b1b')
    label.pack()
    label = tk.Label(master=frame, text=f"TOTAL DEATHS: {human_format(summer_death)}", font=("Montserrat", 26, 'bold'),
                     fg='#cf1b1b')
    label.pack()
    canvi.pack()
    calan.mainloop()


if __name__ == '__main__':
    master = tk.Tk()
    master.title("COVID Dashboard")
    url = 'https://finnhub.io/api/v1/covid19/us?'
    data = init()
    canvi = set_visual()
    dash_visual(data, master)
