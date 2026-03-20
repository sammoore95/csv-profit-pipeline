import pandas as pd

def load_data(input_path):
    job_data = pd.read_csv(input_path)
    return job_data

def transform_data(job_data):
    # Change datatype to date for date columns
    date_cols = ["order_date", "quoted_ship_date", "actual_ship_date"]
    job_data[date_cols] = job_data[date_cols].apply(pd.to_datetime, errors="coerce")

    # Total cost
    job_data["total_cost"] = job_data["material_cost"] + job_data["labor_cost"] + job_data["freight_cost"]

    # Net revenue
    job_data["net_revenue"] = job_data["revenue"] * (1 - job_data["discount_pct"] / 100)

    # Profit
    job_data["profit"] = job_data["net_revenue"] - job_data["total_cost"]

    # Profit margin percent 
    job_data["profit_margin_pct"] = pd.NA           # create blank column for profit margin percent
    valid_margin = job_data["net_revenue"] != 0     # define condition to calculate the profit margin percent to avoid dividing by 0
    job_data.loc[valid_margin, "profit_margin_pct"] = (
        job_data.loc[valid_margin, "profit"] 
        / job_data.loc[valid_margin, "net_revenue"]
        ) * 100

    # Cost per unit
    job_data["cost_per_unit"] = pd.NA                           # create empty column for cost per unit                 
    valid_cost_per_unit = job_data["units_completed"] != 0      # define condition to calculate cost per unit to avoid dividing by 0
    job_data.loc[valid_cost_per_unit, "cost_per_unit"] = (
        job_data.loc[valid_cost_per_unit, "total_cost"]
        / job_data.loc[valid_cost_per_unit,"units_completed"]
    )

    # On time flag
    job_data["on_time_flag"] = pd.NA

    on_time_delivery = job_data["actual_ship_date"] <= job_data["quoted_ship_date"] 
    late_delivery = job_data["actual_ship_date"] > job_data["quoted_ship_date"]

    job_data.loc[on_time_delivery, "on_time_flag"] = "Y"
    job_data.loc[late_delivery, "on_time_flag"] = "N"

    # Late days
    job_data["late_days"] = pd.NA
    job_data.loc[job_data["on_time_flag"] == "Y", "late_days"] = 0
    job_data.loc[job_data["on_time_flag"] == "N", "late_days"] = (job_data["actual_ship_date"] - job_data["quoted_ship_date"]).dt.days

    # Rework flag
    job_data["rework_flag"] = pd.NA
    job_data.loc[job_data["rework_hours"] > 5, "rework_flag"] = "Y"
    job_data.loc[job_data["rework_hours"] <= 5, "rework_flag"] = "N"

    return job_data

def save_data(job_data, output_path):
    job_data.to_csv(output_path, index=False)
    
def main():
    input_path = "data/jobs_practice_2.csv"
    output_path = "data/jobs_practice_2_refactored_output.csv"

    job_data = load_data(input_path)
    job_data = transform_data(job_data)
    save_data(job_data, output_path)

    print("Pipeline complete.")

if __name__ == "__main__":
    main()