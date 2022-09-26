import pandas as pd

# this script will generate the data used in the fig12


def adjust_major(major, age):
    majors = {
        "Computer": [
            "电子信息",
            "计算机科学与技术",
            "计科",
            "计算机"
        ], "Economics": [
            "经济学"
        ], "Mechanism": [
            "过控",
            "过程控制与装备过程",
            "过程装备与控制工程"
        ]}

    if age >= 22:
        return "pro"
    elif major in majors["Computer"]:
        return "Computer"
    elif major in majors["Economics"]:
        return "Economics"
    elif major in majors["Mechanism"]:
        return "Mechanism"
    else:
        return "others"


def main():
    data_ilp_acc = pd.read_csv("./processingResult/ILPCorrectPercent.csv", encoding="utf8")
    data_ilp_time = pd.read_csv("./processingResult/ILPTimecost.csv", encoding="utf8")
    data_neat_acc = pd.read_csv("./processingResult/NEWMethodCorrectPercent.csv", encoding="utf8")
    data_neat_time = pd.read_csv("./processingResult/NEWMethodTimecost.csv", encoding="utf8")
    data_sug_acc = pd.read_csv("./processingResult/sugiyamaCorrectPercent.csv", encoding="utf8")
    data_sug_time = pd.read_csv("./processingResult/sugiyamaTimecost.csv", encoding="utf8")

    def calc_average(data):
        acc = {"Economics": [], "pro": [], "Computer": [], "Mechanism": [], "others": []}
        acc_s = {"Economics": 0, "pro": 0, "Computer": 0, "Mechanism": 0, "others": 0}  # sum
        acc_n = {"Economics": 0, "pro": 0, "Computer": 0, "Mechanism": 0, "others": 0}  # num
        acc_f = {"Economics": 0, "pro": 0, "Computer": 0, "Mechanism": 0, "others": 0}  # final
        for (index, value) in data.groupby("major"):
            for i, t in enumerate(value["age"]):
                major = adjust_major(index, t)

                acn = (value["T1"] + value["T2"] + value["T3"]).values[i]
                acc_s[major] += acn
                acc_n[major] += 1

                acc[major].append(float(format(acn / 3, ".3f")))
        for i in acc_s:
            if acc_n[i] == 0:
                continue
            acc_f[i] = acc_s[i] / acc_n[i] / 3
        return [acc_f, acc]

    def show_result(acc_f, time_f, acc, time):
        print("total part:")
        print(acc_f)
        print(time_f)
        print("single part:")
        for i in acc:
            print(i)
            print(acc[i])
            print(time[i])
        # for t in time:
        #     print(t)

    print("\n\n-----------\nilp\n-----------")
    ilp_acc_f, ilp_acc = calc_average(data_ilp_acc)
    ilp_time_f, ilp_time = calc_average(data_ilp_time)
    show_result(acc_f=ilp_acc_f, time_f=ilp_time_f, acc=ilp_acc, time=ilp_time)

    print("\n\n-----------\nneat\n-----------")
    neat_acc_f, neat_acc = calc_average(data_neat_acc)
    neat_time_f, neat_time = calc_average(data_neat_time)
    show_result(acc_f=neat_acc_f, time_f=neat_time_f, acc=neat_acc, time=neat_time)

    print("\n-----------\nsug\n-----------")
    sug_acc_f, sug_acc = calc_average(data_sug_acc)
    sug_time_f, sug_time = calc_average(data_sug_time)
    show_result(acc_f=sug_acc_f, time_f=sug_time_f, acc=sug_acc, time=sug_time)


if __name__ == '__main__':
    main()
