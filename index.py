import pandas as pd
from datetime import *
from tkinter import *
from textwrap import wrap
data = pd.read_csv("data.csv")
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
#библиотеки и красота
datp = data["Дата поступления"]
datv = data["Дата выполнения"]
tech = data["Технология"].unique()
techsr = {}
for i in tech:
    techsr[i] = []

yb = []
for i in datp:
    b = i.split("/")
    yb.append(int(b[2]))
data["Год поступления"] = pd.Series(yb)



def countDays(a, b, c, d):
    d1 = date(int(a[2]), int(a[0]), int(a[1]))
    d2 = date(int(b[2]), int(b[0]), int(b[1]))
    t1 = int(c[0]) + int(c[1]) / 60 + int(c[2]) / 3600
    t2 = int(d[0]) + int(d[1]) / 60 + int(d[2]) / 3600
    time = abs(t2 - t1)
    days = (d2 - d1).days * 24 + time
    return days
#В ЧАСАХ!!!!!!!!!!!!!


def sredZnach(a, b):
    if len(a) > 0:
        if b == 0:
            a = sum(a) / len(a)
            return a
        else:
            for i in a:
                if len(a[i]) > 0:
                    a[i] = sum(a[i]) / len(a[i])
            return a



def sravnenie(os, le, zi, vs, c, year):
    res = 0
    dn = 0
    proc = []
    an = 0
    if c == 0:
        if year == 2024:
            os = 1
        elif year == 2023:
            zi = 1
            vs = 1
        if (os < le) or (os < le < vs < zi):
            dn = 1
            proc.append(os / le * 100)
            proc.append(le / vs * 100)
            proc.append(vs / zi * 100)
        if year == 2024:
            proc.pop(0)
        elif year == 2023:
            proc = [proc[0]]
        return proc
    elif c == 1:
        k = list(os.keys())
        c = 0
        count = 0
        mini = []
        for i in range(len(k)):
            if count == 0:
                count += 1
                continue
            else:
                if os[k[c]] > os[k[i]] or os[k[c]] < os[k[i]]:
                    dn += 1
                    if os[k[c]] == 1:
                        del os[k[c]]
                        an += 1
                    else:
                        mini.append(os[k[c]])
                c += 1
        count = [i for i in os.keys()]
        mini.append(os[count[-1]])
        minZnach = mini.index(min(mini))
        minZnach = k[minZnach]
        return min(mini), os, an, minZnach
    elif c == 2:
        lish = 0
        for i in os:
            if year == 2024:
                if ((le[i] != 1 and zi[i] != 1) or (vs[i] != 1 and zi[i] != 1) or (vs[i] != 1 and le[i] != 1)):
                    if le[i] < vs[i] < zi[i]:
                        res += 1
                        dn += 1
                else:
                    lish += 1
                if le[i] == 1 or vs[i] == 1 or zi[i] == 1:
                    an += 1
            elif year == 2023:
                if ((os[i] != 1) and (le[i] != 1)):
                    if os[i] < le[i]:
                        res += 1
                        dn += 1
                else:
                    an += 1
        proc = res / (len(os) - an) * 100
        return proc, dn, an
    else:
        lo = {}
        zv = {}
        vl = {}
        for i in os:
            if year == 2023:
                if (os[i] != 1) and (le[i] != 1):
                    proc = os[i] / le[i] * 100
                    lo[i] = proc
            elif year == 2024:
                if vs[i] != 1 and zi[i] != 1:
                    proc = vs[i] / le[i] * 100
                    zv[i] = proc
                if vs[i] != 1 and le[i] != 1:
                    proc = le[i] / vs[i] * 100
                    vl[i] = proc
        fin = {}
        for i in vl:
            if i in zv and i in vl:
                fin[i] = (zv[i] + vl[i]) / 2
        return lo, zv, vl, fin # ло - лето осеньб зв - зима весна, вл - весна лето, фин - средний процент увеличения скорости подачи заявки




def pustoty(a):
    for i in a:
        if a[i] == []:
            a[i] = [1]
    return a





def first(a, year):
    global datp
    if year == 2023:
        datp = data.loc[lambda df: df["Год поступления"] == 2023]
        datp = datp["Дата поступления"]
        c = 0
    elif year == 2024:
        datp = data.loc[lambda df: df["Год поступления"] == 2024]
        datp = datp["Дата поступления"]
        c = 1571
    if a == 0:
        techsrOs, techsrLe, techsrZi, techsrVs = [], [], [], []
    elif a == 1:
        techsrOs = techsr.copy()
    elif a == 2 or a == 3:
        techsrOs = {}
        for i in tech:
            techsrOs[i] = []
        techsrLe = {}
        for i in tech:
            techsrLe[i] = []
        techsrZi = {}
        for i in tech:
            techsrZi[i] = []
        techsrVs = {}
        for i in tech:
            techsrVs[i] = []
    for i in datp:
        b = i.split("/")
        g = data.loc[c, "Дата выполнения"].split("/")
        t1 = data.loc[c, "Время поступления"].split(":")
        t2 = data.loc[c, "Время выполнения"].split(":")
        if a == 0:
            if int(b[0]) in (9, 10, 11):
                techsrOs.append(countDays(b, g, t1, t2))
            elif int(b[0]) in (6, 7, 8):
                techsrLe.append(countDays(b, g, t1, t2))
            elif int(b[0]) in (3, 4, 5):
                techsrVs.append(countDays(b, g, t1, t2))
            elif int(b[0]) in (12, 1, 2):
                techsrZi.append(countDays(b, g, t1, t2))
        elif a == 1:
            techsrOs[data.loc[c, "Технология"]].append(countDays(b, g, t1, t2))
        elif a == 2 or a == 3:
            if int(b[0]) in (9, 10, 11):
                techsrOs[data.loc[c, "Технология"]].append(countDays(b, g, t1, t2))
            elif int(b[0]) in (6, 7, 8):
                techsrLe[data.loc[c, "Технология"]].append(countDays(b, g, t1, t2))
            elif int(b[0]) in (3, 4, 5):
                techsrVs[data.loc[c, "Технология"]].append(countDays(b, g, t1, t2))
            elif int(b[0]) in (12, 1, 2):
                techsrZi[data.loc[c, "Технология"]].append(countDays(b, g, t1, t2))

        c += 1
    if a == 0:
        os = sredZnach(techsrOs, a)
        le = sredZnach(techsrLe, a)
        zi = sredZnach(techsrZi, a)
        vs = sredZnach(techsrVs, a)
        return sravnenie(os, le, zi, vs, a, year)
    elif a == 1:
        os = sredZnach(pustoty(techsrOs), a)
        return sravnenie(os, None, None, None, a, year)
    elif a == 2 or a == 3:
        os = sredZnach(pustoty(techsrOs), a)
        le = sredZnach(pustoty(techsrLe), a)
        zi = sredZnach(pustoty(techsrZi), a)
        vs = sredZnach(pustoty(techsrVs), a)
        return sravnenie(os, le, zi, vs, a, year)



def third(b):
    b = list(b)
    os = b[1]
    le = b[2]
    count = b[0]
    print(count, os)
    c = 0
    for i in os:
        os[i] -= os[i] * (count[c] / 100)
        c += 1
    print(os)




root = Tk()
root["bg"] = "#FFFFFF"
root.title("Приветствие")
root.geometry("600x400")
root.resizable(width=False, height=False)
root.iconbitmap(default="images/icon.ico")
canvas = Canvas(root, height=600, width=1000)
canvas.pack()


def openNewWindow():
    newWindow = Toplevel(root)


    textfin = (f"Срок устранения зависит от множества факторов, если судить по сезонам то, процент изменения скорости заявки за 2023 с лета на осень равен {first(0, 2023)[0]}%,"
               f" а с зиму по весну 2024: {first(0, 2024)[1]}%, и {first(0, 2024)[0]}% с весны на лето того же года, но срок устранения также зависит от технологии, в 2023"
               f"самая быстрая технология это {first(1, 2023)[3]} с результатом {first(1, 2023)[0]} часа, ниже приведены средние скорости технологий за 2023: "
               f"\n {first(1, 2023)[1]} \nВ 2024 самая быстрая технология это {first(1, 2024)[3]} со значением {first(1, 2024)[0]}"
               f" ниже представлены весь список технологий и их среднее время закрытия: \n {first(1, 2024)[1]}. \n В 2023 году отношение количества технологий у которых увеличилась скорость к общему количеству технологий равна {first(2, 2023)[0]}, "
               f"а количество аномалий при этом равно {first(2, 2023)[2]}, но при этом в 2024 году такое же отношение равно {first(2, 2024)[0]}, а аномалий при этом {first(2, 2024)[2]}. Примерное увеличение скорости технологий в процентах за 2023 равен \n{first(3, 2023)[0]}\nв 2024 это предскзание равно \n{first(3, 2024)[3]}\n")


    #ОСТАЛОСЬ ДОДЕЛАТЬ ТОЛЬКО 2 И 3 ЗАДАЧУ!!!!!!! В ТЕКСТЕ


    newWindow.title("Result")
    newWindow.geometry("1000x800")
    Label(newWindow, text="Ваша статистика", font=("Montserrat", 20)).pack()
    Label(newWindow, text=textfin, font=("Montserrat", 12), wraplength=900, justify="left").place(relx=0.05, rely=0.15)


    root.update()
    width = title.winfo_width()

    if width > 350:
        char_width = width / len(text)
        wrapped_text = '\n'.join(wrap(text, int(350 / char_width)))
        title['text'] = wrapped_text
        root.update()
        print(text)


text = "Статистика основанная на данных таблицы"
textBut = "Узнать"

frame = Frame(canvas, bg="#CDCDCD")
frame.place(relx=0.11, rely=0, relwidth=0.8, relheight=1)

title = Label(frame, text=text, bg="#CDCDCD", font=("Montserrat", 20))
title.place(relx=0.13, rely=0.05)

btn = Button(frame, text=textBut, bg="white", font="Montserrat 10", command=openNewWindow)
btn.place(relx=0.41, rely=0.7)


root.update()
width = title.winfo_width()

if width > 350:
    char_width = width / len(text)
    wrapped_text = '\n'.join(wrap(text, int(350 / char_width)))
    title['text'] = wrapped_text
    root.update()
    print(text)








def soedinenie():
    print("nothing now")


root.mainloop()


















# print(datp, data[data["Год поступления"] == 2023]["Дата поступления"])

