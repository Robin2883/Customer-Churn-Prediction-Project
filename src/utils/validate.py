import great_expectations as gx
import pandas as pd


def validate_data(df)->tuple[bool, list[str]]:
    print("Data Validation Started:")
    
    df=df.copy()
    df['TotalCharges']=pd.to_numeric(df['TotalCharges'], errors='coerce')
    context=gx.get_context()
    
    data_source = context.data_sources.add_pandas("pandas")
    data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    expectations = [
    gx.expectations.ExpectColumnToExist(column="customerID"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="customerID"),
    gx.expectations.ExpectColumnToExist(column="gender"),
    gx.expectations.ExpectColumnToExist(column="Partner"),
    gx.expectations.ExpectColumnToExist(column="Dependents"),
    gx.expectations.ExpectColumnToExist(column="PhoneService"),
    gx.expectations.ExpectColumnToExist(column="InternetService"),
    gx.expectations.ExpectColumnToExist(column="Contract"),
    gx.expectations.ExpectColumnToExist(column="tenure"),
    gx.expectations.ExpectColumnToExist(column="MonthlyCharges"),
    gx.expectations.ExpectColumnToExist(column="TotalCharges"),

    gx.expectations.ExpectColumnValuesToBeInSet(column="gender", value_set=["Male", "Female"]), 
    gx.expectations.ExpectColumnValuesToBeInSet(column="Partner", value_set=["Yes", "No"]),
    gx.expectations.ExpectColumnValuesToBeInSet(column="Dependents", value_set=["Yes", "No"]),
    gx.expectations.ExpectColumnValuesToBeInSet(column="PhoneService", value_set=["Yes", "No"]),
    gx.expectations.ExpectColumnValuesToBeInSet(column="Contract", value_set=["Month-to-month", "One year", "Two year"]),
    gx.expectations.ExpectColumnValuesToBeInSet(column="InternetService", value_set=["DSL", "Fiber optic", "No"]),
  

    gx.expectations.ExpectColumnValuesToBeBetween(column="TotalCharges", min_value=0),
    gx.expectations.ExpectColumnValuesToBeBetween(column="tenure", min_value=0, max_value=120),
    gx.expectations.ExpectColumnValuesToBeBetween(column="MonthlyCharges", min_value=0, max_value=200),

    gx.expectations.ExpectColumnValuesToNotBeNull(column="tenure"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="MonthlyCharges"),

    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        column_A="TotalCharges",
        column_B="MonthlyCharges",
        or_equal=True,
        mostly=0.95)

    ]

    results = [batch.validate(exp) for exp in expectations]
    
    failed_expectations = []

    for result in results:
        if not result["success"]:
            failed_expectations.append(
                result["expectation_config"]["type"]
            )
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r['success'])
    failed_checks= total_checks-passed_checks

    if results:
        print(f"Data validation PASSED: {passed_checks}/{total_checks} checks successful")
    else:
        print(f"Data validation FAILED: {failed_checks}/{total_checks} checks failed")
        print(f"Failed expectations: {failed_expectations}")
    
    return results, failed_expectations
