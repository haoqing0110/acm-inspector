from colorama import Fore, Back, Style
from datetime import datetime
import sys
import os
import pandas as pd


def main():
    data_folder = sys.argv[1]
    start_time_str = sys.argv[2]
    end_time_str = sys.argv[3]

    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    print(Back.LIGHTYELLOW_EX + "")
    print(
        "************************************************************************************************"
    )
    print("Starting datetime for History collection - ", start_time)
    print("End datetime for History collection      - ", end_time)
    print(f"Input data folder: ", data_folder)
    print(
        "************************************************************************************************"
    )
    print(Style.RESET_ALL)

    selected_files = []
    # Traverse files in the specified data folder
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            # Check if the file name contains "acm-pod" and has either "mem-usage-wss.csv" or "cpu-usage.csv"
            if "acm-pod" in file and (
                "mem-usage-wss.csv" in file or "cpu-usage.csv" in file
            ):
                selected_files.append(os.path.join(root, file))

    for file in selected_files:
        file_name = "average_" + os.path.basename(file)
        print(f"Processing file: {file}")
        averages = filter_and_average(file, start_time, end_time, debug=False)
        output_path = os.path.join("./output/", file_name)
        write_average_to_csv(averages, output_path)


def filter_and_average(path, start_time, end_time, debug=True):
    print(Back.LIGHTYELLOW_EX + "")
    print(
        "************************************************************************************************"
    )
    print(f"Start to read data from ", path)

    print(
        "************************************************************************************************"
    )
    print(Style.RESET_ALL)

    df = pd.read_csv(path, sep=",")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    filtered_df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    # averages = {}
    # for column in value_columns:
    #     averages[column] = filtered_df[column].mean()
    if debug:
        print(f"Filtered data: \n", filtered_df)
    averages = filtered_df.select_dtypes(include="number").mean()
    return averages


def write_average_to_csv(averages, path):
    print(Back.LIGHTYELLOW_EX + "")
    print(
        "************************************************************************************************"
    )
    print(f"Start to write data to ", path)

    print(
        "************************************************************************************************"
    )
    print(Style.RESET_ALL)

    result_df = pd.DataFrame.from_dict(averages, orient="columns")
    result_df.to_csv(path, header=True)


if __name__ == "__main__":
    main()
