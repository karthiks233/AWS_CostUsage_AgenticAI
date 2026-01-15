import boto3
import json

client = boto3.client('ce')

def get_cost_and_usage(start_date='2025-01-01', end_date='2025-12-31', Granularity='MONTHLY'):
    """
    Retrieves the AWS cost and usage data for a specific time period.

    Args:
        start_date (str): The start date for result retrieval in 'YYYY-MM-DD' format. Defaults to '2025-01-01'.
        end_date (str): The end date for result retrieval in 'YYYY-MM-DD' format. Defaults to '2025-12-31'.

    Returns:
        dict: The response from the AWS Cost Explorer API containing cost and usage data.
    """
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity=Granularity,
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )

    return response

# print(json.dumps(response, indent=2))   

